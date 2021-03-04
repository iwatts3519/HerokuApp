import mysql.connector
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio
import pandas as pd
import os
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import base64

assets_directory = os.getcwd() + '/assets/'
nltk.download('stopwords')

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

attendanceDF1["Type"] = "Seminar"
standDF1["Type"] = "Exhibition Stand"
attendance_full = pd.concat([attendanceDF1, standDF1], ignore_index=True)

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

sql6 = "SELECT exhibitor_message.message as Message, users.organisation as Organiser, " \
       "exhibitor_conversation.started_by as Started from ((exhibitor_message left join exhibitor_conversation " \
       "on exhibitor_message.conversationid = exhibitor_conversation.id) left join users on " \
       "exhibitor_conversation.started_by = users.id)"
cursor.execute(sql6)
messages = cursor.fetchall()

columns = []
for name in cursor.description:
    columns.append(name[0])
messagesDF = pd.DataFrame(messages, columns=columns)
messagesDF.dropna(inplace=True)
messagesDF.drop_duplicates(inplace=True)


def create_wordcloud(df, column=0):
    messages_list = df["Message"].tolist()
    token_data = []
    stop_words = stopwords.words('english')
    for message in messages_list:
        tokens = message.split()
        token_data.append(tokens)
        token_data = [[word for word in doc if word not in stop_words] for doc in token_data]
    text_1 = ' '.join([str(ele) for ele in token_data])
    print(text_1)
    wordcloud = WordCloud(stopwords=STOPWORDS, width=1000, height=666).generate(text_1)
    print(wordcloud)
    wordcloud.to_file(assets_directory + "cloud.png")
    # encoded_image = base64.b64encode(open(assets_directory + 'cloud.png', 'rb').read())
    # return encoded_image


# -------------------------------------------------------------------------------------
app.layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H1("BookMeIn Dashboard"),
            width={'size': 6, 'offset': 3},
            style={"text-align": "center"}
        ),
    ),
    dbc.Row(
        [dbc.Col(
            html.Label("Please Choose One or More Seminars"),
            width={"size": 6}
        ),
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
            ),

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
        ]),
    dbc.Row(
        [
            dbc.Col(
                html.Label("Please Choose One or More Discussion Group Organisers"),
                width={"size": 6}
            ),
            dbc.Col(
                html.Label("Please Choose One or More More Exhibitions"),
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
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='stand_dropdown',
                    options=[{'label': i, 'value': i} for i in standDF1["Reference"]],
                    value=['CCS'],
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
            ),
            dbc.Col(
                dcc.Graph(id='Figure_2'),
                width=6
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id='message_dropdown',
                    options=[{'label': i, 'value': i} for i in messagesDF["Organiser"].unique()],
                    value=['Fordway'],
                    multi=True,
                    clearable=False,
                    style={"color": '#222222'}),
                width={"size": 6, "offset": 1}
            )
        ]),
    dbc.Row(
        [
            dbc.Col(

                html.Img(id="Figure_5", src="/assets/cloud.png"),
                width={"size": 6, "offset": 1})

        ]),

    dbc.Row(
        dbc.Col(
            html.Div("(c) CAD Group 6 - Keele University -  Built by Dash on Flask",
                     style={"text-align": "center"}))
    )

], style={"background-color": "#111111"})


# -------------------------------------------------------------------------------------
@app.callback(
    [Output(component_id="Figure_1", component_property="figure"),
     Output(component_id="Figure_2", component_property="figure"),
     Output(component_id="Figure_3", component_property="figure"),
     Output(component_id="Figure_4", component_property="figure"),
     Output(component_id="Figure_5", component_property="figure")],
    [Input(component_id="event_dropdown", component_property="value"),
     Input(component_id="stand_dropdown", component_property="value"),
     Input(component_id="group_dropdown", component_property="value"),
     Input(component_id="message_dropdown", component_property="value")]
)
def update_graph(ev_dropdown, st_dropdown, gp_dropdown, mg_dropdown):
    dff = attendance_full[(attendance_full["Reference"].isin(ev_dropdown)) & (attendance_full["Type"] == "Seminar")]
    dff2 = attendance_full[
        (attendance_full["Reference"].isin(st_dropdown)) & (attendance_full["Type"] == "Exhibition Stand")]
    dff3 = attendance_timeDF[attendance_timeDF["Reference"].isin(ev_dropdown)]
    dff4 = groupsDF[groupsDF["Organiser"].isin(gp_dropdown)]
    dff5 = messagesDF[messagesDF["Organiser"].isin(mg_dropdown)]
    print(dff5.head())
    create_wordcloud(dff5)
    figa = px.bar(dff, x="Reference", y='Attendance', title="Seminar Attendance")
    figb = px.bar(dff2, x="Reference", y='Attendance', title="Exhibition Attendance")
    figc = px.line(dff3, x='Time', y='Attendance', color="Reference", title="Seminar Attendance Against Time")
    figd = px.bar(dff4, x="Organiser", y="Attendance", title="Attendance at Group Discussions")
    # fige = html.Img(src="data:image/png;base64,{}".format(display_image.decode()))
    fige = '\\assets\\cloud.png'
    return figa, figb, figc, figd, fige


# -------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)

# git push heroku master
