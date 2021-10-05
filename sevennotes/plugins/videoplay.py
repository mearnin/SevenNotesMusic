import os
import asyncio
import ffmpeg
import subprocess
import requests
import sys
from youtube_dl import YoutubeDL
from PIL import Image, ImageDraw, ImageFont
from youtubesearchpython import VideosSearch
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from sevennotes.plugins.userbot import User
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

group_call = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()

VIDEO_CALL = []

ydl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)
VUrl = []
VThumb = []

async def gen_cover(thumb):
	photo = requests.get(thumb)
	picture = open("thumb.jpg", "wb")
	picture.write(photo.content)
	picture.close()
	img = Image.open("thumb.jpg")
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("adds/font.ttf", 80)
	draw.text((205, 400), f"Now playing...", (79, 186, 224), font=font)
	img.save("thumbnail.png")
	os.remove("thumb.jpg")

@Client.on_message(filters.command("vplay") & filters.group & ~filters.private & ~filters.edited)
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
				VUrl.append(x)
				pic = videos["thumbnails"][0]
				pict = pic["url"]
				thum = pict.split("?")
				y = thum[0]
				VThumb.append(y)
				txt += f"\n\n Title: {vtitle}"
				txt += f"\n __Duration: {dur}__"
				txt += f"\n __Views: {views}__"
				j = j + 1
			keyboard = InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						text="1️⃣",
						callback_data="vsong1",
					),
					InlineKeyboardButton(
						text="2️⃣",
						callback_data="vsong2",
					),
					InlineKeyboardButton(
						text="3️⃣",
						callback_data="vsong3",
					),
				],
				[
					InlineKeyboardButton(
						text="4️⃣",
						callback_data="vsong4",
					),
					InlineKeyboardButton(
						text="5️⃣",
						callback_data="vsong5",
					),
				],
			])
			await msg.edit(f"{txt}",
				reply_markup=keyboard,
			)


@Client.on_callback_query(filters.regex("^(vsong1|vsong2|vsong3|vsong4|vsong5)"))
async def song_callbacc(client, CallbackQuery):
	cb = CallbackQuery.matches[0].group(1)
	chet_id = CallbackQuery.message.chat.id
	if cb == "vsong1":
		link = VUrl[0]
		thumb = VThumb[0]
	elif cb == "vsong2":
		link = VUrl[1]
		thumb = VThumb[1]
	elif cb == "vsong3":
		link = VUrl[2]
		thumb = VThumb[2]
	elif cb == "vsong4":
		link = VUrl[3]
		thumb = VThumb[3]
	elif cb == "vsong5":
		link = VUrl[4]
		thumb = VThumb[4]
	await CallbackQuery.message.delete()
	
	try:
		meta = ydl.extract_info(link, download=False)
		m = await client.send_message(chet_id, text=f"Downloading...")
		formats = meta.get('formats', [meta])
		for f in formats:
			ytstreamlink = f['url']
		Limk = ytstreamlink
	except Exception as e:
		await client.send_message(chet_id, text=f"Yotube download error : {e}")
	try:
		await gen_cover(thumb)
		VIDEO_CALL.append(chet_id)
		await asyncio.sleep(2)
		await group_call.join(chet_id)
		await client.send_chat_action(chat_id=chet_id, action="upload_photo")
		await group_call.start_video(Limk, repeat=False)
		await client.send_photo(chat_id=chet_id, photo="thumbnail.png", caption="✅Started streaming video in vc")
		await client.send_chat_action(chat_id=chet_id, action="cancel")
		await m.delete()
		VUrl.clear()
		VThumb.clear()
		os.remove("thumbnail.png")
	except Exception as e:
		await m.edit(f"**An error Occured!! Because of {e}**")
		VUrl.clear()
		VThumb.clear()
		os.remove("thumbnail.png")
		   
