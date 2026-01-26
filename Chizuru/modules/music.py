import os, aiofiles, aiohttp, random, re
import requests
from asyncio.queues import QueueEmpty

from pyrogram import filters
from pyrogram.types import *
from pyrogram.errors import UserAlreadyParticipant

from youtube_search import YoutubeSearch

from pytgcalls.types import Update
from pytgcalls import AudioPiped, AudioVideoPiped

from Chizuru.core.admin_func import authorized_users
from Chizuru import Chizuru, pytgcalls, userbot
from Chizuru.core import utils as rq
from Chizuru.core.utils import DurationLimitError, get_audio_stream, get_video_stream
from Chizuru.core.thumb_func import generate_cover


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

# ---------------------------------------------------------------------------------- #
# PLAY AUDIO

@Chizuru.on_message(filters.command(["play"], prefixes=["/", "."]))
async def play(_, message):
    chat_id = message.chat.id
    user_name = message.from_user.mention
    msg = await message.reply("**🔎 sᴇᴀʀᴄʜɪɴɢ...**")

    # Assistant join
    try:
        user = await userbot.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
            await userbot.join_chat(invitelink)
            await userbot.send_message(chat_id, "✅ Assistant joined.")
        except UserAlreadyParticipant:
            pass
        except:
            return await msg.edit_text("**» Please add assistant as admin first.**")

    audio = (message.reply_to_message.audio if message.reply_to_message else None)

    # ---------------- LOCAL FILE ---------------- #
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError("Song too long.")

        file_path = await message.reply_to_message.download()
        title = audio.file_name or "Local Audio"
        link = "https://t.me"
        thumbnail = random.choice(local_thumb)
        duration = audio.duration
        views = "Local file"
        await generate_cover(user_name, title, views, duration, thumbnail)

    # ---------------- YOUTUBE ---------------- #
    else:
        if len(message.command) < 2:
            return await msg.edit_text("💌 **Usage: /play song name**")

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

        except:
            return await msg.edit("**sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ.**")

        if (dur / 60) > DURATION_LIMIT:
            return await msg.edit("**sᴏɴɢ ᴛᴏᴏ ʟᴏɴɢ.**")

        await generate_cover(user_name, title, views, duration, thumbnail)
        file_path = await get_audio_stream(link)

    ACTV_CALLS = [int(x.chat_id) for x in pytgcalls.active_calls]

    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position}**\n"
                    f"🏷️ **ɴᴀᴍᴇ :** [{title[:15]}]({link})\n"
                    f"👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {user_name}",
            reply_markup=keyboard,
        )
    else:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(file_path),
        )
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n"
                    f"🏷️ **ɴᴀᴍᴇ :** [{title[:15]}]({link})\n"
                    f"👀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {user_name}",
        )

    os.remove("final.png")
    await msg.delete()

# ---------------------------------------------------------------------------------- #
# VIDEO PLAY

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
        await pytgcalls.join_group_call(
            chat_id,
            AudioVideoPiped(file_path),
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
async def skip(_, message):
    chat_id = message.chat.id

    if chat_id not in [int(x.chat_id) for x in pytgcalls.active_calls]:
        return await message.reply_text("**Nothing playing.**")

    rq.task_done(chat_id)

    if rq.is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        await pytgcalls.change_stream(
            chat_id,
            AudioPiped(rq.get(chat_id)["file"]),
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
            AudioPiped(rq.get(chat_id)["file"]),
        )

# ---------------------------------------------------------------------------------- #
# CONTROLS

@Chizuru.on_message(filters.command(["pause"], prefixes=["/", "!"]))
@authorized_users
async def pause(_, msg):
    await pytgcalls.pause_stream(msg.chat.id)
    await msg.reply("**⏸ Paused.**")

@Chizuru.on_message(filters.command(["resume"], prefixes=["/", "!"]))
@authorized_users
async def resume(_, msg):
    await pytgcalls.resume_stream(msg.chat.id)
    await msg.reply("**▶️ Resumed.**")

@Chizuru.on_message(filters.command(["end", "leavevc"], prefixes=["/", "!"]))
@authorized_users
async def stop(_, msg):
    await pytgcalls.leave_group_call(msg.chat.id)
    await msg.reply("**⏹ Stopped.**")
