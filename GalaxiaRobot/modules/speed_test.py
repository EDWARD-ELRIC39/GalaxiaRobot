# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import speedtest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from GalaxiaRobot import DEV_USERS, dispatcher
from GalaxiaRobot.modules.disable import DisableAbleCommandHandler
from GalaxiaRobot.modules.helper_funcs.chat_status import dev_plus


def convert(speed):
    return round(int(speed) / 1048576, 2)


@dev_plus
def speedtestxyz(update: Update, context: CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("ɪᴍᴀɢᴇ", callback_data="speedtest_image"),
            InlineKeyboardButton("ᴛᴇxᴛ", callback_data="speedtest_text"),
        ],
    ]
    update.effective_message.reply_text(
        "ꜱᴇʟᴇᴄᴛ ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ᴍᴏᴅᴇ",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def speedtestxyz_callback(update: Update, context: CallbackContext):
    query = update.callback_query

    if query.from_user.id in DEV_USERS:
        msg = update.effective_message.edit_text("ʀᴜɴɴɪɴɢ ᴀ ꜱᴘᴇᴇᴅᴛᴇꜱᴛ....")
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = "ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ʀᴇꜱᴜʟᴛꜱ:"

        if query.data == "speedtest_image":
            speedtest_image = speed.results.share()
            update.effective_message.reply_photo(
                photo=speedtest_image,
                caption=replymsg,
            )
            msg.delete()

        elif query.data == "speedtest_text":
            result = speed.results.dict()
            replymsg += f"\nᴅᴏᴡɴʟᴏᴀᴅ: `{convert(result['download'])}Mb/s`\nᴜᴘʟᴏᴀᴅ: `{convert(result['upload'])}Mb/s`\nᴘɪɴɢ: `{result['ping']}`"
            update.effective_message.edit_text(replymsg, parse_mode=ParseMode.MARKDOWN)
    else:
        query.answer("ʏᴏᴜ ᴀʀᴇ ʀᴇϙᴜɪʀᴇᴅ ᴛᴏ ᴊᴏɪɴ ʜᴇʀᴏᴇꜱ ᴀꜱꜱᴏᴄɪᴀᴛɪᴏɴ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")


SPEED_TEST_HANDLER = DisableAbleCommandHandler(
    "speedtest", speedtestxyz, run_async=True
)
SPEED_TEST_CALLBACKHANDLER = CallbackQueryHandler(
    speedtestxyz_callback, pattern="speedtest_.*", run_async=True
)

dispatcher.add_handler(SPEED_TEST_HANDLER)
dispatcher.add_handler(SPEED_TEST_CALLBACKHANDLER)

__mod_name__ = "SpeedTest"
__command_list__ = ["speedtest"]
__handlers__ = [SPEED_TEST_HANDLER, SPEED_TEST_CALLBACKHANDLER]
