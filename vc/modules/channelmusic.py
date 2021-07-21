
import json
import os
from os import path
from typing import Callable
from asyncio.queues import QueueEmpty
import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import Voice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch
from vc.modules.play import generate_cover
from vc.modules.play import arq
from vc.modules.play import cb_admin_check
from vc.modules.play import transcode
from vc.modules.play import convert_seconds
from vc.modules.play import time_to_seconds
from vc.modules.play import changeImageSize
from vc.config import BOT_NAME as bn
from vc.config import DURATION_LIMIT
from vc.config import UPDATES_CHANNEL as updateschannel
from vc.config import que
from vc.function.admins import admins as a
from vc.helpers.errors import DurationLimitError
from vc.helpers.decorators import errors
from vc.helpers.admins import get_administrators
from vc.helpers.channelmusic import get_chat_id
from vc.helpers.decorators import authorized_users_only
from vc.helpers.filters import command, other_filters
from vc.helpers.gets import get_file_name
from vc.services.callsmusic import callsmusic, queues
from vc.services.callsmusic.callsmusic import client as USER
from vc.services.converter.converter import convert
from vc.services.downloaders import youtube

chat_id = None



@Client.on_message(filters.command(["cplaylist","cplaylist@Ichigotest_Bot"]) & filters.group & ~filters.edited)
async def playlist(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
    except:
      message.reply("❌ __**Chat Is Not Linked!**__")
      return
    global que
    queue = que.get(lol)
    if not queue:
        await message.reply_text("__**Player is Idle!**__ 😴")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "▶️ **Now Playing** in {}".format(lel.linked_chat.title)
    msg += "\n- " + now_playing
    msg += "\n- Req By: " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "🔂 **Queued Playlist:**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n- {name}"
            msg += f"\n- Req By: {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        # if chat.id in active_chats:
        stats = "⚙️ Settings of **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "🎚 Volume : {}%\n".format(vol)
            stats += "🎵 Songs in Queue : `{}`\n".format(len(que))
            stats += "🔉 Now Playing : **{}**\n".format(queue[0][0])
            stats += "🎧 Requested By : {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏸", "cpuse"),
                InlineKeyboardButton("▶️", "cresume"),
                InlineKeyboardButton("⏭", "cskip"),
                InlineKeyboardButton("⏹", "cleave"),
            ],
            [
                InlineKeyboardButton("Playlist 🎹", "cplaylist"),
                InlineKeyboardButton("Close 🗑", "ccls"),
            ]
        ]
    )
    return mar


@Client.on_message(filters.command(["ccurrent","ccurrent@Ichigotest_Bot"]) & filters.group & ~filters.edited)
async def ee(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("__**There Is No Voice Chat Running!**__ 🙄")


@Client.on_message(filters.command(["csettings","csettings@Ichigotest_Bot"]) & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    playing = None
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("__**There Is No Voice Chat Running!**__ 🙄")


@Client.on_callback_query(filters.regex(pattern=r"^(cplaylist)$"))
async def p_cb(b, cb):
    global que
    try:
      lel = await client.get_chat(cb.message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      return    
    que.get(lol)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(lol)
        if not queue:
            await cb.message.edit("__**Player is Idle!**__ 😴")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "▶️ **Now Playing** in {}".format(conv.title)
        msg += "\n- " + now_playing
        msg += "\n- Req By: " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "🔂 **Queued Playlist:**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req By: {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(cplay|cpause|cskip|cleave|cpuse|cresume|cmenu|ccls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Stream Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
      try:
        lel = await b.get_chat(cb.message.chat.id)
        lol = lel.linked_chat.id
        conv = lel.linked_chat
        chet_id = lol
      except:
        return
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat
    

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "cpause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Voice Chat Is Not Connected!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("Music Paused!")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "cplay":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Voice Chat Is Not Connected!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Music Resumed!")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "cplaylist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("__**Player is Idle!**__ 😴")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "▶️ **Now Playing** in {}".format(cb.message.chat.title)
        msg += "\n- " + now_playing
        msg += "\n- Req By: " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "🔂 **Queued Playlist:**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req By: {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "cresume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Maybe Not Connected or Already Playing!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Music Resumed!")
    elif type_ == "cpuse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Maybe Not Connected or Already Paused!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("Music Paused!")
    elif type_ == "ccls":
        await cb.answer("Closed Menu!")
        await cb.message.delete()

    elif type_ == "cmenu":
        stats = updated_stats(conv, qeue)
        await cb.answer("Menu Opened!")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏸", "cpuse"),
                    InlineKeyboardButton("▶️", "cresume"),
                    InlineKeyboardButton("⏭", "cskip"),
                    InlineKeyboardButton("⏹", "cleave"),
                ],
                [
                    InlineKeyboardButton("Playlist 🎹", "cplaylist"),
                    InlineKeyboardButton("Close 🗑", "ccls"),
                ]
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)
    elif type_ == "cskip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("Voice Chat Is Not Connected!", show_alert=True)
        else:
            callsmusic.queues.task_done(chet_id)

            if callsmusic.queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("__**No Song In Queue!**__ 😪\n**Leaving From Voice Chat...**")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, callsmusic.queues.get(chet_id)["file"]
                )
                await cb.answer("Skipped!")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"__**Skipped Track!**__\n▶️ **Now Playing:** **{qeue[0][0]}**"
                )

    else:
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("✅ __**Successfully Left The Voice Chat!**__")
        else:
            await cb.answer("Voice Chat Is Not Connected!", show_alert=True)


@Client.on_message(filters.command(["cplay","cplay@Ichigotest_Bot"])  & filters.group & ~filters.edited)
@authorized_users_only
async def play(_, message: Message):
    global que
    lel = await message.reply("`Hang On! Processing ...`🎵")

    try:
      conchat = await _.get_chat(message.chat.id)
      conv = conchat.linked_chat
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return
    try:
      administrators = await get_administrators(conv)
    except:
      await message.reply("__**Am I Admin of The Channel ?**__ 🤔")
    try:
        user = await USER.get_me()
    except:
        user.first_name = "Ichigo_Assistant"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Stream Music: "):
                    await lel.edit(
                        "<i><b>Remember To Add @Ichigo_Assistant To Your Channel! 🤔</b></i>",
                    )
                    pass

                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<i><b>Add Me As Admin Of Your Channel First! 🤔</b></i>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "<i><b>@Ichigo_Assistant Joined Your Channel! 😌</b></i>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 Flood Wait Error 🔴 </b>\n<i><b>{user.first_name} Couldn't Join Your Channel Due To Heavy Requests For Userbot! Make Sure My Assistant Is Not Blocked/Banned In Your Channel.</b></i>🤔"
                         " <i><b>Or Manually Add @Ichigo_Assistant To Your Channel & Try Again!!</b></i>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i>{user.first_name} Not In This Chat, Ask Admin To Send /play Command For First Time or Add @Ichigo_Assistant Manually! 😶</i>"
        )
        return
    message.from_user.id
    text_links = None
    message.from_user.first_name
    await lel.edit("`Hang On! Searching ...`🔎")
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]
    else:
        urls=None
    if text_links:
        urls = True    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"__**Sorry! 😞 \nI Can't Play Songs Which Longer Than {DURATION_LIMIT} Minutes!**__"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Playlist 🎹", callback_data="cplaylist"),
                    InlineKeyboardButton("Settings ⚙️", callback_data="cmenu"),
                ],
                [InlineKeyboardButton(text="Close 🗑", callback_data="ccls")],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/820cac7cb7b1a025542e2.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally Added"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("`Hang On! Processing ...`🎵")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "__**Literary Found Noting 😓 \nPlease Try Another Song or Use Correct Spelling!**__"
            )
            print(str(e))
            return
        dlurl = url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Playlist 🎹", callback_data="cplaylist"),
                    InlineKeyboardButton("Settings ⚙️", callback_data="cmenu"),
                ],
                [
                    InlineKeyboardButton(text="YouTube 🎬", url=f"{url}"),
                    InlineKeyboardButton(text="Close 🗑", callback_data="ccls"),
                ]
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))        
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("`Hang On! Processing ...`🎵")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "__**Literary Found Noting 😓 \nPlease Try Another Song or Use Correct Spelling!**__"
            )
            print(str(e))
            return

        dlurl = url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Playlist 🎹", callback_data="cplaylist"),
                    InlineKeyboardButton("Settings ⚙️", callback_data="cmenu"),
                ],
                [
                    InlineKeyboardButton(text="YouTube 🎬", url=f"{url}"),
                    InlineKeyboardButton(text="Close 🗑", callback_data="ccls"),
                ]
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))
    chat_id = chid
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption="🎙 **Title** : [{}]({})\n⏱ **Duration** : `{}`\n💡 **Status** : `Queued ({})`\n🎧 **Requested By** : {}".format(
                title, url, duration, position, message.from_user.mention()
            ),
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = chid
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="🎙 **Title** : [{}]({})\n⏱ **Duration** : `{}`\n💡 **Status** : `Playing`\n🎧 **Requested By** : {}".format(
                title, url, duration, message.from_user.mention()
            ),
        )
        os.remove("final.png")
        return await lel.delete()

