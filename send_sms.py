from twilio.rest import Client
from datetime import date
import pickle
import os

today = date.today()
formatted_date = today.strftime("%a, %b %d, %Y")

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

dec_schedule = pickle.load(open("dec_schedule.pkl", "rb"))
jan_schedule = pickle.load(open("jan_schedule.pkl", "rb"))
feb_schedule = pickle.load(open("feb_schedule.pkl", "rb"))
mar_schedule = pickle.load(open("mar_schedule.pkl", "rb"))

if formatted_date in dec_schedule:
    message = dec_schedule[formatted_date]
elif formatted_date in jan_schedule:
    message = jan_schedule[formatted_date]
elif formatted_date in feb_schedule:
    message = feb_schedule[formatted_date]
elif formatted_date in mar_schedule:
    message = mar_schedule[formatted_date]
else:
    message = "none"

if message != "none":
    message = client.messages \
                    .create(
                         body="Schedule for " + formatted_date + "\n\n" + "\n\n".join(message),
                         from_='+12314327402',
                         to='+15715518265'
                    )
    print(message.sid)
else:
    message = client.messages \
                    .create(
                        body="Schedule for " + formatted_date + "\n\n" + "No games today",
                        from_='+12314327402',
                        to='+15715518265'
                    )
    print(message.sid)
