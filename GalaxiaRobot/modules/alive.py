import asyncio
import random
from sys import version_info

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver

from GalaxiaRobot import BOT_USERNAME as abishnoi
from GalaxiaRobot import OWNER_USERNAME, SUPPORT_CHAT, pbot

PHOTO = [
    "https://telegra.ph/file/8ab162801b5d5cff88fc3.jpg",
    "https://telegra.ph/file/38a95147bb35b2385c26d.jpg",
    "https://telegra.ph/file/02694cf3d19482bcdc50d.jpg",
    "https://telegra.ph/file/768194a9b5ceb4d1d305d.jpg",
    "https://telegra.ph/file/1b126a38ab1ee69e61fef.jpg",
]

NOOBXD = [
    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ", url=f"https://t.me/GALAXIA_X_UPDATES"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="🦋 ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🦋",
            url=f"https://t.me/{abishnoi}?startgroup=true",
        ),
    ],
]


@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("🦋")
    await asyncio.sleep(1)
    await accha.edit("𝑰 𝑳𝒐𝒗𝒆 𝒀𝒐𝒖 🥀💫❤️⚡..")
    await asyncio.sleep(0.1)
    await accha.edit("𝐴𝑙𝑖𝑣𝑖𝑛𝑔 ...")
    await accha.delete()
    await asyncio.sleep(0.1)
    await m.reply_sticker("CAADBQADWgoAAnR2GFQ_zbr6j0ytZAI")

    await asyncio.sleep(0.1)
    await m.reply_photo(
        random.choice(PHOTO),
        caption=f"""**ʜᴇʏ {m.from_user.mention},

     ▱▱▱▱▱▱▱▱▱▱▱▱
⍟ **Mʏ Hᴜʙʙʏ   :** [ᴇᴅᴡᴀʀᴅ ᴇʟʀɪᴄ ](https://t.me/{OWNER_USERNAME})
⍟ **Lɪʙʀᴀʀʏ Vᴇʀsɪᴏɴ  :** `{lver}`
⍟ **Tᴇʟᴇᴛʜᴏɴ Vᴇʀsɪᴏɴ  :** `{tver}`
⍟ **Pʏʀᴏɢʀᴀᴍ Vᴇʀsɪᴏɴ  :** `{pver}`
⍟ **Pʏᴛʜᴏɴ Vᴇʀsɪᴏɴ  :** `{version_info[0]}.{version_info[1]}.{version_info[2]}`
⍟ **Bᴏᴛ Vᴇʀsɪᴏɴ  :** `1.0`
     ▱▱▱▱▱▱▱▱▱▱▱▱""",
        reply_markup=InlineKeyboardMarkup(NOOBXD),
    )
