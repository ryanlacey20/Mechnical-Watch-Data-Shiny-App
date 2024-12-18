from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from src.excelParsing import get_latest_excel_file
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing)
CORS(app)

# Load environment variables from .env file (only in development)
if os.getenv('RUN_ENV') != 'prod':
    load_dotenv()  # Only load .env if it's not production

# Fetch the value of 'RUN_ENV' from the environment
run_env = os.getenv('RUN_ENV')

# Set root_dir based on the environment
if run_env == "dev":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print("Running in development mode")
else:
    root_dir = "/app"  # Heroku sets the app's root directory to "/app"



# Path to the Excel file
excel_file = os.path.join(root_dir, "src/Data", get_latest_excel_file())

# Path to the /tmp/CSVs directory
tmp_dir = os.path.join(root_dir, "tmp")
csv_dir = os.path.join(tmp_dir, "CSVs")
print("DEBUG HERE", csv_dir)
# Ensure /tmp/CSVs exists
os.makedirs(csv_dir, exist_ok=True)

def load_data():
    # Get sheet names from Excel
    excel_sheet_names = pd.ExcelFile(excel_file).sheet_names
    
    watchSheetandNames2D = {}
    for sheet in excel_sheet_names:
        if sheet != "Statistics" and sheet != "1929 Omega PW (Peggie)":  # Exclude 'Statistics' sheet if needed
            df = pd.read_excel(excel_file, sheet_name=sheet)
            
            # Handle datetime columns by converting NaT values to empty strings or another placeholder
            for column in df.columns:
                if df[column].dtype == 'datetime64[ns]':
                    df[column] = df[column].dt.strftime('%Y-%m-%d')  # Convert to string format
                    df[column] = df[column].fillna('')  # Replace NaT with empty string or None if preferred
            
            # Convert DataFrame to JSON and store it in dictionary
            watchSheetandNames2D[sheet] = df.to_dict(orient='records')
            
            # Save to CSV in the /tmp/CSVs directory
            df.to_csv(os.path.join(tmp_dir, "CSVs", f"{sheet}.csv"))
    
    return watchSheetandNames2D


@app.route('/stat_data/get_daily_deviation', methods=['POST'])
def load_daily_deviation_against_day():
    try:
        # Get the table name from the request
        forTable = request.json.get("forTable")
        if not forTable:
            return jsonify({"error": "Table name not provided"}), 400
        
        # Read the Excel file for the specified table/sheet
        dfAllCols = pd.read_excel(excel_file, sheet_name=forTable)
        
        # Columns to keep
        colsToKeep = ['Day No', 'Daily Deviation']
        
        # Ensure the required columns exist in the DataFrame
        missing_cols = [col for col in colsToKeep if col not in dfAllCols.columns]
        if missing_cols:
            return jsonify({"error": f"Missing columns in sheet '{forTable}': {missing_cols}"}), 400
        
        # Keep only relevant columns and drop rows with NaN values
        dfRelevantCols = dfAllCols[colsToKeep].dropna(subset=colsToKeep)
        
        # Convert DataFrame to JSON and send it as a response
        return jsonify(dfRelevantCols.to_dict(orient='records')), 200
    
    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({"error": str(e)}), 500




@app.route('/get_table_data', methods=['POST'])
def get_user_info():
    data = load_data()  # Load the data dictionary

    # Get the requested title from the request JSON body
    requested_title = request.json.get("requestedTitle")

    # Check if the requestedTitle exists in the dictionary keys
    if requested_title in data:
        return jsonify({"requestedTitle": requested_title, "data": data[requested_title]}), 200
    else:
        return jsonify({"error": "Requested title not found", "requestedTitle": requested_title}), 404

@app.route('/api/data', methods=['GET'])
def get_data():
    # Load data and return as JSON
    data = load_data()
    return jsonify(data)

@app.route('/api/getTableTitles', methods=['GET'])
def get_table_title():
    # Load data to get sheet names
    data = load_data()
    return jsonify(list(data.keys()))  # Return only the sheet names as a list

if __name__ == '__main__':
    app.run(debug=True)  # Debug can be True for local testing

