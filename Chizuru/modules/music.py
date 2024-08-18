import os
import aiofiles
import aiohttp
import ffmpeg
import random
import re
import requests
from Chizuru.core.admin_func import authorized_users, admins as a, set_admins as set
from Chizuru import Chizuru, pytgcalls, userbot
from typing import Callable
from pyrogram import filters, Client
from pyrogram.types import *
from youtube_search import YoutubeSearch
from asyncio.queues import QueueEmpty
from pyrogram.errors import UserAlreadyParticipant
from Chizuru.core import utils as rq
from Chizuru.core.utils import DurationLimitError, get_audio_stream, get_video_stream
from pytgcalls.types import Update
from pytgcalls import AudioPiped, AudioVideoPiped, AudioQuality, AudioParameters
from Chizuru.core.thumb_func import transcode, convert_seconds, time_to_seconds, generate_cover

DURATION_LIMIT = 300

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(" ᴄʟᴏsᴇ ", callback_data="close_data")]
])

local_thumb = [
    "https://graph.org/file/e3fa9ab16ebefbfdd29d9.jpg",
    "https://graph.org/file/5938774f48c1f019c73f7.jpg",
    "https://graph.org/file/b13a16734bab174f58482.jpg",
    "https://graph.org/file/2deb4e5cbba862f2d5457.jpg",
]

# Global variables
que = {}
chat_id = None
useer = "NaN"

@Chizuru.on_message(filters.command(["play"], prefixes=["/", "."]))
async def play(_, message: Message):
    global que
    global useer
    chat_id = message.chat.id
    user_name = message.from_user.mention
    msg = await message.reply("**🔎 sᴇᴀʀᴄʜɪɴɢ...**")
    try:
        user = await userbot.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
        except Exception:
            await msg.edit_text("**» ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғɪʀsᴛ.**")
            return
        try:
            await userbot.join_chat(invitelink)
            await userbot.send_message(message.chat.id, text="** ✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        except UserAlreadyParticipant:
            pass
        except Exception:
            await msg.edit_text(f"**ᴘʟᴇᴀsᴇ ᴍᴀɴᴜᴀʟʟʏ ᴀᴅᴅ ᴀssɪsᴛᴀɴᴛ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ [sᴜᴍɪᴛ ʏᴀᴅᴀᴠ](https://t.me/AnonDeveloper)** ")
            return

    audio = message.reply_to_message.audio or message.reply_to_message.voice if message.reply_to_message else None

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"** sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**"
            )

        file_path = await message.reply_to_message.download()
        title = audio.file_name
        link = "https://t.me/ChizuruMusicBot"
        thumbnail = random.choice(local_thumb)
        duration = round(audio.duration / 60)
        views = "Locally added"
        await generate_cover(user_name, title, views, duration, thumbnail)
    else:
        if len(message.command) < 2:
            await msg.edit_text("💌 **ᴜsᴀɢᴇ: /ᴘʟᴀʏ ɢɪᴠᴇ ᴀ ᴛɪᴛʟᴇ sᴏɴɢ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
            return
        await msg.edit_text("▓▓▓▓▓▓▓▓▓▓▓100%\n\n**⇆ ᴘʀᴏᴄᴇssɪɴɢ...**")
        query = message.text.split(None, 1)[1]

        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            with open(thumb_name, "wb") as f:
                f.write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60
        except Exception:
            await msg.edit("**sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ, ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ sᴏɴɢ ɴᴀᴍᴇ.**")
            return

        if (dur / 60) > DURATION_LIMIT:
            await msg.edit(f"**sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**")
            return

        await generate_cover(user_name, title, views, duration, thumbnail)
        file_path = await get_audio_stream(link)

    ACTV_CALLS = [int(x.chat_id) for x in pytgcalls.active_calls]
    if chat_id in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n**​🏷️ ɴᴀᴍᴇ :**[{title[:15]}]({link})\n⏰** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {user_name}",
            reply_markup=keyboard,
        )
    else:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(
                file_path,
                AudioParameters.from_quality(AudioQuality.STUDIO),
            ),
        )
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({link})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : ** {user_name}\n",
        )

    os.remove("final.png")
    await msg.delete()
