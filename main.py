import discord
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = discord.Client()

def generate_sryden_response(query):
    try:
        requestData = {
            'model': 'polaris',
            'messages': [
                {
                    'role': 'user',
                    'content': query
                }
            ]
        }

        response = requests.get('https://api.sryden.com/api/v1/chat/completions', params=requestData)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as err:
        return f'Error from SRYDEN API: {err}'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('@ping'):
        query = message.content[len('@ping'):].strip()
        response = generate_sryden_response(query)

        if 'choices' in response:
            choices = response['choices']
            for part in choices:
                await message.channel.send(part['message']['content'])

@client.event
async def on_message_private(message):
    if message.author == client.user:
        return

    query = message.content
    response = generate_sryden_response(query)

    if 'choices' in response:
        choices = response['choices']
        for part in choices:
            await message.author.send(part['message']['content'])

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run(os.getenv('DISCORD_TOKEN'))
