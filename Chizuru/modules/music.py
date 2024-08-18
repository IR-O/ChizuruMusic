import os, aiofiles, aiohttp, ffmpeg, random, re
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
from Chizuru.core.utils import DurationLimitError
from Chizuru.core.utils import get_audio_stream, get_video_stream
from pytgcalls.types import Update
from pytgcalls.types import AudioQuality, MediaStream, VideoQuality
from Chizuru.core.thumb_func import transcode, convert_seconds, time_to_seconds, generate_cover




DURATION_LIMIT = 300

keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(" ᴄʟᴏsᴇ ", callback_data="close_data"),    
        ]
])

local_thumb = [
"https://graph.org/file/e3fa9ab16ebefbfdd29d9.jpg",
"https://graph.org/file/5938774f48c1f019c73f7.jpg",
"https://graph.org/file/b13a16734bab174f58482.jpg",
"https://graph.org/file/2deb4e5cbba862f2d5457.jpg",
]


# --------------------------------------------------------------------------------------------------------- #

que = {}
chat_id = None
useer = "NaN"

# --------------------------------------------------------------------------------------------------------- #

@Chizuru.on_message(filters.command(["play"], prefixes=["/","."]))
async def play(_, message):
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
        try:
            await userbot.join_chat(invitelink)
            await userbot.send_message(message.chat.id, text="** ✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        except UserAlreadyParticipant:            
            pass
        except Exception as e:
            await msg.edit_text(f"**ᴘʟᴇᴀsᴇ ᴍᴀɴᴜᴀʟʟʏ ᴀᴅᴅ ᴀssɪsᴛᴀɴᴛ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ [sᴜᴍɪᴛ ʏᴀᴅᴀᴠ](https://t.me/AnonDeveloper)** ")
                            
    audio = ((message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None)
   
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
        else:
            await msg.edit_text("▓▓▓▓▓▓▓▓▓▓▓100%\n\n**⇆ ᴘʀᴏᴄᴇssɪɴɢ...**")
                
        query = message.text.split(None, 1)[1]
            
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
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
            
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n**​🏷️ ɴᴀᴍᴇ :**[{title[:15]}]({link})\n⏰** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏᴇ : **{user_name}",
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
            caption=f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({link})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{user_name}\n",
           )

    os.remove("final.png")
    return await msg.delete()



# --------------------------------------------------------------------------------------------------------- #


@Chizuru.on_message(filters.command(["vplay"], prefixes=["/","."]))
async def vplay(_, message):
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
        try:
            await userbot.join_chat(invitelink)
            await userbot.send_message(message.chat.id, text="** ✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        except UserAlreadyParticipant:            
            pass
        except Exception as e:
            await msg.edit_text(f"**ᴘʟᴇᴀsᴇ ᴍᴀɴᴜᴀʟʟʏ ᴀᴅᴅ ᴀssɪsᴛᴀɴᴛ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ [sᴜᴍɪᴛ ʏᴀᴅᴀᴠ](https://t.me/AnonDeveloper)** ")
                            
    video = (message.reply_to_message.video if message.reply_to_message else None)
   
    if video:
        if round(video.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"** sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**"
            )

        file_path = await message.reply_to_message.download()
        title = video.file_name 
        link = "https://t.me/ChizuruMusicBot"
        thumbnail = random.choice(local_thumb)
        duration = round(video.duration / 60)
        views = "Locally added"
        await generate_cover(user_name, title, views, duration, thumbnail)
       
            
    
    else:
        if len(message.command) < 2:
            await msg.edit_text("💌 **ᴜsᴀɢᴇ: /vᴘʟᴀʏ ɢɪᴠᴇ ᴀ ᴛɪᴛʟᴇ sᴏɴɢ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        else:
            await msg.edit_text("▓▓▓▓▓▓▓▓▓▓▓100%\n\n**⇆ ᴘʀᴏᴄᴇssɪɴɢ...**")
                
        query = message.text.split(None, 1)[1]
            
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
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
        file_path = await get_video_stream(link)
            
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n**​🏷️ ɴᴀᴍᴇ :**[{title[:15]}]({link})\n⏰** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏᴇ : **{user_name}",
            reply_markup=keyboard,
        )
       
    else:
        await pytgcalls.join_group_call(
            chat_id,
            AudioVideoPiped(file_path)
                 
        )
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({link})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{user_name}\n",
           )

    os.remove("final.png")
    return await msg.delete()






# --------------------------------------------------------------------------------------------------------- #

@Chizuru.on_message(filters.command(["skip", "next"], prefixes=["/", "!"]))
async def skip(_, message: Message):
    ACTV_CALLS = []
    print(ACTV_CALLS)
    chat_id = message.chat.id
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    
    if chat_id not in ACTV_CALLS:
        await message.reply_text("**ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ᴛᴏ sᴋɪᴘ.**")
    else:
        rq.task_done(chat_id)
        
        if rq.is_empty(chat_id):
            await pytgcalls.leave_group_call(chat_id)
        else:
            await pytgcalls.change_stream(
                    chat_id,
                    AudioPiped(
                        rq.get(chat_id)["file"],
                    ),
                )
            await message.reply_text("**ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴋɪᴘᴘᴇᴅ ᴛʜᴇ sᴏɴɢ.**")




    

# --------------------------------------------------------------------------------------------------------- #


@pytgcalls.on_stream_end()
async def on_stream_end(_, update: Update) -> None:
    chat_id = update.chat_id
    rq.task_done(chat_id)

    if rq.is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        await pytgcalls.change_stream(
            chat_id, 
            AudioPiped(
                
                    rq.get(chat_id)["file"],
                ),
            
        )
            
# --------------------------------------------------------------------------------------------------------- #

@Chizuru.on_message(filters.command("join"))
@authorized_users
async def join_userbot(_,msg):
  chat_id = msg.chat.id
  invitelink = await Chizuru.export_chat_invite_link(chat_id)
  await userbot.join_chat(invitelink)
  await msg.reply("**ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴ.**")


# --------------------------------------------------------------------------------------------------------- #


@Chizuru.on_message(filters.command(["pause"], prefixes=["/", "!"]))    
@authorized_users
async def pause(_, msg):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.pause_stream(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴘᴀᴜsᴇᴅ\nᴘᴀᴜsᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ᴘᴀᴜsᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇʀᴇ ɪs ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")

# --------------------------------------------------------------------------------------------------------- #


@Chizuru.on_message(filters.command(["resume"], prefixes=["/", "!"])) 
@authorized_users
async def resume(_, msg):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.resume_stream(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴜᴍᴇ\nʀᴇsᴜᴍᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ʀᴇsᴜᴍᴇ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇʀᴇ ɪs ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")


# --------------------------------------------------------------------------------------------------------- #


@Chizuru.on_message(filters.command(["end"], prefixes=["/", "!"])) 
@authorized_users
async def stop(_, msg):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.leave_group_call(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴅᴇᴅ sᴏɴɢ\nᴇɴᴅᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ᴇɴᴅ ᴍᴜsɪᴄ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")


# --------------------------------------------------------------------------------------------------------- #


@Chizuru.on_message(filters.command(["leavevc"], prefixes=["/", "!"]))
@authorized_users
async def leavevc(_, msg):
    chat_id = msg.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇᴀᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\nʟᴇᴀᴠᴇᴅ ʙʏ {msg.from_user.mention}",)
    

# --------------------------------------------------------------------------------------------------------- #


@Chizuru.on_message(filters.command("volume", prefixes="/"))
async def change_volume(client, message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) == 2 and args[1].isdigit():
        volume = int(args[1])
        await pytgcalls.change_volume_call(chat_id, volume)
        await message.reply(f"ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ {volume}%")
    else:
        await message.reply("ᴜsᴀɢᴇ: /volume [0-200]")


