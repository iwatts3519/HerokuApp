import mysql.connector
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio
import pandas as pd

pio.templates.default = "plotly_dark"

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.DARKLY])
server = app.server

mydb = mysql.connector.connect(
    host="d3y0lbg7abxmbuoi.chr7pe7iynqr.eu-west-1.rds.amazonaws.com	",
    user="f6h3bik8fkz4m7ll",
    passwd="t2rjjjnx0rndv1pk",
    database="nh5x83ucdvxnlkqx"
)

cursor = mydb.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

sql5 = "SELECT discussion_group.name as Name, users.organisation as Organiser, COUNT(DISTINCT " \
       "discussion_group_people.attendeeid) as Attendance FROM ((discussion_group_people LEFT JOIN " \
       "discussion_group ON discussion_group_people.groupid = discussion_group.id) LEFT JOIN users ON " \
       "discussion_group.created_by = users.id) GROUP BY Name"
cursor.execute(sql5)
groups = cursor.fetchall()

columns = []
for name in cursor.description:
    columns.append(name[0])
groupsDF = pd.DataFrame(groups, columns=columns)

# -------------------------------------------------------------------------------------
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.Label("Please Choose One or More Discussion Group Organisers"),
                width={"size": 6}
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id='group_dropdown',
                    options=[{'label': i, 'value': i} for i in groupsDF["Organiser"].unique()],
                    value=['Xitagy'],
                    multi=True,
                    clearable=False,
                    style={"color": '#222222'}),
                width=6
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='Figure_4'),
                width=6
            )
        ]),

], style={"background-color": "#111111"})


# -------------------------------------------------------------------------------------
@app.callback(
    Output(component_id="Figure_4", component_property="figure"),
    [Input(component_id="group_dropdown", component_property="value")]
)
def update_graph(gp_dropdown):
    dff4 = groupsDF[groupsDF["Organiser"].isin(gp_dropdown)]

    figd = px.bar(dff4, x="Organiser", y="Attendance", title="Attendance at Group Discussions")

    return figd


# -------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)
