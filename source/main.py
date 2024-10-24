# source/main.py
from source.excelParsing import get_latest_excel_file  
import pandas as pd
import os
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as px

root_dir = os.path.dirname(os.path.abspath(__file__)) 

def load_data():
    excel_file = os.path.join(root_dir, "Data", get_latest_excel_file())
    excel_sheet_names = pd.ExcelFile(excel_file).sheet_names
    to_return = []
    for sheet in excel_sheet_names:
        if sheet != "Statistics":
            df = pd.read_excel(excel_file, sheet_name=sheet)  
            to_return.append([sheet, df])
    
    return to_return


app_ui = ui.page_fluid(
    output_widget("plot"),
    ui.output_text("debug_info")  
)


def server(input, output, session):
    df_data = load_data()
    
    for sheet in df_data:
        df_name = sheet[0]
        print("sheet:", df_name)
        df_plot = sheet[1]
        @output
        @render_widget
        def plot():
            scatterplot = px.scatter(
                df_plot,
                x='Day No',
                y='Daily Deviation',
                title=f"Day No vs Daily Deviation: {df_name}"
            )
            return scatterplot
        
    @output
    @render.text
    def debug_info():
        return "test test"


app = App(app_ui, server)
