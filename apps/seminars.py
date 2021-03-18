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
    host="d3y0lbg7abxmbuoi.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
    user="f6h3bik8fkz4m7ll",
    passwd="t2rjjjnx0rndv1pk",
    database="nh5x83ucdvxnlkqx"
)

cursor = mydb.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

sql = "SELECT events.Id as Event_ID, events.event_reference as Reference, event_types.name as Type, " \
      "COUNT(DISTINCT attendee_session_tracking.attendeeId) as Attendance FROM ((attendee_session_tracking " \
      "LEFT JOIN events ON attendee_session_tracking.eventId = events.Id) LEFT JOIN event_types ON events.event_type" \
      " = event_types.Id) GROUP BY events.Id"
cursor.execute(sql)
attendance = cursor.fetchall()

columns = []
for name in cursor.description:
    columns.append(name[0])
attendanceDF1 = pd.DataFrame(attendance, columns=columns)
attendanceDF1 = attendanceDF1.groupby("Reference", as_index=False).sum()[1:]

sql3 = "SELECT events.Id as Event_ID, events.event_reference as Reference, event_types.name as Type, " \
       "DATE_FORMAT(attendee_session_tracking.date_pinged, '%k %i') AS Time, " \
       "COUNT(DISTINCT attendee_session_tracking.attendeeId) as Attendance FROM ((attendee_session_tracking " \
       "LEFT JOIN events ON attendee_session_tracking.eventId = events.Id) LEFT JOIN event_types ON events.event_type " \
       "= event_types.Id) GROUP BY Time"
cursor.execute(sql3)
attendance_time = cursor.fetchall()
columns = []
for name in cursor.description:
    columns.append(name[0])
attendance_timeDF = pd.DataFrame(attendance_time, columns=columns)

# -------------------------------------------------------------------------------------
layout = html.Div([
    dbc.Row(
        [dbc.Col(
            html.Label("Please Choose One or More Seminars"),
            width={"size": 6}
        )
        ]
    ),

    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id='event_dropdown',
                    options=[{'label': i, 'value': i} for i in attendanceDF1["Reference"]],
                    value=['AdEPT'],
                    multi=True,
                    clearable=False,
                    style={"color": '#222222'}),
                width=12
            )

        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='Figure_1'),
                width=6
            ),
            dbc.Col(
                dcc.Graph(id='Figure_3'),
                width=6
            )
        ])

])


# -------------------------------------------------------------------------------------
@app.callback(
    (Output(component_id="Figure_1", component_property="figure"),
     Output(component_id="Figure_3", component_property="figure")),
    [Input(component_id="event_dropdown", component_property="value")]
)
def display_graph(ev_dropdown):
    dff = attendanceDF1[attendanceDF1["Reference"].isin(ev_dropdown)]
    dff3 = attendance_timeDF[attendance_timeDF["Reference"].isin(ev_dropdown)]

    figa = px.bar(dff, x="Reference", y='Attendance', title="Seminar Attendance")
    figc = px.line(dff3, x='Time', y='Attendance', color="Reference", title="Seminar Attendance Against Time")
    return figa, figc
