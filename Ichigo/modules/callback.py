from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, emoji
from utils import mp
from config import Config
playlist=Config.playlist

HELP = """
<b>Add the bot and User account in your Group with admin rights.
Start a VoiceChat
Use /play <song name> or use /play as a reply to an audio file or youtube link.
You can also use /dplay <song name> to play a song from Deezer.</b>
**Common Commands**:
**/play**  Reply to an audio file or YouTube link to play it or use /play <song name>.
**/dplay** Play music from Deezer, Use /dplay <song name>
**/player**  Show current playing song.
**/help** Show help for commands
**/playlist** Shows the playlist.
**Admin Commands**:
**/skip** [n] ...  Skip current or n where n >= 2
**/join**  Join voice chat.
**/leave**  Leave current voice chat
**/vc**  Check which VC is joined.
**/stop**  Stop playing.
**/radio** Start Radio.
**/stopradio** Stops Radio Stream.
**/replay**  Play from the beginning.
**/clean** Remove unused RAW PCM files.
**/pause** Pause playing.
**/resume** Resume playing.
**/mute**  Mute in VC.
**/unmute**  Unmute in VC.
**/restart** Restarts the Bot.
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "Who the hell you are",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Empty Playlist"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Paused\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="resume"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    
    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Resumed\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏯", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Skipped\n\n{pl}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏯", callback_data="pause"),
                        InlineKeyboardButton("⏩", callback_data="skip")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton('⚙️ Update Channel', url='https://t.me/subin_works'),
                InlineKeyboardButton('🤖 Other Bots', url='https://t.me/subin_works/122'),
            ],
            [
                InlineKeyboardButton('👨🏼‍💻 Developer', url='https://t.me/subinps'),
                InlineKeyboardButton('🧩 Source', url='https://github.com/subinps/MusicPlayer'),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP,
            reply_markup=reply_markup

        )
