# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


from pyrogram import filters
from pyrogram.types import Message

from GalaxiaRobot import pbot as app
from GalaxiaRobot.utils.errors import capture_err

__mod_name__ = "Webshot​"


@app.on_message(filters.command("webss"))
@capture_err
async def take_ss(_, message: Message):
    try:
        if len(message.command) != 2:
            return await message.reply_text("ɢɪᴠᴇ ᴀ ᴜʀʟ ᴛᴏ ғᴇᴛᴄʜ sᴄʀᴇᴇɴsʜᴏᴛ.")
        url = message.text.split(None, 1)[1]
        m = await message.reply_text("**ᴛᴀᴋɪɴɢ sᴄʀᴇᴇɴsʜᴏᴛ**")
        await m.edit("**ᴜᴘʟᴏᴀᴅɪɴɢ**")
        try:
            await message.reply_photo(
                photo=f"https://webshot.amanoteam.com/print?q={url}",
                quote=False,
            )
        except TypeError:
            return await m.edit(" ɴᴏ sᴜᴄʜ ᴡᴇʙsɪᴛᴇ. ")
        await m.delete()
    except Exception as e:
        await message.reply_text(str(e))
