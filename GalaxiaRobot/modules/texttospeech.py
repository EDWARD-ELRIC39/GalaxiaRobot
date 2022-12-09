# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import os

from gtts import gTTS, gTTSError

from GalaxiaRobot import telethn as tbot
from GalaxiaRobot.events import register


@register(pattern="^/tts (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.reply(
            "ɪɴᴠᴀʟɪᴅ ꜱʏɴᴛᴀx\n ғᴏʀᴍᴀᴛ `/tts lang | text`\nғᴏʀ eg: `/tts en | hello`"
        )
        return
    text = text.strip()
    lan = lan.strip()
    try:
        tts = gTTS(text, tld="com", lang=lan)
        tts.save("k.mp3")
    except AssertionError:
        await event.reply(
            "ᴛʜᴇ ᴛᴇxᴛ ɪs ᴇᴍᴘᴛʏ.\n"
            "ɴᴏᴛʜɪɴɢ ʟᴇғᴛ ᴛᴏ sᴘᴇᴀᴋ ᴀғᴛᴇʀ ᴘʀᴇ-ᴘʀᴇᴄᴇssɪɴɢ, "
            "ᴛᴏᴋᴇɴɪᴢɪɴɢ ᴀɴᴅ ᴄʟᴇᴀɴɪɴɢ."
        )
        return
    except ValueError:
        await event.reply("ʟᴀɴɢᴜᴀɢᴇ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ.")
        return
    except RuntimeError:
        await event.reply("ᴇʀʀᴏʀ ʟᴏᴀᴅɪɴɢ ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇs ᴅɪᴄᴛɪᴏɴᴀʀʏ.")
        return
    except gTTSError:
        await event.reply("ᴇʀʀᴏʀ ɪɴ ɢᴏᴏɢʟᴇ ᴛᴇxᴛ-ᴛᴏ-sᴘᴇᴇᴄʜ ᴀᴘɪ ʀᴇǫᴜᴇsᴛ !")
        return
    with open("k.mp3", "r"):
        await tbot.send_file(
            event.chat_id, "k.mp3", voice_note=True, reply_to=reply_to_id
        )
        os.remove("k.mp3")
