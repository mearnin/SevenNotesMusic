import os
import asyncio
import pytgcalls
from sevennotes.plugins.userbot import User
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN

Bot = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="sevennotes.plugins"),
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")

Bot.start()
User.start()
print("\n[INFO]: Starting Bot and User client")

idle()

print("\n[INFO]: Stopping Bot and User client")

Bot.stop()
User.stop()








