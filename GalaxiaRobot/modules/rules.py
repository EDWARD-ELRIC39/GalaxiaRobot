# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.utils.helpers import escape_markdown

import GalaxiaRobot.modules.sql.rules_sql as sql
from GalaxiaRobot import dispatcher
from GalaxiaRobot.modules.helper_funcs.chat_status import user_admin
from GalaxiaRobot.modules.helper_funcs.string_handling import markdown_parser


def get_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    send_rules(update, chat_id)


# Do not async - not from a handler
def send_rules(update, chat_id, from_pm=False):
    bot = dispatcher.bot
    user = update.effective_user  # type: Optional[User]
    reply_msg = update.message.reply_to_message
    try:
        chat = bot.get_chat(chat_id)
    except BadRequest as excp:
        if excp.message == "Chat not found" and from_pm:
            bot.send_message(
                user.id,
                "ᴛʜᴇ ʀᴜʟᴇꜱ ꜱʜᴏʀᴛᴄᴜᴛ ғᴏʀ ᴛʜɪꜱ chat hasn't been set properly! Ask admins to "
                "ғɪx ᴛʜɪꜱ.\nᴍᴀʏʙᴇ ᴛʜᴇʏ ғᴏʀɢᴏᴛ ᴛʜᴇ ʜʏᴘʜᴇɴ ɪɴ ID",
            )
            return
        raise

    rules = sql.get_rules(chat_id)
    text = f"ᴛʜᴇ ʀᴜʟᴇꜱ ғᴏʀ *{escape_markdown(chat.title)}* ᴀʀᴇ:\n\n{rules}"

    if from_pm and rules:
        bot.send_message(
            user.id,
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif from_pm:
        bot.send_message(
            user.id,
            "ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ ʜᴀᴠᴇɴ ꜱᴇᴛ ᴀɴʏ ʀᴜʟᴇꜱ ғᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ʏᴇᴛ. "
            "ᴛʜɪꜱ ᴘʀᴏʙᴀʙʟʏ ᴅᴏᴇsɴ'ᴛ ᴍᴇᴀɴ ɪᴛ's ʟᴀᴡʟᴇss ᴛʜᴏᴜɢʜ...!",
        )
    elif rules and reply_msg:
        reply_msg.reply_text(
            "ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ᴛʜᴇ ʀᴜʟᴇs.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ʀᴜʟᴇs",
                            url=f"t.me/{bot.username}?start={chat_id}",
                        ),
                    ],
                ],
            ),
        )
    elif rules:
        update.effective_message.reply_text(
            "ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ the button below to see the rules.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="✦ ʀᴜʟᴇs ✦",
                            url=f"t.me/{bot.username}?start={chat_id}",
                        ),
                    ],
                ],
            ),
        )
    else:
        update.effective_message.reply_text(
            "ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ʜᴀᴠᴇɴ'ᴛ sᴇᴛ ᴀɴʏ ʀᴜʟᴇs ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ ʏᴇᴛ. "
            "ᴛʜɪs ᴘʀᴏʙᴀʙʟʏ ᴅᴏᴇsɴ ᴍᴇᴀɴ it's ʟᴀᴡʟᴇss ᴛʜᴏᴜɢʜ...!",
        )


@user_admin
def set_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message  # type: Optional[Message]
    raw_text = msg.text
    args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
    if len(args) == 2:
        txt = args[1]
        offset = len(txt) - len(raw_text)  # set correct offset relative to command
        markdown_rules = markdown_parser(
            txt,
            entities=msg.parse_entities(),
            offset=offset,
        )

        sql.set_rules(chat_id, markdown_rules)
        update.effective_message.reply_text("sᴜᴄᴄᴇssғᴜʟʟʏ ꜱᴇᴛ ʀᴜʟᴇꜱ ғᴏʀ ᴛʜɪꜱ ɢʀᴏᴜᴘ.")


@user_admin
def clear_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    sql.set_rules(chat_id, "")
    update.effective_message.reply_text("ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʟᴇᴀʀᴇᴅ ʀᴜʟᴇꜱ!")


def __stats__():
    return f"⍟ {sql.num_chats()} ᴄʜᴀᴛꜱ ʜᴀᴠᴇ ʀᴜʟᴇꜱ ꜱᴇᴛ."


def __import_data__(chat_id, data):
    # set chat rules
    rules = data.get("info", {}).get("rules", "")
    sql.set_rules(chat_id, rules)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return f"ᴛʜɪꜱ ᴄʜᴀᴛ ʜᴀꜱ ʜᴀᴅ ɪᴛ'ꜱ ʀᴜʟᴇꜱ ꜱᴇᴛ: `{bool(sql.get_rules(chat_id))}`"


__mod_name__ = "𝚁ᴜʟᴇꜱ 📰"

__help__ = """
*ᴜꜱᴇʀ ᴄᴏᴍᴍᴀɴᴅꜱ*
•➥ /rules*:* ɢᴇᴛ the ʀᴜʟᴇꜱ for ᴛʜɪꜱ 𝚌𝚑𝚊𝚝
.
*ʀᴜʟᴇꜱ:*
•➥ /setrules <your rules here>*:* set the 𝚛𝚞𝚕𝚎𝚜 ғᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ.

•➥ /clearrules*:* ᴄʟᴇᴀʀ ᴛʜᴇ ʀᴜʟᴇꜱ ғᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ.

"""


GET_RULES_HANDLER = CommandHandler(
    "rules", get_rules, filters=Filters.chat_type.groups, run_async=True
)
SET_RULES_HANDLER = CommandHandler(
    "setrules", set_rules, filters=Filters.chat_type.groups, run_async=True
)
RESET_RULES_HANDLER = CommandHandler(
    "clearrules", clear_rules, filters=Filters.chat_type.groups, run_async=True
)

dispatcher.add_handler(GET_RULES_HANDLER)
dispatcher.add_handler(SET_RULES_HANDLER)
dispatcher.add_handler(RESET_RULES_HANDLER)
