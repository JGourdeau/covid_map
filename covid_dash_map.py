# Author: Jack Gourdeau
# Date: July 2nd 2020
# Purpose: Dash app
# filename: covid_map_dash.py

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---- import and clean data -----

df = pd.read_csv("owid-covid-data.csv")
df['date'] = pd.to_datetime(df['date'])  # ensure date is in date format
df['cases_per_person'] = df['total_cases']/df['population']

# get all unique dates
unique_dates = np.sort(df.date.unique())

# create a library of possible dates for slider
date_marks = {}
pos = 0
for date in unique_dates:
    date_marks[pos] = ""
    pos += 1


# ----- App Layout ------
colors = {
    'background': '#0e0e0e',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1("SARS-CoV-2 (COVID19) World Timeline", style={'textAlign': 'center', 'color': colors['text']}),  # title for page

    # slider to select date
    dcc.Slider(
        id='date_slider',
        min=1,
        max=(len(date_marks)-1),
        step=None,
        marks=date_marks,
        value=1,  # initial value
        updatemode='mouseup',
        dots=False
    ),

    html.P(id='selected_date_vis', style={'textAlign': 'center', 'color': colors['text']}),

    dcc.Graph(
        id='world_map',
        figure={},
        style={'background': colors['background']},
    ),

    html.P("Jack Gourdeau", id="copyright_label", style={'textAlign': 'center', 'color': colors['text']})

])


# ---- App Callbacks

@app.callback(
    [Output(component_id='selected_date_vis', component_property='children'),
     Output(component_id='world_map', component_property='figure')],
    [Input(component_id='date_slider', component_property='value')]
)
def update_graph(date_selected):  # input is the component property of the input

    print(date_selected)
    print(type(date_selected))

    date_container = 'Viewing: {}'.format(pd.to_datetime(unique_dates[date_selected]).strftime("%b %d %Y %H:%M:%S")),

    selected_date = unique_dates[date_selected]

    df2 = df.loc[df['date'] == selected_date]

    print(df2)

    # plotly express
    fig = px.choropleth(
        data_frame=df2,
        locationmode='ISO-3',
        locations='iso_code',
        color='cases_per_person',
        scope='world',
        color_continuous_scale=px.colors.sequential.YlOrRd,
        template='plotly_dark',
        hover_data=['location', 'cases_per_person'],
        range_color=[0, 0.008],
    )

    return date_container, fig


# -----
if __name__ == '__main__':
    app.run_server(debug=True)
