# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

from platform import python_version as y

from pyrogram import __version__ as z
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import __version__ as o
from telethon import __version__ as s

from GalaxiaRobot import pbot
from GalaxiaRobot.utils.errors import capture_err
from GalaxiaRobot.utils.functions import make_carbon


@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.`")
    if not message.reply_to_message.text:
        return await message.reply_text("`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.`")
    m = await message.reply_text("`ᴘʀᴇᴘᴀʀɪɴɢ ᴄᴀʀʙᴏɴ`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`ᴜᴘʟᴏᴀᴅɪɴɢ`")
    await pbot.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()


ABISHNOIX = "https://telegra.ph/file/bff9ee4cf39621303e292.jpg"


@pbot.on_message(filters.command("repo"))
async def repo(_, message):
    await message.reply_photo(
        photo=ABISHNOIX,
        caption=f"""✨ **ʜᴇʏ {message.from_user.mention},

**ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{y()}`
**ʟɪʙʀᴀʀʏ ᴠᴇʀꜱɪᴏɴ :** `{o}`
**ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ :** `{s}`
**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀꜱɪᴏɴ :** `{z}`
**ʙᴏᴛ ᴠᴇʀꜱɪᴏɴ:** `2.0`
**ᴇɴᴊᴏʏ**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "•ᴍᴜꜱɪᴄ•", url="https://github.com/Abishnoi69/AsuXMusic"
                    ),
                    InlineKeyboardButton(
                        "•ʀᴏʙᴏᴠ1•", url="https://github.com/Abishnoi69/ExonRobot"
                    ),
                ]
            ]
        ),
    )
