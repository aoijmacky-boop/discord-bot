import discord
from googletrans import Translator

import os
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
translator = Translator()

@client.event
async def on_ready():
    print("起動しました")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content

    try:
        lang = translator.detect(text).lang

        if lang == "ja":
            result = translator.translate(text, dest="ko")
            await message.channel.send(result.text)

        elif lang == "ko":
            result = translator.translate(text, dest="ja")
            await message.channel.send(result.text)

    except Exception as e:
        print(e)

client.run(TOKEN)