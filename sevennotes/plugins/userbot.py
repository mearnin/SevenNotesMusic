from pyrogram import Client
from config import API_ID, API_HASH, SESSION_NAME

User = Client(
          SESSION_NAME,
          API_ID,
          API_HASH
       )
