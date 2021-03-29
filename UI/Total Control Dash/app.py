# -*- coding: utf-8 -*-

# TOTAL CONTROL DASHBOARD

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 10],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")



app.layout = html.Div(children=[
    # add city to city specifications
    html.H1(
        children='Fuel Consumption Reduction Dashboard',
        style={
            'textAlign': 'center',
            'font_size': '15px',
        }
    ),
    
    html.Label('Select Vehicles and Trip Characteristics of Fleet'),
    html.Div(className = "row", children = [
        #id='dd-output-container',
        
        
        
        html.Div(className = 'six columns', children = [
            html.Label('Hybridization', style = {"margin-left": "15px"}),
            dcc.Dropdown(
                id='demo-dropdown1',
                options=[
                        {'label': 'ICE', 'value': 'ICE'},
                        {'label': 'HEV', 'value': 'HEV'},
                        {'label': 'BEV', 'value': 'BEV'},
                        {'label': 'PHEV', 'value': 'PHEV'}
                ],
                value='ICE',
            )
        ], style = dict(width='150%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Weight (units)', style = {"margin-left": "15px"}),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='35%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Displacement (units)', style = {"margin-left": "10px"}),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='35%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Aggressiveness Percentile', style = {"margin-left": "15px"}),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Average Speed (units)', style = {"margin-left": "15px"}),
            dcc.Input(
            placeholder='Enter a value...',
            type='text',
            value=''
            ) 
        ], style = dict(width='35%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Speed Variance (units)', style = {"margin-left": "15px"}),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='35%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Air Temperature (units)', style = {"margin-left": "15px"}),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='35%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Precipitation Level (units)', style = {"margin-left": "15px"}),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='35%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Distance (km)', style = {"margin-left": "15px"}),
            dcc.Input(
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='35%', margin = '15px')),

        
    #], style = {"border":"0.5px grey solid"}),
    ], style=dict(display='flex', border='0.5px grey solid', borderRadius = '15px', margin = '15px')),
    
    
        
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
