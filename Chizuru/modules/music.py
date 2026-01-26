import os, aiofiles, aiohttp, ffmpeg, random, re
import requests
from typing import Callable
from asyncio.queues import QueueEmpty

from pyrogram import filters, Client
from pyrogram.types import *
from pyrogram.errors import UserAlreadyParticipant

from youtube_search import YoutubeSearch

from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream, InputVideoStream, InputStream
from pytgcalls.types.input_stream.quality import HighQualityAudio, HighQualityVideo

from Chizuru.core.admin_func import authorized_users, admins as a, set_admins as set
from Chizuru import Chizuru, pytgcalls, userbot
from Chizuru.core import utils as rq
from Chizuru.core.utils import DurationLimitError
from Chizuru.core.utils import get_audio_stream, get_video_stream
from Chizuru.core.thumb_func import transcode, convert_seconds, time_to_seconds, generate_cover


DURATION_LIMIT = 300

keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(" ᴄʟᴏsᴇ ", callback_data="close_data")]]
)

local_thumb = [
    "https://graph.org/file/e3fa9ab16ebefbfdd29d9.jpg",
    "https://graph.org/file/5938774f48c1f019c73f7.jpg",
    "https://graph.org/file/b13a16734bab174f58482.jpg",
    "https://graph.org/file/2deb4e5cbba862f2d5457.jpg",
]

que = {}
chat_id = None
useer = "NaN"

# ---------------------------------------------------------------------------------- #

@Chizuru.on_message(filters.command(["play"], prefixes=["/", "."]))
async def play(_, message):
    global que, useer

    chat_id = message.chat.id
    user_name = message.from_user.mention
    msg = await message.reply("**🔎 sᴇᴀʀᴄʜɪɴɢ...**")

    # Assistant join logic (unchanged)
    try:
        user = await userbot.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
            await userbot.join_chat(invitelink)
            await userbot.send_message(chat_id, "✅ Assistant joined for music.")
        except UserAlreadyParticipant:
            pass
        except Exception:
            return await msg.edit_text("**» Please manually add assistant as admin.**")

    audio = ((message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None)

    # ------------------ LOCAL FILE PLAY ------------------ #
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError("Song too long.")

        file_path = await message.reply_to_message.download()
        title = audio.file_name
        link = "https://t.me/ChizuruMusicBot"
        thumbnail = random.choice(local_thumb)
        duration = round(audio.duration / 60)
        views = "Local file"
        await generate_cover(user_name, title, views, duration, thumbnail)

    # ------------------ YOUTUBE PLAY ------------------ #
    else:
        if len(message.command) < 2:
            return await msg.edit_text("💌 **Usage: /play song name**")

        await msg.edit_text("▓▓▓▓▓▓▓▓▓▓▓100%\n\n**⇆ ᴘʀᴏᴄᴇssɪɴɢ...**")
        query = message.text.split(None, 1)[1]

        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            secmul, dur = 1, 0
            for i in duration.split(":")[::-1]:
                dur += int(i) * secmul
                secmul *= 60

        except Exception:
            return await msg.edit("**sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ.**")

        if (dur / 60) > DURATION_LIMIT:
            return await msg.edit("**sᴏɴɢ ᴛᴏᴏ ʟᴏɴɢ.**")

        await generate_cover(user_name, title, views, duration, thumbnail)
        file_path = await get_audio_stream(link)

    # ------------------ QUEUE / PLAY LOGIC ------------------ #

    ACTV_CALLS = [int(x.chat_id) for x in pytgcalls.active_calls]

    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position}**\n\n"
                    f"🏷️ **ɴᴀᴍᴇ :** [{title[:15]}]({link})\n"
                    f"⏰ **ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}`\n"
                    f"👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {user_name}",
            reply_markup=keyboard,
        )
    else:
        # 🔥 MAIN FIX: AudioPiped → InputStream(InputAudioStream)
        await pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    file_path,
                    HighQualityAudio()
                )
            ),
        )
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n"
                    f"🏷️ **ɴᴀᴍᴇ :** [{title[:15]}]({link})\n"
                    f"⏰ **ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}`\n"
                    f"👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {user_name}\n",
        )

    os.remove("final.png")
    return await msg.delete()

# ---------------------------------------------------------------------------------- #
# VIDEO PLAY (vplay) – SAME FIX

@Chizuru.on_message(filters.command(["vplay"], prefixes=["/", "."]))
async def vplay(_, message):
    chat_id = message.chat.id
    user_name = message.from_user.mention
    msg = await message.reply("**🔎 sᴇᴀʀᴄʜɪɴɢ...**")

    try:
        user = await userbot.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
            await userbot.join_chat(invitelink)
        except:
            return await msg.edit_text("**» Add assistant first.**")

    if len(message.command) < 2:
        return await msg.edit_text("Usage: /vplay video name")

    query = message.text.split(None, 1)[1]

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        duration = results[0]["duration"]
        views = results[0]["views"]
        thumbnail = results[0]["thumbnails"][0]
    except:
        return await msg.edit("**Video not found.**")

    await generate_cover(user_name, title, views, duration, thumbnail)
    file_path = await get_video_stream(link)

    ACTV_CALLS = [int(x.chat_id) for x in pytgcalls.active_calls]

    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴠɪᴅᴇᴏ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position}**",
            reply_markup=keyboard,
        )
    else:
        # 🔥 MAIN FIX: AudioVideoPiped → InputStream(InputVideoStream)
        await pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputVideoStream(
                    file_path,
                    HighQualityVideo()
                )
            ),
        )
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ sᴛᴀʀᴛᴇᴅ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ**\n"
                    f"🏷️ **ɴᴀᴍᴇ :** [{title[:15]}]({link})",
            reply_markup=keyboard,
        )

    os.remove("final.png")
    await msg.delete()

# ---------------------------------------------------------------------------------- #
# SKIP / NEXT

@Chizuru.on_message(filters.command(["skip", "next"], prefixes=["/", "!"]))
async def skip(_, message: Message):
    chat_id = message.chat.id
    ACTV_CALLS = [int(x.chat_id) for x in pytgcalls.active_calls]

    if chat_id not in ACTV_CALLS:
        return await message.reply_text("**Nothing playing.**")

    rq.task_done(chat_id)

    if rq.is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        await pytgcalls.change_stream(
            chat_id,
            InputStream(
                InputAudioStream(
                    rq.get(chat_id)["file"],
                    HighQualityAudio()
                )
            ),
        )
        await message.reply_text("**⏭ Skipped.**")

# ---------------------------------------------------------------------------------- #
# AUTO NEXT

@pytgcalls.on_stream_end()
async def on_stream_end(_, update: Update):
    chat_id = update.chat_id
    rq.task_done(chat_id)

    if rq.is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        await pytgcalls.change_stream(
            chat_id,
            InputStream(
                InputAudioStream(
                    rq.get(chat_id)["file"],
                    HighQualityAudio()
                )
            ),
        )

# ---------------------------------------------------------------------------------- #
# CONTROL COMMANDS (UNCHANGED)

@Chizuru.on_message(filters.command("join"))
@authorized_users
async def join_userbot(_, msg):
    chat_id = msg.chat.id
    invitelink = await Chizuru.export_chat_invite_link(chat_id)
    await userbot.join_chat(invitelink)
    await msg.reply("**Assistant joined.**")

@Chizuru.on_message(filters.command(["pause"], prefixes=["/", "!"]))
@authorized_users
async def pause(_, msg):
    chat_id = msg.chat.id
    await pytgcalls.pause_stream(chat_id)
    await msg.reply("**⏸ Paused.**")

@Chizuru.on_message(filters.command(["resume"], prefixes=["/", "!"]))
@authorized_users
async def resume(_, msg):
    chat_id = msg.chat.id
    await pytgcalls.resume_stream(chat_id)
    await msg.reply("**▶️ Resumed.**")

@Chizuru.on_message(filters.command(["end"], prefixes=["/", "!"]))
@authorized_users
async def stop(_, msg):
    chat_id = msg.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await msg.reply("**⏹ Stopped.**")

@Chizuru.on_message(filters.command(["leavevc"], prefixes=["/", "!"]))
@authorized_users
async def leavevc(_, msg):
    chat_id = msg.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await msg.reply("**Left voice chat.**")

@Chizuru.on_message(filters.command("volume", prefixes="/"))
async def change_volume(client, message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) == 2 and args[1].isdigit():
        volume = int(args[1])
        await pytgcalls.change_volume_call(chat_id, volume)
        await message.reply(f"**Volume set to {volume}%**")
    else:
        await message.reply("**Usage: /volume 0-200**")
