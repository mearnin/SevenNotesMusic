import os
import asyncio
import ffmpeg
import subprocess
import requests
import sys
from youtube_dl import YoutubeDL
from PIL import Image, ImageDraw, ImageFont
from youtubesearchpython import VideosSearch
from pykeyboard import InlineKeyboard
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from sevennotes.plugins.userbot import User
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sevennotes.helpers.decoraters import admin_check

group_call = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()

VIDEO_CALL = []
ydl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "format" : "135"
}
ydl = YoutubeDL(ydl_opts)

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
  return


@admin_check
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
			button_list = []
			emojilist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
			txt = "**Here are the results:**"
			while j < 5:
				videos = selection[j]
				vtitle = videos["title"]
				dur = videos["duration"]
				views = videos["viewCount"]["short"]
				x = videos["link"]
				pic = videos["thumbnails"][0]
				pict = pic["url"]
				thum = pict.split("?")
				y = thum[0]
				txt += f"\n\n Title: {vtitle}"
				txt += f"\n __Duration: {dur}__"
				txt += f"\n __Views: {views}__"
				emoji = emojilist[j]
				j = j + 1
				button = [f"{emoji}", f"vsong {x} {y}"]
				button_list.append(button)
			keyboard = InlineKeyboard(row_width=3)
		  data = [
			  (
			    InlineKeyboardButton(text=str(i[0]), callback_data=str(i[1]))
			    )
			  for i in button_list
			    ]
			keyboard.add(*data)
			await msg.edit(f"{txt}",
				reply_markup=keyboard,
			)


@Client.on_callback_query(filters.regex(pattern=r"vsong"))
async def song_callbacc(client, CallbackQuery):
	chet_id = CallbackQuery.message.chat.id
	dats = CallbackQuery.data.split(None, 2)
	link = dats[1]
	thumb = dats[2]
	await CallbackQuery.message.delete()
	
	try:
		meta = ydl.download(link)
		m = await client.send_message(chet_id, text=f"Downloading...")
	except Exception as e:
		await client.send_message(chet_id, text=f"Yotube download error : {e}")
	try:
		await gen_cover(thumb)
		VIDEO_CALL.append(chet_id)
		await asyncio.sleep(2)
		await group_call.join(chet_id)
		await client.send_chat_action(chat_id=chet_id, action="upload_photo")
		await group_call.start_video(meta, repeat=False)
		await client.send_photo(chat_id=chet_id, photo="thumbnail.png", caption="✅Started streaming video in vc")
		await client.send_chat_action(chat_id=chet_id, action="cancel")
		await m.delete()
		os.remove("thumbnail.png")
	except Exception as e:
		await m.edit(f"**An error Occured!! Because of {e}**")
		os.remove("thumbnail.png")
		   
