
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from vc.helpers.decorators import authorized_users_only, errors
from vc.services.callsmusic.callsmusic import client as USER
from vc.config import SUDO_USERS

@Client.on_message(filters.command(["ubjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<i><b>Add Me As Admin Of Your Group First! 🤔</b></i>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Ichigo_Assistant"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "I Joined Here As You Requested! ☺️")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<i><b>My Assistant Userbot Is Already Here! 😌</b></i>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🔴 Flood Wait Error 🔴 </b>\n<i><b>{user.first_name} Couldn't Join Your Group Due To Heavy Requests For Userbot! Make Sure My Assistant Is Not Blocked/Banned In Your Group.</b></i>🤔"
            " <i><b>Or Manually Add @Ichigo_Assistant To Your Group & Try Again!!</b></i>",
        )
        return
    await message.reply_text(
        "<i><b>My Assistant Userbot Joined Your Chat! 😌</b></i>",
    )


@USER.on_message(filters.group & filters.command(["ubleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>🔴 Flood Wait Error 🔴 </b>"
            "\n<i><b>My Assistant Couldn't Leave Your Group! Manually Kick Her From Your Group If You Want. 😐</b></i>",
        )
        return
    
@Client.on_message(filters.command(["ubleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("`Assistant Leaving From All Chats...`")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"`Assistant Leaving ...` \nLeft: {left} Chats. Failed: {failed} Chats.")
            except:
                failed=failed+1
                await lol.edit(f"`Assistant Leaving ...` \nLeft: {left} Chats. Failed: {failed} Chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} Chats. Failed {failed} Chats.")
    
    
@Client.on_message(filters.command(["ubjoinchannel","ubcjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<i><b>Add Me As Admin Of Your Channel First! 🤔</b></i>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Ichigo_Assistant"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "I Joined Here As You Requested! ☺️")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<i><b>My Assistant Userbot Is Already Here! 😌</b></i>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🔴 Flood Wait Error 🔴 </b>\n<i><b>{user.first_name} Couldn't Join Your Channel Due To Heavy Requests For Userbot! Make Sure My Assistant Is Not Blocked/Banned In Your Channel.</b></i>🤔"
            " <i><b>Or Manually Add @Ichigo_Assistant To Your Channel & Try Again!!</b></i>",
        )
        return
    await message.reply_text(
        "<i><b>My Assistant Userbot Joined Your Channel! 😌</b></i>",
    )
    
