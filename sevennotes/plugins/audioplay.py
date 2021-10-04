import os
import asyncio
import ffmpeg
import subprocess
import sys
from youtubesearchpython import VideosSearch
from pyrogram import Client, filters
from pyrogram.types import Message
from sevennotes.plugins.videoplay import ydl, group_call
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

AUDIO_CALL = []
Url = []

@Client.on_message(filters.command("aplay") & filters.group & ~filters.private & ~filters.edited)
async def aplay_command(client, message):
	msg = await message.reply_text(f"Processing!...")
	if len(message.command) < 2:
		await msg.edit(f"**❌Give me something to play!!**")
	else:
		query = message.text.split(None, 1)[1]
		vid = query.strip()
		await msg.edit(f"**Processing...**")
		if not "http" in query:
			select = VideosSearch(vid, limit = 5)
			selection = select.result()["result"]
			j = 0
			
			txt = "**Here are the results:**"
			while j < 5:
				videos = selection[j]
				vtitle = videos["title"]
				dur = videos["duration"]
				views = videos["viewCount"]["short"]
				x = videos["link"]
				Url.append(x)
				txt += "\n\n Title: {title}"
				txt += "\n __Duration: {dur}__"
				txt += "\n __Views: {views}__"
				j = j + 1
			keyboard = InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						text="1️⃣",
						callback_data="song1",
					),
					InlineKeyboardButton(
						text="2️⃣",
						callback_data="song2",
					),
					InlineKeyboardButton(
						text="3️⃣",
						callback_data="song3",
					),
				],
				[
					InlineKeyboardButton(
						text="4️⃣",
						callback_data="song4",
					),
					InlineKeyboardButton(
						text="5️⃣",
						callback_data="song4",
					),
				],
			])
			await msg.edit(f"{txt}",
				reply_markup=keyboard,
			)


@Client.on_callback_query(filters.regex("^(song1|song2|song3|song4|song5)"))
async def song_callbacc(client, CallbackQuery):
	cb = CallbackQuery.matches[0].group(1)
	chet_id = CallbackQuery.message.chat.id
	if cb == "song1":
		link = Url[0]
	elif cb == "song2":
		link = Url[1]
	elif cb == "song3":
		link = Url[2]
	elif cb == "song4":
		link = Url[3]
	elif cb == "song5":
		link = Url[4]
	await CallbackQuery.message.delete()
	
	try:
		meta = ydl.extract_info(link, download=False)
		m = await Client.send_message(chat_id=chet_id, text=f"Downloading...")
		formats = meta.get('formats', [meta])
		for f in formats:
			ytstreamlink = f['url']
		Limk = ytstreamlink
	except Exception as e:
		await Client.send_message(chat_id=chet_id, text=f"**Youtube Download error: {e}**")
	try:
		AUDIO_CALL.append(chat_id)
		await asyncio.sleep(2)
		await group_call.join(chat_id)
		await group_call.start_audio(Limk, repeat=False)
		await m.edit("✅Started streaming audio in vc")
	except Exception as e:
		await m.edit("**An error Occured!! Because of {e}**")
		
		      
	
		
		
					
				
			
		
	
