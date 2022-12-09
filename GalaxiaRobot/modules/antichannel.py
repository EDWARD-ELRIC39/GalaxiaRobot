# TG  @Abishnoi1M
# GIT:- KingAbishnoi

# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

import asyncio

from pyrogram import filters
from pyrogram.types import Message

from GalaxiaRobot import eor
from GalaxiaRobot import pbot as app
from GalaxiaRobot.utils.errors import capture_err

active_channel = []


async def channel_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = "**ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ `ᴇɴᴀʙʟᴇᴅ` ✅. ɪ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇꜱꜱᴀɢᴇ ᴛʜᴀᴛ ꜱᴇɴᴅ ᴡɪᴛʜ ᴄʜᴀɴɴᴇʟ ɴᴀᴍᴇꜱ. ᴅᴀʀᴇ ᴛᴏ ʟᴇᴀᴘ**🤐"
            return await eor(message, text=text)
        await eor(message, text="ᴀɴᴛɪᴄʜᴀɴɴᴇʟ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.🤫")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await eor(message, text="ᴀɴᴛɪᴄʜᴀɴɴᴇʟ ᴅɪꜱᴀʙʟᴇᴅ!😏")
        await eor(
            message,
            text=f"**ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ** {message.chat.id} ❌",
        )
    else:
        await eor(
            message,
            text="ɪ ᴜɴᴅᴇꜱᴛᴀɴᴅ `/antichannel on` ᴀɴᴅ `/antichannel off` ᴏɴʟʏ ʙᴀʙʏ 😇",
        )


# Enabled | Disable antichannel


@app.on_message(filters.command("antichannel"))
@capture_err
async def antichannel_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(
            message,
            text="ɪ ᴜɴᴅᴇꜱᴛᴀɴᴅ `/antichannel on` ᴀɴᴅ `/antichannel ᴏғғ` ᴏɴʟʏ ʙᴀʙʏ 😙",
        )
    await channel_toggle(active_channel, message)


@app.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
        | filters.text
    )
    & ~filters.private,
    group=41,
)
async def anitchnl(_, message):
    chat_id = message.chat.id
    if message.sender_chat:
        sender = message.sender_chat.id
        if message.chat.id not in active_channel:
            return
        if chat_id == sender:
            return
        else:
            await message.delete()
            ti = await message.reply_text(
                "**A ᴀɴᴛɪ-ᴄʜᴀɴɴᴇʟ ᴍᴇꜱꜱᴀɢᴇ ᴅᴇᴛᴇᴄᴛᴇᴅ. ɪ ᴅᴇʟᴇᴛᴇᴅ ɪᴛ..** ♨️"
            )
            await asyncio.sleep(7)
            await ti.delete()
