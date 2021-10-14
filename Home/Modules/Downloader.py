

import os
from pyrogram import Client, filters
from Home import vcusr
from Home import yt_video_search, match_url
import youtube_dl

@Client.on_message(filters.command("audio", "!"))
async def audio_dl(client, message):
    msg = await message.reply("⏳ Processing Request...!")
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __Give me a search queue__")
    if match_url(INPUT_SOURCE) is None:
        FINAL_URL = yt_video_search(INPUT_SOURCE)
    else:
        FINAL_URL = INPUT_SOURCE
    aud_opts = {
        'format':'bestaudio[ext=m4a]',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
    }
    try:
        await msg.edit("📥 __Downloading...__")
        with youtube_dl.YoutubeDL(aud_opts) as ytdl:
            ytdl_data = ytdl.extract_info(FINAL_URL, download=True)
            fname = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"`{e}`")
    await msg.edit("📤 __Uploading...__")
    await message.reply_audio(
        fname,
        caption=ytdl_data['title'],
        title=ytdl_data['title'],
        performer='Live_Streamer_TG')
    try:
        os.remove(fname)
        await msg.delete()
    except: pass
    
@Client.on_message(filters.command("video", "!"))
async def video_dl(client, message):
    msg = await message.reply("⏳ Processing Request...")
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __Give me a search queue__")
    if match_url(INPUT_SOURCE) is None:
        FINAL_URL = yt_video_search(INPUT_SOURCE)
    else:
        FINAL_URL = INPUT_SOURCE
    vid_opts = {
        'format':'best',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
    }
    try:
        await msg.edit("📥 __Downloading...__")
        with youtube_dl.YoutubeDL(vid_opts) as ytdl:
            ytdl_data = ytdl.extract_info(FINAL_URL, download=True)
            fname = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"`{e}`")
    await msg.edit("📤 __Uploading...__")
    await message.reply_video(
        fname,
        caption=ytdl_data['title'])
    try:
        os.remove(fname)
        await msg.delete()
    except: pass
