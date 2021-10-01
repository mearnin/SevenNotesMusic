import asyncio
from pyrogram import Client, filters
from youtubesearchpython.__future__ import *
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
from sevennotes.plugins.userbot import User


group_call = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()

VIDEO_CALL = []

ydl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)

@Client.on_message(filters.command("play") & ~filters.edited & filters.group)
async def play_command(client, message):
	chat_id = message.chat.id
	msg = await message.reply_text(f"Processing...")
	if len(message.command) < 2:
		await msg.edit(f"Give me something to play!!")
	else:
		await msg.edit(f"**Finding...**")
		
		text = message.text.split(None, 1)[1]
		meta = ydl.extract_info(text, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                    ytstreamlink = f['url']
                link = ytstreamlink
		 
		try:
			await asyncio.sleep(2)
			await group_call.join(chat_id)
			await msg.edit(f"Starting Video Streaming in VC")
			await group_call.start_video(link, with_audio=True, repeat=False)
			VIDEO_CALL.append(chat_id)
		except:
			await asyncio.sleep(2)
			await group_call.start_video(link, with_audio=True, repeat=False)
			await msg.edit(f"Starting Video Streaming")
			VEDIO_CALL.append(chat_id)
		await msg.delete()
		await msg.reply_text(f"Video is streaming now! Join to the VoiceChat")


@Client.on_message(filters.command("end") & filters.group & ~filters.edited)
async def end_command(client, message):
		chat_id = message.chat.id
		if chat_id in VIDEO_CALL:
			await group_call.stop_media(True)
			VIDEO_CALL.remove(chat_id)
			await msg.reply_text("**Stopped Streaming")
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
 



		
			
			
		
		
