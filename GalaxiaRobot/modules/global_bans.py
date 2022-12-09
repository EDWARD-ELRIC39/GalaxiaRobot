# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import html
import time
from datetime import datetime
from io import BytesIO

from telegram import ParseMode, Update
from telegram.error import BadRequest, TelegramError, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
from telegram.utils.helpers import mention_html

import GalaxiaRobot.modules.sql.global_bans_sql as sql
from GalaxiaRobot import (
    DEMONS,
    DEV_USERS,
    DRAGONS,
    EVENT_LOGS,
    OWNER_ID,
    SPAMWATCH_SUPPORT_CHAT,
    STRICT_GBAN,
    SUPPORT_CHAT,
    TIGERS,
    WOLVES,
    dispatcher,
    sw,
)
from GalaxiaRobot.modules.helper_funcs.chat_status import (
    is_user_admin,
    support_plus,
    user_admin,
)
from GalaxiaRobot.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from GalaxiaRobot.modules.helper_funcs.misc import send_to_list
from GalaxiaRobot.modules.sql.users_sql import get_user_com_chats

GBAN_ENFORCE_GROUP = 6

GBAN_ERRORS = {
    "ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ",
    "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ",
    "ɴᴏᴛ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ/ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ",
    "ᴜꜱᴇʀ_ɴᴏᴛ_ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ",
    "ᴘᴇᴇʀ_ɪᴅ_ɪɴᴠᴀʟɪᴅ",
    "ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴡᴀꜱ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ",
    "ɴᴇᴇᴅ ᴛᴏ ʙᴇ ɪɴᴠɪᴛᴇʀ ᴏғ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴋɪᴄᴋ ɪᴛ ғʀᴏᴍ a ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ",
    "ᴄʜᴀᴛ_ᴀᴅᴍɪɴ_ʀᴇϙᴜɪʀᴇᴅ",
    "ᴏɴʟʏ ᴛʜᴇ ᴄʀᴇᴀᴛᴏʀ ᴏғ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ ᴄᴀɴ ᴋɪᴄᴋ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀs",
    "ᴄʜᴀɴɴᴇʟ_ᴘʀɪᴠᴀᴛᴇ",
    "ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ",
    "ᴄᴀɴ'ᴛ ʀᴇᴍᴏᴠᴇ ᴄʜᴀᴛ ᴏᴡɴᴇʀꜱ",
}

UNGBAN_ERRORS = {
    "ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ",
    "Chat not ғᴏᴜɴᴅ",
    "ɴᴏᴛ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ/ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ",
    "ᴜꜱᴇʀ_ɴᴏᴛ_ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ",
    "ᴍᴇᴛʜᴏᴅ ɪꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ꜱᴜᴘᴇʀɢʀᴏᴜᴘ ᴀɴᴅ ᴄʜᴀɴɴᴇʟ ᴄʜᴀᴛꜱ ᴏɴʟʏ",
    "ɴᴏᴛ ɪɴ the ᴄʜᴀᴛ",
    "ᴄʜᴀɴɴᴇʟ_ᴘʀɪᴠᴀᴛᴇ",
    "ᴄʜᴀᴛ_ᴀᴅᴍɪɴ_ʀᴇϙᴜɪʀᴇᴅ",
    "ᴘᴇᴇʀ_ɪᴅ_ɪɴᴠᴀʟɪᴅ",
    "ᴜꜱᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ",
}


@support_plus
def gban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return

    if int(user_id) in DEV_USERS:
        message.reply_text(
            "ᴛʜᴀᴛ ᴜꜱᴇʀ ɪꜱ ᴘᴀʀᴛ ᴏғ the ᴀꜱꜱᴏᴄɪᴀᴛɪᴏɴ\nI ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴀɢᴀɪɴꜱᴛ ᴏᴜʀ ᴏᴡɴ.",
        )
        return

    if int(user_id) in DRAGONS:
        message.reply_text(
            "I ꜱᴘʏ, ᴡɪᴛʜ ᴍʏ ʟɪᴛᴛʟᴇ ᴇʏᴇ... ᴀ ᴅɪꜱᴀꜱᴛᴇʀ! ᴡʜʏ ᴀʀᴇ ʏᴏᴜ ɢᴜʏꜱ ᴛᴜʀɴɪɴɢ ᴏɴ ᴇᴀᴄʜ ᴏᴛʜᴇʀ?",
        )
        return

    if int(user_id) in DEMONS:
        message.reply_text(
            "ᴏᴏᴏʜ ꜱᴏᴍᴇᴏɴᴇ ᴛʀʏɪɴɢ ᴛᴏ ɢʙᴀɴ ᴀ ᴅᴇᴍᴏɴ ᴅɪꜱᴀꜱᴛᴇʀ! *ɢʀᴀʙꜱ ᴘᴏᴘᴄᴏʀɴ*",
        )
        return

    if int(user_id) in TIGERS:
        message.reply_text("ᴛʜᴀᴛ'ꜱ ᴀ ᴛɪɢᴇʀ! ᴛʜᴇʏ ᴄᴀɴɴᴏᴛ ʙᴇ ʙᴀɴɴᴇᴅ!")
        return

    if int(user_id) in WOLVES:
        message.reply_text("ᴛʜᴀᴛ'ꜱ ᴀ ᴡᴏʟғ! ᴛʜᴇʏ ᴄᴀɴɴᴏᴛ ʙᴇ ʙᴀɴɴᴇᴅ!")
        return

    if user_id == bot.id:
        message.reply_text("ʏᴏᴜ ᴜʜʜ...ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ᴘᴜɴᴄʜ ᴍʏꜱᴇʟғ?")
        return

    if user_id in [777000, 1087968824]:
        message.reply_text("ғᴏᴏʟ ! ʏᴏᴜ ᴄᴀɴ'ᴛ ᴀᴛᴛᴀᴄᴋ ᴛᴇʟᴇɢʀᴀᴍ ɴᴀᴛɪᴠᴇ ᴛᴇᴄʜ!")
        return

    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message == "ᴜꜱᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ.")
            return ""
        return

    if user_chat.type != "private":
        message.reply_text("ᴛʜᴀᴛ'ꜱ ɴᴏᴛ ᴀ ᴜꜱᴇʀ!")
        return

    if sql.is_user_gbanned(user_id):

        if not reason:
            message.reply_text(
                "ᴛʜɪꜱ ᴜꜱᴇʀ is ᴀʟʀᴇᴀᴅʏ ɢʙᴀɴɴᴇᴅ; ɪᴅ ᴄʜᴀɴɢᴇ ᴛʜᴇ ʀᴇᴀꜱᴏɴ, ʙᴜᴛ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ɢɪᴠᴇɴ ᴍᴇ ᴏɴᴇ...",
            )
            return

        old_reason = sql.update_gban_reason(
            user_id,
            user_chat.username or user_chat.first_name,
            reason,
        )
        if old_reason:
            message.reply_text(
                "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ɢʙᴀɴɴᴇᴅ, ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀꜱᴏɴ:\n"
                "<code>{}</code>\n"
                "I'ᴠᴇ ɢᴏɴᴇ ᴀɴᴅ ᴜᴘᴅᴀᴛᴇᴅ ɪᴛ ᴡɪᴛʜ ʏᴏᴜʀ ɴᴇᴡ ʀᴇᴀꜱᴏɴ!".format(
                    html.escape(old_reason),
                ),
                parse_mode=ParseMode.HTML,
            )

        else:
            message.reply_text(
                "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ɢʙᴀɴɴᴇᴅ, ʙᴜᴛ had ɴᴏ ʀᴇᴀꜱᴏɴ ꜱᴇᴛ; I'ᴠᴇ ɢᴏɴᴇ ᴀɴᴅ ᴜᴘᴅᴀᴛᴇᴅ ɪᴛ!",
            )

        return

    message.reply_text("On it!")

    start_time = time.time()
    datetime_fmt = "%Y-%m-%dT%H:%M"
    current_time = datetime.utcnow().strftime(datetime_fmt)

    if chat.type != "private":
        chat_origin = "<b>{} ({})</b>\n".format(html.escape(chat.title), chat.id)
    else:
        chat_origin = "<b>{}</b>\n".format(chat.id)

    log_message = (
        f"#GBANNED\n"
        f"<b>ᴏʀɪɢɪɴᴀᴛᴇᴅ ғʀᴏᴍ:</b> <code>{chat_origin}</code>\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ʙᴀɴɴᴇᴅ ᴜꜱᴇʀ:</b> {mention_html(user_chat.id, user_chat.first_name)}\n"
        f"<b>ʙᴀɴɴᴇᴅ ᴜꜱᴇʀ ɪᴅ:</b> <code>{user_chat.id}</code>\n"
        f"<b>ᴇᴠᴇɴᴛ ꜱᴛᴀᴍᴘ:</b> <code>{current_time}</code>"
    )

    if reason:
        if chat.type == chat.SUPERGROUP and chat.username:
            log_message += f'\n<b>ʀᴇᴀꜱᴏɴ:</b> <a href="https://telegram.me/{chat.username}/{message.message_id}">{reason}</a>'
        else:
            log_message += f"\n<b>ʀᴇᴀꜱᴏɴ:</b> <code>{reason}</code>"

    if EVENT_LOGS:
        try:
            log = bot.send_message(EVENT_LOGS, log_message, parse_mode=ParseMode.HTML)
        except BadRequest:
            log = bot.send_message(
                EVENT_LOGS,
                log_message
                + "\n\nғᴏʀᴍᴀᴛᴛɪɴɢ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ ᴅᴜᴇ ᴛᴏ ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ .",
            )

    else:
        send_to_list(bot, DRAGONS + DEMONS, log_message, html=True)

    sql.gban_user(user_id, user_chat.username or user_chat.first_name, reason)

    chats = get_user_com_chats(user_id)
    gbanned_chats = 0

    for chat in chats:
        chat_id = int(chat)

        # Check if this group has disabled gbans
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            bot.ban_chat_member(chat_id, user_id)
            gbanned_chats += 1

        except BadRequest as excp:
            if excp.message in GBAN_ERRORS:
                pass
            else:
                message.reply_text(f"ᴄᴏᴜʟᴅ ɴᴏᴛ ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ: {excp.message}")
                if EVENT_LOGS:
                    bot.send_message(
                        EVENT_LOGS,
                        f"ᴄᴏᴜʟᴅ ɴᴏᴛ ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ {excp.message}",
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    send_to_list(
                        bot,
                        DRAGONS + DEMONS,
                        f"ᴄᴏᴜʟᴅ ɴᴏᴛ ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ: {excp.message}",
                    )
                sql.ungban_user(user_id)
                return
        except TelegramError:
            pass

    if EVENT_LOGS:
        log.edit_text(
            log_message + f"\n<b>ᴄʜᴀᴛꜱ ᴀғғᴇᴄᴛᴇᴅ:</b> <code>{gbanned_chats}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        send_to_list(
            bot,
            DRAGONS + DEMONS,
            f"ɢʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇ! (ᴜꜱᴇʀ ʙᴀɴɴᴇᴅ ɪɴ <code>{gbanned_chats}</code> ᴄʜᴀᴛꜱ)",
            html=True,
        )

    end_time = time.time()
    gban_time = round((end_time - start_time), 2)

    if gban_time > 60:
        gban_time = round((gban_time / 60), 2)
        message.reply_text("ᴅᴏɴᴇ! ɢʙᴀɴɴᴇᴅ.", parse_mode=ParseMode.HTML)
    else:
        message.reply_text("ᴅᴏɴᴇ! ɢʙᴀɴɴᴇᴅ.", parse_mode=ParseMode.HTML)

    try:
        bot.send_message(
            user_id,
            "#EVENT"
            "ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴍᴀʀᴋᴇᴅ ᴀꜱ ᴍᴀʟɪᴄɪᴏᴜꜱ ᴀɴᴅ ᴀꜱ ꜱᴜᴄʜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴀɴʏ ғᴜᴛᴜʀᴇ ɢʀᴏᴜᴘꜱ ᴡᴇ ᴍᴀɴᴀɢᴇ."
            f"\n<b>ʀᴇᴀꜱᴏɴ:</b> <code>{html.escape(user.reason)}</code>"
            f"</b>ᴀᴘᴘᴇᴀʟ ᴄʜᴀᴛ:</b> @{SUPPORT_CHAT}",
            parse_mode=ParseMode.HTML,
        )
    except:
        pass  # bot probably blocked by user


@support_plus
def ungban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return

    user_chat = bot.get_chat(user_id)
    if user_chat.type != "private":
        message.reply_text("ᴛʜᴀᴛ'ꜱ ɴᴏᴛ ᴀ ᴜꜱᴇʀ!")
        return

    if not sql.is_user_gbanned(user_id):
        message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ɢʙᴀɴɴᴇᴅ!")
        return

    message.reply_text(f"I'ʟʟ ɢɪᴠᴇ {user_chat.first_name} ᴀ ꜱᴇᴄᴏɴᴅ ᴄʜᴀɴᴄᴇ, ɢʟᴏʙᴀʟʟʏ.")

    start_time = time.time()
    datetime_fmt = "%Y-%m-%dT%H:%M"
    current_time = datetime.utcnow().strftime(datetime_fmt)

    if chat.type != "private":
        chat_origin = f"<b>{html.escape(chat.title)} ({chat.id})</b>\n"
    else:
        chat_origin = f"<b>{chat.id}</b>\n"

    log_message = (
        f"#UNGBANNED\n"
        f"<b>ᴏʀɪɢɪɴᴀᴛᴇᴅ ғʀᴏᴍ:</b> <code>{chat_origin}</code>\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜɴʙᴀɴɴᴇᴅ ᴜꜱᴇʀ:</b> {mention_html(user_chat.id, user_chat.first_name)}\n"
        f"<b>ᴜɴʙᴀɴɴᴇᴅ ᴜꜱᴇʀ ɪᴅ:</b> <code>{user_chat.id}</code>\n"
        f"<b>ᴇᴠᴇɴᴛ ꜱᴛᴀᴍᴘ:</b> <code>{current_time}</code>"
    )

    if EVENT_LOGS:
        try:
            log = bot.send_message(EVENT_LOGS, log_message, parse_mode=ParseMode.HTML)
        except BadRequest:
            log = bot.send_message(
                EVENT_LOGS,
                log_message
                + "\n\nғᴏʀᴍᴀᴛᴛɪɴɢ ʜᴀꜱ ʙᴇᴇɴ ᴅɪꜱᴀʙʟᴇᴅ ᴅᴜᴇ ᴛᴏ ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ.",
            )
    else:
        send_to_list(bot, DRAGONS + DEMONS, log_message, html=True)

    chats = get_user_com_chats(user_id)
    ungbanned_chats = 0

    for chat in chats:
        chat_id = int(chat)

        # Check if this group has disabled gbans
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status == "kicked":
                bot.unban_chat_member(chat_id, user_id)
                ungbanned_chats += 1

        except BadRequest as excp:
            if excp.message in UNGBAN_ERRORS:
                pass
            else:
                message.reply_text(f"ᴄᴏᴜʟᴅ ɴᴏᴛ ᴜɴ-ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ: {excp.message}")
                if EVENT_LOGS:
                    bot.send_message(
                        EVENT_LOGS,
                        f"ᴄᴏᴜʟᴅ ɴᴏᴛ ᴜɴ-ɢʙᴀɴ ᴅᴜᴇ ᴛᴏ: {excp.message}",
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    bot.send_message(
                        OWNER_ID,
                        f"ᴄᴏᴜʟᴅ ɴᴏᴛ ᴜɴ-ᴀɴ ᴅᴜᴇ ᴛᴏ: {excp.message}",
                    )
                return
        except TelegramError:
            pass

    sql.ungban_user(user_id)

    if EVENT_LOGS:
        log.edit_text(
            log_message + f"\n<b>ᴄʜᴀᴛꜱ ᴀғғᴇᴄᴛᴇᴅ:</b> {ungbanned_chats}",
            parse_mode=ParseMode.HTML,
        )
    else:
        send_to_list(bot, DRAGONS + DEMONS, "ᴜɴ-ᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇ!")

    end_time = time.time()
    ungban_time = round((end_time - start_time), 2)

    if ungban_time > 60:
        ungban_time = round((ungban_time / 60), 2)
        message.reply_text(f"ᴘᴇʀꜱᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴜɴ-ᴀɴɴᴇᴅ. ᴛᴏᴏᴋ {ungban_time} ᴍɪɴ")
    else:
        message.reply_text(f"ᴘᴇʀꜱᴏɴ ʜᴀꜱ ʙᴇᴇɴ ᴜɴ-ᴀɴɴᴇᴅ. ᴛᴏᴏᴋ {ungban_time} ꜱᴇᴄ")


@support_plus
def gbanlist(update: Update, context: CallbackContext):
    banned_users = sql.get_gban_list()

    if not banned_users:
        update.effective_message.reply_text(
            "ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ɢʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ! ʏᴏᴜ ᴋɪɴᴅᴇʀ ᴛʜᴀɴ I ᴇxᴘᴇᴄᴛᴇᴅ...",
        )
        return

    banfile = "ꜱᴄʀᴇᴡ ᴛʜᴇꜱᴇ ɢᴜʏꜱ.\n"
    for user in banned_users:
        banfile += f"[x] {user['name']} - {user['user_id']}\n"
        if user["reason"]:
            banfile += f"ʀᴇᴀꜱᴏɴ: {user['reason']}\n"

    with BytesIO(str.encode(banfile)) as output:
        output.name = "gbanlist.txt"
        update.effective_message.reply_document(
            document=output,
            filename="gbanlist.txt",
            caption="ʜᴇʀᴇ ɪꜱ ᴛʜᴇ ʟɪꜱᴛ ᴏғ ᴄᴜʀʀᴇɴᴛʟʏ ɢʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ.",
        )


def check_and_ban(update, user_id, should_message=True):

    if user_id in TIGERS or user_id in WOLVES:
        sw_ban = None
    else:
        try:
            sw_ban = sw.get_ban(int(user_id))
        except:
            sw_ban = None

    if sw_ban:
        update.effective_chat.ban_member(user_id)
        if should_message:
            update.effective_message.reply_text(
                f"<b>ᴀʟᴇʀᴛ</b>: ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ.\n"
                f"<code>*ʙᴀɴꜱ ᴛʜᴇᴍ ғʀᴏᴍ ʜᴇʀᴇ*</code>.\n"
                f"<b>ᴀᴘᴘᴇᴀʟ ᴄʜᴀᴛ</b>: {SPAMWATCH_SUPPORT_CHAT}\n"
                f"<b>ᴜꜱᴇʀ ɪᴅ</b>: <code>{sw_ban.id}</code>\n"
                f"<b>ʙᴀɴ ʀᴇᴀꜱᴏɴ</b>: <code>{html.escape(sw_ban.reason)}</code>\n@Abishnoi1M",
                parse_mode=ParseMode.HTML,
            )
        return

    if sql.is_user_gbanned(user_id):
        update.effective_chat.ban_member(user_id)
        if should_message:
            text = (
                f"<b>ᴀʟᴇʀᴛ</b>: ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ.\n"
                f"<code>*ʙᴀɴꜱ ᴛʜᴇᴍ ғʀᴏᴍ ʜᴇʀᴇ*</code>.\n"
                f"<b>ᴀᴘᴘᴇᴀʟ ᴄʜᴀᴛ</b>: @{SUPPORT_CHAT}\n"
                f"<b>ᴜꜱᴇʀ ɪᴅ</b>: <code>{user_id}</code>"
            )
            user = sql.get_gbanned_user(user_id)
            if user.reason:
                text += f"\n<b>ʙᴀɴ ʀᴇᴀꜱᴏɴ:</b> <code>{html.escape(user.reason)}</code>"
            update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def enforce_gban(update: Update, context: CallbackContext):
    # Not using @restrict handler to avoid spamming - just ignore if cant gban.
    bot = context.bot
    try:
        restrict_permission = update.effective_chat.get_member(
            bot.id,
        ).can_restrict_members
    except Unauthorized:
        return
    if sql.does_chat_gban(update.effective_chat.id) and restrict_permission:
        user = update.effective_user
        chat = update.effective_chat
        msg = update.effective_message

        if user and not is_user_admin(chat, user.id):
            check_and_ban(update, user.id)
            return

        if msg.new_chat_members:
            new_members = update.effective_message.new_chat_members
            for mem in new_members:
                check_and_ban(update, mem.id)

        if msg.reply_to_message:
            user = msg.reply_to_message.from_user
            if user and not is_user_admin(chat, user.id):
                check_and_ban(update, user.id, should_message=False)


@user_admin
def gbanstat(update: Update, context: CallbackContext):
    args = context.args
    if len(args) > 0:
        if args[0].lower() in ["on", "yes"]:
            sql.enable_gbans(update.effective_chat.id)
            update.effective_message.reply_text(
                "ᴀɴᴛɪꜱᴘᴀᴍ ɪꜱ ɴᴏᴡ ᴇɴᴀʙʟᴇᴅ ✅ "
                "I ᴀᴍ ɴᴏᴡ ᴘʀᴏᴛᴇᴄᴛɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғʀᴏᴍ ᴘᴏᴛᴇɴᴛɪᴀʟ ʀᴇᴍᴏᴛᴇ ᴛʜʀᴇᴀᴛꜱ!",
            )
        elif args[0].lower() in ["off", "no"]:
            sql.disable_gbans(update.effective_chat.id)
            update.effective_message.reply_text(
                "ᴀɴᴛɪꜱᴘᴀɴ ɪꜱ ɴᴏᴡ ᴅɪꜱᴀʙʟᴇᴅ ❌ " "ꜱᴘᴀᴍᴡᴀᴛᴄʜ ɪꜱ ɴᴏᴡ ᴅɪꜱᴀʙʟᴇᴅ ❌",
            )
    else:
        update.effective_message.reply_text(
            "ɢɪᴠᴇ ᴍᴇ ꜱᴏᴍᴇ ᴀʀɢᴜᴍᴇɴᴛꜱ ᴛᴏ ᴄʜᴏᴏꜱᴇ ᴀ ꜱᴇᴛᴛɪɴɢ! on/off, yes/no!\n\n"
            "ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢ ɪꜱ: {}\n"
            "ᴡʜᴇɴ ᴛʀᴜᴇ, ᴀɴʏ ɢʙᴀɴꜱ ᴛʜᴀᴛ ʜᴀᴘᴘᴇɴ ᴡɪʟʟ ᴀʟꜱᴏ ʜᴀᴘᴘᴇɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ. "
            "ᴡʜᴇɴ ғᴀʟꜱᴇ, ᴛʜᴇʏ ᴡᴏɴ'ᴛ, ʟᴇᴀᴠɪɴɢ ʏᴏᴜ ᴀᴛ ᴛʜᴇ ᴘᴏꜱꜱɪʙʟᴇ ᴍᴇʀᴄʏ ᴏғ "
            "ꜱᴘᴀᴍᴍᴇʀꜱ.".format(sql.does_chat_gban(update.effective_chat.id)),
        )


def __stats__():
    return f"× {sql.num_gbanned_users()} ɢʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ."


def __user_info__(user_id):
    is_gbanned = sql.is_user_gbanned(user_id)
    text = "ᴍᴀʟɪᴄɪᴏᴜꜱ: <b>{}</b>"
    if user_id in [777000, 1087968824]:
        return ""
    if user_id == dispatcher.bot.id:
        return ""
    if int(user_id) in DRAGONS + TIGERS + WOLVES:
        return ""
    if is_gbanned:
        text = text.format("Yes")
        user = sql.get_gbanned_user(user_id)
        if user.reason:
            text += f"\n<b>ʀᴇᴀꜱᴏɴ:</b> <code>{html.escape(user.reason)}</code>"
        text += f"\n<b>ᴀᴘᴘᴇᴀʟ ᴄʜᴀᴛ:</b> @{SUPPORT_CHAT}"
    else:
        text = text.format("???")
    return text


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return f"ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ᴇɴғᴏʀᴄɪɴɢ *ɢʙᴀɴꜱ*: `{sql.does_chat_gban(chat_id)}`."


GBAN_HANDLER = CommandHandler("gban", gban, run_async=True)
UNGBAN_HANDLER = CommandHandler("ungban", ungban, run_async=True)
GBAN_LIST = CommandHandler("gbanlist", gbanlist, run_async=True)
GBAN_STATUS = CommandHandler(
    "antispam", gbanstat, filters=Filters.chat_type.groups, run_async=True
)
GBAN_ENFORCER = MessageHandler(
    Filters.all & Filters.chat_type.groups, enforce_gban, run_async=True
)

dispatcher.add_handler(GBAN_HANDLER)
dispatcher.add_handler(UNGBAN_HANDLER)
dispatcher.add_handler(GBAN_LIST)
dispatcher.add_handler(GBAN_STATUS)

__mod_name__ = "𝚂ᴘᴀᴍ 🧛‍♂️"
__help__ = """
 *ᴀᴅᴍɪɴs ᴏɴʟʏ*
 
➥ /antispam <on/off/yes/no> *:* ᴡɪʟʟ ᴛᴏɢɢʟᴇ ᴏᴜʀ ᴀɴᴛɪsᴘᴀᴍ ᴛᴇᴄʜ ᴏʀ ʀᴇᴛᴜʀɴ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs. 

ɴᴏᴛᴇ *:* ᴜsᴇʀs ᴄᴀɴ ᴀᴘᴘᴇᴀʟ ɢʙᴀɴs ᴏʀ ʀᴇᴘᴏʀᴛ sᴘᴀᴍᴍᴇʀs ᴀᴛ @IDK

"""

__handlers__ = [GBAN_HANDLER, UNGBAN_HANDLER, GBAN_LIST, GBAN_STATUS]

if STRICT_GBAN:  # enforce GBANS if this is set
    dispatcher.add_handler(GBAN_ENFORCER, GBAN_ENFORCE_GROUP)
    __handlers__.append((GBAN_ENFORCER, GBAN_ENFORCE_GROUP))
