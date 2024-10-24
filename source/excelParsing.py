import os

def find_accuracy():
    directory = './source/Data/'
    matching_files = []

    for filename in os.listdir(directory):
        if filename.startswith("Accuracy") and filename.endswith(".xlsx"):
            matching_files.append(filename)

    return matching_files if matching_files else None

def get_latest_excel_file():
    data_file_names = find_accuracy()
    if data_file_names:
        data_file_names.sort(reverse=True)
        return data_file_names[0]
    return None
