from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import io
import base64

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# declare component for opening section
# "" for graph

"""
To add: 
    - more explanatory text
    - statement on data privacy
    - links to benefits of sleep hygiene 

    - link to fitbit site and how to export data
    - big input that says "Upload File" 
"""
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

# also I'll have to do a diff on the file to show it hasn't changed at all. (call this w/ python?)

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
    dcc.Graph(id='graph')
])

@app.callback(Output('graph', 'figure'),
              Input('uploader', 'contents'))
def load_graph(datafile):
    # prevents errors when initially loading page
    if datafile is None: 
        raise PreventUpdate
    
    # unpacking allows us to discard the initial data on format/encoding
    _, contents = datafile.split(',')
    formatted = base64.b64decode(contents)

    df = pd.read_csv(io.StringIO(formatted.decode('utf-8')), parse_dates=True)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    df['time'] = pd.to_datetime(df['timestamp']).dt.time

    # Indices to initially show in graph (past 30 days)
    final_dt = df.date.iat[0]
    start_idx = final_dt - pd.Timedelta(days=120)

    # Min/max values, to set color scale relative to these
    min_score = df.overall_score.min(skipna=True)
    max_score = df.overall_score.max()

    # Remove duplicate logs on same date, keeping last one
    df = df.drop_duplicates(subset=['date'],keep='last')

    graph = px.bar(df, x='date', y='overall_score', color='overall_score', color_continuous_scale='Portland_r', range_color=[min_score,max_score], hover_name='overall_score')
    graph.update_yaxes(range=[50,90],fixedrange=True, automargin='top')
    graph.update_xaxes(range=[start_idx, final_dt])
    graph.update_layout(bargap=0.1)
    graph.update_layout(height=800)
    graph.update_layout(dragmode='pan', modebar_remove=['zoom', 'lasso', 'resetViewMapbox'])
    return graph

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