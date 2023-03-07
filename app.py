from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import io
import base64
import socket
import pickle

HOST = '127.0.0.1'
PORT = 29222

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

intro = dcc.Markdown('''
    # Welcome to FiBiVi!

    ## The FitBit Data Visualizer

    View all your FitBit sleep data, all at once, in interactive visuals with total privacy. 
    ''')

instructions = dbc.Accordion([
    dbc.AccordionItem([
        dcc.Markdown("""
    To look at your sleep data, please first visit [the link here](https://www.fitbit.com/settings/data/export),
    or paste https://www.fitbit.com/settings/data/export into your browser address bar. 
    Once there, select the *Request Data* option at the bottom of the page, under the heading **Export Your Account Data**.

    Make sure to select the correct option; the export under "**Time Export**", at the top of this page, **will
    not include all the necessary data**. There's more information on the export process in FitBit's guide here, if you'd 
    like to take a look!: https://help.fitbit.com/articles/en_US/Help_article/1133.htm

    It can take some time - **up to an hour or more** - for your data to be ready, but you'll receive an email when it's done. (Take 
    a break and come back to it - we'll be here!) You can head back to https://www.fitbit.com/settings/data/export to check 
    on it at any time, and once it's ready, you can download your data there. 

    Finally, locate the **sleep_score.csv** file within your download, and then click the big blue button below to share it with our 
    tool. Your data will be kept fully private; for more information, please see the next section. 
                     """)
    ], title="Getting started and finding your data", id="instructions")
],start_collapsed=True)

privacy_info = dbc.Accordion([
    dbc.AccordionItem([
        dcc.Markdown("""
        None of your data will leave your personal device, or be shared with any person or system in any way, as a result of 
        using the FitBit Data Visualizer. This software will examine the fitness data on your personal device, only
        for the purpose of displaying it to you. No third parties other than yourself and FitBit, including the creator
        of this software, will have access to your information in any way. 
                     """)
    ], title="Data Privacy Statement", id="privacy")
],start_collapsed=True)

article_links = dbc.Accordion([
    dbc.AccordionItem([
        dcc.Markdown("""
            Good sleep is one of the most important things you can do for your health. There are a number of studies showing
            how important sleep is, and what strategies are best for developing a healthy sleep routine. In connection with
            your personal sleep data, the resources below might be a great place to explore healthier lifestyles: 
            - ["Healthy Sleep Habits"](https://sleepeducation.org/healthy-sleep/healthy-sleep-habits/) - American Academy of Sleep Medicine
            - ["Why Sleep is Key"](https://www.sciencedirect.com/science/article/abs/pii/S0887618522000743) - Journal of Sleep Medicine
            - ["Why We Sleep, and Why We Often Can't"](https://www.newyorker.com/magazine/2018/12/10/why-we-sleep-and-why-we-often-cant) - The New Yorker
                    
                     """)
    ], title="(Optional) Information on the science of sleep", id="articles")
],start_collapsed=True)

upload = dcc.Upload(
            id="uploader", 
            children=html.Div(html.A('Click here to select your sleep_score.csv file')),
        style={
            'backgroundColor':'blue',
            'color': 'white',
            'borderStyle':'solid',
            'textAlign': 'center',
            'margin': '10px'
        })

# Layout of app page, generated using Plotly Dash framework syntax
app.layout = html.Div(id="body-div", children=[
    html.Div([
        intro,
        instructions,
        privacy_info,
        article_links,
    ],id="header"),
    html.Div([
        upload
    ], id="body"),
    dcc.Graph(id='bar_graph'),
    html.Button('Randomize Colors (click again to revert)', id='butt0n'),
    dcc.Graph(id='trend_graph'),
    dcc.Graph(id="deepsleep_graph"),
])

def get_colors():
    """
    Retrieves colors from microservice. 
    """
    mysoc = socket.socket()
    mysoc.connect((HOST, PORT))

    count = "4"
    mysoc.send(count.encode())
    data = mysoc.recv(2048)
    colors = pickle.loads(data)
    
    return colors

def unpack_data(datafile, format):
    """
    Unpack and load data from user-uploaded file. 
    """
    # Ensure formatting data is correct
    if format not in ('bar', 'scatter'):
        raise Exception

    # Use tuple unpacking to discard header data concerning file format
    _, contents = datafile.split(',')
    formatted = base64.b64decode(contents)

    # Extract data from decoded file, and add date index as needed
    df = pd.read_csv(io.StringIO(formatted.decode('utf-8')), parse_dates=True)
    if format == 'bar':
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
    elif format == 'scatter':
        df['date'] = df['timestamp'].astype('datetime64').dt.to_pydatetime()

    # Strip duplicate data
    df = df.drop_duplicates(subset=['date'],keep='last')

    return df

@app.callback(Output('bar_graph', 'figure'),
              Input('uploader', 'contents'),
              Input('butt0n', 'n_clicks'))
def load_bargraph(datafile, clicks):
    """
    Load sleep score bar graph at top of page.
    """
    # prevents errors when initially loading page
    if datafile is None: 
        raise PreventUpdate
    
    # Set graph colors according to user button clicks
    if clicks is None:
        clicks = 0
    if clicks % 2 == 0: 
        COLORS = "Portland_r"
    else:
        COLORS = get_colors() if clicks else "Portland_r"
    
    # Load user data from file, via helper function
    df = unpack_data(datafile, 'bar')

    # Indices to initially show in graph (past 120 days)
    final_dt = df.date.iat[0]
    start_idx = final_dt - pd.Timedelta(days=120)

    # Min/max values of overall score, to calibrate color-coding scale
    min_score = df.overall_score.min(skipna=True)
    max_score = df.overall_score.max()

    # Create and style bar graph object 
    bargraph = px.bar(df, x='date', y='overall_score', color='overall_score', color_continuous_scale=COLORS, range_color=[min_score,max_score], hover_name='overall_score')
    bargraph.update_yaxes(range=[50,90],fixedrange=True, automargin='top')
    bargraph.update_xaxes(range=[start_idx, final_dt])
    bargraph.update_layout(bargap=0.1, height=800, dragmode='pan', modebar_remove=['zoom', 'lasso', 'resetViewMapbox'])
    return bargraph

@app.callback(Output('trend_graph', 'figure'),
              Input('uploader', 'contents'))
def load_trendgraph(datafile):
    """
    Load seven-day sleep score trendline graph.
    """
    if datafile is None:
        raise PreventUpdate

    # Load user data from file, via helper function
    df = unpack_data(datafile, 'scatter')
    # Calibrate min/max score and initial indices
    min_score = df.overall_score.min(skipna=True)
    max_score = df.overall_score.max()
    final_dt = df.date.iat[0]
    start_idx = final_dt - pd.Timedelta(days=120)

    # Create and style scatterplot graph object 
    trendgraph = px.scatter(df, x='date', y="overall_score", trendline="rolling", trendline_options=dict(window=7), 
                            hover_data=["overall_score"], color='overall_score', color_continuous_scale="Portland_r", 
                            range_color=[min_score,max_score], trendline_color_override="#3266a8", opacity=0.4)
    trendgraph.update_yaxes(range=[50,90],fixedrange=True, automargin='top')
    trendgraph.update_xaxes(range=[start_idx, final_dt])
    trendgraph.update_layout(height=800, dragmode='pan', modebar_remove=['zoom', 'lasso', 'resetViewMapbox'])

    return trendgraph

@app.callback(Output('deepsleep_graph', 'figure'),
              Input('uploader', 'contents'))
def load_deepsleepgraph(datafile):
    if datafile is None:
        raise PreventUpdate

    # Load user data from file via helper function
    df = unpack_data(datafile, 'scatter')
    # Calibrate min/max score and initial indices
    min_score = df.deep_sleep_in_minutes.min(skipna=True)
    max_score = df.deep_sleep_in_minutes.max()
    final_dt = df.date.iat[0]
    start_idx = final_dt - pd.Timedelta(days=120)

    # Create and style bar graph object
    dsgraph = px.scatter(df, x='date', y="deep_sleep_in_minutes", trendline="rolling", trendline_options=dict(window=7), 
                         hover_data=["deep_sleep_in_minutes"], color='deep_sleep_in_minutes', color_continuous_scale="Portland_r", 
                         range_color=[min_score,max_score], trendline_color_override="#3266a8", opacity=0.4)
    dsgraph.update_yaxes(range=[0,130],fixedrange=True, automargin='top')
    dsgraph.update_xaxes(range=[start_idx, final_dt])
    dsgraph.update_layout(height=800, dragmode='pan', modebar_remove=['zoom', 'lasso', 'resetViewMapbox'])

    return dsgraph

if __name__ == '__main__':
	app.run_server(debug=True)




"""
CSV format: 
sleep_log_entry_id (int)
timestamp (datestr)
overall_score (int)
composition_score (int)
revitalization_score (int)
duration_score (int)
deep_sleep_in_minutes, (int)
resting_heart_rate,(int)
restlessness (float)
"""