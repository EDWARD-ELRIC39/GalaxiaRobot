import random
import time

from telegram import MessageEntity
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler

from GalaxiaRobot import REDIS, dispatcher
from GalaxiaRobot.modules.disable import DisableAbleCommandHandler
from GalaxiaRobot.modules.helper_funcs.readable_time import get_readable_time
from GalaxiaRobot.modules.redis.afk_redis import (
    afk_reason,
    end_afk,
    is_user_afk,
    start_afk,
)
from GalaxiaRobot.modules.users import get_user_id

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


def afk(update, context):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user
    if not user:  # ignore channels
        return

    if user.id == 777000:
        return
    start_afk_time = time.time()
    reason = args[1] if len(args) >= 2 else "none"
    start_afk(update.effective_user.id, reason)
    REDIS.set(f"afk_time_{update.effective_user.id}", start_afk_time)
    fname = update.effective_user.first_name
    try:
        update.effective_message.reply_text("{} \nɪꜱ ɴᴏᴡ ᴀᴡᴀʏ!".format(fname))
    except BadRequest:
        pass


def no_longer_afk(update, context):
    user = update.effective_user
    message = update.effective_message
    if not user:  # ignore channels
        return

    if not is_user_afk(user.id):  # Check if user is afk or not
        return
    end_afk_time = get_readable_time(
        (time.time() - float(REDIS.get(f"afk_time_{user.id}")))
    )
    REDIS.delete(f"afk_time_{user.id}")
    res = end_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                "{} ɪꜱ ᴡᴀꜱᴛɪɴɢ ʜɪꜱ ᴛɪᴍᴇ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ!\n\nʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀғᴛᴇʀ {}",
                "ᴛʜᴇ ᴅᴇᴀᴅ {} ᴄᴀᴍᴇ ʙᴀᴄᴋ ғʀᴏᴍ ʜɪꜱ Grave!\n\nᴋɪɴɢ ɪꜱ ʙᴀᴄᴋ ᴀғᴛᴇʀ {}",
                "Welcome back {}! I hope you bought pizza\n\nʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀғᴛᴇʀ {}",
                "ɢᴏᴏᴅ ᴛᴏ ʜᴇᴀʀ ғʀᴏᴍ ʏᴏᴜ ᴀɢᴀɪɴ {}\n\nᴋɪɴɢ ɪꜱ ʙᴀᴄᴋ ᴀғᴛᴇʀ {}",
                "{} ɢᴏᴏᴅ ᴊᴏʙ ᴡᴀᴋɪɴɢ ᴜᴘ ɴᴏᴡ ɢᴇᴛ ʀᴇᴀᴅʏ ғᴏʀ ʏᴏᴜʀ ᴄʟᴀꜱꜱᴇꜱ!\n\nᴀғᴋ ᴇɴᴅ ᴀғᴛᴇʀ {}",
                "ʜᴇʏ {}! ᴡʜʏ ᴡᴇʀᴇɴ ʏᴏᴜ ᴏɴʟɪɴᴇ ғᴏʀ ꜱᴜᴄʜ ᴀ ʟᴏɴɢ ᴛɪᴍᴇ?\n\nᴀғᴛᴇʀ {}",
                "{} ᴡʜʏ ᴅɪᴅ ʏᴏᴜ ᴄᴀᴍᴇ ʙᴀᴄᴋ?\n\nʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀғᴛᴇʀ {}",
                "{} Is ɴᴏᴡ ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!\n\nɴᴏᴡ ᴏɴʟɪɴᴇ ʙᴀᴄᴋ ᴀғᴛᴇʀ {}",
                "ᴏᴡᴏ, ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ {}\n\nᴀғᴛᴇʀ {}",
                "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟʟ ᴀɢᴀɪɴ {}\n\nʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀғᴛᴇʀᴀ {}",
                "ᴡʜᴀᴛꜱ ᴘᴏᴘᴘɪɴ {}?\n\nɴᴏᴡ ɪɴ ᴄʜᴀᴛ ᴀғᴛᴇʀ {}",
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_text(
                chosen_option.format(firstname, end_afk_time),
            )
        except BaseException:
            pass


def reply_afk(update, context):
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            elif ent.type == MessageEntity.MENTION:
                user_id = get_user_id(
                    message.text[ent.offset : ent.offset + ent.length]
                )
                if not user_id:
                    # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                    return

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

                try:
                    chat = context.bot.get_chat(user_id)
                except BadRequest:
                    print(
                        "Error: ᴄᴏᴜʟᴅ ɴᴏᴛ ғᴇᴛᴄʜ ᴜsᴇʀɪᴅ {} ғᴏʀ AFK ᴍᴏᴅᴜʟᴇ".format(
                            user_id
                        )
                    )
                    return
                fst_name = chat.first_name

            else:
                return

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if is_user_afk(user_id):
        reason = afk_reason(user_id)
        since_afk = get_readable_time(
            (time.time() - float(REDIS.get(f"afk_time_{user_id}")))
        )
        if int(userc_id) == int(user_id):
            return
        if reason == "none":
            res = "{} is ᴏғғʟɪɴᴇ!\nʟᴀꜱᴛ ꜱᴇᴇɴ: {} Ago.".format(fst_name, since_afk)
        else:
            res = "{} ɪꜱ ᴀғᴋ!\nʀᴇᴀꜱᴏɴ: {}\nʟᴀꜱᴛ ꜱᴇᴇɴ: {} Ago.".format(
                fst_name, reason, since_afk
            )

        update.effective_message.reply_text(res)


def __user_info__(user_id):
    is_afk = is_user_afk(user_id)
    text = ""
    if is_afk:
        since_afk = get_readable_time(
            (time.time() - float(REDIS.get(f"afk_time_{user_id}")))
        )
        text = "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ᴀғᴋ (ᴀᴡᴀʏ ғʀᴏᴍ ᴋᴇʏʙᴏᴀʀᴅ)."
        text += f"\nʟᴀꜱᴛ ꜱᴇᴇɴ: {since_afk} ᴀɢᴏ."

    else:
        text = "ᴛʜɪꜱ ᴜꜱᴇʀ ᴄᴜʀʀᴇɴᴛʟʏ ɪꜱɴ'ᴛ ᴀғᴋ \n(ɴᴏᴛ ᴀᴡᴀʏ ғʀᴏᴍ ᴋᴇʏʙᴏᴀʀᴅ)."
    return text


def __stats__():
    return f"• {len(REDIS.keys())} ᴛᴏᴛᴀʟ ᴋᴇʏs ɪɴ ʀᴇᴅɪs ᴅᴀᴛᴀʙᴀsᴇ."


def __gdpr__(user_id):
    end_afk(user_id)


AFK_HANDLER = DisableAbleCommandHandler("afk", afk, run_async=True)
AFK_REGEX_HANDLER = MessageHandler(Filters.regex("(?i)brb|(?i)bye|(?i)byy"), afk)
NO_AFK_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, no_longer_afk, run_async=True
)
AFK_REPLY_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, reply_afk, run_async=True
)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)


__mod_name__ = "𝙰ғᴋ ⚡"

__help__ = """
➥ /afk <ʀᴇᴀꜱᴏɴ> *:* ᴍᴀʀᴋ ʏᴏᴜʀsᴇʟғ ᴀs AFK (ᴀᴡᴀʏ ғʀᴏᴍ ᴋᴇʏʙᴏᴀʀᴅ). ᴡʜᴇɴ ᴍᴀʀᴋᴇᴅ ᴀs ᴀғᴋ, ᴀɴʏ ᴍᴇɴᴛɪᴏɴs ᴡɪʟʟ ʙᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴡɪᴛʜ ᴀᴍᴇssᴀɢᴇ ᴛᴏ sᴀʏ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ!
     
*ᴍᴏʀᴇ ᴛʏᴘᴇ*
➥ byy  <ʀᴇᴀꜱᴏɴ>  *:* sᴀᴍᴇ ᴀs ᴀғᴋ
 
"""
