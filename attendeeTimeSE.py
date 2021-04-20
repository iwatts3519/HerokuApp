import mysql.connector as connection
import pandas as pd
import numpy as np

sql = "SELECT * FROM attendee_session_tracking LEFT JOIN events ON events.id=attendee_session_tracking.eventid \
       LEFT JOIN attendees ON attendees.id=attendee_session_tracking.attendeeid"

try:
    mydb = connection.connect(host="localhost", database="cad", user="root", passwd="")
    df = pd.read_sql(sql, mydb)
    mydb.close()
except Exception as e:
    print("exception")
    mydb.close()
    print(str(e))

# get a set of all unique attendee id's
uniqueAtenId = set(df['attendeeid'])
uniqueEventId = set(df['eventid'])

attendeeTimeDic = {'id': [], 'length': []}

# for every event, gets all unique attendee ids at that event. Finds out how long each were at that event
# then moves onto the next event
# this all gets added onto attendeeTimeDic which then gets turned into a dataframe
# from here we can find the average

# go through every unique event id
for i in uniqueEventId:
    # create a data frame from the current event id - group on attendee and date_pinged
    df2 = df.loc[df['eventid'] == 3463, ['attendeeid', 'date_pinged']]

    # get the set of all unique attendee ids of that event
    uniqueAttendees = set(df2['attendeeid'])

    # loop through the data frame by attendee id
    for index in uniqueAttendees:
        first = True
        df3 = df2.loc[df2['attendeeid'] == index, ['attendeeid', 'date_pinged']]
        for index, row in df3.iterrows():
            if first:
                timeOne = row[1]
                first = False
            else:
                continue

        timeTwo = row[1]
        diff = timeTwo - timeOne

        attendeeTimeDic['id'].append(i)
        attendeeTimeDic['length'].append(diff)

x = pd.DataFrame(attendeeTimeDic)

print(x)
print(x['length'].mean())
