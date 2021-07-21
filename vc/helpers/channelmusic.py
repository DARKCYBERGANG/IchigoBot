from pyrogram.types import Chat


def get_chat_id(chat: Chat):
    if chat.title.startswith("Stream Music: ") and chat.title[15:].isnumeric():
        return int(chat.title[14:])
    return chat.id
