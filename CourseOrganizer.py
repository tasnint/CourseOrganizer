import os
import shutil
import datetime
import schedule
import time
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import pipeline
import PyPDF2
import docx
import logging
from pathlib import Path

# Helper functions for data storage
from StorageUtils import load_course_data, save_course_data

# Initialize the tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
# Initially load course labels to determine the number of courses
initial_course_labels = load_course_data('CourseData.json')
num_courses = len(initial_course_labels)
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=num_courses)

source_dir = "/mnt/c/Users/tanis/Downloads"
previously_copied_files = set()  # Track already processed files

# Zero-shot classifier initialization
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def extract_text(file_path):
    try:
        if file_path.suffix == '.pdf':
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfFileReader(f)
                text = ' '.join(page.extract_text() for page in reader.pages if page.extract_text())
            return text
        elif file_path.suffix == '.docx':
            doc = docx.Document(file_path)
            text = ' '.join(paragraph.text for paragraph in doc.paragraphs)
            return text
    except Exception as e:
        logging.error(f"Failed to extract text from {file_path}: {e}")
    return None

def tokenize_function(text):
    return tokenizer(text, padding="max_length", truncation=True, max_length=512)

def ask_user_to_add_course(filepath):
    print("Would you like to add a course?")
    response = input("If yes, type 'Y': ")
    if response.lower() == 'y':
        course_code = input("Enter course code here: ")
        course_description = input("Enter course description here: ")
        course_data = load_course_data(filepath)
        if course_code not in course_data:
            course_data[course_code] = {"description": course_description}
            save_course_data(filepath, course_data)
            print(f"Added course with code: {course_code}")
            global num_courses
            num_courses = len(course_data)  # Update num_courses
            update_model()  # Update the model to reflect new number of courses
        return course_code, course_description
    else:
        print("No course added.")
        return None, None

def update_model():
    global model
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=num_courses)

def copy_files_with_string(source, dest_dir, target_string):
    today = datetime.date.today()
    date_subdir = os.path.join(dest_dir, str(today))
    if not os.path.exists(date_subdir):
        os.makedirs(date_subdir)
    target_string = target_string.lower()
    for file in os.listdir(source):
        if target_string in file.lower() and file not in previously_copied_files:
            source_file = os.path.join(source, file)
            destination_file = os.path.join(date_subdir, file)
            shutil.copy2(source_file, destination_file)
            previously_copied_files.add(file)
            print(f"Copied {file} to {destination_file}")

def classify_and_copy_file(file_name, source, destination_base, filepath):
    best_match = classify_file(file_name, filepath)
    destination_dir = os.path.join(destination_base, best_match)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    source_file = os.path.join(source, file_name)
    destination_file = os.path.join(destination_dir, file_name)
    shutil.copy2(source_file, destination_file)
    print(f"Classified and copied {file_name} to {destination_file}")

def classify_file(file_name, filepath):
    course_labels = get_course_labels(filepath)
    classification = classifier(file_name, candidate_labels=course_labels)
    return classification['labels'][0]

def get_course_labels(filepath):
    course_data = load_course_data(filepath)
    return list(course_data.keys())



def check_and_process_files():
    source_dir = Path("/mnt/c/Users/tanis/Downloads")
    for file_path in source_dir.iterdir():
        if file_path.name not in previously_copied_files:
            classify_and_decide(file_path, "/mnt/c/Users/tanis/Desktop", 'CourseData.json')
            previously_copied_files.add(file_path.name)

def classify_and_decide(file_path, destination_base, filepath):
    text = extract_text(file_path) or file_path.name  # Use file name as a fallback
    course_labels = get_course_labels(filepath)
    classification = classifier(text, candidate_labels=course_labels)
    best_match, score = classification['labels'][0], classification['scores'][0]

    if score > 0.5:
        destination_dir = Path(destination_base) / best_match
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination_file = destination_dir / file_path.name
        shutil.copy2(file_path, destination_file)
        logging.info(f"Classified and copied {file_path} to {destination_file}")
    else:
        logging.info(f"File {file_path.name} did not match any course label with sufficient confidence.")



def main():
    course_data_filepath = 'CourseData.json'
    schedule.every(1).minute.do(check_and_process_files)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program exited.")




if __name__ == "__main__":
    main()
