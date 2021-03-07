import mysql.connector
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from app import app
import plotly.io as pio

# -------------------------------------------------------------------------------------
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis vitae nibh quis neque tincidunt "
                       "interdum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent a orci vitae "
                       "tortor ultricies tempus aliquam in tortor. Ut sit amet lacus mi. Ut nisl ex, interdum id "
                       "faucibus vel, placerat eu nisi. Sed in elit pellentesque, tempor lorem eu, consectetur "
                       "lectus. Vestibulum bibendum risus sodales nisi hendrerit, et dictum leo mattis.")
            )

        ]),
    dbc.Row(
        [
            dbc.Col(
                html.P("Proin lorem sem, pellentesque non sagittis quis, maximus sed ante. In ut ex fringilla, "
                       "ultrices urna non, dictum eros. Praesent non pretium tortor. Suspendisse vulputate leo "
                       "fermentum orci lacinia, ut consectetur enim elementum. Phasellus turpis nisi, imperdiet vitae "
                       "neque nec, eleifend volutpat eros. Sed quis augue sapien. Integer mauris leo, "
                       "pharetra interdum diam tincidunt, sodales aliquam purus. Praesent enim felis, molestie a "
                       "porttitor nec, porttitor eu lacus. Aenean a enim non lectus pretium euismod. Suspendisse "
                       "sollicitudin et felis id efficitur. Aenean id ipsum eu nunc eleifend sagittis. Vestibulum "
                       "tincidunt nisl mauris, vel lacinia dui posuere quis. Donec venenatis diam eget tortor "
                       "lobortis congue. Nullam vehicula ligula nec luctus sagittis. Ut quis dolor eu diam viverra "
                       "malesuada id ac ipsum.")

            )

        ])

])
