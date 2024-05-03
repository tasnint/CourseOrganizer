import os
import shutil
import datetime
import schedule
import time

source_dir = "/mnt/c/Users/tanis/Downloads"

def ask_user_to_add_course():
    print("Would you like to add a course?")
    response = input("If yes, type 'Y': ")
    if response.lower() == 'y':
        print("What is the course code of the course you would like to add?")
        course_code = input("Enter course code here: ")
        print(f"Adding course with code: {course_code}")
        return course_code
    else:
        print("No course added.")
        return None

def copy_files_with_string(source, dest_dir, target_string):
    today = datetime.date.today()
    date_subdir = os.path.join(dest_dir, str(today))
    if not os.path.exists(date_subdir):
        os.makedirs(date_subdir)
        print(f"Created folder for today's date: {date_subdir}")

    files_copied = 0
    new_files_found = False
    target_string = target_string.lower()

    for file in os.listdir(source):
        if target_string in file.lower():
            source_file = os.path.join(source, file)
            destination_file = os.path.join(date_subdir, file)

            # Check if the file already exists and compare modification times
            if not os.path.exists(destination_file) or os.path.getmtime(source_file) != os.path.getmtime(destination_file):
                try:
                    shutil.copy2(source_file, destination_file)  # copy2 preserves metadata including modification times
                    files_copied += 1
                    print(f"Copied {file} to {destination_file}")
                    new_files_found = True
                except Exception as e:
                    print(f"Failed to copy {file}. Error: {e}")

    if new_files_found:
        print(f"Total {files_copied} new files copied to: {date_subdir}")

def main():
    course_code = ask_user_to_add_course()
    if course_code:
        destination_dir = os.path.join("/mnt/c/Users/tanis/Desktop", course_code)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            print(f"Created directory for course at: {destination_dir}")

        print(f"Proceeding with additional operations for course {course_code}.")
        schedule.every(1).minutes.do(copy_files_with_string, source=source_dir, dest_dir=destination_dir, target_string=course_code)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

