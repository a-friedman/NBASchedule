from twilio.rest import Client
from datetime import date
import pickle
import os

today = date.today()
formatted_date = today.strftime("%a, %b %d, %Y")

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

schedule = pickle.load(open("schedule.pkl", "rb"))

if formatted_date in schedule:
    message = "\n\n".join(schedule[formatted_date])
else:
    message = "No games today"

message = client.messages \
                .create(
                     body="Schedule for " + formatted_date + "\n\n" + message,
                     from_='+12314327402',
                     to='+15715518265'
                )
print(message.sid)
