
import logging
from vc.modules.msg import Messages as tr
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from vc.config import SOURCE_CODE,ASSISTANT_NAME,PROJECT_NAME,SUPPORT_GROUP,UPDATES_CHANNEL,BOT_USERNAME
logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.private & filters.incoming & filters.command(['startm']))
def _start(client, message):
    client.send_message(message.chat.id,
        text=tr.START_MSG.format(message.from_user.first_name, message.from_user.id),
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❔ HOW TO USE ME ❔", url="https://telegra.ph/How-To-Use-Stream-Music-Bot-04-08")],
                [
                    InlineKeyboardButton(
                        "📢 CHANNEL", url=f"https://t.me/{UPDATES_CHANNEL}"), 
                    InlineKeyboardButton(
                        "SUPPORT 💬", url=f"https://t.me/{SUPPORT_GROUP}")
                ],[
                    InlineKeyboardButton(
                        "➕ ADD ME TO YOUR GROUP ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
        )

@Client.on_message(filters.command("startm@Ichigotest_Bot") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
    await message.reply_text(
        f"""**Thanks For Adding Me!** ❤️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🎛 ᴄᴏᴍᴍᴀɴᴅꜱ 🎛", url="https://telegra.ph/Stream-Music-Bot---Commands-04-24"
                    )
                ]
            ]
        ),
    )


@Client.on_message(filters.private & filters.incoming & filters.command(['helpm']))
def _help(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG[1],
        parse_mode="markdown",
        disable_web_page_preview=True,
        disable_notification=True,
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))

@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    disable_web_page_preview=True
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    client.edit_message_text(chat_id=chat_id,    message_id=message_id,
        text=tr.HELP_MSG[msg],    reply_markup=InlineKeyboardMarkup(map(msg))
    )


def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = 'LET\'S START', callback_data = "help+2")]
        ]
    elif(pos==len(tr.HELP_MSG)-1):
        url = f"https://t.me/{SUPPORT_GROUP}"
        button = [
            [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton(text = '📢 CHANNEL', url=f"https://t.me/{UPDATES_CHANNEL}"),
             InlineKeyboardButton(text = 'SUPPORT 💬', url=f"https://t.me/{SUPPORT_GROUP}")],
            [InlineKeyboardButton(text = '◀️', callback_data = f"help+{pos-1}"),
             InlineKeyboardButton(text = '🔐', callback_data = "close")]
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '◀️', callback_data = f"help+{pos-1}"),
                InlineKeyboardButton(text = '▶️', callback_data = f"help+{pos+1}")
            ],
        ]
    return button

@Client.on_message(filters.command("helpm") & ~filters.private & ~filters.channel)
async def ghelp(_, message: Message):
    await message.reply_text(
        f"""**🙋‍♀️ Hello There! \nI Can Play Music In The Voice Chats Of Telegram Groups & Channels 😇!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❔ HOW TO USE ME ❔", url=f"https://t.me/{BOT_USERNAME}?start"
                    )
                ]
            ]
        ),
    )

@Client.on_message(
    filters.command("search")
    & filters.group
    & ~ filters.edited
)
async def search(client: Client, message: Message):
    await message.reply_text(
        "💁🏻‍♂️ Hey, Do You Want To Search For Song?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Yes", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "No ❌", callback_data="close"
                    )
                ]
            ]
        )
    )

@Client.on_callback_query(filters.regex("close"))
async def close(client: Client, query: CallbackQuery):
    await query.message.delete()
