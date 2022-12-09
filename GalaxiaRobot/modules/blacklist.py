# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

import html
import re

from telegram import ChatPermissions, ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, MessageHandler
from telegram.utils.helpers import mention_html

import GalaxiaRobot.modules.sql.blacklist_sql as sql
from GalaxiaRobot import LOGGER, dispatcher
from GalaxiaRobot.modules.connection import connected
from GalaxiaRobot.modules.disable import DisableAbleCommandHandler
from GalaxiaRobot.modules.helper_funcs.alternate import send_message, typing_action
from GalaxiaRobot.modules.helper_funcs.chat_status import user_admin, user_not_admin
from GalaxiaRobot.modules.helper_funcs.extraction import extract_text
from GalaxiaRobot.modules.helper_funcs.misc import split_message
from GalaxiaRobot.modules.helper_funcs.string_handling import extract_time
from GalaxiaRobot.modules.log_channel import loggable
from GalaxiaRobot.modules.sql.approve_sql import is_approved
from GalaxiaRobot.modules.warns import warn

BLACKLIST_GROUP = 11


@user_admin
@typing_action
def blacklist(update, context):
    chat = update.effective_chat
    user = update.effective_user
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if chat.type == "private":
            return
        chat_id = update.effective_chat.id
        chat_name = chat.title

    filter_list = "ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅꜱ ɪɴ <b>{}</b>:\n".format(chat_name)

    all_blacklisted = sql.get_chat_blacklist(chat_id)

    if len(args) > 0 and args[0].lower() == "copy":
        for trigger in all_blacklisted:
            filter_list += "<code>{}</code>\n".format(html.escape(trigger))
    else:
        for trigger in all_blacklisted:
            filter_list += " - <code>{}</code>\n".format(html.escape(trigger))

    # for trigger in all_blacklisted:
    #     filter_list += " - <code>{}</code>\n".format(html.escape(trigger))

    split_text = split_message(filter_list)
    for text in split_text:
        if filter_list == "Current blacklisted words in <b>{}</b>:\n".format(
            html.escape(chat_name),
        ):
            send_message(
                update.effective_message,
                "ɴᴏ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅꜱ ɪɴ <b>{}</b>!".format(html.escape(chat_name)),
                parse_mode=ParseMode.HTML,
            )
            return
        send_message(update.effective_message, text, parse_mode=ParseMode.HTML)


@user_admin
@typing_action
def add_blacklist(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    words = msg.text.split(None, 1)

    conn = connected(context.bot, update, chat, user.id)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            return
        chat_name = chat.title

    if len(words) > 1:
        text = words[1]
        to_blacklist = list(
            {trigger.strip() for trigger in text.split("\n") if trigger.strip()},
        )
        for trigger in to_blacklist:
            sql.add_to_blacklist(chat_id, trigger.lower())

        if len(to_blacklist) == 1:
            send_message(
                update.effective_message,
                "ᴀᴅᴅᴇᴅ ʙʟᴀᴄᴋʟɪꜱᴛ <code>{}</code> ɪɴ ᴄʜᴀᴛ: <b>{}</b>!".format(
                    html.escape(to_blacklist[0]),
                    html.escape(chat_name),
                ),
                parse_mode=ParseMode.HTML,
            )

        else:
            send_message(
                update.effective_message,
                "ᴀᴅᴅᴇᴅ ʙʟᴀᴄᴋʟɪꜱᴛ ᴛʀɪɢɢᴇʀ: <code>{}</code> ɪɴ <b>{}</b>!".format(
                    len(to_blacklist),
                    html.escape(chat_name),
                ),
                parse_mode=ParseMode.HTML,
            )

    else:
        send_message(
            update.effective_message,
            "ᴛᴇʟʟ ᴍᴇ ᴡʜɪᴄʜ ᴡᴏʀᴅꜱ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ᴀᴅᴅ ɪɴ ʙʟᴀᴄᴋʟɪꜱᴛ.",
        )


@user_admin
@typing_action
def unblacklist(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    words = msg.text.split(None, 1)

    conn = connected(context.bot, update, chat, user.id)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            return
        chat_name = chat.title

    if len(words) > 1:
        text = words[1]
        to_unblacklist = list(
            {trigger.strip() for trigger in text.split("\n") if trigger.strip()},
        )
        successful = 0
        for trigger in to_unblacklist:
            success = sql.rm_from_blacklist(chat_id, trigger.lower())
            if success:
                successful += 1

        if len(to_unblacklist) == 1:
            if successful:
                send_message(
                    update.effective_message,
                    "ʀᴇᴍᴏᴠᴇᴅ <code>{}</code> ғʀᴏᴍ ʙʟᴀᴄᴋʟɪꜱᴛ in <b>{}</b>!".format(
                        html.escape(to_unblacklist[0]),
                        html.escape(chat_name),
                    ),
                    parse_mode=ParseMode.HTML,
                )
            else:
                send_message(
                    update.effective_message,
                    "ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ᴀ ʙʟᴀᴄᴋʟɪꜱᴛ ᴛʀɪɢɢᴇʀ!",
                )

        elif successful == len(to_unblacklist):
            send_message(
                update.effective_message,
                "ʀᴇᴍᴏᴠᴇᴅ <code>{}</code> ғʀᴏᴍ ʙʟᴀᴄᴋʟɪꜱᴛ ɪɴ <b>{}</b>!".format(
                    successful,
                    html.escape(chat_name),
                ),
                parse_mode=ParseMode.HTML,
            )

        elif not successful:
            send_message(
                update.effective_message,
                "ɴᴏɴᴇ ᴏғ ᴛʜᴇꜱᴇ ᴛʀɪɢɢᴇʀꜱ ᴇxɪꜱᴛ ꜱᴏ ɪᴛ ᴄᴀɴ'ᴛ ʙᴇ ʀᴇᴍᴏᴠᴇᴅ.",
                parse_mode=ParseMode.HTML,
            )

        else:
            send_message(
                update.effective_message,
                "ʀᴇᴍᴏᴠᴇᴅ <code>{}</code> ғʀᴏᴍ ʙʟᴀᴄᴋʟɪꜱᴛ. {} ᴅɪᴅ ɴᴏᴛ ᴇxɪꜱᴛ, "
                "ꜱᴏ ᴡᴇʀᴇ ɴᴏᴛ ʀᴇᴍᴏᴠᴇᴅ.".format(
                    successful,
                    len(to_unblacklist) - successful,
                ),
                parse_mode=ParseMode.HTML,
            )
    else:
        send_message(
            update.effective_message,
            "ᴛᴇʟʟ ᴍᴇ ᴡʜɪᴄʜ ᴡᴏʀᴅꜱ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ʙʟᴀᴄᴋʟɪꜱᴛ!",
        )


@loggable
@user_admin
@typing_action
def blacklist_mode(update, context):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴏɴʟʏ ᴜꜱᴇᴅ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ PM",
            )
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args[0].lower() in ["off", "nothing", "no"]:
            settypeblacklist = "do nothing"
            sql.set_blacklist_strength(chat_id, 0, "0")
        elif args[0].lower() in ["del", "delete"]:
            settypeblacklist = "delete blacklisted message"
            sql.set_blacklist_strength(chat_id, 1, "0")
        elif args[0].lower() == "warn":
            settypeblacklist = "warn the sender"
            sql.set_blacklist_strength(chat_id, 2, "0")
        elif args[0].lower() == "mute":
            settypeblacklist = "mute the sender"
            sql.set_blacklist_strength(chat_id, 3, "0")
        elif args[0].lower() == "kick":
            settypeblacklist = "kick the sender"
            sql.set_blacklist_strength(chat_id, 4, "0")
        elif args[0].lower() == "ban":
            settypeblacklist = "ban the sender"
            sql.set_blacklist_strength(chat_id, 5, "0")
        elif args[0].lower() == "tban":
            if len(args) == 1:
                teks = """ɪᴛ ʟᴏᴏᴋꜱ ʟɪᴋᴇ ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ ꜱᴇᴛ ᴛɪᴍᴇ ᴠᴀʟᴜᴇ ғᴏʀ ʙʟᴀᴄᴋʟɪꜱᴛ ʙᴜᴛ ʏᴏᴜ ᴅɪᴅɴ'ᴛ ꜱᴘᴇᴄɪғɪᴇᴅ ᴛɪᴍᴇ; ᴛʀʏ, `/blacklistmode tban <timevalue>`.

    Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            restime = extract_time(msg, args[1])
            if not restime:
                teks = """Invalid time value!
    Example of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            settypeblacklist = "ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ʙᴀɴ ғᴏʀ {}".format(args[1])
            sql.set_blacklist_strength(chat_id, 6, str(args[1]))
        elif args[0].lower() == "tmute":
            if len(args) == 1:
                teks = """ɪᴛ ʟᴏᴏᴋꜱ like ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ ꜱᴇᴛ ᴛɪᴍᴇ ᴠᴀʟᴜᴇ ғᴏʀ ʙʟᴀᴄᴋʟɪꜱᴛ ʙᴜᴛ ʏᴏᴜ ᴅɪᴅɴ'ᴛ ꜱᴘᴇᴄɪғɪᴇᴅ  ᴛɪᴍᴇ; ᴛʀʏ, `/blacklistmode tmute <timevalue>`.

    Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            restime = extract_time(msg, args[1])
            if not restime:
                teks = """Invalid time value!
    Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return ""
            settypeblacklist = "ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ᴍᴜᴛᴇ ғᴏʀ {}".format(args[1])
            sql.set_blacklist_strength(chat_id, 7, str(args[1]))
        else:
            send_message(
                update.effective_message,
                "I ᴏɴʟʏ ᴜɴᴅᴇʀꜱᴛᴀɴᴅ: off/del/warn/ban/kick/mute/tban/tmute!",
            )
            return ""
        if conn:
            text = "ᴄʜᴀɴɢᴇᴅ ʙʟᴀᴄᴋʟɪꜱᴛ ᴍᴏᴅᴇ: `{}` in *{}*!".format(
                settypeblacklist,
                chat_name,
            )
        else:
            text = "ᴄʜᴀɴɢᴇᴅ ʙʟᴀᴄᴋʟɪꜱᴛ ᴍᴏᴅᴇ: `{}`!".format(settypeblacklist)
        send_message(update.effective_message, text, parse_mode="markdown")
        return (
            "<b>{}:</b>\n"
            "<b>ᴀᴅᴍɪɴ:</b> {}\n"
            "ᴄʜᴀɴɢᴇᴅ ᴛʜᴇ ʙʟᴀᴄᴋʟɪꜱᴛ ᴍᴏᴅᴇ. ᴡɪʟʟ {}.".format(
                html.escape(chat.title),
                mention_html(user.id, html.escape(user.first_name)),
                settypeblacklist,
            )
        )
    getmode, getvalue = sql.get_blacklist_setting(chat.id)
    if getmode == 0:
        settypeblacklist = "do nothing"
    elif getmode == 1:
        settypeblacklist = "delete"
    elif getmode == 2:
        settypeblacklist = "warn"
    elif getmode == 3:
        settypeblacklist = "mute"
    elif getmode == 4:
        settypeblacklist = "kick"
    elif getmode == 5:
        settypeblacklist = "ban"
    elif getmode == 6:
        settypeblacklist = "temporarily ban for {}".format(getvalue)
    elif getmode == 7:
        settypeblacklist = "temporarily mute for {}".format(getvalue)
    if conn:
        text = "Current blacklistmode: *{}* in *{}*.".format(
            settypeblacklist,
            chat_name,
        )
    else:
        text = "Current blacklistmode: *{}*.".format(settypeblacklist)
    send_message(update.effective_message, text, parse_mode=ParseMode.MARKDOWN)
    return ""


def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i + 1)


@user_not_admin
def del_blacklist(update, context):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    bot = context.bot
    to_match = extract_text(message)
    if not to_match:
        return
    if is_approved(chat.id, user.id):
        return
    getmode, value = sql.get_blacklist_setting(chat.id)

    chat_filters = sql.get_chat_blacklist(chat.id)
    for trigger in chat_filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            try:
                if getmode == 0:
                    return
                if getmode == 1:
                    try:
                        message.delete()
                    except BadRequest:
                        pass
                elif getmode == 2:
                    try:
                        message.delete()
                    except BadRequest:
                        pass
                    warn(
                        update.effective_user,
                        chat,
                        ("ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴛʀɪɢɢᴇʀ: {}".format(trigger)),
                        message,
                        update.effective_user,
                    )
                    return
                elif getmode == 3:
                    message.delete()
                    bot.restrict_chat_member(
                        chat.id,
                        update.effective_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                    )
                    bot.sendMessage(
                        chat.id,
                        f"ᴍᴜᴛᴇᴅ {user.first_name} ғᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}!",
                    )
                    return
                elif getmode == 4:
                    message.delete()
                    res = chat.unban_member(update.effective_user.id)
                    if res:
                        bot.sendMessage(
                            chat.id,
                            f"ᴋɪᴄᴋᴇᴅ {user.first_name} ғᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}!",
                        )
                    return
                elif getmode == 5:
                    message.delete()
                    chat.kick_member(user.id)
                    bot.sendMessage(
                        chat.id,
                        f"ʙᴀɴɴᴇᴅ {user.first_name} ғᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}",
                    )
                    return
                elif getmode == 6:
                    message.delete()
                    bantime = extract_time(message, value)
                    chat.kick_member(user.id, until_date=bantime)
                    bot.sendMessage(
                        chat.id,
                        f"ʙᴀɴɴᴇᴅ {user.first_name} ᴜɴᴛɪʟ '{value}' ғᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}!",
                    )
                    return
                elif getmode == 7:
                    message.delete()
                    mutetime = extract_time(message, value)
                    bot.restrict_chat_member(
                        chat.id,
                        user.id,
                        until_date=mutetime,
                        permissions=ChatPermissions(can_send_messages=False),
                    )
                    bot.sendMessage(
                        chat.id,
                        f"ᴍᴜᴛᴇᴅ {user.first_name} ᴜɴᴛɪʟ '{value}' ғᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}!",
                    )
                    return
            except BadRequest as excp:
                if excp.message != "ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
                    LOGGER.exception("ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛ ᴍᴇꜱꜱᴀɢᴇ.")
            break


def __import_data__(chat_id, data):
    # set chat blacklist
    blacklist = data.get("blacklist", {})
    for trigger in blacklist:
        sql.add_to_blacklist(chat_id, trigger)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    blacklisted = sql.num_blacklist_chat_filters(chat_id)
    return "ᴛʜᴇʀᴇ ᴀʀᴇ {} ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅꜱ.".format(blacklisted)


def __stats__():
    return "× {} ʙʟᴀᴄᴋʟɪꜱᴛ ᴛʀɪɢɢᴇʀꜱ, ᴀᴄʀᴏꜱꜱ {} ᴄʜᴀᴛꜱ.".format(
        sql.num_blacklist_filters(),
        sql.num_blacklist_filter_chats(),
    )


__mod_name__ = "𝙱ʟᴀᴄᴋʟɪsᴛ 🌚"

__help__ = """

*ʙʟᴀᴄᴋʟɪꜱᴛꜱ ᴀʀᴇ ᴜꜱᴇᴅ ᴛᴏ ꜱᴛᴏᴘ ᴄᴇʀᴛᴀɪɴ ᴛʀɪɢɢᴇʀꜱ ғʀᴏᴍ ʙᴇɪɴɢ ꜱᴀɪᴅ ɪɴ ᴀ ɢʀᴏᴜᴘ. ᴀɴʏ ᴛɪᴍᴇ ᴛʜᴇ ᴛʀɪɢɢᴇʀ ɪꜱ ᴍᴇɴᴛɪᴏɴᴇᴅ, ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ. ᴀ ɢᴏᴏᴅ ᴄᴏᴍʙᴏ ɪs sᴏᴍᴇᴛɪᴍᴇs ᴛᴏ ᴘᴀɪʀ ᴛʜɪs ᴜᴘ ᴡɪᴛʜ ᴡᴀʀɴ ғɪʟᴛᴇʀs!*

*ɴᴏᴛᴇ*: ʙʟᴀᴄᴋʟɪsᴛs ᴅᴏ ɴᴏᴛ ᴀғғᴇᴄᴛ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs.

❂ /blacklist*:* ᴠɪᴇᴡ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs.

*ᴀᴅᴍɪɴ ᴏɴʟʏ:*
❂ /addblacklist <ᴛʀɪɢɢᴇʀs>*:* ᴀᴅᴅ ᴀ ᴛʀɪɢɢᴇʀ ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. ᴇᴀᴄʜ ʟɪɴᴇ is ᴄᴏɴsɪᴅᴇʀᴇᴅ ᴏɴᴇ ᴛʀɪɢɢᴇʀ, sᴏ ᴜsɪɴɢ ᴅɪғғᴇʀᴇɴᴛ ʟɪɴᴇs ᴡɪʟʟ ᴀʟʟᴏᴡ ʏᴏᴜ ᴛᴏ ᴀᴅᴅ ᴍᴜʟᴛɪᴘʟᴇ ᴛʀɪɢɢᴇʀs.

❂ /unblacklist <ᴛʀɪɢɢᴇʀs>*:* ʀᴇᴍᴏᴠᴇ ᴛʀɪɢɢᴇʀs ғʀᴏᴍ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛ. sᴀᴍᴇ ɴᴇᴡʟɪɴᴇ ʟᴏɢɪᴄ ᴀᴘᴘʟɪᴇs ʜᴇʀᴇ, sᴏ ʏᴏᴜ ᴄᴀɴ ʀᴇᴍᴏᴠᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴛʀɪɢɢᴇʀs ᴀᴛ ᴏɴᴄᴇ.

❂ /blacklistmode <off/del/warn/ban/kick/mute/tban/tmute>*:* ᴀᴄᴛɪᴏɴ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴡʜᴇɴ sᴏᴍᴇᴏɴᴇ sᴇɴᴅs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs.

ʀʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀ ɪs ᴜsᴇᴅ ᴛᴏ sᴛᴏᴘ ᴄᴇʀᴛᴀɪɴ sᴛɪᴄᴋᴇʀs. ᴡʜᴇɴᴇᴠᴇʀ a sᴛɪᴄᴋᴇʀ ɪs sᴇɴᴛ, ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ.

*ɴᴏᴛᴇ:* ʙʟᴀᴄᴋʟɪsᴛ sᴛɪᴄᴋᴇʀs ᴅᴏ ɴᴏᴛ ᴀғғᴇᴄᴛ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ

❂ /blsticker*:* ꜱᴇᴇ ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ꜱᴛɪᴄᴋᴇʀ


❂ /addblsticker <sticker link>*:* ᴀᴅᴅ ᴛʜᴇ ꜱᴛɪᴄᴋᴇʀ ᴛʀɪɢɢᴇʀ ᴛᴏ ᴛʜᴇ ʙʟᴀᴄᴋ ʟɪꜱᴛ. ᴄᴀɴ ʙᴇ ᴀᴅᴅᴇᴅ ᴠɪᴀ ʀᴇᴘʟʏ ꜱᴛɪᴄᴋᴇʀ

❂ /unblsticker <sticker link>*:* ʀᴇᴍᴏᴠᴇ ᴛʀɪɢɢᴇʀꜱ ғʀᴏᴍ ʙʟᴀᴄᴋʟɪꜱᴛ. ᴛʜᴇ ꜱᴀᴍᴇ ɴᴇᴡʟɪɴᴇ ʟᴏɢɪᴄ ᴀᴘᴘʟɪᴇꜱ ʜᴇʀᴇ, ꜱᴏ ʏᴏᴜ ᴄᴀɴ ᴅᴇʟᴇᴛᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴛʀɪɢɢᴇʀꜱ ᴀᴛ ᴏɴᴄᴇ

❂ /rmblsticker <sticker link>*:* ꜱᴀᴍᴇ ᴀꜱ ᴀʙᴏᴠᴇ

❂ /blstickermode <delete/ban/tban/mute/tmute>*:* ꜱᴇᴛꜱ ᴜᴘ ᴀ ᴅᴇғᴀᴜʟᴛ ᴀᴄᴛɪᴏɴ ᴏɴ ᴡʜᴀᴛ ᴛᴏ ᴅᴏ ɪғ ᴜꜱᴇʀꜱ ᴜꜱᴇ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ꜱᴛɪᴄᴋᴇʀꜱ

ɴᴏᴛᴇ:
❂ <sticker link> ᴄᴀɴ ʙᴇ https://t.me/addstickers/<sticker> ᴏʀ ᴊᴜꜱᴛ <sticker> ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ꜱᴛɪᴄᴋᴇʀ ᴍᴇꜱꜱᴀɢᴇ

"""


BLACKLIST_HANDLER = DisableAbleCommandHandler(
    "blacklist",
    blacklist,
    pass_args=True,
    admin_ok=True,
    run_async=True,
)
ADD_BLACKLIST_HANDLER = CommandHandler("addblacklist", add_blacklist, run_async=True)
UNBLACKLIST_HANDLER = CommandHandler("unblacklist", unblacklist, run_async=True)
BLACKLISTMODE_HANDLER = CommandHandler(
    "blacklistmode", blacklist_mode, pass_args=True, run_async=True
)
BLACKLIST_DEL_HANDLER = MessageHandler(
    (Filters.text | Filters.command | Filters.sticker | Filters.photo)
    & Filters.chat_type.groups,
    del_blacklist,
    allow_edit=True,
    run_async=True,
)

dispatcher.add_handler(BLACKLIST_HANDLER)
dispatcher.add_handler(ADD_BLACKLIST_HANDLER)
dispatcher.add_handler(UNBLACKLIST_HANDLER)
dispatcher.add_handler(BLACKLISTMODE_HANDLER)
dispatcher.add_handler(BLACKLIST_DEL_HANDLER, group=BLACKLIST_GROUP)


__handlers__ = [
    BLACKLIST_HANDLER,
    ADD_BLACKLIST_HANDLER,
    UNBLACKLIST_HANDLER,
    BLACKLISTMODE_HANDLER,
    (BLACKLIST_DEL_HANDLER, BLACKLIST_GROUP),
]
