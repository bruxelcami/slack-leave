from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time

app = Flask(__name__)

SLACK_TOKEN = "YOUR-TOKEN-HERE"
client = WebClient(token=SLACK_TOKEN)
CHANNEL_ID = 'YOUR-CHANNEL-ID-HERE' 

leaves = []
sick_leaves = []

def send_slack_message(channel, text):
    try:
        response = client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

def get_user_id(user_name):
    try:
        response = client.users_list()
        users = response['members']
        for user in users:
            if user['name'] == user_name:
                return user['id']
    except SlackApiError as e:
        print(f"Error fetching user ID: {e.response['error']}")
    return None

def check_leaves():
    today = datetime.now().date()
    messages = []
    
    for leave in leaves:
        if leave['start_date'] <= today <= leave['end_date']:
            messages.append(f"<@{leave['user_id']}> is on leave from {leave['start_date'].strftime('%d/%m/%Y')} to {leave['end_date'].strftime('%d/%m/%Y')}")
        elif today > leave['end_date']:
            leaves.remove(leave)
    
    for sick_leave in sick_leaves:
        if sick_leave['date'] == today:
            messages.append(f"<@{sick_leave['user_id']}> is on sick leave today ({sick_leave['date'].strftime('%d/%m/%Y')})")
    
    if messages:
        send_slack_message(CHANNEL_ID, "\n".join(messages))
    else:
        send_slack_message(CHANNEL_ID, "No one is out today.")

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_leaves, trigger="cron", hour=9, minute=0)
scheduler.start()

@app.route('/leaveday', methods=['POST'])
def leaveday():
    data = request.form
    user = data.get('user_name')
    text = data.get('text')

    user_id = get_user_id(user)
    if not user_id:
        return f"User {user} not found."

    if "from" in text and "to" in text:
        parts = text.split()
        start_date = datetime.strptime(parts[1], "%d/%m/%Y").date()
        end_date = datetime.strptime(parts[3], "%d/%m/%Y").date()
        leaves.append({"user_id": user_id, "start_date": start_date, "end_date": end_date})
        return f"<@{user_id}> leave registered from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}"
    else:
        date = datetime.strptime(text, "%d/%m/%Y").date()
        leaves.append({"user_id": user_id, "start_date": date, "end_date": date})
        return f"<@{user_id}> leave registered for {date.strftime('%d/%m/%Y')}"


@app.route('/sickleave', methods=['POST'])
def sickleave():
    data = request.form
    user = data.get('user_name')
    text = data.get('text')

    user_id = get_user_id(user)
    if not user_id:
        return f"User {user} not found."

    if "today" in text:
        today = datetime.now().date()
        sick_leaves.append({"user_id": user_id, "date": today})
        return f"<@{user_id}> is on sick leave today ({today.strftime('%d/%m/%Y')})"


@app.route('/cancelleave', methods=['POST'])
def cancelleave():
    data = request.form
    user = data.get('user_name')

    user_id = get_user_id(user)
    if not user_id:
        return f"User {user} not found."

    global leaves
    leaves = [leave for leave in leaves if leave['user_id'] != user_id]
    return f"All leaves for <@{user_id}> have been canceled."


@app.route('/cancelsickleave', methods=['POST'])
def cancelsickleave():
    data = request.form
    user = data.get('user_name')

    user_id = get_user_id(user)
    if not user_id:
        return f"User {user} not found."

    global sick_leaves
    sick_leaves = [leave for leave in sick_leaves if leave['user_id'] != user_id]
    return f"All sick leaves for <@{user_id}> have been canceled."


@app.route('/whosout', methods=['POST'])
def whosout():
    today = datetime.now().date()
    messages = []

    for leave in leaves:
        if leave['start_date'] <= today <= leave['end_date']:
            messages.append(f"<@{leave['user_id']}> is on leave from {leave['start_date'].strftime('%d/%m/%Y')} to {leave['end_date'].strftime('%d/%m/%Y')}")

    for sick_leave in sick_leaves:
        if sick_leave['date'] == today:
            messages.append(f"<@{sick_leave['user_id']}> is on sick leave today ({sick_leave['date'].strftime('%d/%m/%Y')})")
    
    if messages:
        return "\n".join(messages)
    else:
        return "No one is out today."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
