import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

from apps import seminars, exhibitions, discussions

app.layout = html.Div([

    dbc.Row(
        dbc.Col(
            html.H1("BookMeIn Dashboard"),
            width={'size': 6, 'offset': 3},
            style={"text-align": "center"}
        )
    ),
    dbc.Row([
        dbc.Col([
            dcc.Link("Seminars ", href='/apps/seminars'),
            dcc.Link("Exhibitions ", href='/apps/exhibitions'),
            dcc.Link("Discussions ", href='/apps/discussions')
        ])
    ]),
    dcc.Location(id="url", refresh=False, pathname=""),
    html.Div(id='page-content', children=[]),
    dbc.Row(
        dbc.Col(
            html.Div("(c) CAD Group 6 - Keele University -  Built by Dash on Flask",
                     style={"text-align": "center"}))
    )
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/seminars':
        return seminars.layout
    if pathname == '/apps/exhibitions':
        return exhibitions.layout
    if pathname == '/apps/discussions':
        return discussions.layout
    else:
        return "404 Page Error: Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
