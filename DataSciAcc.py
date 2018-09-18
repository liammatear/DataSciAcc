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

summaryAll_df = pd.read_excel(
    'C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\input\Stats\\OfficialSensitive_UKMPA_STATS.xlsx',
    'SummaryAll')

# Import UK MPA Network GeoJson data
with open('C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\geojson\\UKMPA_SitInfo_00005_Simp.geojson') as f:
    mpaJson = json.load(f)

# Import OSPAR Region GeoJson data
with open('C:\\Users\\Liam.Matear\\Desktop\\DataSciAcc\\Planning\\geojson\\OSPAR_JSON.geojson') as f:
    osparJson = json.load(f)


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
    'background1': '#F8F8FF',  # Ghost White
    'background2': '#FFFFFF',  # White
    'text': '#262626',  # Very dark grey
    'textbox': '#FFFFFF',  # White


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
        'Region I: Arctic Waters': '#E0BBE4',
        'Region II: Greater North Sea': '#957DAD',
        'Region III: Celtic Seas': '#D291BC',
        'Region V: Wider Atlantic': '#FEC8D8',
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
                    # Set application title, colour and orientation
                    html.H1(
                        children='UK Marine Protected Area (MPA) Network Statistics',
                        className='twelve columns',
                        style={
                            'textAlign': 'center',
                            'color': colors['text'],
                            'backgroundColor': colors['background1'],
                            'width': '100%',
                            # 'display': 'block',
                            'margin-top': '80',
                            'font-size': '58',
                        },
                    ),

                    # html.Img(
                    #     src='https://github.com/liammatear/DataSciAcc/blob/master/JNCCLogo_Grey.png',
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

                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    ' Marine Protected Areas ',
                                    style={
                                        'color': colors['text'],
                                        'text-align': 'left',
                                        'margin-top': '100',
                                        'margin': '20',
                                    },
                                ),
                                dcc.Markdown(
                                    dedent('''
                                
                                Our seas are home to some of the most biologically diverse [habitats](http://jncc.defra.gov.uk/page-1529) and [species](http://jncc.defra.gov.uk/page-1592) in Europe.
                                Marine Protected Areas (MPAs) are one of the tools that can help us to protect the marine environment, whilst also enabling it's [sustainable use](http://jncc.defra.gov.uk/page-1528), ensuring it remains healthy and contributes to our society for generations to come.
                                JNCC is responsible for identifying and providing [conservation advice](http://jncc.defra.gov.uk/page-6849) on MPAs in UK offshore waters (beyond 12 nautical miles). More information on our role can be found on the [MPA Overview page](http://jncc.defra.gov.uk/page-6906).
                                
                                '''
                                           ),
                                    containerProps={
                                        'style': {
                                            'textAlign': 'justify',
                                            'color': colors['text'],
                                            'backgroundColor': colors['textbox'],
                                            'margin': '20',
                                            'font-size': '20'
                                            # 'margin-top': '45'
                                        },
                                    }
                                ),
                            ],
                            className='twelve columns'
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
                                    # Explore Our Protected Area Network:
                                    
                                    ##### Select a location from the drop-down menu below to filter the map and find out key statistics from our [Marine Protected Network](http://jncc.defra.gov.uk/page-4524)
                                    Use the checkbox to filter your options at a UK level, individual countries and OSPAR regions
                                                                       '''),
                                    containerProps={
                                        'style': {
                                            'textAlign': 'left',
                                            'color': colors['text'],
                                            'margin': '20',
                                            'margin-top': '45'
                                        },
                                    },
                                ),
                            ],

                        ),
                    ],
                    className='row'
                ),

                # Set control panel - Location drop-down menu
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.RadioItems(
                                            id='mainSelector',
                                            options=[
                                                {'label': 'UK', 'value': 'UK'},
                                                {'label': 'Country', 'value': 'Country'},
                                                {'label': 'OSPAR Region', 'value': 'OSPAR'},
                                            ],
                                            value='UK',
                                            labelStyle={'display': 'inline-block',
                                                        'color': colors['text']}
                                        ),
                                        dcc.Dropdown(
                                            id='Location',
                                            # options=[{'label': i, 'value': i} for i in availableLocations],
                                            options=[],
                                            # Allows for all or singular filtering
                                            multi=False,
                                            # value=list(availableLocations)
                                            # Old singular dropdown
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

                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='main_graph')
                            ],
                            className='twelve columns',
                            style={'margin-top': '20',
                                   'float': 'center'},
                        ),
                    ],
                    className='row'
                ),

                # Set key stats summary text
                html.Div(
                    [
                        html.H4(
                            '',
                            id='mpa_number',
                            className='two columns',
                            style={
                                'color': colors['text'],
                                'margin': '20',
                            }
                        ),
                        html.H4(
                            '',
                            id='total_area',
                            className='eight columns',
                            style={
                                'text-align': 'center',
                                'color': colors['text'],
                                'margin': '20'
                            }
                        ),
                        html.H4(
                            '',
                            id='total_percentage',
                            className='two columns',
                            style={
                                'text-align': 'right',
                                'color': colors['text'],
                                'margin': '20'
                            },
                        ),
                    ],
                    className='row'
                ),

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

                                        JNCC calculates statistics for the whole of the UK MPA network to assess progress in MPA designation. 
                                        
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
                                with marine components, 107 [Special Protection Areas (SPAs)](http://jncc.defra.gov.uk/page-1414)
                                with marine components, 56 [Marine Conservation Zones](http://jncc.defra.gov.uk/page-4525)
                                and 30 [Nature Conservation Marine Protected Areas](http://jncc.defra.gov.uk/page-5269).
                                [Sites of Special Scientific Interest (SSSIs)](http://jncc.defra.gov.uk/page-2303)
                                with marine components and [Ramsar sites](http://jncc.defra.gov.uk/page-161) will also form
                                part of the UK’s contribution to an MPA network. Currently, the Statutory Nature
                                Conservation Agencies are confirming those SSSIs and Ramsar sites that will contribute to
                                the MPA network through their protection of marine features.
                                
                                The MPA designation types included within this dashboard comprise Marine Conservation Zones
                                (MCZs), Special Areas of Conservation (SACs) with marine components, Special Protection
                                Areas (SPAs) with marine components, and Nature Conservation MPAs (NCMPAs).
                                
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
                                    ## Key Facts by MPA Designation:

                                    ##### Change location using the filter below to toggle the types of MPA displayed in the graphs 
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
                                            options=[{'label': i, 'value': i} for i in availableLocationsGraphs],
                                            # Allows for all or singular filtering
                                            multi=False,
                                            # value=list(availableLocations),
                                            # Old singular dropdown
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
                        # html.Div(
                        #     [
                        #         dcc.Graph(id='area_pie')
                        #     ],
                        #     className='five columns',
                        #     style={'margin-top': '10'}
                        # ),
                        # Create graph areas - mpa count
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
                                    In 2012, Defra and the Devolved Administrations published a [statement](http://www.scotland.gov.uk/Resource/0041/00411304.pdf) 
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
                                dcc.Markdown(
                                    dedent('''
                                        ## Explore the OSPAR Regions 
                                        
                                        ##### Use the checkboxes below to select an OSPAR Region, control the OSPAR map and display key statistics from the OSPAR Regions
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
                            className='twelve columns',
                        ),
                    ],
                    className='row',
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='ospar_graph')
                            ],
                            className='twelve columns',
                            style={'margin-top': '20',
                                   'float': 'center'},
                        ),
                    ],
                    className='row'
                ),
            ],
            className='ten columns offset-by-one'
        ),
    ],
)


########################################################################################################################

#                                          Key Summary Header Text Callbacks

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


# Create application callback decorator to update the Total MPA Number text box in key summary header
@app.callback(
    dash.dependencies.Output('mpa_number', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_count(selected_location):
    filtered_df = summaryAll_df[summaryAll_df.Location == selected_location]
    result = filtered_df['Total no. of MPAs']
    for each in result:
        return 'Total no. of MPAs: ' + str(each)


# Create application callback decorator to update Total Area Number text box in key summary header
@app.callback(
    dash.dependencies.Output('total_area', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_area(selected_location):
    filtered_df = summaryAll_df[summaryAll_df.Location == selected_location]
    result = filtered_df['Total Area of MPAs']
    for each in result:
        return 'Total Area of MPAs (km2):  ' + str(each)


# Create application callback decorator to update Total Percent Covered by MPA text box in key summary header
@app.callback(
    dash.dependencies.Output('total_percentage', 'children'),
    [dash.dependencies.Input('Location', 'value')]
)
def summary_mpa_area(selected_location):
    filtered_df = summaryAll_df[summaryAll_df.Location == selected_location]
    result = filtered_df['Total % of location covered by MPAs']
    for each in result:
        return 'Total % covered by MPAs:  ' + str(each) + '%'


########################################################################################################################

#                                         Graphs / Data Visualisation Callbacks

########################################################################################################################


# Create function to filter data by selected_location
def filtered_location(selected_location):

    """
    Create bespoke returns dependent on the input selection. If these are multiple inputs,
    then provide a return which is a combination of multiple singular returns. Otherwise,
    if the input location is a singular value, then return the singular output.
    """
    # filteredjson = {k: v for k, v in mpaJson.items() if k != "features"}

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

    # Singular returns for singular selected locations
    else:
        return [x for x in mpaJson["features"] if x["properties"]["Country"] == selected_location]


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
            text=[filteredjson['features'][k]['properties']['SITE_NAME'] for k in range(len(filteredjson['features']))],
            marker=dict(
                opacity=0.6,
                color='#FEC8D8'
            ),
        )
    )
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
                l=20,
                r=20,
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
            title='UK MPA Network',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                style='dark',
                # center='auto',
                center=dict(
                    lon=-3.6,
                    lat=56.2
                ),
                zoom=4.2,
                layers=[
                    {
                        'below': 'water',
                        'color': '#FFDFD3',
                        'opacity': 0.8,
                        'source': {
                            'type': 'FeatureCollection',
                            'features': [
                                {
                                    'geometry': {
                                        'type': 'Polygon',
                                        # 'id': 'Region1',
                                        'coordinates': [osparJson['features'][k]['geometry']['coordinates'] for k in range(len(osparJson['features'])) if osparJson['features'][k]['properties']['Region_Nam'] == 'Region I'],
                                    },
                                },
                            ],
                        },
                    },
                ],
            ),
        ),
    }


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






