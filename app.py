import dash
import dash_bootstrap_components as dbc

# metatags needed for mobile responsive
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.DARKLY])
server = app.server
