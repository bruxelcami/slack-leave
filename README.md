# slack-leave

A Flask application that integrates with Slack to manage employee leaves and sick leaves through slash commands.

Description
This Slack bot allows users to:

Register leave days.
Register sick leaves.
Cancel leaves and sick leaves.
Check who is out on a given day.
The bot periodically announces who is on leave or sick leave in a specified Slack channel.

Features
Slash Commands: Integrates with Slack slash commands for easy interaction.
Periodic Notifications: Sends scheduled messages to a Slack channel about current leaves.
User Identification: Maps Slack usernames to user IDs for accurate tagging.
Simple Data Storage: Uses in-memory lists to store leave data (suitable for small-scale or testing purposes).
Requirements
Python 3.x
Flask
slack-sdk
APScheduler
Installation
Clone the Repository

git clone https://github.com/bruxelcami/slack-leave.git
cd slack-leave
Install Dependencies

pip install -r requirements.txt
Configuration
Slack Token

Obtain a Slack Bot Token by creating a new app in your Slack workspace and enabling the necessary permissions.

Set Environment Variables

Create a .env file in the root directory and add the following:

SLACK_TOKEN='your-slack-bot-token'
CHANNEL_ID='your-slack-channel-id'
Replace 'your-slack-bot-token' with your actual Slack Bot Token and 'your-slack-channel-id' with the ID of the Slack channel where you want the bot to send messages.

Update the Application

Ensure the application reads the token and channel ID from the environment variables:

import os

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
Running the Application
Start the Flask application by running:


python app.py
The application will run on http://0.0.0.0:80.

Setting Up Slack Slash Commands
Create a Slack App

Go to Slack API Apps and create a new app.
Enable the following scopes under OAuth & Permissions:
commands
chat:write
users:read
Set Up Slash Commands

Configure the following slash commands under Slash Commands:

/leaveday
/sickleave
/cancelleave
/cancelsickleave
/whosout
For each command, set the request URL to your server's URL corresponding to the command endpoint. For example:


http://your-server-address/leaveday
Install the App to Your Workspace

Complete the OAuth installation to add the app to your Slack workspace.

Usage
Register a Leave Day


/leaveday DD/MM/YYYY
Or for a range:

/leaveday from DD/MM/YYYY to DD/MM/YYYY

Cancel Leaves
/cancelleave

Check Who's Out

/whosout

Notes
The application currently uses in-memory storage for leaves and sick leaves. For production use, consider integrating a database.
Ensure that your Slack Bot Token and Channel ID are kept secure and not exposed in any public repositories.

License
This project is licensed under the MIT License - see the LICENSE file for details.
