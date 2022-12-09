# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import aiohttp
from pyrogram import filters

from GalaxiaRobot import BOT_USERNAME, pbot
from GalaxiaRobot.utils.errors import capture_err

__mod_name__ = "Github"


@pbot.on_message(filters.command(["github", "git", f"git@{BOT_USERNAME}"]))
@capture_err
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("/git KingAbishnoi ")
        return
    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404 ɢᴀᴅᴜ ")

            result = await request.json()
            try:
                url = result["html_url"]
                name = result["name"]
                company = result["company"]
                bio = result["bio"]
                created_at = result["created_at"]
                avatar_url = result["avatar_url"]
                blog = result["blog"]
                location = result["location"]
                repositories = result["public_repos"]
                followers = result["followers"]
                following = result["following"]
                caption = f"""**Info Of {name}**
**ᴜꜱᴇʀɴᴀᴍᴇ:** `{username}`
**ʙɪᴏ:** `{bio}`
**ᴘʀᴏғɪʟᴇ ʟɪɴᴋ:** [Here]({url})
**ᴄᴏᴍᴘᴀɴʏ:** `{company}`
**ᴄʀᴇᴀᴛᴇᴅ ᴏɴ:** `{created_at}`
**ʀᴇᴘᴏꜱɪᴛᴏʀɪᴇꜱ:** `{repositories}` ᴘᴜʙʟɪᴄ
**ʙʟᴏɢ:** `{blog}`
**ʟᴏᴄᴀᴛɪᴏɴ:** `{location}`
**ғᴏʟʟᴏᴡᴇʀꜱ:** `{followers}`
**ғᴏʟʟᴏᴡɪɴɢ:** `{following}`"""
            except Exception as e:
                print(str(e))
    await message.reply_photo(photo=avatar_url, caption=caption)
