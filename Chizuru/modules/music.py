import os, random, requests
from pyrogram import filters
from pyrogram.types import *
from pyrogram.errors import UserAlreadyParticipant
from youtube_search import YoutubeSearch

from pytgcalls import AudioPiped, AudioVideoPiped
from pytgcalls.types import Update

from Chizuru import Chizuru, pytgcalls, userbot
from Chizuru.core import utils as rq
from Chizuru.core.utils import DurationLimitError, get_audio_stream, get_video_stream
from Chizuru.core.admin_func import authorized_users
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

# ================= PLAY AUDIO ================= #

@Chizuru.on_message(filters.command(["play"], prefixes=["/", "."]))
async def play(_, message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.mention
    msg = await message.reply("🔎 Searching...")

    # Assistant join
    try:
        user = await userbot.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
            await userbot.join_chat(invitelink)
        except:
            return await msg.edit("❌ Please add assistant as admin first.")

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None

    # ---------- LOCAL AUDIO ---------- #
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            return await msg.edit("❌ Song too long.")

        file_path = await message.reply_to_message.download()
        title = audio.file_name or "Local Audio"
        link = "https://t.me/ChizuruMusicBot"
        thumbnail = random.choice(local_thumb)
        duration = round(audio.duration / 60)
        views = "Local file"

        await generate_cover(user_name, title, views, duration, thumbnail)

    # ---------- YOUTUBE ---------- #
    else:
        if len(message.command) < 2:
            return await msg.edit("Usage: /play song name")

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
            return await msg.edit("❌ Song not found.")

        if (dur / 60) > DURATION_LIMIT:
            return await msg.edit("❌ Song too long.")

        await generate_cover(user_name, title, views, duration, thumbnail)
        file_path = await get_audio_stream(link)

    # ---------- QUEUE / PLAY ---------- #

    ACTV_CALLS = [int(x.chat_id) for x in pytgcalls.active_calls]

    if chat_id in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"➕ Added to queue at position {position}\n\n"
                    f"🎵 {title}\n"
                    f"⏰ {duration}\n"
                    f"👤 {user_name}",
            reply_markup=keyboard,
        )
    else:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(file_path),
        )
        await message.reply_photo(
            photo="final.png",
            caption=f"▶️ Started streaming\n\n"
                    f"🎵 {title}\n"
                    f"⏰ {duration}\n"
                    f"👤 {user_name}",
            reply_markup=keyboard,
        )

    os.remove("final.png")
    await msg.delete()

# ================= VIDEO PLAY ================= #

@Chizuru.on_message(filters.command(["vplay"], prefixes=["/", "."]))
async def vplay(_, message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.mention
    msg = await message.reply("🔎 Searching video...")

    try:
        user = await userbot.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
            await userbot.join_chat(invitelink)
        except:
            return await msg.edit("❌ Add assistant first.")

    if len(message.command) < 2:
        return await msg.edit("Usage: /vplay video name")

    query = message.text.split(None, 1)[1]

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        duration = results[0]["duration"]
        views = results[0]["views"]
        thumbnail = results[0]["thumbnails"][0]
    except:
        return await msg.edit("❌ Video not found.")

    await generate_cover(user_name, title, views, duration, thumbnail)
    file_path = await get_video_stream(link)

    ACTV_CALLS = [int(x.chat_id) for x in pytgcalls.active_calls]

    if chat_id in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"➕ Video added to queue {position}",
            reply_markup=keyboard,
        )
    else:
        await pytgcalls.join_group_call(
            chat_id,
            AudioVideoPiped(file_path),
        )
        await message.reply_photo(
            photo="final.png",
            caption=f"▶️ Started video stream\n🎵 {title}",
            reply_markup=keyboard,
        )

    os.remove("final.png")
    await msg.delete()

# ================= SKIP / AUTO NEXT ================= #

@Chizuru.on_message(filters.command(["skip", "next"]))
async def skip(_, message):
    chat_id = message.chat.id

    if chat_id not in [int(x.chat_id) for x in pytgcalls.active_calls]:
        return await message.reply("❌ Nothing playing.")

    rq.task_done(chat_id)

    if rq.is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        await pytgcalls.change_stream(
            chat_id,
            AudioPiped(rq.get(chat_id)["file"]),
        )
        await message.reply("⏭ Skipped.")

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
