# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


from pyrogram import filters

from GalaxiaRobot import arq
from GalaxiaRobot import pbot as app
from GalaxiaRobot.utils.errors import capture_err

__mod_name__ = "Reddit"


@app.on_message(filters.command("reddit"))
@capture_err
async def reddit(_, message):
    if len(message.command) != 2:
        return await message.reply_text("/reddit ɴᴇᴇᴅꜱ ᴀɴ ᴀʀɢᴜᴍᴇɴᴛ")
    subreddit = message.text.split(None, 1)[1]
    m = await message.reply_text("ꜱᴇᴀʀᴄʜɪɴɢ..")
    reddit = await arq.reddit(subreddit)
    if not reddit.ok:
        return await m.edit(reddit.result)
    reddit = reddit.result
    nsfw = reddit.nsfw
    sreddit = reddit.subreddit
    title = reddit.title
    image = reddit.url
    link = reddit.postLink
    if nsfw:
        return await m.edit("ɴꜱғᴡ ʀᴇꜱᴜʟᴛꜱ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ꜱʜᴏᴡɴ.")
    caption = f"""
**ᴛɪᴛʟᴇ:** `{title}`
**ꜱᴜʙʀᴇᴅᴅɪᴛ:** {sreddit}
**ᴘᴏꜱᴛʟɪɴᴋ:** {link}"""
    try:
        await message.reply_photo(photo=image, caption=caption)
        await m.delete()
    except Exception as e:
        await m.edit(e.MESSAGE)
