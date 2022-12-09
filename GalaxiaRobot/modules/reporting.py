# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

import html

from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

from GalaxiaRobot import DRAGONS, LOGGER, TIGERS, WOLVES, dispatcher
from GalaxiaRobot.modules.helper_funcs.chat_status import user_admin, user_not_admin
from GalaxiaRobot.modules.log_channel import loggable
from GalaxiaRobot.modules.sql import reporting_sql as sql

REPORT_GROUP = 12
REPORT_IMMUNE_USERS = DRAGONS + TIGERS + WOLVES


@user_admin
def report_setting(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == chat.PRIVATE:
        if len(args) >= 1:
            if args[0] in ("yes", "on"):
                sql.set_user_setting(chat.id, True)
                msg.reply_text(
                    "ᴛᴜʀɴᴇᴅ ᴏɴ ʀᴇᴘᴏʀᴛɪɴɢ! ʏᴏᴜ ʙᴇ ɴᴏᴛɪғɪᴇᴅ ᴡʜᴇɴᴇᴠᴇʀ ᴀɴʏᴏɴᴇ ʀᴇᴘᴏʀᴛꜱ ꜱᴏᴍᴇᴛʜɪɴɢ.",
                )

            elif args[0] in ("no", "off"):
                sql.set_user_setting(chat.id, False)
                msg.reply_text("ᴛᴜʀɴᴇᴅ ᴏғғ ʀᴇᴘᴏʀᴛɪɴɢ! ʏᴏᴜ ᴡᴏɴᴛ ɢᴇᴛ ᴀɴʏ ʀᴇᴘᴏʀᴛꜱ.")
        else:
            msg.reply_text(
                f"ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ʀᴇᴘᴏʀᴛ ᴘʀᴇғᴇʀᴇɴᴄᴇ ɪꜱ: `{sql.user_should_report(chat.id)}`",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if len(args) >= 1:
            if args[0] in ("yes", "on"):
                sql.set_chat_setting(chat.id, True)
                msg.reply_text(
                    f"ᴛᴜʀɴᴇᴅ ᴏɴ ʀᴇᴘᴏʀᴛɪɴɢ ɪɴ {chat.title}!\n\nᴀᴅᴍɪɴꜱ ᴡʜᴏ ʜᴀᴠᴇ ᴛᴜʀɴᴇᴅ ᴏɴ ʀᴇᴘᴏʀᴛꜱ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪғɪᴇᴅ ᴡʜᴇɴ `/report` "
                    "ᴏʀ @admin ɪꜱ ᴄᴀʟʟᴇᴅ.",
                )

            elif args[0] in ("no", "off"):
                sql.set_chat_setting(chat.id, False)
                msg.reply_text(
                    f"ᴛᴜʀɴᴇᴅ ᴏғғ ʀᴇᴘᴏʀᴛɪɴɢ ɪɴ {chat.title}!\n\nɴᴏ ᴀᴅᴍɪɴꜱ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪғɪᴇᴅ ᴏɴ `/report` or @admin.",
                )
        else:
            msg.reply_text(
                f"ᴄᴜʀʀᴇɴᴛ ʀᴇᴘᴏʀᴛ ꜱᴇᴛᴛɪɴɢ ɪꜱ: `{sql.chat_should_report(chat.id)}`.\n\nᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜɪꜱ ꜱᴇᴛᴛɪɴɢ, ᴛʀʏ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴀɢᴀɪɴ , ᴡɪᴛʜ ᴏɴᴇ ᴏғ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴀʀɢꜱ: yes/no/on/off",
                parse_mode=ParseMode.MARKDOWN,
            )


@user_not_admin
@loggable
def report(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if chat and message.reply_to_message and sql.chat_should_report(chat.id):
        reported_user = message.reply_to_message.from_user
        chat_name = chat.title or chat.first or chat.username
        admin_list = chat.get_administrators()
        message = update.effective_message

        if not args:
            message.reply_text("ᴀᴅᴅ ᴀ ʀᴇᴀꜱᴏɴ ғᴏʀ ʀᴇᴘᴏʀᴛɪɴɢ ғɪʀꜱᴛ.")
            return ""

        if user.id == reported_user.id:
            message.reply_text("ᴜʜ ʏᴇᴀʜ, ꜱᴜʀᴇ ꜱᴜʀᴇ...ᴍᴀꜱᴏ ᴍᴜᴄʜ?")
            return ""

        if user.id == bot.id:
            message.reply_text("ɴɪᴄᴇ ᴛʀʏ.")
            return ""

        if reported_user.id in REPORT_IMMUNE_USERS:
            message.reply_text("ᴜʜ? ʏᴏᴜ ʀᴇᴘᴏʀᴛɪɴɢ ᴀ ᴋɪɴɢᴅᴏᴍ ᴀꜱᴏꜱɪᴀᴛɪᴏɴ?")
            return ""

        if chat.username and chat.type == Chat.SUPERGROUP:

            reported = f"{mention_html(user.id, user.first_name)} ʀᴇᴘᴏʀᴛᴇᴅ {mention_html(reported_user.id, reported_user.first_name)} ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴꜱ!"

            msg = (
                f"<b>⚠️ ʀᴇᴘᴏʀᴛ: </b>{html.escape(chat.title)}\n"
                f"<b> • ʀᴇᴘᴏʀᴛ ʙʏ:</b> {mention_html(user.id, user.first_name)}(<code>{user.id}</code>)\n"
                f"<b> • ʀᴇᴘᴏʀᴛᴇᴅ ᴜꜱᴇʀ:</b> {mention_html(reported_user.id, reported_user.first_name)} (<code>{reported_user.id}</code>)\n"
            )
            link = f'<b> • ʀᴇᴘᴏʀᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇ:</b> <a href="https://t.me/{chat.username}/{message.reply_to_message.message_id}">ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>'
            should_forward = False
            keyboard = [
                [
                    InlineKeyboardButton(
                        "➡ ᴍᴇꜱꜱᴀɢᴇ",
                        url=f"https://t.me/{chat.username}/{message.reply_to_message.message_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "⚠ ᴋɪᴄᴋ",
                        callback_data=f"report_{chat.id}=kick={reported_user.id}={reported_user.first_name}",
                    ),
                    InlineKeyboardButton(
                        "⛔️ ʙᴀɴ",
                        callback_data=f"report_{chat.id}=banned={reported_user.id}={reported_user.first_name}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "❎ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇ",
                        callback_data=f"report_{chat.id}=delete={reported_user.id}={message.reply_to_message.message_id}",
                    ),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        else:
            reported = (
                f"{mention_html(user.id, user.first_name)} ʀᴇᴘᴏʀᴛᴇᴅ "
                f"{mention_html(reported_user.id, reported_user.first_name)} ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴꜱ!"
            )

            msg = f'{mention_html(user.id, user.first_name)} ɪꜱ ᴄᴀʟʟɪɴɢ ғᴏʀ ᴀᴅᴍɪɴꜱ ɪɴ "{html.escape(chat_name)}"!'
            link = ""
            should_forward = True

        for admin in admin_list:
            if admin.user.is_bot:  # can't message bots
                continue

            if sql.user_should_report(admin.user.id):
                try:
                    if not chat.type == Chat.SUPERGROUP:
                        bot.send_message(
                            admin.user.id,
                            msg + link,
                            parse_mode=ParseMode.HTML,
                        )

                        if should_forward:
                            message.reply_to_message.forward(admin.user.id)

                            if (
                                len(message.text.split()) > 1
                            ):  # If user is giving a reason, send his message too
                                message.forward(admin.user.id)
                    if not chat.username:
                        bot.send_message(
                            admin.user.id,
                            msg + link,
                            parse_mode=ParseMode.HTML,
                        )

                        if should_forward:
                            message.reply_to_message.forward(admin.user.id)

                            if (
                                len(message.text.split()) > 1
                            ):  # If user is giving a reason, send his message too
                                message.forward(admin.user.id)

                    if chat.username and chat.type == Chat.SUPERGROUP:
                        bot.send_message(
                            admin.user.id,
                            msg + link,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup,
                        )

                        if should_forward:
                            message.reply_to_message.forward(admin.user.id)

                            if (
                                len(message.text.split()) > 1
                            ):  # If user is giving a reason, send his message too
                                message.forward(admin.user.id)

                except Unauthorized:
                    pass
                except BadRequest as excp:  # TODO: cleanup exceptions
                    LOGGER.exception("ᴇxᴄᴇᴘᴛɪᴏɴ ᴡʜɪʟᴇ ʀᴇᴘᴏʀᴛɪɴɢ ᴜꜱᴇʀ")

        message.reply_to_message.reply_text(
            f"{mention_html(user.id, user.first_name)} ʀᴇᴘᴏʀᴛᴇᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴꜱ.",
            parse_mode=ParseMode.HTML,
        )
        return msg

    return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, _):
    return f"ᴛʜɪꜱ ᴄʜᴀᴛ ɪꜱ ꜱᴇᴛᴜᴘ ᴛᴏ ꜱᴇɴᴅ ᴜꜱᴇʀ ʀᴇᴘᴏʀᴛꜱ ᴛᴏ ᴀᴅᴍɪɴꜱ, ᴠɪᴀ /report ᴀɴᴅ @admin: `{sql.chat_should_report(chat_id)}`"


def __user_settings__(user_id):
    if sql.user_should_report(user_id) is True:
        text = "ʏᴏᴜ ᴡɪʟʟ ʀᴇᴄᴇɪᴠᴇ ʀᴇᴘᴏʀᴛꜱ ғʀᴏᴍ ᴄʜᴀᴛꜱ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ."
    else:
        text = "ʏᴏᴜ ᴡɪʟʟ *ɴᴏᴛ* ʀᴇᴄᴇɪᴠᴇ ʀᴇᴘᴏʀᴛꜱ ғʀᴏᴍ ᴄʜᴀᴛꜱ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ."
    return text


def buttons(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    splitter = query.data.replace("report_", "").split("=")
    if splitter[1] == "kick":
        try:
            bot.kickChatMember(splitter[0], splitter[2])
            bot.unbanChatMember(splitter[0], splitter[2])
            query.aswer("✅ ꜱᴜᴄᴄᴇꜱғᴜʟʟʏ ᴋɪᴄᴋᴇᴅ")
            return ""
        except Exception as err:
            query.answer("🛑 ғᴀɪʟᴇᴅ ᴛᴏ ᴋɪᴄᴋ")
            bot.sendMessage(
                text=f"ᴇʀʀᴏʀ: {err}",
                chat_id=query.message.chat_id,
                parse_mode=ParseMode.HTML,
            )
    elif splitter[1] == "banned":
        try:
            bot.kickChatMember(splitter[0], splitter[2])
            query.answer("✅  ꜱᴜᴄᴄᴇꜱғᴜʟʟʏ ʙᴀɴɴᴇᴅ")
            return ""
        except Exception as err:
            bot.sendMessage(
                text=f"ᴇʀʀᴏʀ: {err}",
                chat_id=query.message.chat_id,
                parse_mode=ParseMode.HTML,
            )
            query.answer("🛑 ғᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ")
    elif splitter[1] == "delete":
        try:
            bot.deleteMessage(splitter[0], splitter[3])
            query.answer("✅ ᴍᴇꜱꜱᴀɢᴇ ᴅᴇʟᴇᴛᴇᴅ")
            return ""
        except Exception as err:
            bot.sendMessage(
                text=f"ᴇʀʀᴏʀ: {err}",
                chat_id=query.message.chat_id,
                parse_mode=ParseMode.HTML,
            )
            query.answer("🛑 ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇ!")


SETTING_HANDLER = CommandHandler("reports", report_setting, run_async=True)
REPORT_HANDLER = CommandHandler(
    "report", report, filters=Filters.chat_type.groups, run_async=True
)
ADMIN_REPORT_HANDLER = MessageHandler(
    Filters.regex(r"(?i)@admin(s)?"), report, run_async=True
)
REPORT_BUTTON_USER_HANDLER = CallbackQueryHandler(
    buttons, pattern=r"report_", run_async=True
)

dispatcher.add_handler(REPORT_BUTTON_USER_HANDLER)
dispatcher.add_handler(SETTING_HANDLER)
dispatcher.add_handler(REPORT_HANDLER, REPORT_GROUP)
dispatcher.add_handler(ADMIN_REPORT_HANDLER, REPORT_GROUP)

__mod_name__ = "𝚁ᴇᴘᴏʀᴛ 🤨"

__help__ = """
❂ /report <reason>*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴀᴅᴍɪɴꜱ.
❂ @admin*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴀᴅᴍɪɴs.

*ɴᴏᴛᴇ:* ɴᴇɪᴛʜᴇʀ ᴏғ ᴛʜᴇꜱᴇ ᴡɪʟʟ ɢᴇᴛ ᴛʀɪɢɢᴇʀᴇᴅ ɪғ ᴜsᴇs ʙʏ ᴀᴅᴍɪɴs.

*Admins only:*
❂ /reports <on/off>*:* ᴄʜᴀɴɢᴇ ʀᴇᴘᴏʀᴛ sᴇᴛᴛɪɴɢ, ᴏʀ ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ꜱᴛᴀᴛᴜꜱ.
❂ ɪғ ᴅᴏɴᴇ ɪɴ ᴘᴍ, ᴛᴏɢɢʟᴇꜱ ʏᴏᴜʀ ꜱᴛᴀᴛᴜꜱ.
❂ ɪғ ɪɴ ɢʀᴏᴜᴘ, ᴛᴏɢɢʟᴇꜱ ᴛʜᴀᴛ ɢʀᴏᴜᴘꜱ ꜱᴛᴀᴛᴜꜱ.
"""

__handlers__ = [
    (REPORT_HANDLER, REPORT_GROUP),
    (ADMIN_REPORT_HANDLER, REPORT_GROUP),
    (SETTING_HANDLER),
]
