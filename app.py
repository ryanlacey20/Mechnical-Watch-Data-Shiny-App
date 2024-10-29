from shiny import App, render, ui
from shinywidgets import render_plotly
import os
import pandas as pd
from source.excelParsing import get_latest_excel_file  
import plotly.express as px

root_dir = os.path.dirname(os.path.abspath(__file__)) 

app_ui = ui.page_fluid(
    ui.output_ui("plots")
)

def load_data():
    excel_file = os.path.join(root_dir, "source/Data", get_latest_excel_file())
    excel_sheet_names = pd.ExcelFile(excel_file).sheet_names
    to_return = []
    for sheet in excel_sheet_names:
        if sheet != "Statistics":
            df = pd.read_excel(excel_file, sheet_name=sheet)  
            to_return.append([sheet, df])
            df.to_csv(os.path.join(root_dir, "source","Data", "CSVs", f"{sheet}.csv"))
    
    return to_return


df_data = load_data()
df_name = df_data[0][0]
df_plot = df_data[0][1]

print(df_plot)

# for sheet in df_data:
#         df_name = sheet[0]
#         df_plot = sheet[1]


#         @render_plotly
#         def plot2():
#             scatterplot = px.scatter(
#                 df_plot,
#                 x='Day No',
#                 y='Daily Deviation',
#                 title=f"Day No vs Daily Deviation: {df_name}"
#             )
#             return scatterplot


def server(input, output, session):
    def render_plot_func(j):
        @render_plotly
        def plot():
            scatterplot = px.scatter(
                df_plot,
                x='Day No',
                y='Daily Deviation',
                title=f"Day No vs Daily Deviation: {df_name}"
            )
            return scatterplot
        
        return plot
        
    @output
    @render.ui
    def plots():
        plot_output_list = []
        for i in range(1, len(df_data) + 1):
            plotname = f"plot{i}"

            plot_output_list.append(ui.output_plot(plotname))
            output(render_plot_func(i), id=plotname)
        return ui.TagList(plot_output_list)

app = App(app_ui, server)