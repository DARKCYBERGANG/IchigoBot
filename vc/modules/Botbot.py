import re
from asyncio import gather, get_event_loop, sleep

from aiohttp import ClientSession
from pyrogram import Client, filters, idle
from Python_ARQ import ARQ

from vc.config import ARQ_API_BASE_URL, ARQ_API_KEY, LANGUAGE

luna = Client(
    ":memory:",
    bot_token="1690374847:AAFIyej-OT4CEFDu8CaMiTekXa4sMJAnFlo",
    api_id=6400129,
    api_hash="c1b151498dd24438519e3017097b46ab",
)
bot_token="1690374847:AAFIyej-OT4CEFDu8CaMiTekXa4sMJAnFlo"
bot_id = int(bot_token.split(":")[0])


async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")


@Client.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
        "[GitHub](https://github.com/thehamkercat/LunaChatBot)"
        + " | [Group](t.me/PatheticProgrammers)",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("help") & ~filters.edited)
async def start(_, message):
    await Client.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("/repo - Get Repo Link")


@Client.on_message(
    ~filters.private
    & filters.text
    & ~filters.command("help")
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "[.|\n]{0,}luna[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@Client.on_message(
    filters.private & ~filters.command("help") & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        return
    await type_and_send(message)


async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await Client.start()
    print(
        """
-----------------
| Luna Started! |
-----------------
"""
    )
    await idle()


