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
from textwrap import dedent


# Import all libraries required for back end manipulation
import os
import pandas as pd
import numpy as np


# Import all libraries required for graphics development
import plotly.plotly as py
import plotly.graph_objs as go
import json
import urllib.request
from plotly import tools

########################################################################################################################

# Create application instance
app = dash.Dash()
# Allow multiple callback operators to influence each other - set to True
app.config['suppress_callback_exceptions'] = True

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

# Import summary statistics data
summaryAll_df = pd.read_excel(
    'C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\input\Stats\\OfficialSensitive_UKMPA_STATS.xlsx',
    'SummaryAll')

# Import summary statistics data
summaryOSPAR_df = pd.read_excel(
    'C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\input\Stats\\OfficialSensitive_UKMPA_STATS.xlsx',
    'SummaryOSPAR')

# Import OSPAR management data
summaryManagement_df = pd.read_excel(
    'C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\input\Stats\\OfficialSensitive_UKMPA_STATS.xlsx',
    'SummaryManagement')

# Import UK MPA Network GeoJson data
with open('C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\geojson\\testMPA_SIMP.geojson') as f:
    mpaJson = json.load(f)

# Import OSPAR boundaries GeoJson data
with open('C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\geojson\\testOSPAR_SIMP.geojson') as f2:
    osparBoundaries = json.load(f2)


# Keeps crashing - ODIMS OSPAR server issues when streaming hosted data

# # Import UK OSPAR regions json data - wfs Geo Server request
# with urllib.request.urlopen(
#         'insert ospar link to geojson data'
# ) as url:
#     odimsOspar = json.loads(url.read().decode())


########################################################################################################################


# Set unique location headings to build filtering controls for all statistical data

inshoreOffshore = ['All UK waters (EEZ+UKCS)', 'UK inshore (territorial seas)', 'UK offshore']

availableLocations = [
    'England', 'Wales',
    'Scotland', 'Northern Ireland'
    ]

availableLocationsGraphs = [
    'England', 'Wales',
    'Scotland', 'Northern Ireland',
    'All UK waters (EEZ+UKCS)', 'UK EEZ',
    'UK inshore (territorial seas)',
    'UK offshore'
    ]

osparRegions = [
    'Region I: Arctic Waters', 'Region II: Greater North Sea',
    'Region III: Celtic Seas', 'Region V: Wider Atlantic']


# Setup initial app colours

colors = {
    'background1': 'rgb(248,248,255)',  # Ghost White
    'background2': 'rgb(248,248,255)',  # White '#FFFFFF'
    'text': '#262626',  # Very dark grey
    'textbox': 'rgb(248,248,255)',  # White 'rgb(255,255,255,0.5)'

    'filteredjson': '#b6e1f6',

    'question_cols': {
        'documented_answer': '#957DAD',
        'implemented_answer': '#D291BC',
        'monitoring_answer': '#FEC8D8',
        'movement_answer': '#FFDFD3'
        },

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

    'ospar_cols': {
        'Region I': '#E0BBE4',
        'Region II': '#957DAD',
        'Region III': '#D291BC',
        'Region V': '#FEC8D8',
    },

    'management_cols': {
        'Yes': '#D291BC',
        'Partial': '#957DAD',
        'No': '#b6e1f6',
        'Not available': '#FEC8D8',
        'Unknown': '#FFDFD3',

    },

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
    style={'backgroundColor': colors['background2']}, children=[
        html.Div(
            style={'backgroundColor': colors['background1']}, children=[
                html.Div(
                    children=[
                        # Set application title, colour and orientation
                        html.H1(
                            children='UK Marine Protected Area Network Statistics',
                            className='eight columns',
                            style={
                                'textAlign': 'left',
                                'color': colors['text'],
                                'backgroundColor': colors['background1'],
                                'margin-top': '45',
                                'font-size': '55',
                            },
                        ),
                        html.Img(
                            src='https://github.com/liammatear/DataSciAcc/raw/master/JNCCLogo_Black.png',
                            className='four columns',
                            style={
                                 'float': 'right',
                                 'margin-top': '2',
                                 'backgroundColor': colors['background1']
                            },
                        ),
                    ],
                    className='row'
                ),
                # Create main dashboard area
                html.Div(
                    style={'backgroundColor': colors['text']}, children=[
                        html.Div(
                            style={'backgroundColor': colors['text']}, children=[
                                html.Div(
                                    style={'backgroundColor': colors['text']}, children=[
                                        html.Div(
                                            [
                                                # Set Introductory controls text
                                                dcc.Markdown(
                                                    dedent('''
                                                    Use the checkbox to filter locations at a UK level, by individual 
                                                    country and OSPAR Regions
                                                                       '''),
                                                    containerProps={
                                                        'style': {
                                                            'textAlign': 'left',
                                                            'color': colors['background2'],
                                                            'opacity': 0.9,
                                                            'font-size': '16',
                                                            'margin': 10,
                                                        },
                                                    },
                                                ),
                                                # Create main controls for geospatial regions
                                                dcc.RadioItems(
                                                    id='mainSelector',
                                                    options=[
                                                        {'label': 'UK', 'value': 'UK'},
                                                        {'label': 'Country', 'value': 'Country'},
                                                        {'label': 'OSPAR Region', 'value': 'OSPAR'},
                                                    ],
                                                    value='UK',
                                                    labelStyle={
                                                        'display': 'inline-block',
                                                        'color': colors['background2'],
                                                        'backgroundColor': colors['text'],
                                                        'font-size': 20,
                                                        'opacity': 0.9,
                                                    }
                                                ),
                                            ],
                                        ),
                                    ],
                                    className='six columns'
                                ),
                                # Set second control - locations within regions (this will be updated with callbacks)
                                html.Div(
                                    style={
                                        'backgroundColor': colors['text'],
                                    }, children=[
                                        html.Div(
                                            [
                                                # Set instructions for second drop-down use
                                                dcc.Markdown(
                                                    dedent('''
                                                    Select a location from the drop-down tab below
                                                                       '''),
                                                    containerProps={
                                                        'style': {
                                                            'textAlign': 'right',
                                                            'color': colors['background2'],
                                                            'opacity': 0.9,
                                                            'font-size': '16',
                                                            'margin': 10,
                                                        },
                                                    },
                                                ),
                                                # Create drop-down control
                                                dcc.Dropdown(
                                                    id='Location',
                                                    options=[],
                                                    # Allows for all or singular filtering
                                                    multi=False,
                                                    # value=list(availableLocations)
                                                    value='All UK waters (EEZ+UKCS)',
                                                    placeholder="Select a location to begin exploring!",
                                                ),
                                            ],
                                        ),
                                    ],
                                    className='six columns'
                                ),
                            ],
                            className='row'
                        ),
                        # html.Div(
                        #     style={'backgroundColor': colors['text']}, children=[
                        #         html.H2('',
                        #                 id='main_selection',
                        #                 style={
                        #                     'float': 'left',
                        #                     'color': colors['background1'],
                        #                     'margin': '20',
                        #                     'margin-top': '10',
                        #                 },
                        #                 ),
                        #     ],
                        #     className='row',
                        # ),
                        # Create HTML Divisions for key statistical data
                        html.Div(
                            style={'backgroundColor': colors['text']}, children=[
                                html.Div(
                                    [
                                        # Create main map / graph
                                        dcc.Graph(id='main_graph')
                                    ],
                                    className='ten columns',
                                    style={# 'margin-top': '20',
                                           'float': 'center',
                                           'backgroundColor': colors['text'],
                                           },
                                ),
                                # Create accompanying key summary statistics as headers
                                html.Div(
                                    [
                                        html.H1(
                                            '',
                                            id='mpa_number',
                                            style={
                                                'text-align': 'center',
                                                'color': colors['background2'],
                                                'height': 200,
                                                # 'margin-top': 10,
                                                'margin': 10,
                                                'font-size': 34,
                                            },
                                        ),
                                        html.H1(
                                            '',
                                            id='total_area',
                                            style={
                                                'text-align': 'center',
                                                'color': colors['background2'],
                                                'display': 'inline-block',
                                                'height': 200,
                                                'font-size': 34,
                                                'margin-top': 20,
                                                'margin': 20,
                                            }
                                        ),
                                        html.H1(
                                            '',
                                            id='total_percentage',
                                            style={
                                                'text-align': 'center',
                                                'color': colors['background2'],
                                                'display': 'inline-block',
                                                'height': 200,
                                                'font-size': 34,
                                                'margin-top': 20,
                                                'margin': 20,
                                            },
                                        ),
                                    ],
                                    className='two columns'
                                ),
                            ],
                            className='row'
                        ),
                        # Create HTML Divisions for OSPAR management data / graphs and introduction
                        html.Div(
                            style={'backgroundColor': colors['text']}, children=[
                                html.H2('',
                                        id='main_selection',
                                        style={
                                            'float': 'left',
                                            'color': colors['background1'],
                                            'margin': '20',
                                            'margin-top': '10',
                                        },
                                        ),
                            ],
                            className='row',
                        ),
                        # Create OSPAR management data displays
                        html.Div(
                            [
                                dcc.Markdown(
                                    dedent('''
                                    ## OSPAR, UK & Country Data 
                                    
                                    UK MPA management have been evaluated under the Oslo and Paris 
                                    Convention [(OSPAR)](http://www.ospar.org/). Data below can be explored 
                                    at a UK, individual country level, OSPAR regional scale and a site specific basis.
                                    Use the main filters at the top of the dashboard to filter information shown in the 
                                    pie charts. Toggle which data are visible by clicking their icon in the legend below 
                                    the graphs
                                                                                    '''),
                                    containerProps={
                                        'style': {
                                            'float': 'center',
                                            'textAlign': 'center',
                                            'color': colors['background1'],
                                            'margin': '20'
                                        },
                                    },
                                ),
                                # Create OSPAR management pie charts
                                dcc.Graph(
                                    id='management_pies'
                                ),
                            ],
                            className='row'
                        ),
                        # Create MPA site specific area displays
                        html.Div(
                            style={'backgroundColor': colors['text']}, children=[
                                html.Div(
                                    [
                                        dcc.Markdown(
                                            dedent('''
                                            ## Site Specific Management Data
                                            Load site specific data by clicking on the MPA within the interactive 
                                            mapper. 
                                            '''),
                                            containerProps={
                                                'style': {
                                                    'float': 'center',
                                                    'textAlign': 'center',
                                                    'color': colors['background1'],
                                                },
                                            },
                                        ),
                                    ],
                                    className='row'
                                ),
                                # Create interactive information callbacks - data controlled by clickData from map
                                html.Div(
                                    style={'backgroundColor': colors['text']}, children=[
                                        html.H3('Site selected: Select a site by clicking an MPA boundary',
                                                id='selected_site',
                                                style={
                                                    'float': 'left',
                                                    'color': colors['background1'],
                                                    'margin': '20',
                                                    'margin-top': '10',
                                                },
                                                ),
                                    ],
                                    className='row',
                                    ),
                                html.Div(
                                    style={'backgroundColor': colors['text']}, children=[
                                        html.Div(
                                            [
                                                html.H5(
                                                    'Is MPA management documented?',
                                                    id='documented_answer',
                                                    style={
                                                        'text-align': 'center',
                                                        'color': colors['background2'],
                                                        'margin': '30',
                                                        # 'height': '90',
                                                        'width': '240',
                                                    },
                                                ),
                                            ],
                                            className='three columns',
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    'Are management measures implemented?',
                                                    id='implemented_answer',
                                                    style={
                                                        'text-align': 'center',
                                                        'color': colors['background2'],
                                                        'margin': '30',
                                                        'width': '240',
                                                        # 'height': '90',
                                                    },
                                                ),
                                            ],
                                            className='three columns'
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    'Is monitoring in place?',
                                                    id='monitoring_answer',
                                                    style={
                                                        'text-align': 'center',
                                                        'color': colors['background2'],
                                                        'margin': '10',
                                                        'margin-top': '30',
                                                        'width': '240',
                                                        # 'height': '90',
                                                    },
                                                ),
                                            ],
                                            className='three columns'
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    'Moving towards conservation objectives?',
                                                    id='movement_answer',
                                                    style={
                                                        'text-align': 'center',
                                                        'color': colors['background2'],
                                                        'margin': '0',
                                                        'margin-top': '20',
                                                        'width': '240',
                                                        # 'height': '90',
                                                    },
                                                ),
                                            ],
                                            className='three columns'
                                        ),
                                    ],
                                    className='row'
                                ),
                                # Create HTML Divisions for management descriptions
                                html.Div(
                                    style={'backgroundColor': colors['text']}, children=[
                                        html.Div(
                                            style={'margin': 16,
                                                   'float': 'center'}, children=[
                                                dcc.Markdown(
                                                    dedent('''
                                                    Documentation description
                                                    '''),
                                                    containerProps={
                                                        'style': {
                                                            'textAlign': 'center',
                                                            'color': colors['background1'],
                                                        },
                                                    }
                                                ),
                                                dcc.Textarea(
                                                    id='documented_explanation',
                                                    value='Click an MPA on the map to get site information',
                                                    style={
                                                        'width': '290',
                                                        'text-align': 'center',
                                                        'color': colors['text'],
                                                        'height': '100',
                                                        'resize': 'None'
                                                    },
                                                    draggable=False,
                                                    disabled=True,
                                                    readOnly=True,
                                                    contentEditable=False
                                                ),
                                            ],
                                            className='three columns'
                                        ),
                                        html.Div(
                                            style={'margin': 16,
                                                   'float': 'center'}, children=[
                                                dcc.Markdown(
                                                    dedent('''
                                                                    Implementation description
                                                                                                        '''),
                                                    containerProps={
                                                        'style': {
                                                            'textAlign': 'center',
                                                            'color': colors['background1'],
                                                        },
                                                    }
                                                ),
                                                dcc.Textarea(
                                                    id='implemented_explanation',
                                                    value='Click an MPA on the map to get site information',
                                                    style={
                                                        'width': '290',
                                                        'text-align': 'center',
                                                        'color': colors['text'],
                                                        'height': '100',
                                                        'resize': 'None'
                                                    },
                                                    draggable=False,
                                                    disabled=True,
                                                    readOnly=True,
                                                    contentEditable=False
                                                ),
                                            ],
                                            className='three columns'
                                        ),
                                        html.Div(
                                            style={'margin': 16,
                                                   'float': 'center'}, children=[
                                                dcc.Markdown(
                                                    dedent('''
                                                    Monitoring description
                                                    '''),
                                                    containerProps={
                                                        'style': {
                                                            'textAlign': 'center',
                                                            'color': colors['background1'],
                                                        },
                                                    }
                                                ),
                                                dcc.Textarea(
                                                    id='monitoring_explanation',
                                                    value='Click an MPA on the map to get site information',
                                                    style={
                                                        'width': '290',
                                                        'text-align': 'center',
                                                        'color': colors['text'],
                                                        'height': '100',
                                                        'resize': 'None'
                                                    },
                                                    draggable=False,
                                                    disabled=True,
                                                    readOnly=True,
                                                    contentEditable=False
                                                ),
                                            ],
                                            className='three columns'
                                        ),
                                        html.Div(
                                            style={'margin': 16,
                                                   'float': 'center'}, children=[
                                                dcc.Markdown(
                                                    dedent('''
                                                                    Movement description
                                                                                                        '''),
                                                    containerProps={
                                                        'style': {
                                                            'textAlign': 'center',
                                                            'color': colors['background1'],
                                                        },
                                                    }
                                                ),
                                                dcc.Textarea(
                                                    id='movement_explanation',
                                                    value='Click an MPA on the map to get site information',
                                                    style={
                                                        'width': '290',
                                                        'text-align': 'center',
                                                        'color': colors['text'],
                                                        'height': '100',
                                                        'resize': 'None'
                                                    },
                                                    draggable=False,
                                                    disabled=True,
                                                    readOnly=True,
                                                    contentEditable=False
                                                ),
                                            ],
                                            className='three columns'
                                        ),
                                    ],
                                    className='row'
                                ),
                            ],
                        ),
                        # Create tabbed versions of management data displays

                        # html.Div(
                        #     style={'backgroundColor': colors['text']}, children=[
                        #         html.Div(
                        #             [
                        #                 dcc.Tabs(
                        #                     id='tab_controls',
                        #                     value='tab2_Site',
                        #                     children=[
                        #                         dcc.Tab(label='Site Specific Data', value='tab2_Site'),
                        #                         dcc.Tab(label='OSPAR, UK & Country Data', value='tab1_OSPAR'),
                        #                     ],
                        #                     colors={
                        #                         'border': colors['text'],
                        #                         'primary': colors['text'],
                        #                         'background': 'rgb(136,136,136)'
                        #                     }
                        #                 ),
                        #                 html.Div(
                        #                     id='tab_content'
                        #                 ),
                        #             ],
                        #         ),
                        #     ],
                        #     className='row'
                        #  ),
                        # html.Div(
                        #     style={'backgroundColor': colors['text']}, children=[
                        #         html.Div(
                        #             [
                        #                 dcc.Graph(
                        #                     id='management_pies'
                        #                 ),
                        #             ],
                        #         ),
                        #     ],
                        #     className='row'
                        # ),
                        # html.Div(
                        #     style={'backgroundColor': colors['text']}, children=[
                        #         html.Div(
                        #             [
                        #                 dcc.Markdown(
                        #                     dedent('''
                        #                     ## Site Specific Management Data:
                        #                     Click the protected areas on the map to load site specific MPA performance
                        #                     descriptions below
                        #                             '''),
                        #                     containerProps={
                        #                         'style': {
                        #                             'float': 'left',
                        #                             'color': colors['background1'],
                        #                             'margin': '20',
                        #                             'display': 'inline-block'
                        #                         },
                        #                     },
                        #                 ),
                        #             ],
                        #         ),
                        #         html.Div(
                        #             [
                        #                 html.P(
                        #                     'Site selected: No site currently selected',
                        #                     id='selected_site',
                        #                     style={
                        #                         'float': 'right',
                        #                         'color': colors['background1'],
                        #                         'margin': '20',
                        #                         # 'display': 'inline-block',
                        #                         'margin-top': '100',
                        #                     },
                        #                 ),
                        #             ],
                        #         ),
                        #     ],
                        #     className='row'
                        # ),
                        # # Create HTML Divisions for management descriptions
                        # html.Div(
                        #     style={'backgroundColor': colors['text']}, children=[
                        #         html.Div(
                        #             style={'margin': 16,
                        #                    'float': 'center'}, children=[
                        #                 dcc.Markdown(
                        #                     dedent('''
                        #             Documentation description
                        #                                                 '''),
                        #                     containerProps={
                        #                         'style': {
                        #                             'textAlign': 'center',
                        #                             'color': colors['background1'],
                        #                         },
                        #                     }
                        #                 ),
                        #                 dcc.Textarea(
                        #                     id='documented_explanation',
                        #                     value='Click an MPA on the map to get site information',
                        #                     style={
                        #                         'width': '290',
                        #                         'text-align': 'center',
                        #                         'color': colors['text'],
                        #                         'height': '100',
                        #                         'resize': 'None'
                        #                     },
                        #                     draggable=False,
                        #                     disabled=True,
                        #                     readOnly=True,
                        #                     contentEditable=False
                        #                 ),
                        #             ],
                        #             className='three columns'
                        #         ),
                        #         html.Div(
                        #             style={'margin': 16,
                        #                    'float': 'center'}, children=[
                        #                 dcc.Markdown(
                        #                     dedent('''
                        #             Implementation description
                        #                                                 '''),
                        #                     containerProps={
                        #                         'style': {
                        #                             'textAlign': 'center',
                        #                             'color': colors['background1'],
                        #                         },
                        #                     }
                        #                 ),
                        #                 dcc.Textarea(
                        #                     id='implemented_explanation',
                        #                     value='Click an MPA on the map to get site information',
                        #                     style={
                        #                         'width': '290',
                        #                         'text-align': 'center',
                        #                         'color': colors['text'],
                        #                         'height': '100',
                        #                         'resize': 'None'
                        #                     },
                        #                     draggable=False,
                        #                     disabled=True,
                        #                     readOnly=True,
                        #                     contentEditable=False
                        #                 ),
                        #             ],
                        #             className='three columns'
                        #         ),
                        #         html.Div(
                        #             style={'margin': 16,
                        #                    'float': 'center'}, children=[
                        #                 dcc.Markdown(
                        #                     dedent('''
                        #             Monitoring description
                        #                                                 '''),
                        #                     containerProps={
                        #                         'style': {
                        #                             'textAlign': 'center',
                        #                             'color': colors['background1'],
                        #                         },
                        #                     }
                        #                 ),
                        #                 dcc.Textarea(
                        #                     id='monitoring_explanation',
                        #                     value='Click an MPA on the map to get site information',
                        #                     style={
                        #                         'width': '290',
                        #                         'text-align': 'center',
                        #                         'color': colors['text'],
                        #                         'height': '100',
                        #                         'resize': 'None'
                        #                     },
                        #                     draggable=False,
                        #                     disabled=True,
                        #                     readOnly=True,
                        #                     contentEditable=False
                        #                 ),
                        #             ],
                        #             className='three columns'
                        #         ),
                        #         html.Div(
                        #             style={'margin': 16,
                        #                    'float': 'center'}, children=[
                        #                 dcc.Markdown(
                        #                     dedent('''
                        #             Movement description
                        #                                                 '''),
                        #                     containerProps={
                        #                         'style': {
                        #                             'textAlign': 'center',
                        #                             'color': colors['background1'],
                        #                         },
                        #                     }
                        #                 ),
                        #                 dcc.Textarea(
                        #                     id='movement_explanation',
                        #                     value='Click an MPA on the map to get site information',
                        #                     style={
                        #                         'width': '290',
                        #                         'text-align': 'center',
                        #                         'color': colors['text'],
                        #                         'height': '100',
                        #                         'resize': 'None'
                        #                     },
                        #                     draggable=False,
                        #                     disabled=True,
                        #                     readOnly=True,
                        #                     contentEditable=False
                        #                 ),
                        #             ],
                        #             className='three columns'
                        #         ),
                        #     ],
                        #     className='row'
                        # ),
                    ]
                ),
                # Create detailed descriptions of conservation management mechanisms / MPAs
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    'Marine Protected Areas (MPAs)',
                                    style={
                                        'color': colors['text'],
                                        'text-align': 'left',
                                        'margin-top': '100',
                                        'margin': '20',
                                    },
                                ),
                                dcc.Markdown(
                                    dedent('''

                                Our seas are home to some of the most biologically diverse 
                                [habitats](http://jncc.defra.gov.uk/page-1529) and 
                                [species](http://jncc.defra.gov.uk/page-1592) in Europe. Marine Protected Areas (MPAs) 
                                are one of the tools that can help us to protect the marine environment, whilst also 
                                enabling it's [sustainable use](http://jncc.defra.gov.uk/page-1528), ensuring it remains
                                healthy and contributes to our society for generations to come. JNCC is responsible for 
                                identifying and providing [conservation advice](http://jncc.defra.gov.uk/page-6849) on
                                MPAs in UK offshore waters (beyond 12 nautical miles). More information on our role can 
                                be found on the [MPA Overview page](http://jncc.defra.gov.uk/page-6906).

                                '''
                                           ),
                                    containerProps={
                                        'style': {
                                            'textAlign': 'justify',
                                            'color': colors['text'],
                                            'backgroundColor': colors['textbox'],
                                            'margin': '20',
                                            'font-size': '20',
                                        },
                                    }
                                ),
                            ],
                            className='twelve columns'
                        ),
                    ],
                    className='row'
                ),
                # Set descriptions for statistical data overview
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    ' Marine Protected Area Network Statistics ',
                                    style={
                                        'color': colors['text'],
                                        'text-align': 'left',
                                        'margin-top': '60',
                                        'margin': '20',
                                    },
                                ),
                                dcc.Markdown(
                                    dedent('''

                                    JNCC calculates statistics for the whole of the UK MPA network to assess 
                                    progress in MPA designation. 
                                    
                                    The statistical data represented within this dashboard comprises data from:
                                         
                                    * The [UK Exclusive Economic Zone (EEZ)](http://www.legislation.gov.uk/uksi/2013/3161/contents/made) and the [UK continental shelf](https://www.legislation.gov.uk/uksi/2013/3162/made).
                                    * All UK Inshore waters between the coast (here defined by mean high water (springs) and the [UK Territorial Sea](https://www.legislation.gov.uk/ukpga/1987/49) limit (up to 12 nautical miles out).
                                    * All UK Offshore waters between the UK Territorial Sea limit and the UK Exclusive Economic Zone or UK continental shelf.
                                    
                                    
                                    '''
                                           ),
                                    containerProps={
                                        'style': {
                                            'textAlign': 'justify',
                                            'color': colors['text'],
                                            'backgroundColor': colors['textbox'],
                                            'margin': '20',
                                            'font-size': '20',
                                        },
                                    },
                                ),
                            ],
                            className='twelve columns',
                        ),
                    ],
                    className='row'
                ),
                # Statistics by designation introduction, controls and graphs
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    ' Types of Marine Protected Area ',
                                    style={
                                        'color': colors['text'],
                                        'text-align': 'left',
                                        'margin-top': '60',
                                        'margin': '20',
                                    },
                                ),
                                dcc.Markdown(
                                    dedent('''

                                In the UK, as of March 2018 approximately 24% of our waters are currently within MPAs.
                                There are 105 [Special Areas of Conservation (SACs)](http://jncc.defra.gov.uk/page-1445)
                                with marine components, 107 
                                [Special Protection Areas (SPAs)](http://jncc.defra.gov.uk/page-1414) with marine 
                                components, 56 [Marine Conservation Zones](http://jncc.defra.gov.uk/page-4525)
                                and 30 [Nature Conservation Marine Protected Areas](http://jncc.defra.gov.uk/page-5269).
                                [Sites of Special Scientific Interest (SSSIs)](http://jncc.defra.gov.uk/page-2303)
                                with marine components and [Ramsar sites](http://jncc.defra.gov.uk/page-161) will also
                                form part of the UK’s contribution to an MPA network. Currently, the Statutory Nature
                                Conservation Agencies are confirming those SSSIs and Ramsar sites that will contribute 
                                to the MPA network through their protection of marine features.
                                
                                The MPA designation types included within this dashboard comprise Marine Conservation 
                                Zones (MCZs), Special Areas of Conservation (SACs) with marine components, Special 
                                Protection Areas (SPAs) with marine components, and Nature Conservation MPAs (NCMPAs).
                                
                                '''
                                           ),
                                    containerProps={
                                        'style': {
                                            'textAlign': 'justify',
                                            'color': colors['text'],
                                            'backgroundColor': colors['textbox'],
                                            'margin': '20',
                                            'font-size': '20',
                                        },
                                    },
                                ),
                            ],
                            className='twelve columns',
                        ),
                    ],
                    className='row'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Markdown(
                                    dedent('''
                                    ## Data by MPA Designation:

                                    ##### Change location using the filter below to toggle data displayed in the graphs 
                                                                        '''),
                                    containerProps={
                                        'style': {
                                            'textAlign': 'left',
                                            'color': colors['text'],
                                            'margin': '20',
                                            'margin-top': '45'
                                        },
                                    }
                                ),
                            ],

                        ),
                    ],
                    className='row'
                ),
                # Control panel for designation statistics graphs
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id='LocationGraphs',
                                            options=[{'label': i, 'value': i} for i in availableLocations],
                                            # Allows for all or singular filtering
                                            multi=False,
                                            value='All UK waters (EEZ+UKCS)',
                                        ),
                                    ],
                                ),
                            ],
                            className='twelve columns'
                        ),
                    ],
                    className='row'
                ),
                # Statistics by designation graphs
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='percentage_pie')
                            ],
                            className='six columns',
                            style={'margin-top': '10'}
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='mpa_count')
                            ],
                            className='six columns',
                            style={'margin-top': '10'}
                        ),
                    ],
                    className='row',
                ),
                # OSPAR Introduction and controls
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    ' Our Work Internationally ',
                                    style={
                                        'color': colors['text'],
                                        'text-align': 'left',
                                        'margin-top': '60',
                                        'margin': '20',
                                    },
                                ),
                                html.H4(
                                    'OSPAR Regions',
                                    style={
                                        'color': colors['text'],
                                        'text-align': 'left',
                                        'margin-top': '60',
                                        'margin': '20',
                                    },
                                ),
                                dcc.Markdown(
                                    dedent("""
                                    
                                    The UK is a signatory to the [Oslo and Paris Convention (OSPAR)](http://www.ospar.org/), 
                                    which requires contracting parties to establish an ecologically coherent and 
                                    well-managed network of MPAs across the North-east Atlantic as per the [North-east 
                                    Atlantic biodiversity strategy](http://www.ospar.org/site/assets/files/1466/biodiversity_strategy.pdf).
                                    In 2012, Defra and the Devolved Administrations published a 
                                    [statement](http://www.scotland.gov.uk/Resource/0041/00411304.pdf) 
                                    setting out how the UK will contribute to this target. The UK MPA network is 
                                    intended to contribute toward the protection of [OSPAR threatened and/or declining 
                                    habitats and species](http://www.ospar.org/work-areas/bdc/species-habitats/list-of-threatened-declining-species-habitats),
                                    and the conservation of areas which best represent the range of species, habitats 
                                    and ecological processes in the OSPAR Maritime Area.
                                    
                                    
                                    JNCC leads on the provision of scientific advice to the UK delegation at OSPAR MPA 
                                    working group meetings, including methods of assessment for ecological coherence and
                                    management effectiveness. Our work has included taking a leading role as part of an
                                    ecological coherence steering group in the OSPAR Commission’s contract to 
                                    [assess the ecological coherence of the MPA network across the North-East Atlantic](http://www.ospar.org/documents?d=7346). 
                                    JNCC staff lead work within OSPAR on assessing ecological coherence through the 
                                    OSPAR ecological coherence task group. The UK has identified a total of 283 OSPAR 
                                    MPAs to date, consisting of existing MPAs already established in UK waters 
                                    (such as Special Areas of Conservation, Special Protection Areas, Nature 
                                    Conservation MPAs and Marine Conservation Zones). Information on OSPAR MPAs 
                                    that have been submitted by Contracting Parties is available from the 
                                    [OSPAR Commission](http://www.ospar.org/data).
                                    
                                """),
                                    containerProps={
                                        'style': {
                                            'textAlign': 'justify',
                                            'color': colors['text'],
                                            'backgroundColor': colors['textbox'],
                                            'margin': '20',
                                            'font-size': '20',
                                        },
                                    },
                                ),
                            ],
                            className='twelve columns',
                        ),
                    ],
                    className='row',
                ),
            ],
            className='ten columns offset-by-one'
        ),
    ],
)


########################################################################################################################

#                                     Main Controls: RadioItems / checkbox callbacks

########################################################################################################################

# Create main control panel controls - combination of radio items which update drop-down menu

@app.callback(
    dash.dependencies.Output('Location', 'options'),
    [dash.dependencies.Input('mainSelector', 'value')]
)
def main_control(main_filter):
    options = []
    if main_filter == 'UK':
        options = [{'label': i, 'value': i} for i in inshoreOffshore]
    elif main_filter == 'Country':
        options = [{'label': i, 'value': i} for i in availableLocations]
    elif main_filter == 'OSPAR':
        options = [{'label': i, 'value': i} for i in osparRegions]
    return options


########################################################################################################################

#                                     Summary Statistics: Key output callbacks

########################################################################################################################

# Create callback operators for key summary statistical returns

# Create application callback decorator to update the Total MPA Number text box in key summary header
@app.callback(
    dash.dependencies.Output('mpa_number', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_count(selected_location):
    if selected_location == 'Region I: Arctic Waters':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['Area of OSPAR region (km2)']
        for each in result:
            return 'Area of OSPAR Region (km2): ' + str(each)
    elif selected_location == 'Region II: Greater North Sea':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['Area of OSPAR region (km2)']
        for each in result:
            return 'Area of OSPAR Region (km2): ' + str(each)
    elif selected_location == 'Region III: Celtic Seas':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['Area of OSPAR region (km2)']
        for each in result:
            return 'Area of OSPAR Region (km2): ' + str(each)
    elif selected_location == 'Region V: Wider Atlantic':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['Area of OSPAR region (km2)']
        for each in result:
            return 'Area of OSPAR Region (km2): ' + str(each)
    else:
        filtered_df = summaryAll_df[summaryAll_df.Location == selected_location]
        result = filtered_df['Total no. of MPAs']
        for each in result:
            return str(each) + ' Marine Protected Areas'


# Create application callback decorator to update Total Area Number text box in key summary header
@app.callback(
    dash.dependencies.Output('total_area', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_area(selected_location):
    if selected_location == 'Region I: Arctic Waters':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['Area of UK MPAs (km2)']
        for each in result:
            return 'Area of UK MPAs (km2): ' + str(each)
    elif selected_location == 'Region II: Greater North Sea':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['Area of UK MPAs (km2)']
        for each in result:
            return 'Area of UK MPAs (km2): ' + str(each)
    elif selected_location == 'Region III: Celtic Seas':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['Area of UK MPAs (km2)']
        for each in result:
            return 'Area of UK MPAs (km2): ' + str(each)
    elif selected_location == 'Region V: Wider Atlantic':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['Area of UK MPAs (km2)']
        for each in result:
            return 'Area of UK MPAs (km2): ' + str(each)
    else:
        filtered_df = summaryAll_df[summaryAll_df.Location == selected_location]
        result = filtered_df['Total Area of MPAs']
        for each in result:
            return 'Area of MPAs (km2):  ' + str(each)


# Create application callback decorator to update Total Percent Covered by MPA text box in key summary header
@app.callback(
    dash.dependencies.Output('total_percentage', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_area(selected_location):
    if selected_location == 'Region I: Arctic Waters':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['% of OSPAR region']
        for each in result:
            return '% of OSPAR Region: ' + str(each) + '%'
    elif selected_location == 'Region II: Greater North Sea':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['% of OSPAR region']
        for each in result:
            return '% of OSPAR Region: ' + str(each) + '%'
    elif selected_location == 'Region III: Celtic Seas':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['% of OSPAR region']
        for each in result:
            return '% of OSPAR Region: ' + str(each) + '%'
    elif selected_location == 'Region V: Wider Atlantic':
        filtered_df = summaryOSPAR_df[summaryOSPAR_df.Location == selected_location]
        result = filtered_df['% of OSPAR region']
        for each in result:
            return '% of OSPAR Region: ' + str(each) + '%'
    else:
        filtered_df = summaryAll_df[summaryAll_df.Location == selected_location]
        result = filtered_df['Total % of location covered by MPAs']
        for each in result:
            return 'Total % covered by MPAs:  ' + str(each) + '%'


########################################################################################################################

#                                     Main Dashboard: Main Graph callbacks

########################################################################################################################

# Functions to filter data used within the main map

# Create function to filter latitude based on selected_location

def filtered_lat(selected_location):
    # Returns for all UK data
    if selected_location == 'All UK waters (EEZ+UKCS)':
        return 56.6
    elif selected_location == 'UK inshore (territorial seas)':
        return 56.6
    elif selected_location == 'UK offshore':
        return 56.6

    # Returns for Inshore and Offshore by country data
    elif selected_location == 'England':
        return 52.6
    elif selected_location == 'Wales':
        return 52.15
    elif selected_location == 'Scotland':
        return 59.5
    elif selected_location == 'Northern Ireland':
        return 54.4

    # Returns for OSPAR Selections - THANK YOU TOM
    elif selected_location == 'Region I: Arctic Waters':
        return 61.6
    elif selected_location == 'Region II: Greater North Sea':
        return 57.2
    elif selected_location == 'Region III: Celtic Seas':
        return 54.5
    elif selected_location == 'Region V: Wider Atlantic':
        return 54.5


# Create function to filter longitude based on selected_location

def filtered_long(selected_location):
    # Returns for all UK data
    if selected_location == 'All UK waters (EEZ+UKCS)':
        return -3.9
    elif selected_location == 'UK inshore (territorial seas)':
        return -3.9
    elif selected_location == 'UK offshore':
        return -3.9

    # Returns for Inshore and Offshore by country data
    elif selected_location == 'England':
        return -2.5
    elif selected_location == 'Wales':
        return -4.8
    elif selected_location == 'Scotland':
        return -6.2
    elif selected_location == 'Northern Ireland':
        return -5.8

    # Returns for OSPAR Selections - THANK YOU TOM
    elif selected_location == 'Region I: Arctic Waters':
        return -4.6
    elif selected_location == 'Region II: Greater North Sea':
        return -4.2
    elif selected_location == 'Region III: Celtic Seas':
        return -6.2
    elif selected_location == 'Region V: Wider Atlantic':
        return -10.0


# Create function to reset zoom dependent on selected_location

def filtered_zoom(selected_location):
    # Returns for all UK data
    if selected_location == 'All UK waters (EEZ+UKCS)':
        return 4.0
    elif selected_location == 'UK inshore (territorial seas)':
        return 4.0
    elif selected_location == 'UK offshore':
        return 4.0

    # Returns for Inshore and Offshore by country data
    elif selected_location == 'England':
        return 5.0
    elif selected_location == 'Wales':
        return 6.1
    elif selected_location == 'Scotland':
        return 4.6
    elif selected_location == 'Northern Ireland':
        return 6.5

    # Returns for OSPAR Selections - THANK YOU TOM
    elif selected_location == 'Region I: Arctic Waters':
        return 5.0
    elif selected_location == 'Region II: Greater North Sea':
        return 4.1
    elif selected_location == 'Region III: Celtic Seas':
        return 4.5
    elif selected_location == 'Region V: Wider Atlantic':
        return 4.4


# Create function to filter data by selected_location
def filtered_location(selected_location):

    """
    Create bespoke returns dependent on the input selection. If these are multiple inputs,
    then provide a return which is a combination of multiple singular returns. Otherwise,
    if the input location is a singular value, then return the singular output.
    """

    # Returns for all UK data
    if selected_location == 'All UK waters (EEZ+UKCS)':
        return [x for x in mpaJson["features"]]
    elif selected_location == 'UK inshore (territorial seas)':
        return [x for x in mpaJson["features"] if 'inshore' in x["properties"]["Country"]]
    elif selected_location == 'UK offshore':
        return [x for x in mpaJson["features"] if 'offshore' in x["properties"]["Country"]]

    # Returns for Inshore and Offshore by country data
    elif selected_location == 'England':
        return [x for x in mpaJson["features"] if 'England' in x["properties"]["Country"]]
    elif selected_location == 'Wales':
        return [x for x in mpaJson["features"] if 'Wales' in x["properties"]["Country"]]
    elif selected_location == 'Scotland':
        return [x for x in mpaJson["features"] if 'Scotland' in x["properties"]["Country"]]
    elif selected_location == 'Northern Ireland':
        return [x for x in mpaJson["features"] if 'Northern Ireland' in x["properties"]["Country"]]

    # Returns for OSPAR Selections - YAY THANK YOU TOM
    elif selected_location == 'Region I: Arctic Waters':
        return [x for x in mpaJson["features"] if 'Arctic Waters' in x["properties"]["OSPAR_Re_1"]]
    elif selected_location == 'Region II: Greater North Sea':
        return [x for x in mpaJson["features"] if 'Greater North Sea' in x["properties"]["OSPAR_Re_1"]]
    elif selected_location == 'Region III: Celtic Seas':
        return [x for x in mpaJson["features"] if 'Celtic Seas' in x["properties"]["OSPAR_Re_1"]]
    elif selected_location == 'Region V: Wider Atlantic':
        return [x for x in mpaJson["features"] if 'Wider Atlantic' in x["properties"]["OSPAR_Re_1"]]

    # Singular returns for singular selected locations
    else:
        return [x for x in mpaJson["features"] if x["properties"]["Country"] == selected_location]


# Create function to filter opacity for OSPAR boundary data
def filtered_opacity(selected_location):
    # Returns for all UK data
    if selected_location == 'All UK waters (EEZ+UKCS)':
        return 0.2
    elif selected_location == 'UK inshore (territorial seas)':
        return 0.2
    elif selected_location == 'UK offshore':
        return 0.2

    # Returns for Inshore and Offshore by country data
    elif selected_location == 'England':
        return 0.2
    elif selected_location == 'Wales':
        return 0.2
    elif selected_location == 'Scotland':
        return 0.2
    elif selected_location == 'Northern Ireland':
        return 0.2

    # Returns for OSPAR Selections - THANK YOU TOM
    elif selected_location == 'Region I: Arctic Waters':
        return 0.8
    elif selected_location == 'Region II: Greater North Sea':
        return 0.8
    elif selected_location == 'Region III: Celtic Seas':
        return 0.8
    elif selected_location == 'Region V: Wider Atlantic':
        return 0.8


# Create function to return correct components of filtered GeoJson properties for hover info

def hover_info(filteredjson):
    site_name = [filteredjson['features'][k]['properties']['SITE_NAME'] for k in
                 range(len(filteredjson['features']))]
    designation = [filteredjson['features'][k]['properties']['SITE_STATU'] for k in
                   range(len(filteredjson['features']))]
    hover_list = zip(site_name, designation)
    string_list = [f'{x} ({y})' for x, y in hover_list]
    return string_list

########################################################################################################################


# Callback operators for main map

# Create application callback decorator for main graph
@app.callback(
    dash.dependencies.Output('main_graph', 'figure'),
    # Functioning radioItems code
    [dash.dependencies.Input('Location', 'value')]
)
def make_main_graph(selected_location):
    # Identify locations of all entries within json file
    print(selected_location)
    # Create filtered json data from mpaJson and add features to newly created object
    # moved into function above
    filteredjson = {k: v for k, v in mpaJson.items() if k != "features"}
    filteredjson['features'] = filtered_location(selected_location)

    traces = []

    traces.append(
        go.Scattermapbox(
            lat=[filteredjson['features'][k]['properties']['LAT_dd'] for k in range(len(filteredjson['features']))],
            lon=[filteredjson['features'][k]['properties']['LONG_dd'] for k in range(len(filteredjson['features']))],
            text=hover_info(filteredjson),
            hoverinfo='text',
            marker=dict(
                color=colors['text'],
                opacity=0,
            ),
        ),
    ),
    return {
        'data': traces,
        'layout': go.Layout(
            autosize=True,
            height=700,
            font=dict(
                color=colors['text']
            ),
            titlefont=dict(
                color=colors['text'],
                size=14
            ),
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            ),
            hovermode='closest',
            plot_bgcolor=colors['background1'],
            paper_bgcolor=colors['background1'],
            legend=dict(
                font=dict(
                    size=10
                ),
                orientation='h'
            ),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style='dark',
                center=dict(
                    lon=filtered_long(selected_location),
                    lat=filtered_lat(selected_location),
                ),
                zoom=filtered_zoom(selected_location),
                # Add OSPAR Regional Data Layers - Outlines to map
                layers=[
                    dict(
                        sourcetype='geojson',
                        source=osparBoundaries,
                        type='line',
                        color=colors['background1'],
                        opacity=filtered_opacity(selected_location)
                        ),
                    dict(
                        sourcetype='geojson',
                        source=filteredjson,
                        type='fill',
                        color=colors['filteredjson'],
                        opacity=0.4
                        ),
                ],
            ),
        ),
    }

# Tab callbacks not currently in use

########################################################################################################################

#                                     Main Dashboard: Tab callbacks

########################################################################################################################
#
# # Create callback operator to return individual tabs - OSPAR level or site specific data
#
# @app.callback(dash.dependencies.Output('tab_content', 'children'),
#               [dash.dependencies.Input('tab_controls', 'value')]
#               )
# def render_tab_content(tab):
#     if tab == 'tab1_OSPAR':
#         return html.Div(
#             [
#                 dcc.Markdown(
#                     dedent('''
#                     ## OSPAR, UK & Country Data
#                     Use the main filters at the top of the dashboard to filter information shown in the pie
#                     charts. Toggle which data are visible by clicking their icon in the legend below the graphs
#                                                                     '''),
#                     containerProps={
#                         'style': {
#                             'float': 'center',
#                             'textAlign': 'center',
#                             'color': colors['background1'],
#                         },
#                     },
#                 ),
#                 dcc.Graph(
#                     id='management_pies'
#                 ),
#             ],
#         ),
#     elif tab == 'tab2_Site':
#         return html.Div(
#             style={'backgroundColor': colors['text']}, children=[
#                 html.Div(
#                     [
#                         dcc.Markdown(
#                             dedent('''
#                             ## Site Specific Management Data
#                             Load site specific data by clicking on the MPA within the interactive mapper.
#                             '''),
#                             containerProps={
#                                 'style': {
#                                     'float': 'center',
#                                     'textAlign': 'center',
#                                     'color': colors['background1'],
#                                 },
#                             },
#                         ),
#                     ],
#                     className='row'
#                 ),
#                 html.Div(
#                     style={'backgroundColor': colors['text']}, children=[
#                         html.H3('Site selected: Select a site by clicking an MPA boundary',
#                             id='selected_site',
#                             style={
#                                 'float': 'left',
#                                 'color': colors['background1'],
#                                 'margin': '20',
#                                 'margin-top': '10',
#                             },
#                         ),
#                     ],
#                     className='row',
#                 ),
#                 html.Div(
#                     style={'backgroundColor': colors['text']}, children=[
#                         html.Div(
#                             [
#                                 html.H5(
#                                     'Is MPA management documented?',
#                                     id='documented_answer',
#                                     style={
#                                         'text-align': 'center',
#                                         'color': colors['background2'],
#                                         'margin': '30',
#                                         'height': '90',
#                                         'width': '240',
#                                     },
#                                 ),
#                             ],
#                             className='three columns',
#                         ),
#                         html.Div(
#                             [
#                                 html.H5(
#                                     'Are management measures implemented?',
#                                     id='implemented_answer',
#                                     style={
#                                         'text-align': 'center',
#                                         'color': colors['background2'],
#                                         'margin': '30',
#                                         'width': '240',
#                                         'height': '90',
#                                     },
#                                 ),
#                             ],
#                             className='three columns'
#                         ),
#                         html.Div(
#                             [
#                                 html.H5(
#                                     'Is monitoring in place?',
#                                     id='monitoring_answer',
#                                     style={
#                                         'text-align': 'center',
#                                         'color': colors['background2'],
#                                         'margin': '10',
#                                         'margin-top': '30',
#                                         'width': '240',
#                                         'height': '90',
#                                     },
#                                 ),
#                             ],
#                             className='three columns'
#                         ),
#                         html.Div(
#                             [
#                                 html.H5(
#                                     'Moving towards conservation objectives?',
#                                     id='movement_answer',
#                                     style={
#                                         'text-align': 'center',
#                                         'color': colors['background2'],
#                                         'margin': '0',
#                                         'margin-top': '20',
#                                         'width': '240',
#                                         'height': '90',
#                                     },
#                                 ),
#                             ],
#                             className='three columns'
#                         ),
#                     ],
#                     className='row'
#                 ),
#                 # Create HTML Divisions for management descriptions
#                 html.Div(
#                     style={'backgroundColor': colors['text']}, children=[
#                         html.Div(
#                             style={'margin': 16,
#                                    'float': 'center'}, children=[
#                                 dcc.Markdown(
#                                     dedent('''
#                                     Documentation description
#                                     '''),
#                                     containerProps={
#                                         'style': {
#                                             'textAlign': 'center',
#                                             'color': colors['background1'],
#                                         },
#                                     }
#                                 ),
#                                 dcc.Textarea(
#                                     id='documented_explanation',
#                                     value='Click an MPA on the map to get site information',
#                                     style={
#                                         'width': '290',
#                                         'text-align': 'center',
#                                         'color': colors['text'],
#                                         'height': '100',
#                                         'resize': 'None'
#                                     },
#                                     draggable=False,
#                                     disabled=True,
#                                     readOnly=True,
#                                     contentEditable=False
#                                 ),
#                             ],
#                             className='three columns'
#                         ),
#                         html.Div(
#                             style={'margin': 16,
#                                    'float': 'center'}, children=[
#                                 dcc.Markdown(
#                                     dedent('''
#                                                     Implementation description
#                                                                                         '''),
#                                     containerProps={
#                                         'style': {
#                                             'textAlign': 'center',
#                                             'color': colors['background1'],
#                                         },
#                                     }
#                                 ),
#                                 dcc.Textarea(
#                                     id='implemented_explanation',
#                                     value='Click an MPA on the map to get site information',
#                                     style={
#                                         'width': '290',
#                                         'text-align': 'center',
#                                         'color': colors['text'],
#                                         'height': '100',
#                                         'resize': 'None'
#                                     },
#                                     draggable=False,
#                                     disabled=True,
#                                     readOnly=True,
#                                     contentEditable=False
#                                 ),
#                             ],
#                             className='three columns'
#                         ),
#                         html.Div(
#                             style={'margin': 16,
#                                    'float': 'center'}, children=[
#                                 dcc.Markdown(
#                                     dedent('''
#                                     Monitoring description
#                                     '''),
#                                     containerProps={
#                                         'style': {
#                                             'textAlign': 'center',
#                                             'color': colors['background1'],
#                                         },
#                                     }
#                                 ),
#                                 dcc.Textarea(
#                                     id='monitoring_explanation',
#                                     value='Click an MPA on the map to get site information',
#                                     style={
#                                         'width': '290',
#                                         'text-align': 'center',
#                                         'color': colors['text'],
#                                         'height': '100',
#                                         'resize': 'None'
#                                     },
#                                     draggable=False,
#                                     disabled=True,
#                                     readOnly=True,
#                                     contentEditable=False
#                                 ),
#                             ],
#                             className='three columns'
#                         ),
#                         html.Div(
#                             style={'margin': 16,
#                                    'float': 'center'}, children=[
#                                 dcc.Markdown(
#                                     dedent('''
#                                                     Movement description
#                                                                                         '''),
#                                     containerProps={
#                                         'style': {
#                                             'textAlign': 'center',
#                                             'color': colors['background1'],
#                                         },
#                                     }
#                                 ),
#                                 dcc.Textarea(
#                                     id='movement_explanation',
#                                     value='Click an MPA on the map to get site information',
#                                     style={
#                                         'width': '290',
#                                         'text-align': 'center',
#                                         'color': colors['text'],
#                                         'height': '100',
#                                         'resize': 'None'
#                                     },
#                                     draggable=False,
#                                     disabled=True,
#                                     readOnly=True,
#                                     contentEditable=False
#                                 ),
#                             ],
#                             className='three columns'
#                         ),
#                     ],
#                     className='row'
#                 ),
#             ],
#         ),


########################################################################################################################

#                                     Main Dashboard: OSPAR evaluation callbacks

########################################################################################################################

# Functions to filter data used within the OSPAR


# Define function which calculates and returns the total count of the targeted OSPAR management question column values

def ospar_selector(selected_location):
    # Create filters for all UK data
    if selected_location == 'All UK waters (EEZ+UKCS)':
        return summaryManagement_df
    elif selected_location == 'UK inshore (territorial seas)':
        return summaryManagement_df.loc[summaryManagement_df['Country'].isin([
            'England inshore', 'Wales inshore', 'Scotland inshore', 'Northern Ireland inshore'])]
    elif selected_location == 'UK offshore':
        return summaryManagement_df.loc[summaryManagement_df['Country'].isin([
            'England offshore', 'Wales offshore', 'Scotland offshore', 'Northern Ireland offshore'])]

    # Returns for Inshore and Offshore by country data
    elif selected_location == 'England':
        return summaryManagement_df.loc[summaryManagement_df['Country'].isin([
            'England inshore', 'England offshore'])]
    elif selected_location == 'Wales':
        return summaryManagement_df.loc[summaryManagement_df['Country'].isin([
            'Wales inshore', 'Wales offshore'])]
    elif selected_location == 'Scotland':
        return summaryManagement_df.loc[summaryManagement_df['Country'].isin([
            'Scotland inshore', 'Scotland offshore'])]
    elif selected_location == 'Northern Ireland':
        return summaryManagement_df.loc[summaryManagement_df['Country'].isin([
            'Northern Ireland inshore', 'Northern Ireland offshore'])]


# Define function to return the total count of each value within each OSPAR management question
def ospar_counter(df, target, score):
    if target == 'MANAGEMENT DOCUMENTED':
        return len(df[target].loc[df[target].isin([score])])
    elif target == 'MEASURES IMPLEMENTED':
        return len(df[target].loc[df[target].isin([score])])
    elif target == 'MONITORING IN PLACE':
        return len(df[target].loc[df[target].isin([score])])
    elif target == 'MOVING TOWARDS OBJECTIVES':
        return len(df[target].loc[df[target].isin([score])])


########################################################################################################################

# Create callback operator to build ospar management pie graphs

# Create application callback decorator to update management pie charts with location selection
@app.callback(
    dash.dependencies.Output('management_pies', 'figure'),
    [dash.dependencies.Input('Location', 'value')]
)
def update_management_pies(selected_location):
    filtered_df = ospar_selector(selected_location)

    # Data filtered for Documented Pie
    doc_partial = ospar_counter(filtered_df, 'MANAGEMENT DOCUMENTED', 'Partial')
    doc_yes = ospar_counter(filtered_df, 'MANAGEMENT DOCUMENTED', 'Yes')

    # Data filtered for Implemented Pie
    imp_partial = ospar_counter(filtered_df, 'MEASURES IMPLEMENTED', 'Partial')
    imp_yes = ospar_counter(filtered_df, 'MEASURES IMPLEMENTED', 'Yes')
    imp_n_avail = ospar_counter(filtered_df, 'MEASURES IMPLEMENTED', 'Not available')

    # Data filtered for Monitoring Pie
    mon_no = ospar_counter(filtered_df, 'MONITORING IN PLACE', 'No')
    mon_n_avail = ospar_counter(filtered_df, 'MEASURES IMPLEMENTED', 'Not available')
    mon_partial = ospar_counter(filtered_df, 'MONITORING IN PLACE', 'Partial')
    mon_yes = ospar_counter(filtered_df, 'MONITORING IN PLACE', 'Yes')

    # Data filtered for Objectives Pie
    obj_no = ospar_counter(filtered_df, 'MOVING TOWARDS OBJECTIVES', 'No')
    obj_partial = ospar_counter(filtered_df, 'MOVING TOWARDS OBJECTIVES', 'Partial')
    obj_yes = ospar_counter(filtered_df, 'MOVING TOWARDS OBJECTIVES', 'Yes')
    obj_unknown = ospar_counter(filtered_df, 'MOVING TOWARDS OBJECTIVES', 'Unknown')

    return {'data': [
                {
                    'labels': ['Partially', 'Yes'],
                    'values': [doc_partial, doc_yes],
                    'type': 'pie',
                    'title': 'Is MPA Management Documented?',
                    'marker': dict(
                        # colors=pd.Series(colors['management_cols']),
                        colors=['#957DAD', '#D291BC'],
                        line=dict(color='#ccccc0', width=2)
                    ),
                    'domain': {'x': [0, 0.25],
                               'y': [0, 1]},
                    'hoverinfo': 'label',
                    'textposition': 'outside',
                    'textinfo': 'value',
                    'pull': 0.1,
                    'hole': 0.1
                },
                {
                    'labels': ['Partially', 'Yes', 'Not available'],
                    'values': [imp_partial, imp_yes, imp_n_avail],
                    'type': 'pie',
                    'title': 'Is MPA Management Implemented?',
                    'marker': dict(
                        # colors=pd.Series(colors['management_cols']),
                        colors=['#957DAD', '#D291BC', '#FEC8D8'],
                        line=dict(color='#ccccc0', width=2)
                    ),
                    'domain': {'x': [0.25, 0.5],
                               'y': [0, 1]},
                    'hoverinfo': 'label',
                    'textposition': 'outside',
                    'textinfo': 'value',
                    'pull': 0.1,
                    'hole': 0.1
                },
                {
                    'labels': ['No', 'Not available', 'Partially', 'Yes'],
                    'values': [mon_no, mon_n_avail, mon_partial, mon_yes],
                    'type': 'pie',
                    'title': 'Is MPA Monitoring In Place?',
                    'marker': dict(
                        # colors=pd.Series(colors['management_cols']),
                        colors=['#b6e1f6', '#FEC8D8', '#957DAD', '#D291BC'],
                        line=dict(color='#ccccc0', width=2)
                    ),
                    'domain': {'x': [0.5, 0.75],
                               'y': [0, 1]},
                    'hoverinfo': 'label',
                    'textposition': 'outside',
                    'textinfo': 'value',
                    'pull': 0.1,
                    'hole': 0.1
                },
                {
                    'labels': ['No', 'Partially', 'Yes', 'Unknown'],
                    'values': [obj_no, obj_partial, obj_yes, obj_unknown],
                    'type': 'pie',
                    'title': 'Moving To Meet Objectives?',
                    'marker': dict(
                        # colors=pd.Series(colors['management_cols']),
                        colors=['#b6e1f6', '#957DAD', '#D291BC', '#FFDFD3'],
                        line=dict(color='#ccccc0', width=2)
                    ),
                    'domain': {'x': [0.75, 1],
                               'y': [0, 1]},
                    'hoverinfo': 'label',
                    'textposition': 'outside',
                    'textinfo': 'value',
                    'pull': 0.1,
                    'hole': 0.1
                }
    ],
        'layout': go.Layout(
            font=dict(color=colors['background1']),
            hovermode='closest',
            paper_bgcolor=colors['text'],
            plot_bgcolor=colors['text'],
            autosize=True,
            legend=dict(orientation="h",
                        x=0.3,
                        y=-0.1),
            annotations=[
                {
                    "font": {
                        "size": 14
                    },
                    "showarrow": False,
                    "text": 'Is Management Documented?',
                    "x": 0.0,
                    "y": 1.3
                },
                {
                    "font": {
                        "size": 14
                    },
                    "showarrow": False,
                    "text": 'Is Management Implemented?',
                    "x": 0.26,
                    "y": 1.3
                },
                {
                    "font": {
                        "size": 14
                    },
                    "showarrow": False,
                    "text": 'Is Monitoring In Place?',
                    "x": 0.71,
                    "y": 1.3
                },
                {
                    "font": {
                        "size": 14
                    },
                    "showarrow": False,
                    "text": 'Moving Towards Objectives?',
                    "x": 0.99,
                    "y": 1.3
                },
            ],
        )
    }

########################################################################################################################


# Define function to return OSPAR documentation answer
@app.callback(
    dash.dependencies.Output('documented_answer', 'children'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def documented_answer(clickData):
    selected_site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    strsite = str(selected_site)
    for siteName in summaryManagement_df['Site Name']:
        if siteName in strsite:
            data = summaryManagement_df.loc[summaryManagement_df['Site Name'].isin([siteName])]
            return 'Is management documented: ' + data['MANAGEMENT DOCUMENTED']


# Define function to return OSPAR implementation answer
@app.callback(
    dash.dependencies.Output('implemented_answer', 'children'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def documented_answer(clickData):
    selected_site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    strsite = str(selected_site)
    for siteName in summaryManagement_df['Site Name']:
        if siteName in strsite:
            data = summaryManagement_df.loc[summaryManagement_df['Site Name'].isin([siteName])]
            return 'Are measures implemented: ' + data['MEASURES IMPLEMENTED']


# Define function to return OSPAR monitoring answer
@app.callback(
    dash.dependencies.Output('monitoring_answer', 'children'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def documented_answer(clickData):
    selected_site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    strsite = str(selected_site)
    for siteName in summaryManagement_df['Site Name']:
        if siteName in strsite:
            data = summaryManagement_df.loc[summaryManagement_df['Site Name'].isin([siteName])]
            return 'Is monitoring in place: ' + data['MONITORING IN PLACE']


# Define function to return OSPAR monitoring answer
@app.callback(
    dash.dependencies.Output('movement_answer', 'children'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def documented_answer(clickData):
    selected_site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    strsite = str(selected_site)
    for siteName in summaryManagement_df['Site Name']:
        if siteName in strsite:
            data = summaryManagement_df.loc[summaryManagement_df['Site Name'].isin([siteName])]
            return 'Moving towards conservation objectives: ' + data['MOVING TOWARDS OBJECTIVES']


########################################################################################################################

# Create main control title selection header
@app.callback(
    dash.dependencies.Output('main_selection', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def main_selection(selected_location):
    return 'Selected location: ' + str(selected_location)


# Define function to return string value of the selected site
@app.callback(
    dash.dependencies.Output('selected_site', 'children'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def display_selected_site(clickData):
    site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    selected_site = ''.join(site)
    return 'Site selected: ' + str(selected_site)


# Define function to return documented management descriptions for each selected site
@app.callback(
    dash.dependencies.Output('documented_explanation', 'value'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def display_documented_click_data(clickData):
    selected_site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    strsite = str(selected_site)
    for siteName in summaryManagement_df['Site Name']:
        if siteName in strsite:
            data = summaryManagement_df.loc[summaryManagement_df['Site Name'].isin([siteName])]
            return data['MANAGEMENT DOCUMENTED desc']


# Define function to return implementation descriptions for each selected site
@app.callback(
    dash.dependencies.Output('implemented_explanation', 'value'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def display__implemented_click_data(clickData):
    selected_site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    strsite = str(selected_site)
    for siteName in summaryManagement_df['Site Name']:
        if siteName in strsite:
            data = summaryManagement_df.loc[summaryManagement_df['Site Name'].isin([siteName])]
            return data['MEASURES IMPLEMENTED desc']
        # else:
        #     return 'Data not available'


# Define function to return monitoring descriptions for each selected site
@app.callback(
    dash.dependencies.Output('monitoring_explanation', 'value'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def display_monitoring_click_data(clickData):
    selected_site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    strsite = str(selected_site)
    for siteName in summaryManagement_df['Site Name']:
        if siteName in strsite:
            data = summaryManagement_df.loc[summaryManagement_df['Site Name'].isin([siteName])]
            return data['MONITORING IN PLACE desc']
        # else:
        #     return 'Data not available'


# Define function to return monitoring descriptions for each selected site
@app.callback(
    dash.dependencies.Output('movement_explanation', 'value'),
    [dash.dependencies.Input('main_graph', 'clickData')]
)
def display_movement_click_data(clickData):
    selected_site = [clickData['points'][k]['text'] for k in range(len(clickData['points']))]
    strsite = str(selected_site)
    for siteName in summaryManagement_df['Site Name']:
        if siteName in strsite:
            data = summaryManagement_df.loc[summaryManagement_df['Site Name'].isin([siteName])]
            return data['MOVING TOWARDS OBJECTIVES desc']
        # else:
        #     return 'Data not available'


########################################################################################################################

#                                            Summary Stats by Designation Callbacks

########################################################################################################################


# Create application callback decorator to update bar chart with location selection
@app.callback(
    dash.dependencies.Output('mpa_count', 'figure'),
    [dash.dependencies.Input('LocationGraphs', 'value')]
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
            paper_bgcolor=colors['background1'],
            plot_bgcolor=colors['background1'],

        )
    }


# Create application callback decorator to percentage area pie chart with location selection
@app.callback(
    dash.dependencies.Output('percentage_pie', 'figure'),
    [dash.dependencies.Input('LocationGraphs', 'value')]
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
            title='Percentage area of MPAs within administrative area (%)',
            font=dict(color=colors['text']),
            hovermode='closest',
            paper_bgcolor=colors['background1'],
            plot_bgcolor=colors['background1']
        )
    }


app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True)


########################################################################################################################






