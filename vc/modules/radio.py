from pyrogram import Client, filters
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME
from config import STREAM


@Client.on_message(filters.command(["radio", f"radio@{USERNAME}"]))
async def radio(client, message: Message):
    if 1 in RADIO:
        await message.reply_text("Kindly stop existing Radio Stream /stopradio")
        return
    await mp.start_radio()
    await message.reply_text(f"Started Radio: <code>{STREAM}</code>")
    await message.delete()

@Client.on_message(filters.command(['stopradio', f"stopradio@{USERNAME}"]))
async def stop(_, message: Message):
    if 0 in RADIO:
        await message.reply_text("Kindly start Radio First /radio")
        return
    await mp.stop_radio()
    await message.reply_text("Radio stream ended.")
    await message.delete()
