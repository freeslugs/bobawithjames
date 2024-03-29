# from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, render_template, json, request, redirect

import base64
from time import strftime
import dateutil.parser

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None
flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'

app = Flask(__name__)
app.config['DEBUG'] = True 

@app.route('/')
def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 20 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=20, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')

    latest_time = strftime('%I:%M %p')
    latest_date = strftime("%a %m/%d")
    return_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start = dateutil.parser.parse(start)
        start_time = start.strftime('%I:%M %p')
        start_date = start.strftime("%a %m/%d")
        end = dateutil.parser.parse(end)
        end_time = end.strftime('%I:%M %p')
        end_date = end.strftime("%a %m/%d")
        # print(start, end, event['summary'])

        if (start_time > latest_time):
            return_list.append([latest_time, latest_date, start_time, start_date])
        latest_time = end_time
        latest_date = end_date

    # print(return_list)
    return render_template('index.html', api_data=return_list)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # try:
    #     import argparse
    #     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    # except ImportError:
    #     flags = None
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    print(credentials)
    if not credentials or credentials.invalid:
    # if True:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        from oauth2client import tools
        flags = tools.argparser.parse_args(args=[])
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

@app.route('/signup', methods = ['GET','POST'])
def signup():
	name = request.form['name']
	email = request.form['email']
	time = request.form['time']
	# print(name, email, time)

	me = "jamesxue100@gmail.com"
	you = email

	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Link"
	msg['From'] = me
	msg['To'] = you

	html = open("/Users/jamesxue/Documents/projects/boba/templates/email.html").read()
	# print(html)

	part2 = MIMEText(html, 'html')

	msg.attach(part2)

	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	username = "jamesxue100@gmail.com"
	# s.login(username,password) 
	# s.sendmail(me, you, msg.as_string())
	# s.quit()

	return redirect('/yay')

@app.route('/yay')
def yay():
	return render_template('yay.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')