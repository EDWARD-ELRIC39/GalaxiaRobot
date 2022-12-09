# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

import html
import re

from telegram import ChatPermissions, Update
from telegram.error import BadRequest
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

from GalaxiaRobot import TIGERS, WOLVES, dispatcher
from GalaxiaRobot.modules.connection import connected
from GalaxiaRobot.modules.helper_funcs.alternate import send_message
from GalaxiaRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    is_user_admin,
    user_admin,
    user_admin_no_reply,
)
from GalaxiaRobot.modules.helper_funcs.string_handling import extract_time
from GalaxiaRobot.modules.log_channel import loggable
from GalaxiaRobot.modules.sql import antiflood_sql as sql
from GalaxiaRobot.modules.sql.approve_sql import is_approved

FLOOD_GROUP = 3


@loggable
def check_flood(update, context) -> str:
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]
    if not user:  # ignore channels
        return ""

    # ignore admins and whitelists
    if is_user_admin(chat, user.id) or user.id in WOLVES or user.id in TIGERS:
        sql.update_flood(chat.id, None)
        return ""
    # ignore approved users
    if is_approved(chat.id, user.id):
        sql.update_flood(chat.id, None)
        return
    should_ban = sql.update_flood(chat.id, user.id)
    if not should_ban:
        return ""

    try:
        getmode, getvalue = sql.get_flood_setting(chat.id)
        if getmode == 1:
            chat.ban_member(user.id)
            execstrings = "ʙᴀɴɴᴇᴅ"
            tag = "BANNED"
        elif getmode == 2:
            chat.ban_member(user.id)
            chat.unban_member(user.id)
            execstrings = "ᴋɪᴄᴋᴇᴅ"
            tag = "KICKED"
        elif getmode == 3:
            context.bot.restrict_chat_member(
                chat.id,
                user.id,
                permissions=ChatPermissions(can_send_messages=False),
            )
            execstrings = "ᴍᴜᴛᴇᴅ"
            tag = "MUTED"
        elif getmode == 4:
            bantime = extract_time(msg, getvalue)
            chat.ban_member(user.id, until_date=bantime)
            execstrings = "ʙᴀɴɴᴇᴅ ғᴏʀ {}".format(getvalue)
            tag = "TBAN"
        elif getmode == 5:
            mutetime = extract_time(msg, getvalue)
            context.bot.restrict_chat_member(
                chat.id,
                user.id,
                until_date=mutetime,
                permissions=ChatPermissions(can_send_messages=False),
            )
            execstrings = "ᴍᴜᴛᴇᴅ ғᴏʀ {}".format(getvalue)
            tag = "TMUTE"
        send_message(
            update.effective_message,
            "ʙᴇᴇᴘ ʙᴏᴏᴘ! ʙᴏᴏᴘ ʙᴇᴇᴘ!\n{}!".format(execstrings),
        )

        return (
            "<b>{}:</b>"
            "\n#{}"
            "\n<b>ᴜꜱᴇʀ:</b> {}"
            "\nғʟᴏᴏᴅᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ.".format(
                tag,
                html.escape(chat.title),
                mention_html(user.id, html.escape(user.first_name)),
            )
        )

    except BadRequest:
        msg.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ʜᴇʀᴇ, ɢɪᴠᴇ ᴍᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ғɪʀꜱᴛ! ᴜɴᴛɪʟ ᴛʜᴇɴ, ɪ'ʟʟ ᴅɪꜱᴀʙʟᴇ ᴀɴᴛɪ-ғʟᴏᴏᴅ 💤.",
        )
        sql.set_flood(chat.id, 0)
        return (
            "<b>{}:</b>"
            "\n#INFO"
            "\nᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ ꜱᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅɪꜱᴀʙʟᴇᴅ ᴀɴᴛɪ-ғʟᴏᴏᴅ 🀄".format(
                chat.title,
            )
        )


@user_admin_no_reply
@bot_admin
def flood_button(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    user = update.effective_user
    match = re.match(r"unmute_flooder\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat = update.effective_chat.id
        try:
            bot.restrict_chat_member(
                chat,
                int(user_id),
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                ),
            )
            update.effective_message.edit_text(
                f"ᴜɴᴍᴜᴛᴇᴅ ʙʏ {mention_html(user.id, html.escape(user.first_name))}.",
                parse_mode="HTML",
            )
        except:
            pass


@user_admin
@loggable
def set_flood(update, context) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴍᴇᴀɴᴛ ᴛᴏ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴘᴍ ʙᴀʙʏ 👨‍🔧",
            )
            return ""
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if len(args) >= 1:
        val = args[0].lower()
        if val in ["off", "no", "0"]:
            sql.set_flood(chat_id, 0)
            if conn:
                text = message.reply_text(
                    "ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ ɪɴ {}.".format(chat_name),
                )
            else:
                text = message.reply_text("ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ.")

        elif val.isdigit():
            amount = int(val)
            if amount <= 0:
                sql.set_flood(chat_id, 0)
                if conn:
                    text = message.reply_text(
                        "ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ ɪɴ {}.".format(chat_name),
                    )
                else:
                    text = message.reply_text("ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ.")
                return (
                    "<b>{}:</b>"
                    "\n#SETFLOOD"
                    "\n<b>ᴀᴅᴍɪɴ:</b> {}"
                    "\nᴅɪꜱᴀʙʟᴇ ᴀɴᴛɪғʟᴏᴏᴅ.".format(
                        html.escape(chat_name),
                        mention_html(user.id, html.escape(user.first_name)),
                    )
                )

            if amount <= 3:
                send_message(
                    update.effective_message,
                    "ᴀɴᴛɪғʟᴏᴏᴅ ᴍᴜꜱᴛ ʙᴇ ᴇɪᴛʜᴇʀ 0 (disabled) ᴏʀ ɴᴜᴍʙᴇʀ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 3!",
                )
                return ""
            sql.set_flood(chat_id, amount)
            if conn:
                text = message.reply_text(
                    "ᴀɴᴛɪ-ғʟᴏᴏᴅ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇᴛ ᴛᴏ {} ɪɴ ᴄʜᴀᴛ: {}".format(
                        amount,
                        chat_name,
                    ),
                )
            else:
                text = message.reply_text(
                    "Successfully updated anti-flood limit to {}!".format(amount),
                )
            return (
                "<b>{}:</b>"
                "\n#SETFLOOD"
                "\n<b>ᴀᴅᴍɪɴ:</b> {}"
                "\nꜱᴇᴛ ᴀɴᴛɪғʟᴏᴏᴅ ᴛᴏ <code>{}</code>.".format(
                    html.escape(chat_name),
                    mention_html(user.id, html.escape(user.first_name)),
                    amount,
                )
            )

        else:
            message.reply_text("ɪɴᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛ ᴘʟᴇᴀꜱᴇ ᴜꜱᴇ ᴀ ɴᴜᴍʙᴇʀ, 'off' ᴏʀ 'no'")
    else:
        message.reply_text(
            (
                "ᴜꜱᴇ `/setflood number` ᴛᴏ ᴇɴᴀʙʟᴇ ᴀɴᴛɪ-ғʟᴏᴏᴅ .\n ᴏʀ ᴜꜱᴇ `/setflood off` ᴛᴏ ᴅɪꜱᴀʙʟᴇ ᴀɴᴛɪғʟᴏᴏᴅ!."
            ),
            parse_mode="markdown",
        )
    return ""


def flood(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴍᴇᴀɴᴛ ᴛᴏ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴘᴍ 👨‍💻",
            )
            return
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        if conn:
            text = msg.reply_text(
                "ɪ'ᴍ ɴᴏᴛ ᴇɴғᴏʀᴄɪɴɢ ᴀɴʏ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ ɪɴ {}!".format(chat_name),
            )
        else:
            text = msg.reply_text("Iɪ'ᴍ ɴᴏᴛ ᴇɴғᴏʀᴄɪɴɢ ᴀɴʏ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ ʜᴇʀᴇ 👊!")
    else:
        if conn:
            text = msg.reply_text(
                "ɪ'ᴍ ᴄᴜʀʀᴇɴᴛʟʏ ᴅᴇꜱᴛʀᴜᴄᴛɪɴɢ ᴍᴇᴍʙᴇʀꜱʜɪᴘ ᴀғᴛᴇʀ {} ᴄᴏɴꜱᴇᴄᴜᴛɪᴠᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ {}.".format(
                    limit,
                    chat_name,
                ),
            )
        else:
            text = msg.reply_text(
                "ɪ'ᴍ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴇꜱᴛʀɪᴄᴛɪɴɢ ᴍᴇᴍʙᴇʀꜱ ᴀғᴛᴇʀ {} ᴄᴏɴꜱᴇᴄᴜᴛɪᴠᴇ ᴍᴇꜱꜱᴀɢᴇꜱ.".format(
                    limit,
                ),
            )


@user_admin
def set_flood_mode(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
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
                "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴍᴇᴀɴᴛ ᴛᴏ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴘᴍ 🖕",
            )
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args[0].lower() == "ban":
            settypeflood = "ban"
            sql.set_flood_strength(chat_id, 1, "0")
        elif args[0].lower() == "kick":
            settypeflood = "kick"
            sql.set_flood_strength(chat_id, 2, "0")
        elif args[0].lower() == "mute":
            settypeflood = "mute"
            sql.set_flood_strength(chat_id, 3, "0")
        elif args[0].lower() == "tban":
            if len(args) == 1:
                teks = """ɪᴛ ʟᴏᴏᴋꜱ ʟɪᴋᴇ ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ ꜱᴇᴛ ᴛɪᴍᴇ ᴠᴀʟᴜᴇ ғᴏʀ ᴀɴᴛɪғʟᴏᴏᴅ ʙᴜᴛ ʏᴏᴜ ᴅɪᴅɴ'ᴛ ꜱᴘᴇᴄɪғɪᴇᴅ ᴛɪᴍᴇ; ᴛʀʏ, `/setfloodmode tban <timevalue>`.
    Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeflood = "ᴛʙᴀɴ ғᴏʀ {}".format(args[1])
            sql.set_flood_strength(chat_id, 4, str(args[1]))
        elif args[0].lower() == "tmute":
            if len(args) == 1:
                teks = (
                    update.effective_message,
                    """ɪᴛ ʟᴏᴏᴋꜱ ʟɪᴋᴇ ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ ꜱᴇᴛ ᴛɪᴍᴇ ᴠᴀʟᴜᴇ ғᴏʀ ᴀɴᴛɪғʟᴏᴏᴅ ʙᴜᴛ ʏᴏᴜ ᴅɪᴅɴ ꜱᴘᴇᴄɪғɪᴇᴅ ᴛɪᴍᴇ; ᴛʀʏ, `/setfloodmode tmute <timevalue>`.
    Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.""",
                )
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeflood = "ᴛᴍᴜᴛᴇ ғᴏʀ {}".format(args[1])
            sql.set_flood_strength(chat_id, 5, str(args[1]))
        else:
            send_message(
                update.effective_message,
                "ɪ ᴏɴʟʏ ᴜɴᴅᴇʀꜱᴛᴀɴᴅ ban/kick/mute/tban/tmute 🤪!",
            )
            return
        if conn:
            text = msg.reply_text(
                "ᴇxᴄᴇᴇᴅɪɴɢ ᴄᴏɴꜱᴇᴄᴜᴛɪᴠᴇ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇꜱᴜʟᴛ ɪɴ {} ɪɴ {}!".format(
                    settypeflood,
                    chat_name,
                ),
            )
        else:
            text = msg.reply_text(
                "ᴇxᴄᴇᴇᴅɪɴɢ ᴄᴏɴꜱᴇᴄᴜᴛɪᴠᴇ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇꜱᴜʟᴛ ɪɴ {}!".format(
                    settypeflood,
                ),
            )
        return (
            "<b>{}:</b>\n"
            "<b>ᴀᴅᴍɪɴ:</b> {}\n"
            "ʜᴀꜱ ᴄʜᴀɴɢᴇᴅ ᴀɴᴛɪғʟᴏᴏᴅ ᴍᴏᴅᴇ. ᴜꜱᴇʀ ᴡɪʟʟ {}.".format(
                settypeflood,
                html.escape(chat.title),
                mention_html(user.id, html.escape(user.first_name)),
            )
        )
    getmode, getvalue = sql.get_flood_setting(chat.id)
    if getmode == 1:
        settypeflood = "ʙᴀɴ"
    elif getmode == 2:
        settypeflood = "ᴋɪᴄᴋ"
    elif getmode == 3:
        settypeflood = "ᴍᴜᴛᴇ"
    elif getmode == 4:
        settypeflood = "ᴛʙᴀɴ ғᴏʀ {}".format(getvalue)
    elif getmode == 5:
        settypeflood = "ᴛᴍᴜᴛᴇ ғᴏʀ {}".format(getvalue)
    if conn:
        text = msg.reply_text(
            "ꜱᴇɴᴅɪɴɢ ᴍᴏʀᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ᴛʜᴀɴ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇꜱᴜʟᴛ ɪɴ {} ɪɴ {}.".format(
                settypeflood,
                chat_name,
            ),
        )
    else:
        text = msg.reply_text(
            "ꜱᴇɴᴅɪɴɢ ᴍᴏʀᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛʜᴀɴ ғʟᴏᴏᴅ ʟɪᴍɪᴛ ᴡɪʟʟ ʀᴇꜱᴜʟᴛ ɪɴ {}.".format(
                settypeflood,
            ),
        )
    return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        return "ɴᴏᴛ ᴇɴғᴏʀᴄɪɴɢ ᴛᴏ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ."
    return "ᴀɴᴛɪғʟᴏᴏᴅ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇᴛ ᴛᴏ`{}`.".format(limit)


__mod_name__ = "𝙵ʟᴏᴏᴅ 😕"

__help__ = """
*ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴛᴀᴋᴇ ᴀᴄᴛɪᴏɴ ᴏɴ ᴜsᴇʀs ᴛʜᴀᴛ sᴇɴᴅᴍᴏʀᴇᴛʜᴀɴ x ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʀᴏᴡ. Exᴄᴇᴇᴅɪɴɢ ᴛʜᴇ sᴇᴛ ғʟᴏᴏᴅ \nᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ ʀᴇsᴛʀɪᴄᴛɪɴɢ ᴛʜᴀᴛ ᴜsᴇʀ.
Tʜɪs ᴡɪʟʟ ᴍᴜᴛᴇ ᴜsᴇʀs ɪғ ᴛʜᴇʏ sᴇɴᴅ ᴍᴏʀᴇ ᴛʜᴀɴ 5 ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʀᴏᴡ, ʙᴏᴛs ᴀʀᴇ ɪɢɴᴏʀᴇᴅ.*

➥ /flood *:* Gᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ sᴇᴛᴛɪɴɢ

 • *ᴀᴅᴍɪɴs ᴏɴʟʏ:*
 
➥ /setflood <ɪɴᴛ/'ᴏɴ'/'ᴏғғ'>*:* ᴇɴᴀʙʟᴇs ᴏʀ ᴅɪsᴀʙʟᴇs ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ
   ᴇxᴀᴍᴘʟᴇ *:* /setflood 5
     
➥ /setfloodmode <ʙᴀɴ/ᴋɪᴄᴋ/ᴍᴜᴛᴇ/ᴛʙᴀɴ/ᴛᴍᴜᴛᴇ> <ᴠᴀʟᴜᴇ>*:* Aᴄᴛɪᴏɴ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴡʜᴇɴ ᴜsᴇʀ ʜᴀᴠᴇ ᴇxᴄᴇᴇᴅᴇᴅ ғʟᴏᴏᴅ ʟɪᴍɪᴛ. ʙᴀɴ/ᴋɪᴄᴋ/ᴍᴜᴛᴇ/ᴛᴍᴜᴛᴇ/ᴛʙᴀɴ

 • *ɴᴏᴛᴇ:*
 
 • Vᴀʟᴜᴇ ᴍᴜsᴛ ʙᴇ ғɪʟʟᴇᴅ ғᴏʀ ᴛʙᴀɴ ᴀɴᴅ ᴛᴍᴜᴛᴇ!!
 Iᴛ ᴄᴀɴ ʙᴇ:
 5ᴍ = 5 ᴍɪɴᴜᴛᴇs
 6ʜ = 6 ʜᴏᴜʀs
 3ᴅ = 3 ᴅᴀʏs
 1ᴡ = 1 ᴡᴇᴇᴋ
 
➥ /antichannel *:* ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇ ᴄʜᴀɴɴᴇʟ ᴍᴀssᴀɢᴇ
"""


FLOOD_BAN_HANDLER = MessageHandler(
    Filters.all & ~Filters.status_update & Filters.chat_type.groups,
    check_flood,
    run_async=True,
)
SET_FLOOD_HANDLER = CommandHandler(
    "setflood", set_flood, filters=Filters.chat_type.groups, run_async=True
)
SET_FLOOD_MODE_HANDLER = CommandHandler(
    "setfloodmode",
    set_flood_mode,
    pass_args=True,
    run_async=True,
)  # , filters=Filters.chat_type.group)
FLOOD_QUERY_HANDLER = CallbackQueryHandler(
    flood_button, pattern=r"unmute_flooder", run_async=True
)
FLOOD_HANDLER = CommandHandler(
    "flood", flood, filters=Filters.chat_type.groups, run_async=True
)

dispatcher.add_handler(FLOOD_BAN_HANDLER, FLOOD_GROUP)
dispatcher.add_handler(FLOOD_QUERY_HANDLER)
dispatcher.add_handler(SET_FLOOD_HANDLER)
dispatcher.add_handler(SET_FLOOD_MODE_HANDLER)
dispatcher.add_handler(FLOOD_HANDLER)

__handlers__ = [
    (FLOOD_BAN_HANDLER, FLOOD_GROUP),
    SET_FLOOD_HANDLER,
    FLOOD_HANDLER,
    SET_FLOOD_MODE_HANDLER,
]
