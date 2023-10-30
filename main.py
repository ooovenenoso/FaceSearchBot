import discord
from discord.ext import commands
import time
import requests
import urllib.request

TESTING_MODE = True
APITOKEN = 'your_facecheckid_token_here' # Your API Token

# Initialize Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# Your Discord bot token
DISCORD_TOKEN = 'your_discord_token_here'

# Initialize bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

def search_by_face(image_file):
    # [Your face search code goes here]

@bot.event
async def on_message(message):
    if message.content.startswith('/findit') and message.attachments:
        attachment = message.attachments[0]
        image_file = await attachment.save(fp=f"{attachment.filename}")

        error, urls_images = search_by_face(image_file)
        
        if urls_images:
            response = "\n".join([f"{im['score']} {im['url']} {im['base64'][:32]}..." for im in urls_images])
            await message.channel.send(f"Results:\n{response}")
        else:
            await message.channel.send(error)

# Run bot
bot.run(DISCORD_TOKEN)
