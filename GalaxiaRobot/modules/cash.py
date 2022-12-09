# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import requests
from telegram import Bot, Update
from telegram.ext import CommandHandler

from GalaxiaRobot import CASH_API_KEY, dispatcher


def convert(bot: Bot, update: Update):

    args = update.effective_message.text.split(" ", 3)
    if len(args) > 1:

        orig_cur_amount = float(args[1])

        try:
            orig_cur = args[2].upper()
        except IndexError:
            update.effective_message.reply_text(
                "ʏᴏᴜ ғᴏʀɢᴏᴛ ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴛʜᴇ ᴄᴜʀʀᴇɴᴄʏ ᴄᴏᴅᴇ."
            )
            return

        try:
            new_cur = args[3].upper()
        except IndexError:
            update.effective_message.reply_text(
                "ʏᴏᴜ ғᴏʀɢᴏᴛ ᴛᴏ ᴍᴇɴᴛɪᴏɴ ᴛʜᴇ ᴄᴜʀʀᴇɴᴄʏ ᴄᴏᴅᴇ to ᴄᴏɴᴠᴇʀᴛ ɪɴᴛᴏ."
            )
            return

        request_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={orig_cur}&to_currency={new_cur}&apikey={CASH_API_KEY}"
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response["ʀᴇᴀʟᴛɪᴍᴇ ᴄᴜʀʀᴇɴᴄʏ ᴇxᴄʜᴀɴɢᴇ ʀᴀᴛᴇ"]["5. ᴇxᴄʜᴀɴɢᴇ ʀᴀᴛᴇ"]
            )
        except KeyError:
            update.effective_message.reply_text(f"ᴄᴜʀʀᴇɴᴄʏ ɴᴏᴛ ꜱᴜᴘᴘᴏʀᴛᴇᴅ.")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        update.effective_message.reply_text(
            f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}"
        )
    else:
        update.effective_message.reply_text(__help__)


CONVERTER_HANDLER = CommandHandler("cash", convert, run_async=True)

dispatcher.add_handler(CONVERTER_HANDLER)

__command_list__ = ["cash"]
__handlers__ = [CONVERTER_HANDLER]
