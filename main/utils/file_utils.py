import json

############################ SCRAPING ############################
def save_json(filename, new_dict):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(new_dict, f, ensure_ascii=False, indent=4, default=str)
    except:
        print(f'Error saving {filename}.')

def create_json(filename):
    empty_dict = {}
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(empty_dict, f, ensure_ascii=False, indent=4, default=str)
    except:
        print(f'Error saving {filename}.')

## work in progress ---> save file by appending
# def append_json(submissions_dict, filename):
#     '''
#     Takes in a filename and 
#     '''
#     with open(filename,'r+') as file:
#         # First we load existing data into a dict.
#         file_data = json.load(file)
#         # Join new_data with file_data inside emp_details
#         file_data["emp_details"].append(submissions_dict)
#         # Sets file's current position at offset.
#         file.seek(0)
#         # convert back to json.
#         json.dump(file_data, file, indent = 4)