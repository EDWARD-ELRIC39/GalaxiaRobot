import os
import re

import aiofiles
from pyrogram import filters

from GalaxiaRobot import pbot as app
from GalaxiaRobot.pyroerror import capture_err
from GalaxiaRobot.utils.keyboard import ikb
from GalaxiaRobot.utils.pastebin import paste

__mod_name__ = "Paste"

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@app.on_message(filters.command("paste"))
@capture_err
async def paste_func(_, message):
    if not message.reply_to_message:
        return await message.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ `/paste`")
    r = message.reply_to_message

    if not r.text and not r.document:
        return await message.reply("ᴏɴʟʏ ᴛᴇxᴛ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛꜱ ᴀʀᴇ ꜱᴜᴘᴘᴏʀᴛᴇᴅ.")

    m = await message.reply("ᴘᴀꜱᴛɪɴɢ...")

    a = (await app.get_me()).mention

    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit("ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴘᴀꜱᴛᴇ ғɪʟᴇꜱ ꜱᴍᴀʟʟᴇʀ ᴛʜᴀɴ 40ᴋʙ.")
        if not pattern.search(r.document.mime_type):
            return await m.edit("ᴏɴʟʏ ᴛᴇxᴛ ғɪʟᴇꜱ ᴄᴀɴ ʙᴇ ᴘᴀꜱᴛᴇᴅ.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)

    link = await paste(content)
    kb = ikb({"•ᴘᴀꜱᴛᴇ ʟɪɴᴋ•": link})
    caption = (f"➥\nᴄʀᴇᴀᴛᴇᴅ ʙʏ: [ᴀʙɢ ✘ ʀᴏʙᴏᴛ ](https://t.me/Abishnoi_ro_bot)",)
    try:
        await message.reply_photo(
            caption,
            photo=link,
            quote=False,
            reply_markup=kb,
        )
    except Exception:
        await message.reply(
            f"➥ʀᴇϙᴜᴇꜱᴛ ʙʏ {message.from_user.mention} \n\n➥ᴘᴀꜱᴛᴇ ʙʏ {a} ",
            reply_markup=kb,
        )
    await m.delete()
