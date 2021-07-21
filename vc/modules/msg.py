
import os
from vc.config import SOURCE_CODE,ASSISTANT_NAME,PROJECT_NAME,SUPPORT_GROUP,UPDATES_CHANNEL

class Messages():
      START_MSG = f"👋🏻 **Hello**,\n\nI'm **{PROJECT_NAME}** 🎵\nI Can Stream Music In Voice Chats of Telegeam Groups & Channels. I Have A Lot's of Cool Features That Will Definately Amaze You! Please Checkout /help To Know How Stream Music 😉! \n\n**Made With ❤️ By @riderprovider2op** 👑"
      HELP_MSG = [
        ".",
f"""
Hello Dear 😇! 
**Welcome Back!!**
{PROJECT_NAME} Can Play Music In Your Group's Voice Chat As Well As Channel Voice Chats. It Have A Lot's of Cool Features That Will Definately Amaze You! Please Go Through The Tutorial To Learn More!!
""",

f"""
🏷 --**Setting Up**--
1) Make me an admin
2) Start the voice chat
3) Try /play [song name] for the first time by an admin in group
*) If userbot joined enjoy music, If not add @{ASSISTANT_NAME} to your group and retry
🏷 --**Song Playing**--
- /play [song name]: Play the requestd song
- /play [yt url]: Play the given yt url
- /play [reply to audio]: Play replied audio
🏷 --**Song Playback**--
- /skip: Skip the current track
- /pause: Pause the current track
- /resume: Resume the paused track
- /stop: Stop song/music playback
- /settings: Open settings menu of player
- /current: Shows the current playing track
- /playlist: Shows playlist of the chat
""",
        
f"""
🏷 --**Setting Up Channel**--
1) Make me admin of your channel 
2) Send /ubjoinchannel in linked group
3) Now send commands in channel linked group
🏷 --**Linked Channel Playback**--
- /cplay [song name]: Play the requested song
- /cplaylist: Shows channel playlist
- /ccurrent: Shows the current track
- /csettings: Open settings menu of player
- /cpause: Pause the current track
- /cresume: Resume the current track
- /cskip: Skip the current track
- /cstop: Stop channel music playing
- /ubcjoin: Invite assistant to your chat
🏷 --**Don't Like Linking Group**--
1) Get your channel ID
2) Create a group with tittle: `Stream Music: your_channel_id`
3) Add bot as Channel admin with full permissions
4) Add @{ASSISTANT_NAME} to the channel as an admin
5) Simply send commands in your newly created group
""",

f"""
🏷 --**More Tools**--
- /musicplayer [on/off]: Enable/Disable music player
- /admincache: Updates admin info of your group. Try if bot isn't recognize admin
- /ubjoin: Invite @{ASSISTANT_NAME} userbot to your chat
🏷 --**Song Download**--
- /song [song name]: Download audio song from youtube
- /saavn [song name]: Download song from saavn
- /deezer [song name]: Download song from deezer
- /video [song mame]: Download video song from youtube
🏷 --**For Sudo Users**--
 - /reload: Update sudo users info of the bot
 - /ubleaveall - Remove assistant from all chats
 - /broadcast [reply to message] - Broadcast replied message to all chats
 - /pmpermit [on/off] - Enable/Disable pmpermit message
"""
      ]
