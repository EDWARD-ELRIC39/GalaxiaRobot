# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


from geopy.geocoders import Nominatim
from telethon import *
from telethon.tl import *

from GalaxiaRobot import *
from GalaxiaRobot import telethn as tbot
from GalaxiaRobot.events import register

GMAPS_LOC = "https://maps.googleapis.com/maps/api/geocode/json"


@register(pattern="^/gps (.*)")
async def _(event):
    args = event.pattern_match.group(1)

    try:
        geolocator = Nominatim(user_agent="SkittBot")
        location = args
        geoloc = geolocator.geocode(location)
        longitude = geoloc.longitude
        latitude = geoloc.latitude
        gm = "https://www.google.com/maps/search/{},{}".format(latitude, longitude)
        await tbot.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(
                types.InputGeoPoint(float(latitude), float(longitude))
            ),
        )
        await event.reply(
            "Oᴘᴇɴ ᴡɪᴛʜ : [🌏Gᴏᴏɢʟᴇ ᴍᴀᴘs]({})".format(gm),
            link_preview=False,
        )
    except Exception as e:
        print(e)
        await event.reply("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ")


__mod_name__ = "𝙶ᴘꜱ 🗺️ "

__help__ = """
*ᴜꜱᴇʀ ᴄᴏᴍᴍᴀɴᴅꜱ*
•➥ /gps *:*  ɢᴘꜱ

"""

