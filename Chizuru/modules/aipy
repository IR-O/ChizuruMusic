import asyncio
import base64
import mimetypes
import os
from pyrogram import filters, types as t
from lexica import AsyncClient
from Chizuru import Chizuru
from lexica.constants import languageModels


async def ChatCompletion(prompt, model) -> tuple | str:
    try:
        modelInfo = getattr(languageModels, model)
        client = AsyncClient()
        output = await client.ChatCompletion(prompt, modelInfo)
        if model == "bard":
            return output['content'], output['images']
        return output['content']
    except Exception as e:
        raise Exception(f"API error: {e}")


async def geminiVision(prompt, model, images) -> tuple | str:
    imageInfo = []
    for image in images:
        with open(image, "rb") as imageFile:
            data = base64.b64encode(imageFile.read()).decode("utf-8")
            mime_type, _ = mimetypes.guess_type(image)
            imageInfo.append({
                "data": data,
                "mime_type": mime_type
            })
        os.remove(image)
    payload = {
        "images": imageInfo
    }
    modelInfo = getattr(languageModels, model)
    client = AsyncClient()
    output = await client.ChatCompletion(prompt, modelInfo, json=payload)
    return output['content']['parts'][0]['text']


def getMedia(message):
    """Extract Media"""
    media = message.media or (message.reply_to_message.media if message.reply_to_message else None)
    if media:
        if message.photo:
            return message.photo
        elif message.document and message.document.mime_type in ['image/png', 'image/jpg', 'image/jpeg'] and message.document.file_size < 5242880:
            return message.document
    elif message.reply_to_message and message.reply_to_message.media:
        if message.reply_to_message.photo:
            return message.reply_to_message.photo
        elif message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png', 'image/jpg', 'image/jpeg'] and message.reply_to_message.document.file_size < 5242880:
            return message.reply_to_message.document
    return None


def getText(message):
    """Extract Text From Commands"""
    if not message.text:
        return None
    parts = message.text.split(None, 1)
    return parts[1] if len(parts) > 1 else None


@Chizuru.on_message(filters.command(["gpt", "bard", "llama", "mistral", "palm", "gemini"]))
async def chatbots(_, m: t.Message):
    prompt = getText(m)
    media = getMedia(m)
    if media:
        return await askAboutImage(_, m, [media], prompt)
    if not prompt:
        return await m.reply_text("Hello, how can I assist you today?")
    model = m.command[0].lower()
    output = await ChatCompletion(prompt, model)
    if model == "bard":
        output_text, images = output
        if not images:
            return await m.reply_text(output_text)
        media_group = [t.InputMediaPhoto(img) for img in images]
        media_group[0] = t.InputMediaPhoto(images[0], caption=output_text)
        await _.send_media_group(
            m.chat.id,
            media_group,
            reply_to_message_id=m.id
        )
        return
    await m.reply_text(output['parts'][0]['text'] if model == "gemini" else output)


async def askAboutImage(_, m: t.Message, mediaFiles: list, prompt: str):
    images = []
    for media in mediaFiles:
        image = await _.download_media(media.file_id, file_name=f'./downloads/{m.from_user.id}_ask.jpg')
        images.append(image)
    output = await geminiVision(prompt or "What's this?", "geminiVision", images)
    await m.reply_text(output)
