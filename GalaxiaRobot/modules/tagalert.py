# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

from datetime import timedelta

import dateparser
from pymongo import MongoClient
from pyrogram import filters
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from GalaxiaRobot import MONGO_DB_URI
from GalaxiaRobot import pbot as Galaxia

client = MongoClient(MONGO_DB_URI)
dbd = client["ashau"]
approved_users = dbd.approve
db = dbd

tagdb = db.tagdb1
alarms = db.alarm
shedule = db.shedule
nightmod = db.nightmode4


def get_info(id):
    return nightmod.find_one({"id": id})


@Galaxia.on_message(filters.command(["tagalert"]) & filters.private)
async def locks_dfunc(_, message):
    lol = await message.reply("ᴘʀᴏᴄᴇꜱꜱɪɴɢ..")
    if len(message.command) != 2:
        return await lol.edit("ᴇxᴘᴇᴄᴛᴇᴅ ᴏɴ ᴏʀ ᴏғғ 👀")
    parameter = message.text.strip().split(None, 1)[1].lower()

    if parameter == "on" or parameter == "ON":
        if not message.from_user:
            return
        if not message.from_user.username:
            return await lol.edit(
                "ᴏɴʟʏ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ᴜꜱᴇʀɴᴀᴍᴇꜱ ᴀʀᴇ ᴇʟɪɢɪʙʟᴇ ғᴏʀ ᴛᴀɢ ᴀʟᴇʀᴛ ꜱᴇʀᴠɪᴄᴇ"
            )
        uname = str(message.from_user.username)
        uname = uname.lower()
        isittrue = tagdb.find_one({f"teg": uname})
        if not isittrue:
            tagdb.insert_one({f"teg": uname})
            return await lol.edit(
                f"ᴛᴀɢ ᴀʟᴇʀᴛꜱ ᴇɴᴀʙʟᴇᴅ.\nWhen ꜱᴏᴍᴇᴏɴᴇ ᴛᴀɢꜱ ʏᴏᴜ ᴀꜱ @{uname} ʏᴏᴜ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪғɪᴇᴅ"
            )
        else:
            return await lol.edit("ᴛᴀɢ ᴀʟᴇʀᴛꜱ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ ғᴏʀ ʏᴏᴜ")
    if parameter == "off" or parameter == "OFF":
        if not message.from_user:
            return
        if not message.from_user.username:
            return await lol.edit(
                "ᴏɴʟʏ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ᴜꜱᴇʀɴᴀᴍᴇꜱ ᴀʀᴇ ᴇʟɪɢɪʙʟᴇ ғᴏʀ ᴛᴀɢ ᴀʟᴇʀᴛ ꜱᴇʀᴠɪᴄᴇ"
            )
        uname = message.from_user.username
        uname = uname.lower()
        isittrue = tagdb.find_one({f"teg": uname})
        if isittrue:
            tagdb.delete_one({f"teg": uname})
            return await lol.edit("ᴛᴀɢ ᴀʟᴇʀᴛꜱ ʀᴇᴍᴏᴠᴇᴅ")
        else:
            return await lol.edit("ᴛᴀɢ ᴀʟᴇʀᴛꜱ ᴀʟʀᴇᴀᴅʏ ᴅɪꜱᴀʙʟᴇᴅ ғᴏʀ ʏᴏᴜ")
    else:
        await lol.edit("ᴇxᴘᴇᴄᴛᴇᴅ ᴏɴ ᴏʀ ᴏғғ 👀")


@Galaxia.on_message(filters.incoming)
async def mentioned_alert(client, message):
    try:
        if not message:
            message.continue_propagation()
            return
        if not message.from_user:
            message.continue_propagation()
            return
        input_str = message.text
        input_str = input_str.lower()
        if "@" in input_str:

            input_str = input_str.replace("@", "  |")
            inuka = input_str.split("|")[1]
            text = inuka.split()[0]
        else:
            chats = alarms.find({})
            for c in chats:
                # print(c)
                chat = c["chat"]
                user = c["user"]
                time = c["time"]
                zone = c["zone"]
                reason = c["reason"]
                present = dateparser.parse(
                    f"now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
                )
                ttime = dateparser.parse(f"{time}", settings={"TIMEZONE": f"{zone}"})
                # print(ttime)
                # print(present)
                # print (zone)
                # print(present>=ttime)
                if present > ttime:
                    try:
                        alarms.delete_one(
                            {
                                "chat": chat,
                                "user": user,
                                "time": time,
                                "zone": zone,
                                "reason": reason,
                            }
                        )
                        await client.send_message(
                            chat,
                            f"**🚨 ʀᴇᴍɪɴᴅᴇʀ 🚨**\n\n__ᴛʜɪꜱ ɪꜱ ᴀ ʀᴇᴍɪɴᴅᴇʀ ꜱᴇᴛ ʙʏ__ {user}\n__ʀᴇᴀꜱᴏɴ__: {reason} \n\n`ʀᴇᴍɪɴᴅᴇᴅ ᴀᴛ: {ttime}`",
                        )

                        message.continue_propagation()
                    except:
                        alarms.delete_one(
                            {
                                "chat": chat,
                                "user": user,
                                "time": time,
                                "zone": zone,
                                "reason": reason,
                            }
                        )
                        return message.continue_propagation()
                    break
                    return message.continue_propagation()
                continue
            chats = shedule.find({})
            for c in chats:
                # print(c)
                chat = c["chat"]
                user = c["user"]
                time = c["time"]
                zone = c["zone"]
                reason = c["reason"]
                present = dateparser.parse(
                    f"now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
                )
                ttime = dateparser.parse(f"{time}", settings={"TIMEZONE": f"{zone}"})
                # print(ttime)alarms
                # print(present)
                # print (zone)
                # print(present>=ttime)
                if present > ttime:
                    try:
                        shedule.delete_one(
                            {
                                "chat": chat,
                                "user": user,
                                "time": time,
                                "zone": zone,
                                "reason": reason,
                            }
                        )
                        await client.send_message(chat, f"{reason}")
                        message.continue_propagation()
                    except:
                        shedule.delete_one(
                            {
                                "chat": chat,
                                "user": user,
                                "time": time,
                                "zone": zone,
                                "reason": reason,
                            }
                        )
                        return message.continue_propagation()
                    break
                    return message.continue_propagation()
                continue
            chats = nightmod.find({})

            for c in chats:
                # print(c)
                id = c["id"]
                valid = c["valid"]
                zone = c["zone"]
                c["ctime"]
                otime = c["otime"]
                present = dateparser.parse(
                    "now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
                )
                try:
                    if present > otime and valid:
                        newtime = otime + timedelta(days=1)
                        to_check = get_info(id=id)
                        if not to_check:
                            return message.continue_propagation()
                        if not newtime:
                            return message.continue_propagation()
                        # print(newtime)
                        # print(to_check)
                        nightmod.update_one(
                            {
                                "_id": to_check["_id"],
                                "id": to_check["id"],
                                "valid": to_check["valid"],
                                "zone": to_check["zone"],
                                "ctime": to_check["ctime"],
                                "otime": to_check["otime"],
                            },
                            {"$set": {"otime": newtime}},
                        )
                        await client.set_chat_permissions(
                            id,
                            ChatPermissions(
                                can_send_messages=True,
                                can_send_media_messages=True,
                                can_send_stickers=True,
                                can_send_animations=True,
                            ),
                        )

                        await client.send_message(
                            id,
                            "**🌗 ɴɪɢʜᴛ ᴍᴏᴅᴇ ᴇɴᴅᴇᴅ: `ᴄʜᴀᴛ ᴏᴘᴇɴɪɴɢ` \n\n ᴇᴠᴇʀʏᴏɴᴇ ꜱʜᴏᴜʟᴅ ʙᴇ ᴀʙʟᴇ ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇꜱ.**",
                        )
                        message.continue_propagation()
                        break
                        return message.continue_propagation()
                except:
                    print("Chat open error in nightbot")
                    return message.continue_propagation()
                continue
            chats = nightmod.find({})
            for c in chats:
                # print(c)
                id = c["id"]
                valid = c["valid"]
                zone = c["zone"]
                ctime = c["ctime"]
                c["otime"]
                c["otime"]
                present = dateparser.parse(
                    "now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
                )
                try:
                    if present > ctime and valid:
                        newtime = ctime + timedelta(days=1)
                        to_check = get_info(id=id)
                        if not to_check:
                            return message.continue_propagation()
                        if not newtime:
                            return message.continue_propagation()
                        # print(newtime)
                        # print(to_check)
                        nightmod.update_one(
                            {
                                "_id": to_check["_id"],
                                "id": to_check["id"],
                                "valid": to_check["valid"],
                                "zone": to_check["zone"],
                                "ctime": to_check["ctime"],
                                "otime": to_check["otime"],
                            },
                            {"$set": {"ctime": newtime}},
                        )
                        await client.set_chat_permissions(id, ChatPermissions())
                        await client.send_message(
                            id,
                            "**🌗ɴɪɢʜᴛ ᴍᴏᴅᴇ ꜱᴛᴀʀᴛɪɴɢ: `ᴄʜᴀᴛ ᴄʟᴏꜱᴇ ɪɴɪᴛɪᴀᴛᴇᴅ`\n\nᴏɴʟʏ ᴀᴅᴍɪɴꜱ ꜱʜᴏᴜʟᴅ ʙᴇ ᴀʙʟᴇ ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇꜱ**",
                        )
                        message.continue_propagation()
                        break
                        return message.continue_propagation()
                except:
                    print("Chat close err")
                    return message.continue_propagation()
                continue
            return message.continue_propagation()
        # print(text)
        if tagdb.find_one({f"teg": text}):
            pass
        else:
            return message.continue_propagation()
        # print("Im inn")
        try:
            chat_name = message.chat.title
            message.chat.id
            tagged_msg_link = message.link
        except:
            return message.continue_propagation()
        user_ = message.from_user.mention or f"@{message.from_user.username}"

        final_tagged_msg = f"**🔔 ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ** [ᴛᴀɢɢᴇᴅ]({tagged_msg_link}) **ɪɴ** {chat_name} **ʙʏ** {user_}"
        button_s = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔔 ᴠɪᴇᴡ ᴍᴇꜱꜱᴀɢᴇ 🔔", url=tagged_msg_link)]]
        )
        # print(final_tagged_msg)
        try:
            await client.send_message(
                chat_id=f"{text}",
                text=final_tagged_msg,
                reply_markup=button_s,
                disable_web_page_preview=True,
            )

        except:
            return message.continue_propagation()
        message.continue_propagation()
    except:
        return message.continue_propagation()



__mod_name__ = "𝚃ᴀɢs 📯"


__help__ = """
**─「 ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ғᴜɴᴄᴛɪᴏɴ 」─**

*ᴀꜱᴜx ᴄᴀɴ ʙᴇ ᴀ ᴍᴇɴᴛɪᴏɴ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ɢʀᴏᴜᴘ.*
*ᴏɴʟʏ ᴀᴅᴍɪɴꜱ can ᴛᴀɢ all.  ʜᴇʀᴇ ɪꜱ ᴀ ʟɪꜱᴛ ᴏғ ᴄᴏᴍᴍᴀɴᴅꜱ*

➥ /tagall or @all (ʀᴇᴘʟʏ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ ᴏʀ ᴀᴅᴅ ᴀɴᴏᴛʜᴇʀ ᴍᴇꜱꜱᴀɢᴇ) ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ, ᴡɪᴛʜᴏᴜᴛ ᴇxᴄᴇᴘᴛɪᴏɴ.

➥ /cancel : ғᴏʀ ᴄᴀɴᴄᴇʟɪɴɢ ᴛʜᴇ ᴍᴇɴᴛɪᴏɴ-ᴀʟʟ .

➥ /tagalert on & off *:* ᴛᴀɢ ɴᴏᴛɪᴄᴇ ʙʏ  ʙᴏᴛ   
   ᴡʜᴇɴ ꜱᴏᴍᴇᴏɴᴇ ᴛᴀɢꜱ ʏᴏᴜ ᴀꜱ @  ʏᴏᴜ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪғɪᴇᴅ [ ᴏɴ & ᴏғғ ɪɴ ᴘᴍ]

"""
