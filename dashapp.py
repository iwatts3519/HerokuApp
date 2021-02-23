import mysql.connector
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
columns = []
for name in cursor.description:
    columns.append(name[0])
attendanceDF1 = pd.DataFrame(attendance, columns=columns)
attendanceDF1 = attendanceDF1.groupby("Reference", as_index=False).sum()[1:]

# -------------------------------------------------------------------------------------
app.layout = html.Div([
    html.H1(children='BookMeIn Dashboard'),

    html.Label(["Please Choose One or More Events"]),
    dcc.Dropdown(
        id='event_dropdown',
        options=[{'label': i, 'value': i} for i in attendanceDF1["Reference"]],
        value=['CISCO'],
        multi=True,
        clearable=False,
        style={"width": "50%"}
    ),
    html.Div([
        html.Div([dcc.Graph(id='Figure_1', )], className='six columns'),
        html.Div([dcc.Graph(id='Figure_2', )], className="six columns")
    ]),
    html.Div("(c) CAD Group 6 - Keele University -  Built by Dash on Flask", style={"text-align": "center"})
], className='row')


# -------------------------------------------------------------------------------------
@app.callback(
    Output(component_id="Figure_1", component_property="figure"),
    Output(component_id="Figure_2", component_property="figure"),
    [Input(component_id="event_dropdown", component_property="value")]
)
def update_graph(my_dropdown):
    dff = attendanceDF1[attendanceDF1["Reference"].isin(my_dropdown)]
    figa = px.bar(dff, x="Reference", y='Attendance')
    figb = px.bar(dff, x="Reference", y='Attendance')
    return figa, figb


# -------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)
