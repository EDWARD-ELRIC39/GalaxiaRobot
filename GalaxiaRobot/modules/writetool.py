# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from GalaxiaRobot import dispatcher
from GalaxiaRobot import pbot as loda


@loda.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        name = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1].replace(" ", "%20")
        )
        m = await loda.send_message(
            message.chat.id, "**ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n\nʟᴇᴍᴍᴇ ᴡʀɪᴛᴇ ɪᴛ ᴏɴ ᴍʏ ᴄᴏᴩʏ..."
        )
        photo = "https://apis.xditya.me/write?text=" + name
        caption = f"""
sᴜᴄᴄᴇssғᴜʟʟʏ ᴡʀɪᴛᴛᴇɴ ᴛᴇxᴛ 💘

✨ **ᴡʀɪᴛᴛᴇɴ ʙʏ :** [{dispatcher.bot.first_name}](https://t.me/{dispatcher.bot.username})
🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {message.from_user.mention}
"""
        await loda.send_photo(
            message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="💞 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 💞",
                            url="https://t.me/{fuck}?startgroup=new",
                        )
                    ]
                ]
            ),
        )
        await m.delete()
    else:
        lol = message.reply_to_message.text
        name = lol.split(None, 0)[0].replace(" ", "%20")
        m = await loda.send_message(
            message.chat.id, "**ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n\nʟᴇᴍᴍᴇ ᴡʀɪᴛᴇ ɪᴛ ᴏɴ ᴍʏ ᴄᴏᴩʏ..."
        )
        photo = "https://apis.xditya.me/write?text=" + name
        caption = f"""
sᴜᴄᴄᴇssғᴜʟʟʏ ᴡʀɪᴛᴛᴇɴ ᴛᴇxᴛ 💘

✨ **ᴡʀɪᴛᴛᴇɴ ʙʏ :** [{dispatcher.bot.first_name}](https://t.me/{dispatcher.bot.username})
🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {message.from_user.mention}
"""
        await loda.send_photo(
            message.chat.id,
            photo=photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="💞 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 💞",
                            url="https://t.me/{fuck}?startgroup=new",
                        )
                    ]
                ]
            ),
        )
        await m.delete()


__mod_name__ = "𝚆ʀɪᴛᴇ ️🖊️"

__help__ = """
/write  *:* » ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴡʀɪᴛᴇ ɪᴛ ᴏɴ ᴍʏ ᴄᴏᴩʏ...
"""
