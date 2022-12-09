import asyncio
import random
from sys import version_info

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver

from GalaxiaRobot import OWNER_USERNAME, SUPPORT_CHAT, pbot, BOT_USERNAME as abishnoi

PHOTO = [
    "https://telegra.ph/file/47f1c6b57321808e9eb61.jpg",
    "https://telegra.ph/file/d2433e011fb8eff1650f8.mp4",
    "https://telegra.ph/file/4af05a90d3058915d20e6.jpg",
    "https://telegra.ph/file/a0a79755bc3336f47a30b.jpg",
    "https://telegra.ph/file/c35acfb3cd4699c7a9e2c.jpg",
]

NOOBXD = [
    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ", url=f"https://t.me/Abishnoi_bots"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
            url=f"https://t.me/{abishnoi}?startgroup=true",
        ),
    ],
]


@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("⚡")
    await asyncio.sleep(1)
    await accha.edit("ᴀʟɪᴠɪɴɢ..")
    await asyncio.sleep(0.1)
    await accha.edit("ᴀʟɪᴠɪɴɢ ʙᴀʙʏ ....")
    await accha.delete()
    await asyncio.sleep(0.1)
    umm = await m.reply_sticker(
        "CAACAgUAAx0CUgguZAACdL9iuTsITX6x0Z7kSMhZ_2IeIBlmewAC8gUAAnEhyFVGFPeLco2P_x4E"
    )

    await asyncio.sleep(0.1)
    await m.reply_photo(
        random.choice(PHOTO),
        caption=f"""**ʜᴇʏ {m.from_user.mention},

     ▱▱▱▱▱▱▱▱▱▱▱▱
» **ᴍʏ ᴏᴡɴᴇʀ :** [ᴄʟɪᴄᴋ ᴍᴇ](https://t.me/{OWNER_USERNAME})
» **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{lver}`
» **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tver}`
» **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pver}`
» **ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{version_info[0]}.{version_info[1]}.{version_info[2]}`
⍟ **ʙᴏᴛ ᴠᴇʀꜱɪᴏɴ :** `2.0`
     ▱▱▱▱▱▱▱▱▱▱▱▱""",
        reply_markup=InlineKeyboardMarkup(NOOBXD),
    )
