from source.excelParsing import get_latest_excel_file  
import pandas as pd
import os
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as px
from shiny import express as shiny_exp  # Import Shiny Express

root_dir = os.path.dirname(os.path.abspath(__file__)) 

def load_data():
    excel_file = os.path.join(root_dir, "Data", get_latest_excel_file())
    excel_sheet_names = pd.ExcelFile(excel_file).sheet_names
    to_return = []
    for sheet in excel_sheet_names:
        if sheet != "Statistics":
            df = pd.read_excel(excel_file, sheet_name=sheet)  
            to_return.append([sheet, df])
            df.to_csv(os.path.join(root_dir, "Data", "CSVs", f"{sheet}.csv"))
    
    return to_return

# Using Shiny Express to define UI
def app_ui():
    df_data = load_data()  # Load data for the UI
    output_widgets = [output_widget(f"plot_{sheet[0]}") for sheet in df_data]
    return ui.page_fluid(
        *output_widgets,  # Dynamically create output widgets for plots
        ui.output_text("debug_info")  # Placeholder for debug info
    )

# Using Shiny Express to define server logic
def server(input, output, session):
    df_data = load_data()  # Load data for server processing

    # Create dynamic output functions for each sheet
    for sheet in df_data:
        df_name = sheet[0]
        df_plot = sheet[1]

        @output(f"plot_{df_name}")  # Use dynamic output ID
        @render_widget
        def plot():
            scatterplot = px.scatter(
                df_plot,
                x='Day No',
                y='Daily Deviation',
                title=f"Day No vs Daily Deviation: {df_name}"
            )
            return scatterplot

    @output("debug_info")  # Output ID for debug info
    @render.text
    def debug_info():
        return "This is the debug info."

# Create Shiny app with app_ui and server functions
app = App(app_ui, server)
