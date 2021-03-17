import mysql.connector as connection
import pandas as pd
import numpy as np

sql = "SELECT * FROM attendee_session_tracking LEFT JOIN events ON events.id=attendee_session_tracking.eventid \
       LEFT JOIN attendees ON attendees.id=attendee_session_tracking.attendeeid"

try:
    mydb = connection.connect(host="localhost", database='cad', user="root", passwd="")
    df = pd.read_sql(sql, mydb)
    mydb.close()
except Exception as e:
    print("exception")
    mydb.close()
    print(str(e))

# get a set of all unique ids
eventidcol = set(df['eventid'])

# create a dictionary
eventTimeDic = {'id': [], 'length': []}

# loop through every unique id
for i in eventidcol:
    # create a new df with filter on eventid
    eventFilt = df.loc[df['eventid'] == i, ['eventid', 'date_pinged']]

    first = True
    for index, row in eventFilt.iterrows():
        if first:
            # print(index, row[1])
            timeOne = row[1]
            # set first to false
            first = False
        else:
            continue
    # this will be the last row
    timeTwo = row[1]

    diff = timeTwo - timeOne
    # add to dictionary
    eventTimeDic['id'].append(i)
    eventTimeDic['length'].append(diff)

eventLengthDF = pd.DataFrame(eventTimeDic)
print(eventLengthDF)

print(eventLengthDF['length'].mean())
