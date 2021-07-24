from pyrogram import Client, filters
from vc.config import ARQ_API_BASE_URL, ARQ_API_KEY, LOG_GRP
from vc.botinfo import BOT_ID
import aiohttp
import aiofiles
from aiohttp import ClientSession
from Python_ARQ import ARQ
from functools import wraps
from vc.fetch import fetch

session = ClientSession()
arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

__MODULE__ = "ChatBot"
__HELP__ = "/chatbot [ON|OFF] To Enable Or Disable ChatBot In Your Chat."

active_chats = []

# Enabled | Disable Chatbot


@Client.on_message(filters.command("chatbot"))
async def chatbot_status(_, message):
    global active_chats
    if len(message.command) != 2:
        await message.reply_text("/chatbot [ON|OFF]")
        return
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id

    if status == "ON" or status == "on" or status == "On":
        if chat_id not in active_chats:
            active_chats.append(chat_id)
            text = "Chatbot Enabled Reply To Any Message" \
                   + "Of Mine To Get A Reply"
            await message.reply_text(text)
            return
        await message.reply_text("ChatBot Is Already Enabled.")
        return

    elif status == "OFF" or status == "off" or status == "Off":
        if chat_id in active_chats:
            active_chats.remove(chat_id)
            await message.reply_text("Chatbot Disabled!")
            return
        await message.reply_text("ChatBot Is Already Disabled.")
        return

    else:
        await message.reply_text("/chatbot [ON|OFF]")


@Client.on_message(filters.text & filters.reply & filters.incoming & ~filters.bot)
async def chatbot_talk(_, message):
    if message.chat.id not in active_chats:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    query = message.text
    luna = await arq.luna(query)
    response = luna.response
    await app.send_chat_action(message.chat.id, "typing")
    await message.reply_text(response)
    
    
