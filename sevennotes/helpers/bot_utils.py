from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

Bot = Client(
    "SevenNotesMusic",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN
)
Bot.start()
util = Bot.get_me()
USERNAME = util.username
BOT_NAME = util.first_name
