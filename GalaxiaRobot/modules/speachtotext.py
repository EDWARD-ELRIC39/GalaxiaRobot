# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import os
from datetime import datetime

import requests
from telethon import *
from telethon.tl import functions, types
from telethon.tl.types import *

from GalaxiaRobot import *
from GalaxiaRobot import telethn as tbot
from GalaxiaRobot.events import register


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


@register(pattern="^/stt$")
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await event.client.download_media(
            previous_message, TEMP_DOWNLOAD_DIRECTORY
        )
        if IBM_WATSON_CRED_URL is None or IBM_WATSON_CRED_PASSWORD is None:
            await event.reply(
                "ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ꜱᴇᴛ ᴛʜᴇ ʀᴇϙᴜɪʀᴇᴅ ᴇɴᴠ ᴠᴀʀɪᴀʙʟᴇꜱ ғᴏʀ ᴛʜɪꜱ ᴍᴏᴅᴜʟᴇ. \nᴍᴏᴅᴜʟᴇ ꜱᴛᴏᴘᴘɪɴɢ"
            )
        else:
            # await event.reply("Starting analysis")
            headers = {
                "Content-Type": previous_message.media.document.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                IBM_WATSON_CRED_URL + "/v1/recognize",
                headers=headers,
                data=data,
                auth=("apikey", IBM_WATSON_CRED_PASSWORD),
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                transcript_confidence = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + str(alternatives["transcript"])
                    transcript_confidence += (
                        " " + str(alternatives["confidence"]) + " + "
                    )
                end = datetime.now()
                ms = (end - start).seconds
                if transcript_response != "":
                    string_to_show = "ᴛʀᴀɴꜱᴄʀɪᴘᴛ: `{}`\n ᴛɪᴍᴇ ᴛᴀᴋᴇɴ: {} ꜱᴇᴄᴏɴᴅꜱ\n ᴄᴏɴғɪᴅᴇɴᴄᴇ: `{}`".format(
                        transcript_response, ms, transcript_confidence
                    )
                else:
                    string_to_show = "ᴛʀᴀɴꜱᴄʀɪᴘᴛ: `Nil`\n ᴛɪᴍᴇ ᴛᴀᴋᴇɴ: {} ꜱᴇᴄᴏɴᴅꜱ\n\n**ɴᴏ ʀᴇꜱᴜʟᴛꜱ ғᴏᴜɴᴅ**".format(
                        ms
                    )
                await event.reply(string_to_show)
            else:
                await event.reply(r["error"])
            # now, remove the temporary file
            os.remove(required_file_name)
    else:
        await event.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇ, ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴛᴇxᴛ ᴏᴜᴛ ᴏғ ɪᴛ.")


__mod_name__ = "TTS/STT"
