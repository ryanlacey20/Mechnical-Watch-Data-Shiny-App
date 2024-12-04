import csv
import os
import shutil
from dotenv import load_dotenv


# curr_dir = os.path.dirname(os.path.abspath(__file__)) 
# data_dir =curr_dir+"/Data" 
# csv_dir = "/tmp/CSVs"

# Load environment variables from .env file (only in development)
if os.getenv('RUN_ENV') != 'prod':
    load_dotenv()  # Only load .env if it's not production

# Fetch the value of 'RUN_ENV' from the environment
run_env = os.getenv('RUN_ENV')

# Set root_dir based on the environment
if run_env == "dev":
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(cur_dir, "..")
    print("Running in development mode")
else:
    root_dir = "/app"  # Heroku sets the app's root directory to "/app"


def clear_directory(dir_to_clear):
    shutil.rmtree(dir_to_clear)
    os.makedirs(dir_to_clear)  

data_dir = os.path.join(root_dir, "src/Data")
csv_dir = os.path.join(root_dir, "tmp/CSVs")

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