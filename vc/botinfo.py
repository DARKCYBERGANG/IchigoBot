from Ichigo import LOG_GRP
from pyrogram import Client
BOT_ID = 0
BOT_NAME = ""

async def get_info(Client):
    global BOT_ID, BOT_NAME
    getme = await Client.get_me()
    BOT_ID = getme.id
    try:
        await Client.send_message(LOG_GRP, text=f"{BOT_NAME} Started!")
    except:
        pass
