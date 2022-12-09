import re

import aiohttp
import emoji
from googletrans import Translator as google_translator
from pyrogram import filters

from GalaxiaRobot import BOT_ID
from GalaxiaRobot import BOT_USERNAME as bu
from GalaxiaRobot import arq, pbot
from GalaxiaRobot.utils.pluginhelper import admins_only, edit_or_reply

url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"

translator = google_translator()


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI response Timeout")
        return


ewe_chats = []
en_chats = []


@pbot.on_message(
    filters.command(["talkbot", f"talkbot@{bu}"]) & ~filters.bot & ~filters.private
)
@admins_only
async def hmm(_, message):
    global ewe_chats
    if len(message.command) != 2:
        await message.reply_text("ɪ ᴏɴʟʏ ʀᴇᴄᴏɢɴɪᴢᴇ /talkbot ᴏɴ ᴀɴᴅ /talkbot ᴏғғ ᴏɴʟʏ")
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await edit_or_reply(message, "`Processing...`")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("ᴀʙɢ ᴀɪ ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ")
            return
        await lel.edit(
            f"ᴀʙɢ ᴀɪ ᴀᴄᴛɪᴠᴇᴅ ʙʏ {message.from_user.mention()} ғᴏʀ ᴜꜱᴇʀꜱ ɪɴ {message.chat.title}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await edit_or_reply(message, "`ᴘʀᴏᴄᴇꜱꜱɪɴɢ...`")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("ᴀʙɢ ᴀ:ɪ ᴡᴀꜱ ɴᴏᴛ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ")
            return
        await lel.edit(
            f"ᴀʙɢ ᴀɪ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙʏ {message.from_user.mention()} ғᴏʀ ᴜꜱᴇʀꜱ ɪɴ {message.chat.title}"
        )

    elif status == "EN" or status == "en" or status == "english":
        if not chat_id in en_chats:
            en_chats.append(chat_id)
            await message.reply_text(
                f"ᴇɴɢʟɪꜱʜ ᴀɪ ᴄʜᴀᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ {message.from_user.mention()}"
            )
            return
        await message.reply_text(
            f"ᴇɴɢʟɪꜱʜ ᴀɪ ᴄʜᴀᴛ ᴅɪꜱᴀʙʟᴇᴅ ʙʏ {message.from_user.mention()}"
        )
        message.continue_propagation()
    else:
        await message.reply_text(
            "ɪ ᴏɴʟʏ ʀᴇᴄᴏɢɴɪᴢᴇ `/talkbot ᴏɴ` ᴀɴᴅ `talkbot off` ᴏɴʟʏ"
        )


@pbot.on_message(
    filters.text & filters.reply & ~filters.bot & ~filters.via_bot & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("ABG", "Aco")
        test = test.replace("ABG", "Aco")
        test = test.replace("My Owner Is @Abishnoi1M", "I'm ABG")
        test = test.replace("16", "9")
        test = test.replace("@Abishnoi1M is my love.", "I'm single.")
        test = test.replace("My love is @Abishnoi1M", "I'm single.")
        test = test.replace("@Abishnoi_bots", "@Abishnoi")
        test = test.replace("I live in @Abishnoi_bots.", "I live in Your heart ❤️.")
        test = test.replace("I was created by @Abishnoi1M", "I made myself")
        test = test.replace(
            "Hello there I am ABG...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?",
        )
        test = test.replace("@Abishnoi1M is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is ABG Nice to meet you.",
            "Hi, my friend, what can I do for you today?",
        )
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "ABG")
        response = response.replace("aco", "ABG")
        response = response.replace("Luna", "ABG")
        response = response.replace("luna", "ABG")
        response = response.replace("I'm a ABG", "My love is @Abishnoi1M")
        response = response.replace("9", "16")
        response = response.replace(
            "I'm married to my job.", "I'm married with @Abishnoi1M"
        )
        response = response.replace("I'm single.", "My love 😍 is @Abishnoi1M")
        response = response.replace("@Abishnoi", "@Abishnoi_bots")
        response = response.replace(
            "I live in your heart ❤.", "I live in @Abishnoi_bots."
        )
        response = response.replace("I made myself", "I was Created by @Abishnoi1M")
        response = response.replace(
            "Hi, my friend! Do you want me to tell you a joke?",
            "Hello there I am ABG...nice to meet u",
        )
        response = response.replace(
            "Have the control right.", "@Abishnoi1M is my owner."
        )
        response = response.replace(
            "Hi, my friend, what can I do for you today?",
            "Hi, My name is ABG Nice to meet you",
        )
        response = response.replace("Bc ", "Bc , nai vc hota h")

        pro = response
        try:
            await pbot.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return

    else:
        u = msg.split()
        emj = extract_emojis(msg)
        msg = msg.replace(emj, "")
        if (
            [(k) for k in u if k.startswith("@")]
            and [(k) for k in u if k.startswith("#")]
            and [(k) for k in u if k.startswith("/")]
            and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
        ):

            h = " ".join(filter(lambda x: x[0] != "@", u))
            km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
            tm = km.split()
            jm = " ".join(filter(lambda x: x[0] != "#", tm))
            hm = jm.split()
            rm = " ".join(filter(lambda x: x[0] != "/", hm))
        elif [(k) for k in u if k.startswith("@")]:

            rm = " ".join(filter(lambda x: x[0] != "@", u))
        elif [(k) for k in u if k.startswith("#")]:
            rm = " ".join(filter(lambda x: x[0] != "#", u))
        elif [(k) for k in u if k.startswith("/")]:
            rm = " ".join(filter(lambda x: x[0] != "/", u))
        elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
            rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
        else:
            rm = msg
            # print (rm)
        try:
            lan = translator.detect(rm)
            lan = lan.lang
        except:
            return
        test = rm
        if not "en" in lan and not lan == "":
            try:
                test = translator.translate(test, dest="en")
                test = test.text
            except:
                return
        # test = emoji.demojize(test.strip())

        test = test.replace("ABG", "Aco")
        test = test.replace("ABG", "Aco")
        test = test.replace("My king is @Abishnoi1M", "I'm a ABG")
        test = test.replace("16", "9")
        test = test.replace("@Abishnoi1M is my husband.", "I'm single.")
        test = test.replace("@Abishnoi_bots", "@Abishnoi")
        test = test.replace("I live in @Abishnoi_bots.", "I live in your heart ❤")
        test = test.replace("I was created by @Abishnoi1M", "I made myself")
        test = test.replace(
            "Hello there I am ABG...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?",
        )
        test = test.replace("@Abishnoi1M is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is ABG Nice to meet you.",
            "Hi, my friend, what can I do for you today?",
        )

        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "ABG")
        response = response.replace("aco", "ABG")
        response = response.replace("Luna", "ABG")
        response = response.replace("luna", "ABG")
        response = response.replace("I'm a ABG", "My king is @Abishnoi1M")
        response = response.replace("9", "16")
        response = response.replace(
            "I'm married to my job.", "I'm married with @Abishnoi1M"
        )
        response = response.replace("I'm single.", "My love 😍 is @Abishnoi1M")
        response = response.replace("@Abishnoi", "@Abishnoi_bots")
        response = response.replace(
            "I live in your heart ❤.", "I live in @Abishnoi_bots."
        )
        response = response.replace("I made myself", "I was Created by @Abishnoi1M")
        response = response.replace(
            "Hi, my friend! Do you want me to tell you a joke?",
            "Hello there I am ABG...nice to meet u",
        )
        response = response.replace(
            "Have the control right.", "@Abishnoi1M is my owner."
        )
        response = response.replace(
            "Hi, my friend, what can I do for you today?",
            "Hi, My name is ABG Nice to meet you",
        )
        response = response.replace("Bc ?", "Bc , nai vc hota h ")

        pro = response
        if not "en" in lan and not lan == "":
            try:
                pro = translator.translate(pro, dest=lan)
                pro = pro.text
            except:
                return
        try:
            await pbot.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return


@pbot.on_message(filters.text & filters.private & filters.reply & ~filters.bot)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return
    test = test.replace("ABG", "Aco")
    test = test.replace("ABG", "Aco")
    test = test.replace("My king is @Abishnoi1M", "I'm a ABG")
    test = test.replace("16", "9")
    test = test.replace("@Abishnoi1M is my husband.", "I'm single.")
    test = test.replace("@Abishnoi_bots", "@Abishnoi")
    test = test.replace("I live in @Abishnoi_bots.", "I live in your heart ❤.")
    test = test.replace("I was created by @Abishnoi1M", "I made myself")
    test = test.replace(
        "Hello there I am ABG...nice to meet u",
        "Hi, my friend! Do you want me to tell you a joke?",
    )
    test = test.replace("@Abishnoi1M is my owner", "Have the control right.")
    test = test.replace(
        "Hi, My name is ABG Nice to meet you.",
        "Hi, my friend, what can I do for you today?",
    )
    response = response.replace("Gand mera tu", "Bc")

    response = await lunaQuery(test, message.from_user.id if message.from_user else 0)
    response = response.replace("Aco", "ABG")
    response = response.replace("aco", "ABG")
    response = response.replace("Luna", "ABG")
    response = response.replace("luna", "ABG")
    response = response.replace("I'm a ABG", "My king is @Abishnoi1M")
    response = response.replace("9", "16")
    response = response.replace(
        "I'm married to my job.", "I'm married with @Abishnoi1M"
    )
    response = response.replace("I'm single.", "My love 😍 is @Abishnoi1M")
    response = response.replace("@Abishnoi", "@Abishnoi_bots")
    response = response.replace("I live in your heart ❤.", "I live in @Abishnoi_bots")
    response = response.replace("I made myself", "I was Created by @Abishnoi1M")
    response = response.replace(
        "Hi, my friend! Do you want me to tell you a joke?",
        "Hello there I am ABG...nice to meet u",
    )
    response = response.replace("Have the control right.", "@Abishnoi1M is my owner.")
    response = response.replace(
        "Hi, my friend, what can I do for you today?",
        "Hi, My name is ABG Nice to meet you",
    )
    response = response.replace("Bc?", "Bc nai vc hota h ")

    pro = response
    if not "en" in lan and not lan == "":
        pro = translator.translate(pro, dest=lan)
        pro = pro.text
    try:
        await pbot.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@pbot.on_message(
    filters.regex("ABG|bot|robot|ashok|Abishnoi|bot|bc|chutiya|abg|Robot|asu|")
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.reply
    & ~filters.channel
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return

    # test = emoji.demojize(test.strip())

    test = test.replace("ABG", "Aco")
    test = test.replace("ABG", "Aco")
    test = test.replace("My king is @Abishnoi1M", "I'm a ABG")
    test = test.replace("16", "9")
    test = test.replace("@Abishnoi1M is my husband.", "I'm single.")
    test = test.replace("@Abishnoi_bots", "@Abishnoi")
    test = test.replace("I live in @Abishnoi_bots.", "I live in your heart ❤️.")
    test = test.replace("I was created by @Abishnoi1M", "I made myself")
    test = test.replace(
        "Hello there I am ABG...nice to meet u",
        "Hi, my friend! Do you want me to tell you a joke?",
    )
    test = test.replace("@Abishnoi1M is my owner", "Have the control right.")
    test = test.replace(
        "Hi, My name is ABG Nice to meet you.",
        "Hi, my friend, what can I do for you today?",
    )
    response = await lunaQuery(test, message.from_user.id if message.from_user else 0)
    response = response.replace("Aco", "ABG")
    response = response.replace("aco", "ABG")
    response = response.replace("Luna", "ABG")
    response = response.replace("luna", "ABG")
    response = response.replace("I'm a ABG", "My king is @Abishnoi1M")
    response = response.replace(
        "I'm married to my job.", "I'm married with @Abishnoi1M"
    )
    response = response.replace("9", "16")
    response = response.replace("I'm single.", "My love 😍 is @Abishnoi1M")
    response = response.replace("@Abishnoi", "@Abishnoi_bots")
    response = response.replace("I live in your heart ❤.", "I live in @Abishnoi_bots.")
    response = response.replace("I made myself", "I was Created by @Abishnoi1M")
    response = response.replace(
        "Hi, my friend! Do you want me to tell you a joke?",
        "Hello there I am ABG...nice to meet u",
    )
    response = response.replace("Have the control right.", "@Abishnoi1M is my owner.")
    response = response.replace(
        "Hi, my friend, what can I do for you today?",
        "Hi bro, my name is Abishnoi_ro_bot Nice to meet you",
    )

    pro = response
    if not "en" in lan and not lan == "":
        try:
            pro = translator.translate(pro, dest=lan)
            pro = pro.text
        except Exception:
            return
    try:
        await pbot.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


__mod_name__ = "🗨️  - talkbot"
