from CuteImageBot import CuteImageBot

# Set your bot token, allowed users and channel ID
token = 'your_token_here'
allowed_users = [User1Id,User2ID]    #your allowed users ID
channel_id = ''    #your channel ID
UnsentFolderName = './your_unsent_folder_name/'
SentFolderName = './your_sent_folder_name/'

# Create a new instance of the bot and run it
bot = CuteImageBot(token, allowed_users, channel_id, UnsentFolderName=UnsentFolderName, SentFolderName=SentFolderName)
bot.run()