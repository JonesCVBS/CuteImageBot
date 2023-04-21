import discord
import asyncio
import datetime
import shutil
import random
import uuid
import os
import imageio
from io import BytesIO
import requests
from PIL import Image


class CuteImageBot:

    def __init__(self, token, allowed_users, channel_id, UnsentFolderName='./NewImages/', SentFolderName='./UsedImages/'):
        self.intents = discord.Intents.default()
        self.intents.messages = True
        self.client = discord.Client(intents=self.intents)
        self.token = token
        self.allowed_users = allowed_users
        self.channel_id = channel_id
        self.UnsentFolderName = UnsentFolderName
        self.SentFolderName = SentFolderName

        for folder in [self.UnsentFolderName, self.SentFolderName]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        @self.client.event
        async def on_ready():
            post_time = datetime.datetime.now().replace(hour=9, minute=15, second=0, microsecond=0) + datetime.timedelta(days=1)
            await self.subbed_images(post_time, self.channel_id)

        @self.client.event
        async def on_message(message):
            await self.handle_message(message)

    def run(self):
        self.client.run(self.token)

    def download_and_add_to_queue(self, url):
        # Generate a unique identifier for the image
        image_id = str(uuid.uuid4())
        # Download the image
        response = requests.get(url)
        # Define accepted file types
        accepted_filetypes = ('.gif', '.mp4', '.jpeg', '.jpg', '.png')

        # Check if the file is an accepted type
        if any(url.lower().endswith(ft) for ft in accepted_filetypes):
            # Check if the file is a gif
            if url.endswith('.gif'):
                # Use imageio to read the gif file
                image = imageio.imread(BytesIO(response.content))
                # Save the gif to a file with the unique identifier as the file name
                image_name = f'{image_id}.gif'
                image_path = './NewImages/' + image_name
                image.save(image_path)
            elif url.endswith('.mp4'):
                video_name = f'{image_id}.mp4'
                video_path = './NewImages/' + video_name
                with open(video_path, 'wb') as f:
                    f.write(response.content)
            else:
                # Open the image using PIL
                image = Image.open(BytesIO(response.content))
                if image.mode == 'RGBA':
                    # Convert the image to RGB mode if it's in RGBA mode
                    image = image.convert('RGB')
                # Save the image to a file with the unique identifier as the file name
                image_name = f'{image_id}.jpg'
                image_path = './NewImages/' + image_name
                image.save(image_path)
        else:
            return f"I can't accept that image/video filetype, please use one of the following: {', '.join(accepted_filetypes)}"

    async def send_images(self, message, num_images=1):
        NewImgs = [os.path.join('./NewImages', i) for i in os.listdir('./NewImages')]
        OldImgs = [os.path.join('./UsedImages', i) for i in os.listdir('./UsedImages')]
        all_images = NewImgs + OldImgs
        if num_images <= 0 or num_images > len(all_images):
            await message.channel.send(
                "Invalid number of images. Please enter a number between 1 and {}.".format(len(all_images)))
            return
        selected_images = random.sample(all_images, num_images)

        # send the selected images to the Discord channel
        for image in selected_images:
            with open(image, 'rb') as f:
                await message.channel.send(file=discord.File(f))

    async def subbed_images(self, post_time, channel_id):
        print("Message received in group ")
        # Set the channel that the images will be posted to
        # channel_id = '547938658397716507'
        channel = self.client.get_channel(int(channel_id))

        # Send a message to confirm that the command was received
        server = channel.guild
        server_name = server.name
        channel_name = channel.name

        # await channel.send('You have subscribed to cute image bot, get ready to receive cute images every day!')
        print(f'The bot is subscribed to the channel "{channel_name}" on the server "{server_name}"')
        # Schedule the posting of the images
        while True:

            # Get the current time
            current_time = datetime.datetime.now()
            # If it is time to post the image, send the next image in the queue
            if current_time > post_time:
                print('Cute image time :D !')
                # Send a message before the pic
                await channel.send('Cute image time :D !')
                # Generate a random number between 1 and 3
                num_images = random.randint(1, 3)

                # Read the image files in the folder
                image_files = os.listdir('./NewImages')
                random.shuffle(image_files)
                # Send the first n images
                for i, current_image in enumerate(image_files):
                    if i < num_images:
                        # move the image
                        shutil.move('./NewImages/' + current_image, './UsedImages/' + current_image)
                        # Send the image
                        await channel.send(file=discord.File('./UsedImages/' + current_image))
                if len(image_files) < num_images:
                    await channel.send('Oh no you have run out of posts :( , make sure you send me more!')

                # Reset the post time to the next day
                RNG_hour = random.randint(8, 15)
                post_time = datetime.datetime.now().replace(hour=RNG_hour, minute=15, second=0,
                                                            microsecond=0) + datetime.timedelta(days=1)

                await asyncio.sleep(60)
            # Wait for a minute before checking the time again
            await asyncio.sleep(60)

    async def handle_message(self, message):
        print(message.content)

        # Set the time that the images will be posted (in this example, 9 AM)
        post_time = datetime.datetime.now()
        # Check if the message is a private message
        if message.channel.type == discord.ChannelType.private:
            # Check if the message was sent by a user that you want to allow to send the bot images
            print("Message received")
            if message.content.startswith('/help'):
                help_text = 'Here are the available commands\n'
                help_text += '/SendRandomPosts x -- it will send x cute images, if x is omitted I will send 1 \n'
                help_text += '/HowManyPosts -- This command tells you how many images are in the UsedImages folder and how many are in the NewImages folder \n'

                await message.channel.send(help_text)
            elif message.content.startswith('/HowManyPosts'):
                NewImgs = [os.path.join('./NewImages', i) for i in os.listdir('./NewImages')]
                OldImgs = [os.path.join('./UsedImages', i) for i in os.listdir('./UsedImages')]
                all_images = NewImgs + OldImgs

                Message_text = f'There are {len(NewImgs)} posts in the folder for future and I have so far sent {len(OldImgs)}'
                await message.channel.send(Message_text)
            elif message.author.id in self.allowed_users:
                # Process the message attachments
                print("Allowed user")
                for attachment in message.attachments:
                    # Download the image and add it to the queue
                    self.download_and_add_to_queue(attachment.url)
                    # Send a message to confirm that the image was received and added to the queue
                    await message.channel.send('Post received and added to the queue!')
            else:
                return
        # Check if the message starts with the "/postCuteImages" command
        if message.content.startswith('/SendRandomPosts'):
            command_components = message.content.split()
            if len(command_components) > 1 and command_components[1].isdigit():
                num_images = int(command_components[1])
            else:
                num_images = 1  # default value
            await self.send_images(message, num_images)



