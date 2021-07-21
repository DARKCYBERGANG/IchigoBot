
from asyncio.queues import QueueEmpty
from vc.config import que
from pyrogram import Client, filters
from pyrogram.types import Message

from vc.function.admins import set
from vc.helpers.channelmusic import get_chat_id
from vc.helpers.decorators import authorized_users_only, errors
from vc.helpers.filters import command, other_filters
from vc.services.callsmusic import callsmusic



@Client.on_message(filters.command(["cpause","cpause@Ichigotest_Bot"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def pause(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return    
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗ __**Nothing Is Playing To Paused!**__")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("⏸ __**Paused! Use `/resume` To Resume.**__")


@Client.on_message(filters.command(["cresume","cresume@Ichigotest_Bot"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def resume(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return    
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ __**Nothing Is Paused To Resume!**__")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("▶️ __**Resumed! Use `/pause` To Pause.**__")


@Client.on_message(filters.command(["cstop","cstop@Ichigotest_Bot"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return    
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ __**Nothing Is Streaming To Stop!**__")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹ __**Stopped & Left From Voice Chat!**__")


@Client.on_message(filters.command(["cskip","cskip@Ichigotest_Bot"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return    
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ __**Queue Is Empty, Just Like Your Life!**__")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"⏭ __**Skipped:**__ `{skip[0]}`\n- Now Playing: `{qeue[0][0]}`")


@Client.on_message(filters.command(["cadmincache","admincache@Ichigotest_Bot"]))
@errors
async def admincache(client, message: Message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("❌ __**Chat Is Not Linked!**__")
      return
    set(
        chid,
        [
            member.user
            for member in await conchat.linked_chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ `Admin Cache Refreshed!`")
