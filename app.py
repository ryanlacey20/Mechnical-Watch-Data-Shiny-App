from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
from src.excelParsing import get_latest_excel_file, get_latest_excel_file
import json

# Initialize Flask app
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing)
CORS(app)

root_dir = os.path.dirname(os.path.abspath(__file__))

def load_data():
    # Path to the Excel file
    excel_file = os.path.join(root_dir, "src/Data", get_latest_excel_file())
    
    # Get sheet names from Excel
    excel_sheet_names = pd.ExcelFile(excel_file).sheet_names
    
    watchSheetandNames2D = {}
    for sheet in excel_sheet_names:
        if sheet != "Statistics":  # Exclude 'Statistics' sheet if needed
            df = pd.read_excel(excel_file, sheet_name=sheet)
            
            # Handle datetime columns by converting NaT values to empty strings or another placeholder
            for column in df.columns:
                if df[column].dtype == 'datetime64[ns]':
                    df[column] = df[column].dt.strftime('%Y-%m-%d')  # Convert to string format
                    df[column] = df[column].fillna('')  # Replace NaT with empty string or None if preferred
            
            # Convert DataFrame to JSON and store it in dictionary
            # This will be the JSON response
            watchSheetandNames2D[sheet] = df.to_dict(orient='records')
            
            # Optionally save to CSV
            df.to_csv(os.path.join(root_dir, "src/Data", "CSVs", f"{sheet}.csv"))
    
    return watchSheetandNames2D


@app.route('/api/data', methods=['GET'])
def get_data():
    # Load data and return as JSON
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    # Run the app, accessible only on localhost
    app.run(host='127.0.0.1', port=5000, debug=True)
