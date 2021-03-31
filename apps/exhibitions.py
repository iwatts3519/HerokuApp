import mysql.connector
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from app import app
import plotly.io as pio

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="bookmein"
)

cursor = mydb.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

sql4 = "SELECT events.Id as Event_ID, events.event_reference as Reference, event_types.name as Type, " \
       "COUNT(DISTINCT stand_attendance.attendeeId) as Attendance FROM ((stand_attendance " \
       "LEFT JOIN events ON stand_attendance.eventId = events.Id) LEFT JOIN event_types ON events.event_type" \
       " = event_types.Id) GROUP BY events.Id"
cursor.execute(sql4)
stand = cursor.fetchall()

columns = []
for name in cursor.description:
    columns.append(name[0])
standDF1 = pd.DataFrame(stand, columns=columns)
standDF1 = standDF1.groupby("Reference", as_index=False).sum()[1:]

# -------------------------------------------------------------------------------------
layout = html.Div([

    dbc.Row(
        [
            dbc.Col(
                html.Label("Please Choose One or More More Exhibitions"),
                width={"size": 12}
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id='stand_dropdown',
                    options=[{'label': i, 'value': i} for i in standDF1["Reference"]],
                    value=['CCS'],
                    multi=True,
                    clearable=False,
                    style={"color": '#222222'}),
                width=12
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='Figure_2'),
                width=12
            )
        ])

])


# -------------------------------------------------------------------------------------
@app.callback(
    Output(component_id="Figure_2", component_property="figure"),
    [Input(component_id="stand_dropdown", component_property="value")]
)
def update_graph(st_dropdown):
    dff2 = standDF1[
        (standDF1["Reference"].isin(st_dropdown))]

    figb = px.bar(dff2, x="Reference", y='Attendance', title="Exhibition Attendance")

    return figb
