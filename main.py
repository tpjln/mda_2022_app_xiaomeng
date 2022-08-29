import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

app = dash.Dash(__name__, title='MDA 2022 Xiaomeng Zhang', external_stylesheets=[dbc.themes.BOOTSTRAP],
                serve_locally=False)

# add this for heroku
server = app.server

fig = make_subplots(rows=1, cols=1)
df = pd.read_csv("month_topic_count.csv")
df.rename(columns={'topic_theme': 'Topic'}, inplace=True)

theme_checklist = dcc.Checklist(
    id="theme_checklist",
    options=[
        {"label": "Economy/Education/Job/Family", "value": 29},
        {"label": "War/Conflict/Religion/Nation", "value": 2},
        {"label": 'Policy/Govenment/Foreign Affairs', "value": 5},
        {"label": 'Insurance/Health', "value": 26},
        {"label": 'Iran/Sanction', "value": 19},
        {"label": 'Veteran Affairs', "value": 13},
        {"label": 'Oil/Gas/Energy/Viecle/Climate', "value": 10}
    ],
    labelStyle=dict(display='block'),
    value=[29]
)

input_groups = dbc.Row([dbc.Col(
    html.Div([
        dbc.InputGroup([
            html.H6('Please select the topics(s):', style={'display': 'block', 'margin-top': 20, 'color': 'blue'}),
        ], ),
        theme_checklist,
        dbc.InputGroup([
            html.H6('Please select a start date and an end date between 2009-01-01 and 2017-01-01:',
                    style={'display': 'block', 'margin-top': 20, 'color': 'blue'}),
            html.H6('Start Date', style={'margin-right': 10}),
            dbc.Input(id='id_start_date', value="2009-01-01", type="date"),
            html.H6('End Date', style={'margin-left': 10, 'margin-right': 10}),
            dbc.Input(id='id_end_date', value="2017-01-01", type="date")
        ],
        )
    ],
    )),
]
)

app.layout = dbc.Container(
    [
        html.Div(children=[
            dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height=70,
                             style={'display': 'inline', 'textAlign': 'left'})),
            dbc.Col([
                html.H1(children='MDA 2022 Obama\'s Speech', style={'display': 'block', 'textAlign': 'center', }),
                (html.H4(children='Xiaomeng Zhang', style={'textAlign': 'center', }))
            ]),
        ],
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(input_groups, md=4),
                dbc.Col(dcc.Graph(id="id_graph", figure=fig, ), md=8, )],
            align="center"),
    ],
    fluid=True,
)


@app.callback(
    Output('id_graph', 'figure'),
    [Input('theme_checklist', 'value'),
     Input('id_start_date', 'value'),
     Input('id_end_date', 'value'),
     ]
)
def update_chart(theme_checklist, start_date, end_date):
    try:
        mask = df.dominant_topic.isin(theme_checklist) & (df['Time'] >= start_date) & (df['Time'] <= end_date)
        fig = px.line(df[mask], x="Time", y="num of speeches", color='Topic', title="Topic Distribution over Time")
        fig.update_layout(title_x=0.5, height=550, )
    except:
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Scatter(x=np.arange(0, 10, 1),
                       y=np.arange(0, 10, 1) * 2 + np.random.randn(),
                       name='Example'),
            row=1, col=1)
        fig.update_layout(width=1500)
        return fig

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)