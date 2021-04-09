import os, glob, json

from Ichigo.modules.sql.clear_cmd_sql import get_clearcmd
from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext, run_async
from Ichigo import dispatcher
from Ichigo.modules.disable import DisableAbleCommandHandler
from Ichigo.modules.helper_funcs.misc import delete
from youtubesearchpython import SearchVideos

from youtube_dl import YoutubeDL


def youtube(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
    yt = message.text[len("/youtube ") :]
    if yt:
        search = SearchVideos(yt, offset=1, mode="json", max_results=1)
        test = search.result()
        
        try:
            p = json.loads(test)
        except:
            return message.reply_text(
                "Failed to find song or video", 
                parse_mode = ParseMode.MARKDOWN
            )
        
        q = p.get("search_result")
        url = q[0]["link"]
        title = q[0]["title"]

        buttons = [
            [
                InlineKeyboardButton("Song", callback_data=f"youtube;audio;{url}"),
                InlineKeyboardButton("Video", callback_data=f"youtube;video;{url}"),
            ]
        ]

        msg = "*Preparing to upload file:*\n"
        msg += f"`{title}`\n"
        delmsg = message.reply_text(
            msg, 
            parse_mode=ParseMode.MARKDOWN,            
            reply_markup = InlineKeyboardMarkup(buttons)
        )
    else:
        delmsg = message.reply_text("Specify a song or video"
        )

    cleartime = get_clearcmd(chat.id, "youtube")
    
    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)

def youtube_callback(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
    query = update.callback_query

    media = query.data.split(";")
    media_type = media[1]
    media_url = media[2]
    
    if media_type == "audio":    
        opts = {
        "format": "bestaudio/best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": False,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
        }
        
        codec = "mp3"

        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(media_url)
            
            try:
                delmsg = message.reply_audio(
                audio = open(f"{rip_data['id']}.{codec}", "rb"),
                duration = int(rip_data['duration']),
                title = str(rip_data['title']),
                parse_mode = ParseMode.HTML)
            except:
                delmsg = message.reply_text(
                    "Song is too large for processing, or any other error happened. Try again later"
                )

    else:
        opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
        }

        codec = "mp4"

        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(media_url)
            
            try:
                delmsg = message.reply_video(
                video = open(f"{rip_data['id']}.{codec}", "rb"),
                duration = int(rip_data['duration']),
                caption = rip_data['title'],
                supports_streaming = True,
                parse_mode = ParseMode.HTML)
            except:
                delmsg = message.reply_text(
                    "Video is too large for processing, or any other error happened. Try again later"
                )

    try:
        os.remove(f"{rip_data['id']}.{codec}")
    except Exception:
        pass

    cleartime = get_clearcmd(chat.id, "youtube")
    
    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)


YOUTUBE_HANDLER = DisableAbleCommandHandler(["youtube", "yt"], youtube, run_async = True)
YOUTUBE_CALLBACKHANDLER = CallbackQueryHandler(
    youtube_callback, pattern="youtube*", run_async=True
)
dispatcher.add_handler(YOUTUBE_HANDLER)
dispatcher.add_handler(YOUTUBE_CALLBACKHANDLER)
