import discord
import os
from googletrans import Translator

# ===== TOKEN =====
TOKEN = os.environ["TOKEN"]

# ===== intents =====
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
translator = Translator()

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')

@client.event
async def on_message(message):
    # Botのメッセージは無視
    if message.author.bot:
        return

    # 空メッセージ防止
    if not message.content:
        return

    try:
        text = message.content

        # ===== 言語判定 =====
        detected = translator.detect(text)

        # ===== 翻訳先を決定 =====
        if detected.lang == 'ja':
            target_lang = 'ko'  # 日本語 → 韓国語
        elif detected.lang == 'ko':
            target_lang = 'ja'  # 韓国語 → 日本語
        else:
            return  # 日本語・韓国語以外は無視

        # ===== 翻訳 =====
        translated = translator.translate(text, dest=target_lang)

        # ===== Webhook取得 or 作成 =====
        webhooks = await message.channel.webhooks()
        webhook = None

        for wh in webhooks:
            if wh.name == "translator":
                webhook = wh
                break

        if webhook is None:
            webhook = await message.channel.create_webhook(name="translator")

        # ===== 送信（名前＆アイコンを再現）=====
        await webhook.send(
            content=translated.text,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url
        )

    except Exception as e:
        print(f"エラー: {e}")

# ===== 起動 =====
client.run(TOKEN)
