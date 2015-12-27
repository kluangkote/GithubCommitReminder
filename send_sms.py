#!/usr/bin/env python

import json
import time
from datetime import datetime
import random
import requests
from twilio.rest import TwilioRestClient
import datetime
from pytz import timezone
import pytz


def send(s):
    client.sms.messages.create(to="YOURPHONENUMBER", from_="YOURTWILIONUMBER", body=s)

# Various messages to send
messages = [
    "You haven't committed anything today!",
    "Hey busy bee. Time to commit!",
    "Do you want to keep your streak or not?",
    "You better commit soon.",
    "You haven't committed yet.",
    "Don't forget to commit today!"
]

# Initialize Twilio credentials
client = TwilioRestClient("YOURACCOUNTSID", "YOURAUTHTOKEN")

# Get Github contributions activity
url = 'https://api.github.com/users/INSERTUSERNAMEHERE/events'
request = requests.get(url)
if request.ok:
    try:
        data = json.loads(request.text)
        x = 0
        # Different commit events
        while(data[x].get('type') != "PushEvent" and data[x].get('type') != "CreateEvent" and data[x].get('type') != "IssuesEvent" and data[x].get('type') != "PullRequestEvent"):
            x = x+1
        timestamp = data[x].get('created_at')
        timestamp = timestamp.replace("Z", "")
        UTC = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        # Convert UTC to your timezone
        myTimezone = UTC.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('YOURTIMEZONE'))
        stringMyTimezone = myTimezone.strftime("%Y-%m-%d")
        if stringMyTimezone != time.strftime("%Y-%m-%d"):
            message = random.choice(messages)
            send(message)
    except:
        send('There was an error getting the number of commits today')
else:
    send('There was a problem accessing the Github API :(')