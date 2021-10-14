
import os, asyncio
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from Home import vcusr, CHAT_ID, ADMINS
from Home.Modules.player import group_call, vc_live, music_queue

vc_paused = False
    
@Client.on_message(filters.command("pause", "!"))
async def pause_vc(client, message):
    global vc_paused
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    if vc_paused is False:
        await group_call.set_pause(True)
        await message.reply("__VC Paused!__")
        vc_paused = True
    elif vc_paused is True:
        return await message.reply("__Already Paused.__")
          
@Client.on_message(filters.command("resume", "!"))
async def resume_vc(client, message):
    global vc_paused
    if not message.chat.id == CHAT_ID: return
    if not message.from_user.id in ADMINS: return
    if vc_paused is True:
        await group_call.set_pause(False)
        await message.reply("__VC Resumed!__")
        vc_paused = False
    elif vc_paused is False:
        return await message.reply("__VC not Paused.__")

@Client.on_message(filters.command("help", "!"))
async def help_vc(client, message):
    text = '''====== Help Menu ======
**Play as Audio**
- !play __(reply to audio / youtube url / search query)__
- !radio __(radio stream url)__

**Play as Video**
- !stream __(reply to video / youtube url / search query)__
- !live __(youtube live stream url)__

**Extra**
- !endvc: Leave from vc.
- !skip: Skip the current song.
- !pause: Pause the vc.
- !resume: Resume the vc.
- !video: Download url or search query in video format.
- !audio: Download url or search query in audio format.'''
    await message.reply(text)
