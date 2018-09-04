########################################################################################################################

# Title: Data Science Accelerator

# Authors: Matear, L.(2018)                                                               Email: Liam.Matear@jncc.gov.uk
# Version Control: 1.0

# Script description:
#
#                        For any enquiries please contact Liam Matear by email: Liam.Matear@jncc.gov.uk

########################################################################################################################

#   Section 1:                   Loading, manipulating and formatting the data within Python

########################################################################################################################


#   1a) Load in all required packages for script:
#       If required install packages using 'pip install package name command in terminal

#       Import all packages used for data formatting and manipulation
# -*- coding: utf-8 -*-

# Import all libraries required for application and front end development
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64

# Import all libraries required for back end manipulation
import os
import pandas as pd
import numpy as np


# Import all libraries required for graphics development
import plotly.plotly as py
import plotly.graph_objs as go
import json

########################################################################################################################

# Create application instance
app = dash.Dash()

# Import MPA count data
count_df = pd.read_excel(
    'C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\input\Stats\\OfficialSensitive_UKMPA_STATS.xlsx',
    'UK_count')


# Import MPA area data
area_df = pd.read_excel(
    'C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\input\Stats\\OfficialSensitive_UKMPA_STATS.xlsx',
    'UK_area')

# Import MPA percentage data
percentage_df = pd.read_excel(
    'C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\input\Stats\\OfficialSensitive_UKMPA_STATS.xlsx',
    'UK_percentage')

# Import UK MPA Network GeoJson data
with open('C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\geojson\\UKMPA_ALL_Simp.geojson') as f:
    mpaJson = json.load(f)


########################################################################################################################


# Set unique location headings to build filtering controls for all statistical data

# availableLocations = count_df['Location'].unique()

availableLocations = [
    'All UK waters (EEZ+UKCS)', 'UK EEZ',
    'UK inshore (territorial seas)', 'UK offshore',
    'England inshore+offshore', 'Wales inshore+offshore',
    'Scotland inshore+offshore', 'Northern Ireland inshore+offshore',
    'England inshore', 'Wales inshore', 'Scotland inshore',
    'Northern Ireland inshore', 'England offshore', 'Wales offshore',
    'Scotland offshore', 'Northern Ireland offshore']

osparRegions = [
    'Region I: Arctic Waters', 'Region II: Greater North Sea',
    'Region III: Celtic Seas', 'Region V: Wider Atlantic']


# Setup initial app colours

colors = {
    'background': '#262626',
    'text': '#ccccc0',

    'mpa_count_cols': {
        'Total no. of MPAs': '#E0BBE4',
        'Total no. of SACs': '#957DAD',
        'Total no. of SPAs': '#D291BC',
        'Total no. of MCZs': '#FEC8D8',
        'Total no. of NCMPAs': '#FFDFD3'},

    'mpa_area_cols': {
        'Total Area of MPAs': '#E0BBE4',
        'Total Area of SACs': '#957DAD',
        'Total Area of SPAs': '#D291BC',
        'Total Area of MCZs': '#FEC8D8',
        'Total Area of NCMPAs': '#FFDFD3'},

    'location_cols': {
            'All UK waters (EEZ+UKCS)': '#E0BBE4',
            'UK EEZ': '#E0BBE4',
            'UK inshore (territorial seas)': '#E0BBE4',
            'UK offshore': '#E0BBE4',

            'England inshore+offshore': '#957DAD',
            'Wales inshore+offshore': '#D291BC',
            'Scotland inshore+offshore': '#FEC8D8',
            'Northern Ireland inshore+offshore': '#FFDFD3',

            'England inshore': '#957DAD',
            'Wales inshore': '#D291BC',
            'Scotland inshore': '#FEC8D8',
            'Northern Ireland inshore': '#FFDFD3',

            'England offshore': '#957DAD',
            'Wales offshore': '#D291BC',
            'Scotland offshore': '#FEC8D8',
            'Northern Ireland offshore': '#FFDFD3'}
    }

########################################################################################################################


# Create global chart template

# Set MapBox Access Token for map development
mapbox_access_token = 'pk.eyJ1IjoibGlhbW1hdGVhciIsImEiOiJjamxnZTRicHQxMzRnM3BxZ2kweWh2Y2drIn0.kAm_AQ9uJJs0N_qb-5HEyg'


# Setup app layout

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
        html.Div(
                # Set application title, colour and orientation
                html.H1(
                    children='UK MPA Network Statistics',
                    className='eight columns',
                    style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'backgroundColor': colors['background'],
                        'width': '100%',
                        # 'height': '20',
                        'display': 'block',
                        'float': 'center'
                    }),

                # html.Img(
                #     src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                #     className='one columns',
                #     style={
                #          'height': '100',
                #          'width': '225',
                #          'float': 'right',
                #          'position': 'relative',
                #          'backgroundColor': colors['background']
                #     },
                # ),
            ),

        # Set key stats summary text

        html.Div(
            [
                html.H5(
                    '',
                    id='mpa_number',
                    className='two columns',
                    style={'color': colors['text']}
                ),
                html.H5(
                    '',
                    id='total_area',
                    className='eight columns',
                    style={'text-align': 'center',
                           'color': colors['text']}
                ),
                html.H5(
                    '',
                    id='total_percentage',
                    className='two columns',
                    style={'text-align': 'right',
                           'color': colors['text']}
                ),
            ],
            className='row'
        ),

        # Set control panel - Location drop-down menu
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'Filter by geospatial location',
                            style={'color': colors['text']}
                               ),
                        dcc.RadioItems(
                            id='country_selector',
                            options=[
                                {'label': 'All ', 'value': 'all'},
                                {'label': 'England ', 'value': 'eng'},
                                {'label': 'Scotland ', 'value': 'scot'},
                                {'label': 'N. Ireland ', 'value': 'nire'},
                                {'label': 'Wales ', 'value': 'wales'},
                                {'label': 'OSPAR Regions', 'value': 'ospar'},
                            ],
                            value='all',
                            labelStyle={'display': 'inline-block',
                                        'color': colors['text']}
                        ),
                        dcc.Dropdown(
                            id='Location',
                            options=[{'label': i, 'value': i} for i in availableLocations],
                            # Allows for all or singular filtering
                            multi=False,
                            # value=list(availableLocations) - if multi
                            value='All UK waters (EEZ+UKCS)'
                        ),
                    ],
                    className='twelve columns'
                ),
            ],
            className='row'
        ),

        # Create graph areas - main map
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='main_graph')
                    ],
                    className='six columns',
                    style={'margin-top': '20'}
                ),
                # Create graph areas - mpa count
                html.Div(
                    [
                        dcc.Graph(id='mpa_count')
                    ],
                    className='six columns',
                    style={'margin-top': '20'}
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='area_pie')
                    ],
                    className='five columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        dcc.Graph(id='percentage_pie')
                    ],
                    className='seven columns',
                    style={'margin-top': '10'}
                ),
            ],
            className='row'
        ),
    ],
    # className='ten columns offset-by-one'
)


########################################################################################################################

#                                          Key Summary Header Text Callbacks

########################################################################################################################


# Create application callback decorator to update the Total MPA Number text box in key summary header
@app.callback(
    dash.dependencies.Output('mpa_number', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_count(selected_location):
    filtered_df = count_df[count_df.Location == selected_location]
    result = filtered_df['Total no. of MPAs']
    for each in result:
        return 'Total no. of MPAs: ' + str(each)


# Create application callback decorator to update Total Area Number text box in key summary header
@app.callback(
    dash.dependencies.Output('total_area', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_area(selected_location):
    filtered_df = area_df[area_df.Location == selected_location]
    result = filtered_df['Total Area of MPAs']
    for each in result:
        return 'Total Area of MPAs (km2):  ' + str(each)


# Create application callback decorator to update Total Percent Covered by MPA text box in key summary header
@app.callback(
    dash.dependencies.Output('total_percentage', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_area(selected_location):
    filtered_df = percentage_df[percentage_df.Location == selected_location]
    result = filtered_df['Total % of location covered by MPAs']
    for each in result:
        return 'Total % covered by MPAs:  ' + str(each) + '%'


########################################################################################################################

#                                         Graphs / Data Visualisation Callbacks

########################################################################################################################

# Create function to filter data by selected_location


# Create application callback decorator for main graph
@app.callback(
    dash.dependencies.Output('main_graph', 'figure'),
    [dash.dependencies.Input('Location', 'value')]
)
def make_main_graph(selected_location):
    # Identify locations of all entries within json file
    print(selected_location)
    # Create filtered json data from mpaJson and add features to newly created object
    filteredjson = {k: v for k, v in mpaJson.items() if k != "features"}
    filteredjson["features"] = [x for x in mpaJson["features"] if x["properties"]["Country"] == selected_location]
    traces = []

    traces.append(
        go.Scattermapbox(
            lon=[filteredjson['features'][k]['properties']['LONG_dd'] for k in range(len(filteredjson['features']))],
            lat=[filteredjson['features'][k]['properties']['LAT_dd'] for k in range(len(filteredjson['features']))],
            text=[filteredjson['features'][k]['properties']['SITE_NAME'] for k in range(len(filteredjson['features']))],
            marker=dict(
                opacity=0.6,
                color=colors['location_cols'][selected_location]
            ),
        )
    )
    return {
        'data': traces,
        'layout': go.Layout(
            autosize=True,
            height=500,
            font=dict(
                color=colors['text']
            ),
            titlefont=dict(
                color=colors['text'],
                size=14
            ),
            margin=dict(
                l=35,
                r=35,
                b=35,
                t=45
            ),
            hovermode='closest',
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            legend=dict(
                font=dict(
                    size=10
                ),
                orientation='h'
            ),
            title='UK MPA Network',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style='dark',
                center=dict(
                    lon=-3.6,
                    lat=55
                ),
                zoom=4.1
            ),
        )
    }


# Create application callback decorator to update bar chart with location selection
@app.callback(
    dash.dependencies.Output('mpa_count', 'figure'),
    [dash.dependencies.Input('Location', 'value')]
)
def update_count(selected_location):
    filtered_df = count_df[count_df.Location == selected_location]
    traces = []
    for column in filtered_df:
        if column != 'Location':

            traces.append(go.Bar(
                x=filtered_df['Location'],
                y=filtered_df[column],
                textposition='auto',
                marker=dict(
                    color=colors['mpa_count_cols'][column]),
                opacity=0.8,
                name=column
                ),
            )
    return {
        'data': traces,
        'layout': go.Layout(
            title='Total Number of MPAs by Designation',
            font=dict(color=colors['text']),
            barmode='group',
            xaxis={'title': 'Location',
                   'color': colors['text']},
            yaxis={'title': 'Count',
                   'color': colors['text']},
            margin={'l': 50, 'b': 40, 't': 50, 'r': 10},
            showlegend=True,
            hovermode='closest',
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background'],

        )
    }


# Create application callback decorator to update area pie chart with location selection
@app.callback(
    dash.dependencies.Output('area_pie', 'figure'),
    [dash.dependencies.Input('Location', 'value')]
)
def update_pie(selected_location):
    traces = []
    filtered_df = area_df[area_df.Location == selected_location]
    filtered_df2 = filtered_df.drop(['Location'], axis=1, inplace=False)
    # NEED TO REMOVE PERCENTAGE VALUES
    traces.append(go.Pie(
        labels=list(filtered_df2),
        values=pd.Series(filtered_df2.iloc[0]),
        textposition='outside',
        textinfo='value',
        marker=dict(
            colors=pd.Series(colors['mpa_area_cols']),
            line=dict(color='#ccccc0', width=2)),
        pull=0.2,
        hole=0.1
    ))
    return {
        'data': traces,
        'layout': go.Layout(
            title='Total MPA Area by Location (km2)',
            font=dict(color=colors['text']),
            hovermode='closest',
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background']
        )
    }


# Create application callback decorator to percentage area pie chart with location selection
@app.callback(
    dash.dependencies.Output('percentage_pie', 'figure'),
    [dash.dependencies.Input('Location', 'value')]
)
def update_per_pie(selected_location):
    traces = []
    filtered_df = percentage_df[percentage_df.Location == selected_location]
    filtered_df2 = filtered_df.drop(['Location'], axis=1, inplace=False)
    traces.append(go.Pie(
        labels=list(filtered_df2),
        values=pd.Series(filtered_df2.iloc[0]),
        textposition='outside',
        textinfo='value',
        marker=dict(
            colors=pd.Series(colors['mpa_area_cols']),
            line=dict(color='#ccccc0', width=2)),
        pull=0.2,
        hole=0.1
    ))
    return {
        'data': traces,
        'layout': go.Layout(
            title='Percent of Location Covered by MPA (%)',
            font=dict(color=colors['text']),
            hovermode='closest',
            paper_bgcolor=colors['background'],
            plot_bgcolor=colors['background']
        )
    }


app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True)


########################################################################################################################






