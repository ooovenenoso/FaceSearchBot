import discord
from discord.ext import commands
import requests

# Define TESTING_MODE global variable
TESTING_MODE = True

# Your Discord bot token
DISCORD_TOKEN = 'DISCORD_API_KEY'

# Initialize bot with intents
# Initialize Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='/', intents=intents)

# URL for the FaceCheck API
UPLOAD_URL = "https://facecheck.id/api/upload_pic"

# API token for authorization
API_TOKEN = 'FaceCheck_API_KEY'

async def search_by_face(image_bytes, testing_mode=True):
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    params = {'test_mode': testing_mode} if testing_mode else {}

    try:
        files = {'images': image_bytes}
        response = requests.post(UPLOAD_URL, files=files, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for unsuccessful responses
        data = response.json()

        # Check if there's an error in the response
        error = data.get('error')
        if error:
            return f"Error searching by face: {error}", None

        # Check if there are items in the output
        output = data.get('output')
        if output and 'items' in output:
            items = output['items']
            if items:
                return None, items

        return "No items found in response", None

    except Exception as e:
        return f"Error searching by face: {str(e)}", None

@bot.event
async def on_message(message):
    if message.content.startswith('/findit') and message.attachments:
        attachment = message.attachments[0]
        image_bytes = await attachment.read()

        error, urls_images = await search_by_face(image_bytes, testing_mode=TESTING_MODE)

        if urls_images:
            response = "\n".join([f"{im['score']} {im['url']['value']} {im['base64'][:32]}..." for im in urls_images])
            await message.channel.send(f"Results:\n{response}")
        else:
            await message.channel.send(error)

# Run bot
bot.run(DISCORD_TOKEN)
