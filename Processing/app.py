# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sys

from simple_regression import reg1

print("REGRESSION: ", reg1.coef_)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children = [
    #html.Label('Enter Input Driver Aggressiveness'),
    
    html.Div(children = [
        html.Label('Enter Driver Aggressiveness: '),
        dcc.Input(id = "agg", type = "number", placeholder = 120683),
        html.Label(id = 'result'),
    ],),
    
], style = {'columnCount' : 1})

@app.callback(
    Output(component_id = 'result', component_property = 'children'),
    [Input(component_id = 'agg', component_property = 'value')] )
def update_fuel_consumption(agg):
    try:
        fuel_consumption = reg1.predict(agg)
        return fuel_consumption
    except ValueError:
        return 'unable to report fuel consumption'

if __name__ == '__main__':
    app.run_server(debug=True)
