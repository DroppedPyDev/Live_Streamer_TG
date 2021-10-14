import os, asyncio, pafy, youtube_dl
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from Home import video_info_extract, yt_video_search, match_url
from Home import vcusr, ADMINS, CHAT_ID

group_call = GroupCallFactory(vcusr).get_group_call()
music_queue = []
vc_live = False
    
async def play_or_queue(status, data=None):
    global music_queue, group_call
    if not group_call.is_connected:
        await group_call.join(CHAT_ID)
    if status == "add":
        if len(music_queue) == 0:
            music_queue.append(data)
            if data['TYPE'] == "audio":
                await group_call.start_audio(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Playing...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
            elif data['TYPE'] == "video":
                await group_call.start_video(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Streaming...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
        elif len(music_queue) > 0:
            music_queue.append(data)
            return {"status":"queue", "msg":f"🚩 __Queued at {len(music_queue)-1}__"}
    elif status == "check":
        if len(music_queue) == 0:
            await group_call.stop()
            return {"status":"empty", "msg":"💬 __Queue empty. Leaving...__"}
        elif len(music_queue) > 0:
            data = music_queue[0]
            if data['TYPE'] == "audio":
                await group_call.start_audio(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Playing...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
            elif data['TYPE'] == "video":
                await group_call.start_video(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Streaming...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}

@Client.on_message(filters.command("endvc", "!"))
async def leave_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    await group_call.stop()
    vc_live = False
    music_queue.clear()
    await message.reply_sticker("CAADBQADCAMAAtFreFVNNKAMgNe-YwI")
    
@Client.on_message(filters.command("live", "!"))
async def live_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __Give me a URL__")
    if match_url(INPUT_SOURCE, key="yt") is None:
        return await msg.edit("🔎 __Give me a valid URL__")
    #ytlink = await run_cmd(f"youtube-dl -g {INPUT_SOURCE}")
    videof = pafy.new(INPUT_SOURCE)
    ytlink = videof.getbest().url
    if match_url(ytlink) is None:
        return await msg.edit(f"`{ytlink}`")
    try:
        if not group_call.is_connected:
            await group_call.join(CHAT_ID)
        else:
            await group_call.stop()
            await asyncio.sleep(3)
            await group_call.join(CHAT_ID)
            
        await msg.edit("🚩 __Live Streaming...__")
        await group_call.start_video(ytlink, repeat=False, enable_experimental_lip_sync=True)
        vc_live = True
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()

@Client.on_message(filters.command("radio", "!"))
async def radio_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    msg = await message.reply("⏳ __Please wait.__")
    media = message.reply_to_message
    try: INPUT_SOURCE = message.text.split(" ", 1)[1]
    except IndexError: return await msg.edit("🔎 __All radio stations listed [here](https://github.com/AnjanaMadu/radio_stations). Please get link from [here](https://github.com/AnjanaMadu/radio_stations)__", disable_web_page_preview=True)
    if match_url(INPUT_SOURCE) is None:
        return await msg.edit("🔎 __Give me a valid URL__")
    try:
        if not group_call.is_connected:
            await group_call.join(CHAT_ID)
        else:
            await group_call.stop()
            await asyncio.sleep(3)
            await group_call.join(CHAT_ID)
            
        await msg.edit("🚩 __Radio Playing...__")
        await group_call.start_audio(INPUT_SOURCE, repeat=False)
        vc_live = True
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()
    
@Client.on_message(filters.command("play", "!"))
async def play_vc(client, message):
    global vc_live
    if not message.chat.id == CHAT_ID: return
    msg = await message.reply("⏳ __Please wait.__")
    if vc_live == True:
        return await msg.edit("💬 __Live or Radio Ongoing. Please stop it via `!endvc`.__")
    media = message.reply_to_message
    THUMB_URL, VIDEO_TITLE, VIDEO_DURATION = "https://appletld.com/wp-content/uploads/2020/10/E3593D8D-6F1C-4A16-B065-2154ED6B2355.png", "Music", "Not Found"
    if media and media.media:
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 __Give me a URL or Search Query. Look__ `!help`")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
