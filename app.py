from shiny import render, ui
from shiny.express import input
from shinywidgets import render_plotly
import os
import pandas as pd
from source.excelParsing import get_latest_excel_file  
import plotly.express as px


ui.panel_title("Hello Shiny!")
ui.input_slider("n", "N", 0, 100, 20)
root_dir = os.path.dirname(os.path.abspath(__file__)) 

def load_data():
    excel_file = os.path.join(root_dir, "source/Data", get_latest_excel_file())
    print("DEBUG", excel_file)
    excel_sheet_names = pd.ExcelFile(excel_file).sheet_names
    to_return = []
    for sheet in excel_sheet_names:
        if sheet != "Statistics":
            df = pd.read_excel(excel_file, sheet_name=sheet)  
            to_return.append([sheet, df])
            df.to_csv(os.path.join(root_dir, "source","Data", "CSVs", f"{sheet}.csv"))
    
    return to_return


df_data = load_data()

for sheet in df_data:
        df_name = sheet[0]
        df_plot = sheet[1]


        @render_plotly
        def plot():
            scatterplot = px.scatter(
                df_plot,
                x='Day No',
                y='Daily Deviation',
                title=f"Day No vs Daily Deviation: {df_name}"
            )
            return scatterplot
