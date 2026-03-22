import discord
import os
from googletrans import Translator

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
translator = Translator()

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.content:
        return

    try:
        text = message.content
        detected = translator.detect(text)

        if detected.lang == 'ja':
            target_lang = 'ko'
        elif detected.lang == 'ko':
            target_lang = 'ja'
        else:
            return

        translated = translator.translate(text, dest=target_lang)

        # ===== Webhook作成（強制）=====
        webhook = await message.channel.create_webhook(name="translator")
        print("Webhook作成成功")

        await webhook.send(
            content=translated.text,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url
        )

        print("Webhook送信成功")

    except Exception as e:
        print(f"エラー: {e}")

client.run(TOKEN)
