from config import SESSION_NAME
from config import API_ID
from config import API_HASH
from pyrogram import Client

USER = Client(
    Config.SESSION,
    Config.API_ID,
    Config.API_HASH
)
USER.start()
