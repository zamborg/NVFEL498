# -*- coding: utf-8 -*-

# GENERATED DASHBOARD

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from FleetGeneration import generate_trip_data, ManualFleet
import dash_table as dt

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

m = ManualFleet()
fleet_cols = ['Vehicle ID', 'Hybridization', 'Weight (units)', 'Displacement (units)', 'Aggressiveness Percentile',
                 'Average Speed (units)', 'Speed Variance (units)', 'Air Temperature (units)',
                 'Precipitation Level (units)', 'Distance (units)']


app.layout = html.Div(children=[
    # add city to city specifications
    html.H1(
        children='Fuel Consumption Reduction Dashboard',
        style={
            'textAlign': 'center',
            'font_size': '15px',
        }
    ),
    
    html.H2(
        children='Drive Cycle Generator',
        style={
            'textAlign': 'left',
            'font_size': '15px',
        }
    ),
    
    html.Label('Select Number of Vehicles'),
    html.Div(children = [
        dcc.Input(
            id='num-vehicles',
            placeholder='Enter a value...',
            type='text',
            value=''
        ), 
    ], style = dict(width='50%', margin = '3px')),
    
    html.Label('Specify Proportion of each Vehicle Type'),
    html.Div(className = "row", children = [
        #id='dd-output-container',
        
        
        html.Div(className = 'six columns', children = [
            html.Label('ICE (Internal Combustion Engine)', style = {"margin-left": "15px"}),
            dcc.Input(
                id='ICE',
                placeholder='Enter a value...',
                type='text',
                value=''
            )
        ], style = dict(width='50%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('HEV (Hybrid Electric Vehicle)', style = {"margin-left": "15px"}),
            dcc.Input(
                id='HEV',
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('BEV (Battery Electric Vehicle)', style = {"margin-left": "15px"}),
            dcc.Input(
                id='BEV',
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '15px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('PHEV (Plug-In Hybrid Electric Vehicle)', style = {"margin-left": "15px"}),
            dcc.Input(
                id='PHEV',
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '15px')),

        
    #], style = {"border":"0.5px grey solid"}),
    ], style=dict(display='flex', border='0.5px grey solid', borderRadius = '15px', margin = '15px')),
    
    
    html.Label('Specify Mean and Variance for Vehicle Characteristics'),
    html.Div(className = "row", children = [
        #id='dd-output-container',
        
        
        html.Div(className = 'six columns', children = [
            html.Label('Displacement (units)', style = {"margin-left": "15px"}),
            html.Label('Mean', style = {"margin-left": "3px"}),
            dcc.Input(
                id='displacement-mean', 
                placeholder='Enter a value...',
                type='text',
                value=''
            ), 
            html.Label('Variance', style = {"margin-left": "3px"}),
            dcc.Input(
                id='displacement-var',
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '3px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Weight (units)', style = {"margin-left": "15px"}),
            html.Label('Mean', style = {"margin-left": "3px"}),
            dcc.Input(
                id='weight-mean', 
                placeholder='Enter a value...',
                type='text',
                value=''
            ), 
            html.Label('Variance', style = {"margin-left": "3px"}),
            dcc.Input(
                id='weight-var',
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '3px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Driver Aggressiveness (units)', style = {"margin-left": "15px"}),
            html.Label('Mean', style = {"margin-left": "3px"}),
            dcc.Input(
                id='agg-mean', 
                placeholder='Enter a value...',
                type='text',
                value=''
            ), 
            html.Label('Variance', style = {"margin-left": "3px"}),
            dcc.Input(
                id='agg-var',
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '3px')),

        
    #], style = {"border":"0.5px grey solid"}),
    ], style=dict(display='flex', border='0.5px grey solid', borderRadius = '15px', margin = '15px')),
    
    html.Label('Select Mean and Variance for Characteristics of Trips'),

    
    html.Div(children = [
        #id='dd-output-container',
        
        html.Div(className = 'six columns', children = [
            html.Label('Average Speed (units)', style = {"margin-left": "15px"}),
            
            html.Label('Mean', style = {"margin-left": "3px"}),
            dcc.Input(
                id='avg-speed-mean',
                placeholder='Enter a value...',
                type='text',
                value=''
            ), 
            html.Label('Variance', style = {"margin-left": "3px"}),
            dcc.Input(
                id='avg-speed-var',
                placeholder='Enter a value...',
                type='text',
                value=''
            )
        ], style = dict(width='50%', margin = '3px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Speed Variance (units)', style = {"margin-left": "15px"}),
            html.Label('Mean', style = {"margin-left": "3px"}),
            dcc.Input(
                id='speed-var-mean',
                placeholder='Enter a value...',
                type='text',
                value=''
            ), 
            html.Label('Variance', style = {"margin-left": "3px"}),
            dcc.Input(
                id='speed-var-var',
                placeholder='Enter a value...',
                type='text',
                value=''
            )
        ], style = dict(width='50%', margin = '3px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Distance (km)', style = {"margin-left": "15px"}),
            html.Label('Mean', style = {"margin-left": "3px"}),
            dcc.Input(
                id='distance-mean',
                placeholder='Enter a value...',
                type='text',
                value=''
            ), 
            html.Label('Variance', style = {"margin-left": "3px"}),
            dcc.Input(
                id='distance-var',
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '3px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Air Temperature (units)', style = {"margin-left": "15px"}),
            html.Label('Mean', style = {"margin-left": "3px"}),
            dcc.Input(
                id='temp-mean',
                placeholder='Enter a value...',
                type='text',
                value=''
            ), 
            html.Label('Variance', style = {"margin-left": "3px"}),
            dcc.Input(
                id='temp-var',
                placeholder='Enter a value...',
                type='text',
                value=''
            )
        ], style = dict(width='50%', margin = '3px')),
        
        html.Div(className = 'six columns', children = [
            html.Label('Precipitation Level (units)', style = {"margin-left": "15px"}),
            html.Label('Mean', style = {"margin-left": "3px"}),
            dcc.Input(
                id='precipitation-mean',
                placeholder='Enter a value...',
                type='text',
                value=''
            ), 
            html.Label('Variance', style = {"margin-left": "3px"}),
            dcc.Input(
                id='precipitation-var',
                placeholder='Enter a value...',
                type='text',
                value=''
            ) 
        ], style = dict(width='50%', margin = '3px')),

        
    #], style = {"border":"0.5px grey solid"}),
    ], style=dict(display = 'flex', border='0.5px grey solid', borderRadius = '15px', margin = '15px')),
    
    html.Label('Select Number of Trips'),
    html.Div(children = [
        dcc.Input(
            id='num-trips',
            placeholder='Enter a value...',
            type='text',
            value=''
        ), 
    ], style = dict(width='50%', margin = '3px')),
    
    html.Div([
        html.Button('Submit Fleet Characteristics', id='submit-val', n_clicks=0, style = {"margin": "15px"}),
        html.Button('Reset Fleet Generation', id='reset-val', n_clicks = 0, style = {"margin": "15px"}),
    ]),
    
    #html.Button('Submit', id='submit-val', n_clicks=0, style = {"margin": "15px"}),
    
    html.Div(id='my-output'),
    

    
    html.H2(
        children='Select Vehicle + Trip Characteristics for Fleet',
        style={
            'textAlign': 'left',
            'font_size': '15px',
        }
    ),
    
    #dash_table.DataTable(id='trip-table'),

    
    
    dt.DataTable(
        id = 'fleet-table',
        columns = (
            [{'id': p, 'name': p} for p in fleet_cols]
        ),
        data=[
            dict(Model=i, **{param: 0 for param in fleet_cols})
            for i in range(0)
        ],
        editable = True,
        row_deletable = True,
        style_cell={'textAlign': 'center'},
    
    ),
    
    html.Button('Add Vehicle', id='add-vehicle', n_clicks=0, style = {"margin": "15px"}),

])

#user_inputs = ['num-vehicles', 'num-trips', 'ICE', 'HEV', 'BEV', 'PHEV', 'displacement-mean', 'displacement-var', 'weight-mean', 'weight-var', 'avg-speed-mean', 'avg-speed-var', 'speed-var-mean', 'speed-var-var', 'distance-mean', 'distance-var', 'temp-mean', 'temp-var', 'precipitation-mean']

@app.callback(
    #[Output(component_id='trip-table', component_property='data'),
    # Output(component_id='trip-table', component_property='columns')],
    Output('my-output', 'children'),
    [Input('submit-val', 'n_clicks'), Input('reset-val', 'n_clicks')],
    #state=[State(component_id='ICE', component_property='value')]
    State('num-vehicles', 'value'),
    State('num-trips', 'value'),
    State('ICE', 'value'),
    State('HEV', 'value'),
    State('BEV', 'value'),
    State('PHEV', 'value'),
    State('displacement-mean', 'value'),
    State('displacement-var', 'value'),
    State('weight-mean', 'value'),
    State('weight-var', 'value'),
    State('agg-mean', 'value'),
    State('agg-var', 'value'),
    State('avg-speed-mean', 'value'),
    State('avg-speed-var', 'value'),
    State('speed-var-mean', 'value'),
    State('speed-var-var', 'value'),
    State('distance-mean', 'value'),
    State('distance-var', 'value'),
    State('temp-mean', 'value'),
    State('temp-var', 'value'),
    State('precipitation-mean', 'value'),
    State('precipitation-var', 'value'),

)

def update_output(n_clicks1, n_clicks2, vehicle_num, trip_num, ICE_val, HEV_val, BEV_val, PHEV_val, 
                 disp_mean, disp_var, weight_mean, weight_var, agg_mean, agg_var, avg_speed_mean, avg_speed_var, speed_var_mean, speed_var_var, 
                 dist_mean, dist_var, temp_mean, temp_var, precip_mean, precip_var):
    
    args = {'size':int(trip_num), 'num_vehicles':int(vehicle_num),
        'trips':{'Air Temp (units)':(float(temp_mean), float(temp_var)), 
                 'Precipitation (units)':(float(precip_mean), float(precip_var)),
                 'Average Speed (units)':(float(avg_speed_mean), float(avg_speed_var)),
                 'Speed Variance (units)':(float(speed_var_mean), float(speed_var_var)),
                 'Distance (units)':(float(dist_mean), float(dist_var)),},
        'cars':{'Displacement (units)':(float(disp_mean), float(disp_var)), 
                'Weight (units)':(float(weight_mean), float(weight_var)),
               'Aggressiveness (units)':(float(agg_mean), float(agg_var))}
    }

    trips_df = generate_trip_data(**args)
    data = trips_df.to_dict('rows')
    columns = [{'name': col, 'id': col} for col in trips_df.columns]

    return dt.DataTable(data = data, columns = columns)


        
# Either find shortcut to clear every user input box, or repeat this block for every box
@app.callback(Output('num-vehicles', 'value'),
              Output('num-trips', 'value'),
               [Input('reset-val','n_clicks')])

def clearInput(n_clicks):
    if n_clicks != 0:
        return ""
    
    
@app.callback(
    #[Output(component_id='trip-table', component_property='data'),
    # Output(component_id='trip-table', component_property='columns')],
    Output('fleet-table', 'data'),
    [Input('add-vehicle', 'n_clicks')],
    State('fleet-table', 'data'),
    State('fleet-table', 'columns'),


)

#fleet_cols = ['Hybridization', 'Weight (units)', 'Displacement (units)', 'Aggressiveness Percentile',
#                 'Average Speed (units)', 'Speed Variance (units)', 'Air Temperature (units)',
#                 'Precipitation Level (units)', 'Distance (units)']



def add_vehicle(n_clicks, rows, columns):
    print("ROWS: ", rows)
    if n_clicks > 0:
        new_row = {c['id']: '' for c in columns}
        #new_row['Vehicle ID'] = n_clicks
        rows.append(new_row)
           
    return rows
    
    


if __name__ == '__main__':
    app.run_server(debug=True)
