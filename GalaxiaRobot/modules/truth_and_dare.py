# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import requests

from GalaxiaRobot import SUPPORT_CHAT
from GalaxiaRobot.events import register as ashok


@ashok(pattern="[/!]dare")
async def _(rj):
    try:
        resp = requests.get("https://api.truthordarebot.xyz/v1/dare").json()
        results = f"{resp['question']}"
        return await rj.reply(results)
    except Exception:
        await rj.reply(f"ᴇʀʀᴏʀ ʀᴇᴘᴏʀᴛ @{SUPPORT_CHAT}")


@ashok(pattern="[/!]truth")
async def _(rj):
    try:
        resp = requests.get("https://api.truthordarebot.xyz/v1/truth").json()
        results = f"{resp['question']}"
        return await rj.reply(results)
    except Exception:
        await rj.reply(f"ᴇʀʀᴏʀ ʀᴇᴘᴏʀᴛ @{SUPPORT_CHAT}")



__mod_name__ = "𝚃ʀᴜᴛʜ 🔹"

__help__ = """
*ᴛʀᴜᴛʜ & ᴅᴀʀᴇ*
 ❍ /truth *:* sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴛʀᴜᴛʜ sᴛʀɪɴɢ.
 ❍ /dare *:* sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴅᴀʀᴇ sᴛʀɪɴɢ.
"""
