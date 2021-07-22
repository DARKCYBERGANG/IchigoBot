import re
import os
from os import getenv
from youtube_dl import YoutubeDL
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")
    
ydl_opts = {
   "geo-bypass": True,
   "nocheckcertificate": True
   }
ydl = YoutubeDL(ydl_opts)
links=[]
finalurl=""
STREAM=os.environ.get("STREAM_URL", "http://node-25.zeno.fm/kezsc0y2wwzuv?listening-from-radio-garden=1622271954020&rj-ttl=5&rj-tok=AAABec5bAE4Aj31dmRAEFgcbvw")
regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
match = re.match(regex,STREAM)
if match:
    meta = ydl.extract_info(STREAM, download=False)
    formats = meta.get('formats', [meta])
    for f in formats:
        links.append(f['url'])
    finalurl=links[0]
else:
    finalurl=STREAM


que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
STREAM_URL=finalurl
TOKEN = getenv("TOKEN")
BOT_NAME = getenv("BOT_NAME")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "AsmSafone")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/5fed93ca29be49d1a6ed0.png")
admins = {}
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "Ichigo_Assistant")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "SafoTheBot")
PROJECT_NAME = getenv("PROJECT_NAME", "Stream Music Bot")
SOURCE_CODE = getenv("SOURCE_CODE", "github.com/AsmSafone")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "30"))
ARQ_API_KEY = getenv("ARQ_API_KEY", None)
PMPERMIT = getenv("PMPERMIT", None)
LOG_GRP = getenv("LOG_GRP", None)
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
msg = {}
