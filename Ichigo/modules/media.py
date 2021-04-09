from Ichigo.modules.disable import DisableAbleCommandHandler
from Ichigo import dispatcher

from telegram.ext import CallbackContext, Filters, CommandHandler

__help__ = """
*Available commands:*\n
*Lyrics:*
 • `/lyrics <song name>`: does a lyric search for a given song name\n
*Image reverse:*
 • `/reverse`: does a *reverse image search* of the media which it was replied to\n
*Text to speech:*
 • `/tts <text>`: convert text to speech\n
*Youtube:*
 • `/youtube`, `/yt` `<song or video name>`: download songs or videos from youtube in standar quality
"""

__mod_name__ = "Media"
__command_list__ = ["reverse", "tts", "song", "video"]
