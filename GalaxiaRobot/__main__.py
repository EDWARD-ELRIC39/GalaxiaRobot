import html
import importlib
import json
import re
import time
import traceback
from sys import argv, version_info

from pyrogram import __version__ as pver
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as lver
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tver

import GalaxiaRobot.modules.sql.users_sql as sql
from GalaxiaRobot import (
    BOT_USERNAME,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
)
from GalaxiaRobot import Galaxia as bot
from GalaxiaRobot import StartTime, bot, dispatcher, pbot, telethn, updater

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from GalaxiaRobot.modules import ALL_MODULES
from GalaxiaRobot.modules.Asustats import bot_sys_stats
from GalaxiaRobot.modules.helper_funcs.chat_status import is_user_admin
from GalaxiaRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅᴀʏs"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEX = """
ʜᴇʟʟᴏ `{}`, ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ \nᴡᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ ʙʀᴏ . . . 
"""

PM_START_TEXT = """
*ʜᴇʟʟᴏ {} !*
𝐈 𝐀ᴍ 𝐀ɴɪᴍᴇ ᴛʜᴇᴍᴇᴅ ᴀᴅᴠᴀɴᴄᴇ 𝐆ʀᴏᴜᴘ 
𝐌ᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴡɪᴛʜ 𝐀 ʟᴏᴛ ᴏғ ᴄᴏᴏʟ 𝐅ᴇᴀᴛᴜʀᴇs.
*─────────────*
 ➻ *ᴜᴘᴛɪᴍᴇ:* `{}`
 ➻ *ᴜsᴇʀs:* `{}`
 ➻ *chats:* `{}`
*─────────────*
✪ ʜɪᴛ *ʜᴇʟᴘ* [ᴛᴏ sᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ ᴅᴇᴀʀ ](https://telegra.ph/file/c857b2eef66caa121531b.mp4):
"""


buttons = [
    [
        InlineKeyboardButton(text=f" 🦋 ɪɴғᴏ 🦋", callback_data="Galaxia_"),
        InlineKeyboardButton(text="⚡ ᴅᴇᴠᴇʟᴏᴘᴇʀ ⚡", url=f"tg://user?id={OWNER_ID}"),
    ],
    [
        InlineKeyboardButton(text="💫 ʜᴇʟᴘ 💫", callback_data="help_back"),
        InlineKeyboardButton(text="🌋 ɪɴʟɪɴᴇ 🌋", switch_inline_query_current_chat=""),
    ],
    [
        InlineKeyboardButton(
            text="❣︎ ᴀᴅᴅ ᴍᴇ ᴅᴇᴀʀ  ❣︎", url=f"t.me/{BOT_USERNAME}?startgroup=new"
        ),
    ],
]


HELP_STRINGS = """
`ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴘᴇᴄɪғɪᴄs ᴄᴏᴍᴍᴀɴᴅ`."""


DONATE_STRING = """ʜᴇʏᴀ, ɢʟᴀᴅ ᴛᴏ ʜᴇᴀʀ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏɴᴀᴛᴇ!
 ʏᴏᴜ ᴄᴀɴ sᴜᴘᴘᴏʀᴛ ᴛʜᴇ ᴘʀᴏᴊᴇᴄᴛ ʙʏ ᴄᴏɴᴛᴀᴄᴛɪɴɢ @lI_EDWARD_Il 
 sᴜᴘᴘᴏʀᴛɪɴɢ ɪsɴᴛ ᴀʟᴡᴀʏs ғɪɴᴀɴᴄɪᴀʟ! 
 ᴛʜᴏsᴇ ᴡʜᴏ ᴄᴀɴɴᴏᴛ ᴘʀᴏᴠɪᴅᴇ ᴍᴏɴᴇᴛᴀʀʏ sᴜᴘᴘᴏʀᴛ ᴀʀᴇ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴜs ᴅᴇᴠᴇʟᴏᴘ ᴛʜᴇ ʙᴏᴛ ᴀᴛ ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("GalaxiaRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("ᴄᴀɴ'ᴛ ʜᴀᴠᴇ ᴛᴡᴏ ᴍᴏᴅᴜʟᴇs ᴡɪᴛʜ ᴛʜᴇ sᴀᴍᴇ ɴᴀᴍᴇ! ᴘʟᴇᴀsᴇ ᴄʜᴀɴɢᴇ ᴏɴᴇ")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("ᴛʜɪs ᴘᴇʀsᴏɴ ᴇᴅɪᴛᴇᴅ ᴀ ᴍᴇssᴀɢᴇ")
    print(update.effective_message)


def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    usr = update.effective_user
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="•ɢᴏ ʙᴀᴄᴋ•", callback_data="help_back"
                                )
                            ]
                        ]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.2)
            lol.edit_text("🌹")
            time.sleep(0.2)
            lol.edit_text("🦋")
            time.sleep(0.3)
            lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ... ")
            time.sleep(0.2)
            lol.delete()
            update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAJmfWNmIFkF0RCmxIYI3m2bxSNdihN-AAKXBQACVK0xVxvLLIOpwoNpKwQ"
            )
            update.effective_message.reply_text(
                PM_START_TEXT.format(
                    escape_markdown(first_name),
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats(),
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
            )

    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ʜᴇʏ `{}`,\n\nɪ ᴀᴍ ᴀʟɪᴠᴇ ᴅᴇᴀʀ  !\n➣ ᴜᴘᴛɪᴍᴇ: `{}` \n➣ ᴜsᴇʀs: `{}` \n➣ ᴄʜᴀᴛs: `{}` ".format(
                usr.first_name,
                uptime,
                sql.num_users(),
                sql.num_chats(),
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ꜱᴜᴘᴘᴏʀᴛ",
                            url=f"https://t.me/GALAXIA_X_SUPPORT",
                        ),
                        InlineKeyboardButton(
                            text="ᴜᴘᴅᴀᴛᴇꜱ",
                            url=f"https://t.me/GALAXIA_X_UPDATES",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴏᴡɴᴇʀ",
                            url="https://t.me/lI_EDWARD_Il",
                        ),
                        InlineKeyboardButton(
                            text="ᴄʟᴏsᴇ",
                            callback_data="close_",
                        ),
                    ],
                ]
            ),
        )


"""
@bot.on_callback_query()
async def close(Client, cb: Callbackquery):
    if cb.data == "close_":
        await cb.answer("Closed!")
        await cb.message.delete()
"""


def error_handler(update, context):
    """ʟᴏɢ ᴛʜᴇ ᴇʀʀᴏʀ ᴀɴᴅ sᴇɴᴅ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴛᴏ ɴᴏᴛɪғʏ ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="ᴇxᴄᴇᴘᴛɪᴏɴ ᴡʜɪʟᴇ ʜᴀɴᴅʟɪɴɢ ᴀɴ ᴜᴘᴅᴀᴛᴇ:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "ᴀɴ ᴇxᴄᴇᴘᴛɪᴏɴ ᴡᴀs ʀᴀɪsᴇᴅ ᴡʜɪʟᴇ ʜᴀɴᴅʟɪɴɢ ᴀɴ ᴜᴘᴅᴀᴛᴇ\n"
        "<pre>ᴜᴘᴅᴀᴛᴇ = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("ɴᴏ ɴᴏɴᴏ1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("ɴᴏ ɴᴏɴᴏ2")
        print("ʙᴀᴅʀᴇǫᴜᴇsᴛ ᴄᴀᴜɢʜᴛ")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("ɴᴏ ɴᴏɴᴏ3")
        # handle slow connection problems
    except NetworkError:
        print("ɴᴏ ɴᴏɴᴏ4")
        # handle other connection problems
    except ChatMigrated as err:
        print("ɴᴏ ɴᴏɴᴏ5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "*⍟ᴘᴏᴡᴇʀᴇᴅ ʙʏ ©* [ᴇᴅᴡᴀʀᴅ ᴇʟʀɪᴄ](https://t.me/lI_EDWARD_Il)\n*ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="•ɢᴏ ʙᴀᴄᴋ•", callback_data="help_back"
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


# Musi


def Galaxia_about_callback(update, context):
    update.effective_user.first_name
    query = update.callback_query
    if query.data == "Galaxia_":
        query.message.edit_text(
            text=f"๏ ʜᴇʟʟᴏ 👋 ɪ ᴀᴍ *{dispatcher.bot.first_name}*, `ᴀ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ʙᴜɪʟᴛ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀsɪʟʏ`\n"
            "\n`• ɪ ᴄᴀɴ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs .`\n"
            "\n`• ɪ ᴄᴀɴ ɢʀᴇᴇᴛ ᴜsᴇʀs ᴡɪᴛʜ ᴄᴜsᴛᴏᴍɪᴢᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs ᴀɴᴅ ᴇᴠᴇɴ sᴇᴛ ᴀ ɢʀᴏᴜᴘ's ʀᴜʟᴇs ᴀɴᴅ ᴍᴀɴʏ ᴍᴏʀᴇ.`\n"
            "\n`• ɪ ʜᴀᴠᴇ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-ғʟᴏᴏᴅ sʏsᴛᴇᴍ.`\n"
            "\n`• ɪ ᴄᴀɴ ᴡᴀʀɴ ᴜsᴇʀs ᴜɴᴛɪʟ ᴛʜᴇʏ ʀᴇᴀᴄʜ ᴍᴀx ᴡᴀʀɴs, ᴡɪᴛʜ ᴇᴀᴄʜ ᴘʀᴇᴅᴇғɪɴᴇᴅ ᴀᴄᴛɪᴏɴs sᴜᴄʜ ᴀs ʙᴀɴ, ᴍᴜᴛᴇ, ᴋɪᴄᴋ, ᴇᴛᴄ.`\n"
            "\n`• ɪ ʜᴀᴠᴇ ᴀ ɴᴏᴛᴇ ᴋᴇᴇᴘɪɴɢ sʏsᴛᴇᴍ, ʙʟᴀᴄᴋʟɪsᴛs, ᴀɴᴅ ᴇᴠᴇɴ ᴘʀᴇᴅᴇᴛᴇʀᴍɪɴᴇᴅ ʀᴇᴘʟɪᴇs ᴏɴ ᴄᴇʀᴛᴀɪɴ ᴋᴇʏᴡᴏʀᴅs.`\n"
            "\n`• ɪ ᴄʜᴇᴄᴋ ғᴏʀ ᴀᴅᴍɪɴs' ᴘᴇʀᴍɪssɪᴏɴs ʙᴇғᴏʀᴇ ᴇxᴇᴄᴜᴛɪɴɢ ᴀɴʏ ᴄᴏᴍᴍᴀɴᴅ ᴀɴᴅ ᴍᴏʀᴇ sᴛᴜғғs.`\n "
            f"\n\n_{dispatcher.bot.first_name}'s ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ ɢɴᴜ ɢᴇɴᴇʀᴀʟ ᴘᴜʙʟɪᴄ ʟɪᴄᴇɴsᴇ ᴠ3.0_"
            f"\n\n `ɴᴏᴡ ᴇɴᴢᴏ ᴡɪᴛʜ {dispatcher.bot.first_name}.`",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🍷ᴏᴡɴᴇʀ 🍷", url="tg://user?id=5977878551"
                        ),
                        InlineKeyboardButton(
                            text="🎿 sᴜᴘᴘᴏʀᴛ 🎿", callback_data="Galaxia_x_support"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="✨ ʀᴇᴘᴏ ✨", url="https://github.com/EDWARD-ELRIC39"
                        ),
                        InlineKeyboardButton(
                            text="🔎 ɪɴғᴏ 🔍", callback_data="Galaxia_credit"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="💫 ɢɪᴛʜᴜʙ 💫", url="https://github.com/EDWARD-ELRIC39"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="•ʙᴀᴄᴋ•", callback_data="Galaxia_back"
                        ),
                    ],
                ]
            ),
        )

    elif query.data == "Galaxia_back":
        first_name = update.effective_user.first_name
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            PM_START_TEXT.format(
                escape_markdown(first_name),
                escape_markdown(uptime),
                sql.num_users(),
                sql.num_chats(),
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )

    elif query.data == "Galaxia_support":
        query.message.edit_text(
            text="🦋"
            f"\nᴊᴏɪɴ ᴍʏ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ ғᴏʀ sᴇᴇ ᴏʀ ʀᴇᴘᴏʀᴛ ᴀ ᴘʀᴏʙʟᴇᴍ ᴏɴ {dispatcher.bot.first_name}.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔻 sᴜᴘᴘᴏʀᴛ 🔺", url="t.me/GALAXIA_x_SUPPORT"
                        ),
                        InlineKeyboardButton(
                            text="🔸 ᴜᴘᴅᴀᴛᴇ 🔹", url="https://t.me/YOUR_EDWARD"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=" •ɢᴏ ʙᴀᴄᴋ• ", callback_data="Galaxia_"
                        ),
                    ],
                ]
            ),
        )

    elif query.data == "stats_callback":
        text = bot_sys_stats()
        query.answer(text, show_alert=True)

    elif query.data == "Galaxia_credit":
        query.message.edit_text(
            text=f"๏ {dispatcher.bot.first_name}\n" f"\nɪɴғᴏ ᴀʙᴏᴜᴛ ᴇᴅᴡᴀʀᴅ  ",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🧫 ɢɪᴛʜᴜʙ 🧫", url="https://github.com/EDWARD-ELRIC39"
                        ),
                        InlineKeyboardButton(
                            text="🔧 ᴜᴘᴅᴀᴛᴇ 🔧", url="https://t.me/GALAXIA_X_UPDATES"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🧬 ᴇᴅᴡᴀʀᴅ ᴇʟʀɪᴄ 🧬", url="https://t.me/YOUR_EDWARD"
                        ),
                        InlineKeyboardButton(
                            text="🥊 ᴄʜᴀɴɴᴇʟ 🥊", url="https://t.me/YOUR_EDWARD"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🤝 ᴄʜᴀᴛ ɢʀᴏᴜᴘ 🤝", url="https://t.me/DARK_COUNCIL"
                        ),
                        InlineKeyboardButton(
                            text="🎉 ғᴜɴ 🎉", url="https://t.me/DARK_COUNCIL"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🤷‍♂️ ɪɴғᴏ 🤷‍♂️", callback_data="Galaxia_"
                        ),
                        InlineKeyboardButton(
                            text="• ʙᴀᴄᴋ • ", callback_data="Galaxia_back"
                        ),
                    ],
                ]
            ),
        )


def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴏғ {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="• ʜᴇʟᴘ •​",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "» ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴩ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="• ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ •",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="• ᴏᴩᴇɴ ʜᴇʀᴇ •",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "*ᴘᴏᴡᴇʀᴇᴅ ʙʏ ©* [ᴇᴅᴡᴀʀᴅ ᴇʟʀɪᴄ](https://t.me/lI_EDWARD_Il) \n`ʜᴇʀᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ` *{}*:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="• ɢᴏ ʙᴀᴄᴋ •", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "ᴛʜᴇsᴇ ᴀʀᴇ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ ᴀɴʏ ᴜsᴇʀ sᴘᴇᴄɪғɪᴄ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="ᴡʜɪᴄʜ ᴍᴏᴅᴜʟᴇ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴄʜᴇᴄᴋ {}'s sᴇᴛᴛɪɴɢs ғᴏʀ?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "sᴇᴇᴍs ʟɪᴋᴇ the:re ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴄʜᴀᴛ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :'(\nSend ᴛʜɪs "
                "ɪɴ ᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ ɪɴ ᴛᴏ ғɪɴᴅ ɪᴛs ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* ʜᴀꜱ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ꜱᴇᴛᴛɪɴɢꜱ ғᴏʀ ᴛʜᴇ *{}* ᴍᴏᴅᴜʟᴇ:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="• ɢᴏ ʙᴀᴄᴋ •",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ a ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ "
                "ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ a ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ "
                "ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ "
                "ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "ᴍᴇssᴀɢᴇ ɪs ɴᴏᴛ ᴍᴏᴅɪғɪᴇᴅ",
            "Query_id_invalid",
            "ᴍᴇssᴀɢᴇ ᴄᴀɴ'ᴛ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ",
        ]:
            LOGGER.exception("ᴇxᴄᴇᴘᴛɪᴏɴ ɪɴ sᴇᴛᴛɪɴɢs ʙᴜᴛᴛᴏɴs. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪs ᴄʜᴀᴛ sᴇᴛᴛɪɴɢs, ᴀs ᴡᴇʟʟ ᴀs ʏᴏᴜʀs."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="• sᴇᴛᴛɪɴɢs •",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs."

    else:
        send_settings(chat.id, user.id, True)


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 5977878551:
            update.effective_message.reply_text(
                "I'ᴍ ғʀᴇᴇ ғᴏʀ ᴇᴠᴇʀʏᴏɴᴇ ❤️ ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ᴍᴀᴋᴇ ᴍᴇ ꜱᴍɪʟᴇ, ᴊᴜꜱᴛ ᴊᴏɪɴ"
                "[ʟɪɴᴋ]({})".format(DONATION_LINK),
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "I'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ PM ғɪʀꜱᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("ᴍɪɢʀᴀᴛɪɴɢ ғʀᴏᴍ %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("sᴜᴄᴄᴇssғᴜʟʟʏ ᴍɪɢʀᴀᴛᴇᴅ!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendAnimation(
                f"@{SUPPORT_CHAT}",
                animation="https://telegra.ph/file/a6ed8df3986302848f4e5.mp4",
                caption=f"""
ㅤ🥀 {dispatcher.bot.first_name} ɪs ᴀʟɪᴠᴇ.

━━━━━━━━━━━━━
⍟ **ᴍʏ ᴏᴡɴᴇʀ :** [❣️](https://t.me/lI_EDWARD_Il)
⍟ **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{lver}`
⍟ **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tver}`
⍟ **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pver}`
⍟ **ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{version_info[0]}.{version_info[1]}.{version_info[2]}`
⍟ **ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `1.0`
━━━━━━━━━━━━━
""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                "ʙᴏᴛ ɪsɴᴛ ᴀʙʟᴇ ᴛᴏ sᴇɴᴅ ᴍᴇssᴀɢᴇ ᴛᴏ support_chat, ɢᴏ ᴀɴᴅ ᴄʜᴇᴄᴋ !"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    test_handler = CommandHandler("test", test, run_async=True)
    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    about_callback_handler = CallbackQueryHandler(
        Galaxia_about_callback, pattern=r"Galaxia_", run_async=True
    )

    donate_handler = CommandHandler("donate", donate, run_async=True)
    migrate_handler = MessageHandler(
        Filters.status_update.migrate, migrate_chats, run_async=True
    )

    dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)

    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("ᴜꜱɪɴɢ ᴡᴇʙʜᴏᴏᴋꜱ.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("ᴜꜱɪɴɢ ʟᴏɴɢ ᴘᴏʟʟɪɴɢ.")
        updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ʟᴏᴀᴅᴇᴅ ᴍᴏᴅᴜʟᴇꜱ ᴀʙ ᴇɴᴊᴏʏ ᴋᴀʀ ᴛᴜ : " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    bot.start(bot_token=TOKEN)
    pbot.start()
    main()
