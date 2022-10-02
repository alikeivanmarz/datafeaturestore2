import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash_table import DataTable
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import qualitative
from datetime import date


import pandas as pd

df = pd.read_csv('data/gapminderDataFiveYear.csv')

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app = dash_app.server

dash_app.layout = html.Div([
    
    html.Div([
            html.H6("Data Feature Store Dashboard", id="info-title"),
            html.H6(f"Data updated through {last_update_text}", id="data-update"),
        ]),

    # Page Header
    html.Div([
        html.H1('Data Feature Store')
    ]),

    # Dropdown Grid
    html.Div([
        html.Div([
            # Select Data Source Dropdown
            html.Div([
                html.Div('Data Sources', className='three columns'),
                html.Div(dcc.Dropdown(id='data_sorce-selector',
                                      options=[{'label':'ATMS', 'value':'ATMS' },
                                      {'label': 'SRMS', 'value':'SRMS'},
                                      {'label': 'TomTom', 'value':'TTOM'}
                                      ]),
                         className='nine columns')
            ]),

            # Select Location Dropdown
            html.Div([
                html.Div('Locations', className='three columns'),
                html.Div(dcc.Dropdown(id='location-selector',
                                      options=[{'label':'A', 'value':'A' },
                                      {'label': 'B', 'value':'B'},
                                      {'label': 'C', 'value':'C'}
                                      ]),
                         className='nine columns')
            ]),

            # Select Data Feature Dropdown
            html.Div([
                html.Div('Data Feature', className='three columns'),
                html.Div(dcc.Dropdown(id='data_feature-selector',
                                      options=[{'label':'Week', 'value':'WEEK' },
                                      {'label': 'Holiday', 'value':'HOLY'},
                                      {'label': 'Rain', 'value':'RAIN'}
                                      ]),
                         className='nine columns')
            ]),
        ], className='six columns'),

        # Empty
        html.Div(className='six columns'),
    ], className='twleve columns'),

    # Results Grid
    html.Div([

        # Match Results Table
        html.Div(
            html.Table(id='results'),
            className='six columns'
        ),

        # Season Summary Table and Graph
        html.Div([
            # summary table
            dcc.Graph(id='Data-summary'),

            # graph
            dcc.Graph(id='Data-graph')
            # style={},

        ], className='six columns')
    ]),

    dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        ),
])




@dash_app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))

def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55, template="plotly_dark")

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    dash_app.run_server(debug=True)