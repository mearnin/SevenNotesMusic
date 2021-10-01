import os
import asyncio
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

Bot.run()
User.run()

if __name__ == '__main__':
    pyro_client = pyrogram.Client('pytgcalls', API_ID, API_HASH)
    pyro_client.start()

    asyncio.get_event_loop().run_until_complete(main(pyro_client))

