import json

def load_course_data(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)

            if not data or not isinstance(data, dict):
                return {}
            
        return data
        
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_course_data(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent =4)