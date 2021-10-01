import asyncio
from pyrogram import Client, filters
from pyrogram.errors import BotInlineDisabled
from sevennotes.helpers.bot_utils import USERNAME
from config import API_ID, API_HASH, SESSION_NAME

User = Client(
          session_name=SESSION_NAME,
          api_id=API_ID,
          api_hash=API_HASH
       )
REPLY_MESSAGE = """Hello Sir! I'm the userbot of a music bot!! **Don't PM ME**"""
@User.on_message(filters.private & filters.incoming & ~filters.bot & ~filters.service & ~filters.me & ~filters.edited & ~filters.chat([777000, 454000]))
async def nopm(client, message):
    if REPLY_MESSAGE is not None:
        try:
            inline = await client.get_inline_bot_results(USERNAME, "SAF_ONE")
            await client.send_inline_bot_result(
                message.chat.id,
                query_id=inline.query_id,
                result_id=inline.results[0].id,
                hide_via=True
            )
        except BotInlineDisabled:
            print(f"[WARN] - Inline Mode for @{USERNAME} is not enabled. Enable from @Botfather to enable PM Permit !")
            await message.reply_text(f"{REPLY_MESSAGE}\n\n<b>© Powered By : \n@superasunasupport 👑</b>")
        except Exception as e:
            print(e)
            pass
