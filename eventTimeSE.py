import mysql.connector
import pandas as pd

sql = "SELECT attendee_session_tracking.eventid as eventid, events.event_reference as Name, attendee_session_tracking.date_pinged as date_pinged " \
      "FROM ((attendee_session_tracking LEFT JOIN events ON events.id =attendee_session_tracking.eventid " \
      ")LEFT JOIN attendees ON attendees.id=attendee_session_tracking.attendeeid)"

mydb = mysql.connector.connect(
    host="d3y0lbg7abxmbuoi.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
    user="f6h3bik8fkz4m7ll",
    passwd="t2rjjjnx0rndv1pk",
    database="nh5x83ucdvxnlkqx"
)
df = pd.read_sql(sql, mydb)
df1 = df[df["date_pinged"] == df.groupby('eventid', as_index=True)['date_pinged'].transform('min')].sort_values(
    "date_pinged").drop_duplicates('eventid')
df2 = df[df["date_pinged"] == df.groupby('eventid', as_index=True)['date_pinged'].transform('max')].sort_values(
    "date_pinged").drop_duplicates('eventid')

df3 = df1.merge(df2, left_on='eventid', right_on='eventid', suffixes=('Earliest', 'Latest'))
df3['Length'] = df3['date_pingedLatest'] - df3['date_pingedEarliest']
df3.drop(["date_pingedLatest", "date_pingedEarliest", "NameEarliest"], axis=1, inplace=True)
df3.rename(columns={"eventid": "Event ID", "NameLatest": "Name", "Length": "Length"}, inplace=True)

df3["Length"] = round(df3["Length"].dt.seconds / 60)
print(df3)
print(f"Average Length of event = {round(df3['Length'].mean())} minutes")
# get a set of all unique ids
# eventidcol = set(df['eventid'])
#
# # create a dictionary
# eventTimeDic = {'id': [], 'length': []}
#
# # loop through every unique id
# for i in eventidcol:
#     # create a new df with filter on eventid
#     eventFilt = df.loc[df['eventid'] == i, ['eventid', 'date_pinged']]
#
#     first = True
#     for index, row in eventFilt.iterrows():
#         if first:
#             # print(index, row[1])
#             timeOne = row[1]
#             # set first to false
#             first = False
#         else:
#             continue
#     # this will be the last row
#     timeTwo = row[1]
#
#     diff = timeTwo - timeOne
#     print(type(diff))
#     # add to dictionary
#     eventTimeDic['id'].append(i)
#     eventTimeDic['length'].append(diff)
#
# eventLengthDF = pd.DataFrame(eventTimeDic)
# eventLengthDF["length"] = round(eventLengthDF["length"].dt.seconds / 60).
# print(eventLengthDF)
#
# print(eventLengthDF['length'].mean())
