import mysql.connector
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
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

sql = "SELECT events.Id as Event_ID, events.event_reference as Reference, event_types.name as Type, " \
      "COUNT(DISTINCT attendee_session_tracking.attendeeId) as Attendance FROM ((attendee_session_tracking " \
      "LEFT JOIN events ON attendee_session_tracking.eventId = events.Id) LEFT JOIN event_types ON events.event_type" \
      " = event_types.Id) GROUP BY events.Id"
cursor.execute(sql)
attendance = cursor.fetchall()
print(attendance)
columns = []
for name in cursor.description:
    columns.append(name[0])
attendanceDF1 = pd.DataFrame(attendance, columns=columns)
attendanceDF1 = attendanceDF1.groupby("Reference", as_index=False).sum()[1:]
print(attendanceDF1)

sql2 = "SELECT events.Id as Event_ID, events.event_reference as Reference, event_types.name as Type, " \
       "COUNT(DISTINCT attendee_session_tracking.attendeeId) as Attendance FROM ((events LEFT JOIN event_types ON " \
       "events.event_type = event_types.Id) LEFT JOIN attendee_session_tracking ON attendee_session_tracking.eventId " \
       "= events.Id) GROUP BY events.Id ORDER BY Type"
cursor.execute(sql2)
test = cursor.fetchall()
testDF = pd.DataFrame(test)
columns = []
for name in cursor.description:
    columns.append(name[0])
testDF = pd.DataFrame(test, columns=columns)
testDF = testDF.groupby("Type", as_index=False).count()
print(testDF)
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
print(attendance_timeDF)

sql4 = "SELECT events.Id as Event_ID, events.event_reference as Reference, event_types.name as Type, " \
       "COUNT(DISTINCT stand_attendance.attendeeId) as Attendance FROM ((stand_attendance " \
       "LEFT JOIN events ON stand_attendance.eventId = events.Id) LEFT JOIN event_types ON events.event_type" \
       " = event_types.Id) GROUP BY events.Id"
cursor.execute(sql4)
stand = cursor.fetchall()
print(stand)
columns = []
for name in cursor.description:
    columns.append(name[0])
standDF1 = pd.DataFrame(stand, columns=columns)
standDF1 = standDF1.groupby("Reference", as_index=False).sum()[1:]
print(standDF1)

attendanceDF1["Type"] = "Seminar"
standDF1["Type"] = "Exhibition Stand"
attendance_full = pd.concat([attendanceDF1, standDF1], ignore_index=True)
print(attendance_full)
# -------------------------------------------------------------------------------------
app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H1("BookMeIn Dashboard"),
            width=12
        )
    ),
    dbc.Row(
        [dbc.Col(
            html.Label("Please Choose One or More Seminars"),
            width=6
        ),
            dbc.Col(
                html.Label("Please Choose One or More More Exhibitions"),
                width=6
            )]
    ),

    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id='event_dropdown',
                    options=[{'label': i, 'value': i} for i in attendanceDF1["Reference"]],
                    value=['AdEPT'],
                    multi=True,
                    clearable=False),
                width=6
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='stand_dropdown',
                    options=[{'label': i, 'value': i} for i in standDF1["Reference"]],
                    value=['CCS'],
                    multi=True,
                    clearable=False),
                width=6
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='Figure_1'),
                width=6
            ),
            dbc.Col(
                dcc.Graph(id='Figure_2'),
                width=6
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='Figure_3'),
                width=12
            )
        ]),

    dbc.Row(
        dbc.Col(
            html.Footer("(c) CAD Group 6 - Keele University -  Built by Dash on Flask", style={"text-align": "center"}))
    )

])


# -------------------------------------------------------------------------------------
@app.callback(
    [Output(component_id="Figure_1", component_property="figure"),
     Output(component_id="Figure_2", component_property="figure"),
     Output(component_id="Figure_3", component_property="figure")],
    [Input(component_id="event_dropdown", component_property="value"),
     Input(component_id="stand_dropdown", component_property="value")]
)
def update_graph(ev_dropdown, st_dropdown):
    dff = attendance_full[(attendance_full["Reference"].isin(ev_dropdown)) & (attendance_full["Type"] == "Seminar")]
    dff2 = attendance_full[
        (attendance_full["Reference"].isin(st_dropdown)) & (attendance_full["Type"] == "Exhibition Stand")]
    dff3 = attendance_timeDF[attendance_timeDF["Reference"].isin(ev_dropdown)]
    figa = px.bar(dff, x="Reference", y='Attendance', title="Seminar Attendance")
    figb = px.bar(dff2, x="Reference", y='Attendance', title="Exhibition Attendance")
    figc = px.line(dff3, x='Time', y='Attendance', color="Reference", title="Seminar Attendance Against Time")
    return figa, figb, figc


# -------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)

# git push heroku master
