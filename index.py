import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

from apps import seminars, discussions, welcome, exhibitions, wordclouds

app.layout = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.NavbarSimple([
                dbc.NavItem([
                    dbc.Button(dbc.NavLink("Seminars ", href='/apps/seminars'), className="lg mx-2", color="primary")
                ]),
                dbc.NavItem([

                    dbc.Button(dbc.NavLink("Exhibitions ", href='/apps/exhibitions'), className="lg mx-2",
                               color="primary")
                ]),
                dbc.NavItem([
                    dbc.Button(dbc.NavLink("Discussions ", href='/apps/discussions'), className="lg mx-2",
                               color="primary")
                ]),

                dbc.NavItem([
                    dbc.Button(dbc.NavLink("Wordclouds ", href='/apps/wordclouds'), className="lg mx-2",
                               color="primary")
                ])
            ],
                brand="BookMeIn Analytics",
                brand_href="welcome.layout",
                fluid=True,
                dark=True,
                color="primary")
        ], width=12)
    ]),

    dcc.Location(id="url", refresh=False, pathname="/apps/welcome"),
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
    if pathname == '/apps/wordclouds':
        return wordclouds.layout
    else:
        return welcome.layout


if __name__ == '__main__':
    app.run_server(debug=False)
