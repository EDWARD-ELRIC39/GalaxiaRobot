# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import asyncio
import os
import re
import subprocess
import sys
from statistics import mean
from time import monotonic as time
from time import sleep

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telethon import events

from GalaxiaRobot import DEV_USERS, OWNER_ID, dispatcher, telethn
from GalaxiaRobot.modules.helper_funcs.chat_status import dev_plus


def leave_cb(update: Update, context: CallbackContext):
    bot = context.bot
    callback = update.callback_query
    if callback.from_user.id not in DEV_USERS:
        callback.answer(text="This isn't for you", show_alert=True)
        return

    match = re.match(r"leavechat_cb_\((.+?)\)", callback.data)
    chat = int(match.group(1))
    bot.leave_chat(chat_id=chat)
    callback.answer(text="Left chat")


@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        state = "Lockdown is " + "on" if not GalaxiaRobot.ALLOW_CHATS else "off"
        update.effective_message.reply_text(f"Current state: {state}")
        return
    if args[0].lower() in ["off", "no"]:
        GalaxiaRobot.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        GalaxiaRobot.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("Format: /lockdown Yes/No or Off/On")
        return
    update.effective_message.reply_text("Done! Lockdown value toggled.")


class Store:
    def __init__(self, func):
        self.func = func
        self.calls = []
        self.time = time()
        self.lock = asyncio.Lock()

    def average(self):
        return round(mean(self.calls), 2) if self.calls else 0

    def __repr__(self):
        return f"<Store func={self.func.__name__}, average={self.average()}>"

    async def __call__(self, event):
        async with self.lock:
            if not self.calls:
                self.calls = [0]
            if time() - self.time > 1:
                self.time = time()
                self.calls.append(1)
            else:
                self.calls[-1] += 1
        await self.func(event)


async def nothing(event):
    pass


messages = Store(nothing)
inline_queries = Store(nothing)
callback_queries = Store(nothing)

telethn.add_event_handler(messages, events.NewMessage())
telethn.add_event_handler(inline_queries, events.InlineQuery())
telethn.add_event_handler(callback_queries, events.CallbackQuery())


@telethn.on(events.NewMessage(pattern=r"/getstats", from_users=OWNER_ID))
async def getstats(event):
    await event.reply(
        f"**__EVENT STATISTICS__**\n**Average messages:** {messages.average()}/s\n**Average Callback Queries:** {callback_queries.average()}/s\n**Average Inline Queries:** {inline_queries.average()}/s",
        parse_mode="md",
    )


@dev_plus
def pip_install(update: Update, context: CallbackContext):
    message = update.effective_message
    args = context.args
    if not args:
        message.reply_text("Enter a package name.")
        return
    if len(args) >= 1:
        cmd = "py -m pip install {}".format(" ".join(args))
        process = subprocess.Popen(
            cmd.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        stdout, stderr = process.communicate()
        reply = ""
        stderr = stderr.decode()
        stdout = stdout.decode()
        if stdout:
            reply += f"*Stdout*\n`{stdout}`\n"
        if stderr:
            reply += f"*Stderr*\n`{stderr}`\n"

        message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN)


@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        leave_msg = " ".join(args[1:])
        try:
            context.bot.send_message(chat_id, leave_msg)
            bot.leave_chat(int(chat_id))
            update.effective_message.reply_text("Left chat.")
        except TelegramError:
            update.effective_message.reply_text("Failed to leave chat for some reason.")
    else:
        chat = update.effective_chat
        # user = update.effective_user
        GalaxiaRobot_leave_bt = [
            [
                InlineKeyboardButton(
                    text="I am sure of this action.",
                    callback_data="leavechat_cb_({})".format(chat.id),
                )
            ]
        ]
        update.effective_message.reply_text(
            "I'm going to leave {}, press the button below to confirm".format(
                chat.title
            ),
            reply_markup=InlineKeyboardMarkup(GalaxiaRobot_leave_bt),
        )


@dev_plus
def gitpull(update: Update, context: CallbackContext):
    sent_msg = update.effective_message.reply_text(
        "Pulling all changes from remote and then attempting to restart."
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\nChanges pulled...I guess.. Restarting in "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("Restarted.")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@dev_plus
def restart(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Exiting all Processes and starting a new Instance!"
    )
    process = subprocess.run(
        "pkill python3 && python3 -m GalaxiaRobot", shell=True, check=True
    )
    process.communicate()


PIP_INSTALL_HANDLER = CommandHandler("install", pip_install, run_async=True)
LEAVE_HANDLER = CommandHandler("leave", leave, run_async=True)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull, run_async=True)
RESTART_HANDLER = CommandHandler("reboot", restart, run_async=True)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups, run_async=True)
LEAVE_CALLBACK_HANDLER = CallbackQueryHandler(
    leave_cb, pattern=r"leavechat_cb_", run_async=True
)

dispatcher.add_handler(PIP_INSTALL_HANDLER)
dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)
dispatcher.add_handler(LEAVE_CALLBACK_HANDLER)

__mod_name__ = "Dev"
__handlers__ = [
    LEAVE_HANDLER,
    GITPULL_HANDLER,
    RESTART_HANDLER,
    ALLOWGROUPS_HANDLER,
    LEAVE_CALLBACK_HANDLER,
    PIP_INSTALL_HANDLER,
]
