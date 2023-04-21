# Cute Image Bot

Cute Image Bot is a Discord bot that sends images and videos to your server. You can make it send whatever type of images/videos you want,
Tested on windows 10 and ubuntu 20.04
## Features

    -Send cute images on command.

    -Schedule images to be sent daily at a randomized time.

    -Download and add new images to the bot through private messages.
You can do /help in the bots DMs for commands

## How to Use

After setting up the bot, use the following commands in Discord to interact with the bot:

- `/help`: Sends a list of available commands in a private message.
- '/SendRandomPosts x': it will send x cute images, if x is omitted I will send 1.
- `/HowManyPosts`: Tells how many posts where sent and how many are left.

To add new images to the bot, send a direct message with the image/video to the bot, doesn't work with URLs, only the files. The bot will download the image and add it to the queue. 

## Getting Started

Follow these steps to set up and run Cute Image Bot on your own computer.
### 1. Clone the repository

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/JonesCVBS/CuteImageBot
cd CuteImageBot
```
### 2. Install requirements

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Create a Discord bot and get the token

    1-Go to the Discord Developer Portal.

    2-Log in to your account (or create one if you haven't already).

    3-Click on "New Application" in the top-right corner.

    4-Give your application a name and click on "Create".

    5-In the left sidebar, click on "Bot".

    6-Click on "Add Bot" and confirm by clicking "Yes, do it!".

    7-Under the "TOKEN" section, click on "Copy" to copy the bot token to your clipboard. Make sure to keep this token secret, as it can be used to control your bot.

### 4. Invite the bot to your server

    1-Go back to the "General Information" tab in the left sidebar.

    2-Under the "CLIENT ID" section, click on "Copy" to copy the client ID to your clipboard.

    3-Open a new browser tab and paste the following link, replacing YOUR_CLIENT_ID with the actual client ID you just copied:
  
```bash
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot
```
    4-Select the server you want to add the bot to and click "Authorize". Confirm that you're not a robot, if asked.

### 5. Update the bot token, allowed users, and channel ID in the example script

Open the example.py file in your favorite text editor. Replace the following variables with your own values:

    Replace 'your_token_here' with the bot token you copied in step 3.7.
    Replace User1Id, User2ID in the allowed_users list with the user IDs of the users who are allowed to add images to the bot.
    Replace '' in channel_id with the ID of the channel where you want the bot to send images.
    You can change the folder names by changing the names in UnsentFolderName = './NewImages/' and SentFolderName = './UsedImages/'

Save the changes.
### 6. Run the Cute Image Bot script using the example script

Run the example.py script using Python in a terminal:

```bash
python example.py
```
Now the bot should be running and connected to your server. You can start interacting with it by sending commands in your Discord server or by sending direct messages to the bot.

### 7. Stopping the bot
You can stop the bot by doing ctrl+c in the terminal window
