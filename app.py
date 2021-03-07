import dash
import dash_bootstrap_components as dbc

# metatags needed for mobile responsive
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.DARKLY],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
