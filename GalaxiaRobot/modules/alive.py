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
    "https://telegra.ph/file/9c0775e5e6deea4b1e6bf.jpg",
    "https://telegra.ph/file/d2433e011fb8eff1650f8.mp4",
    "https://telegra.ph/file/7a93bb9a367fbc030052e.jpg",
    "https://telegra.ph/file/19b3d1eb1aae90dcaf303.jpg",
    "https://telegra.ph/file/8183e618bef12ab9e45dd.jpg",
]

NOOBXD = [
    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ", url=f"https://t.me/GALAXIA_X_UPDATES"),
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
    accha = await m.reply("🦋")
    await asyncio.sleep(1)
    await accha.edit(
        "CAACAgUAAx0CbDw4ugACBnVjqxILieXxSzMFR2qF4D8uDcxRhgACzQcAAlJhWVU1cIXnopdXeSwE.."
    )
    await asyncio.sleep(0.1)
    await accha.edit("Aʟɪᴠɪɴɢ...")
    await accha.delete()
    await asyncio.sleep(0.1)
    await m.reply_sticker("CAADBQADOwgAApqCiVf47RXri2_MrwI")

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
