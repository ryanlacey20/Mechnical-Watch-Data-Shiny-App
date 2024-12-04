import csv
import os
import shutil


curr_dir = os.path.dirname(os.path.abspath(__file__)) 
data_dir =curr_dir+"/Data" 
csv_dir = "/tmp/CSVs"

if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

def clear_directory(dir_to_clear):
    shutil.rmtree(dir_to_clear)
    os.makedirs(dir_to_clear)  



def find_excel_files():
    matching_files = []

    for filename in os.listdir(data_dir):
        if filename.startswith("Accuracy") and filename.endswith(".xlsx"):
            matching_files.append(filename)

    return matching_files if matching_files else None

def get_latest_excel_file():
    clear_directory(csv_dir)

    data_file_names = find_excel_files()
    if data_file_names:
        data_file_names.sort(reverse=True)
        return data_file_names[0]
    return None