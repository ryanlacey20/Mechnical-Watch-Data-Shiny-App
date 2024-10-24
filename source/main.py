
from source.excelParsing import get_latest_excel_file  
import pandas as pd
import os
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as px


def load_data():
    excel_file = "Data/" + get_latest_excel_file()
    excel_sheet_names = pd.ExcelFile(excel_file).sheet_names
    df = pd.read_excel(excel_file, sheet_name=excel_sheet_names[0])  
    return df


app_ui = ui.page_fluid(
    ui.input_slider("n", "Number of bins", 1, 100, 20),
    output_widget("plot"),
)


def server(input, output, session):
    df_plot = load_data()

    @output
    @render_widget
    def plot():
        scatterplot = px.scatter(
            df_plot,
            x='Day No',
            y='Daily Deviation',
            title="Day No vs Daily Deviation"
        )
        return scatterplot


app = App(app_ui, server)
