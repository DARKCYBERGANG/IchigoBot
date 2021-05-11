from os import path

from Ichigo import pbot
from pyrogram.types import Message

from ..callsmusic import callsmusic
from .. import converter
from ..downloaders import youtube
from ..helpers.decorators import errors
from ..helpers.errors import DurationLimitError
from ..helpers.filters import command, other_filters
from ..helpers.gets import get_url, get_file_name
from .. import queues


@pbot.on_message(command("play") & other_filters)
@errors
async def play(_, message: Message):
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > 10:
            raise DurationLimitError(
                f"Videos longer than 10 minute(s) aren’t allowed, the provided video is {audio.duration / 60} minute(s)"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await message.reply_text("You did not give me anything to play!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        await message.reply_text(f"Queued at position {await queues.put(message.chat.id, file_path=file_path)}!")
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_text("Playing...")
