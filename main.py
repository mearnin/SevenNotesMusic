import os
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
print("\n[INFO] - STARTED VIDEO PLAYER BOT, JOIN @ASMSAFONE !")

idle()
Bot.stop()
User.stop()
print("\n[INFO] - STOPPED VIDEO PLAYER BOT, JOIN @ASMSAFONE !")
