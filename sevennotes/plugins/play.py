import asyncio
from pyrogram import Message
from pyrogram import Client, filters
from youtubesearchpython import VideosSearch
import os
import re
import sys
import time
import ffmpeg
import asyncio
import subprocess
from youtube_dl import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from sevennotes.userbot import User


group_call = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()

VIDEO_CALL = []
thumb = ""
ydl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)

def gen_cover(vtitle, views, desc, rating):
	ctxt = f"**Information on {vtitle} video**"
	ctxt += "\n\nTitle: {vtitle}"
	ctxt += "\nViews: {views}"
	ctxt += "\nDescription: {desc}"
	ctxt += "\nRating: {rating}"
	return ctxt

@Client.on_message(filters.command("play")) & ~filters.edited & ~filters.bot & ~filters.private & filters.group
async def play_command(client, message):
	chat_id = message.chat.id
	text = message.text.split(None, 1)[1]
	msg = await message.reply_text(f"Processing...")
	if text = None:
		await msg.edit(f"Give me something to play!!")
	else:
		await msg.edit(f"Finding...")
		try:
			info = await Video.get(text, mode=ResultMode.json)
			rtext = text
			vtitle = info.["title"]
			mb = info.["viewCount"]
			views = mb.["text"]
			desc = info.["description"]
			rating = info.["averageRating"]
			rthumb = info.["thumbnails"]
			pthumb = rthumb.[0]
			thumb = rthumb.["url"]
		except:
			rtext = text.replace("http", "https")
			info = await Video.get(rtext, mode=ResultMode.json)
			vtitle = info.["title"]
			mb = info.["viewCount"]
			views = mb.["text"]
			desc = info.["description"]
			rating = info.["averageRating"]
			rthumb = info.["thumbnails"]
			pthumb = rthumb.[0]
			thumb = rthumb.["url"]
		cover = await gen_cover(vtitle, views, desc, rating)
		req =message.from_user.first_name
		usrn = message.from_user.username
		cover += "\n\n Requested by: {req}"
		cover += "{usrn}"
		await msg.edit(f"**🎦Starting video streaming!!!")
		try:
			await asyncio.sleep(2)
			await group_call.join(chat_id)
			await group_call.start_video(text, with_audio=True, repeat=False)
			VIDEO_CALL.append(chat_id)
		except:
			await asyncio.sleep(2)
			await group_call.start_video(text, with_audio=True, repeat=False)
			VEDIO_CALL.append(chat_id)
		await msg.delete()
		await msg.reply_photo(
					photo=thumb,
					text=cover)


@Client.on_message(filters.command("end")) & filters.group & ~filters.private & ~filters.edited
async def end_command(client, message):
		chat_id = message.chat.id
		if chat_id in VIDEO_CALL:
			await group_call.stop_media(True)
			VIDEO_CALL.remove(chat_id)
		else:
			await message.reply_text(f"**Nothing is playing to stop")



@group_call.on_audio_playout_ended
async def audio_ended_handler(_, __):
    await asyncio.sleep(3)
    await group_call.stop()
    print(f"[INFO] - AUDIO_CALL ENDED !")

@group_call.on_video_playout_ended
async def video_ended_handler(_, __):
    await asyncio.sleep(3)
    await group_call.stop()
    print(f"[INFO] - VIDEO_CALL ENDED !")


		
			
			
		
		
