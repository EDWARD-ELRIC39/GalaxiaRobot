# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


from gpytranslate import Translator
from pyrogram import filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import CallbackContext

from GalaxiaRobot import dispatcher, pbot
from GalaxiaRobot.modules.disable import DisableAbleCommandHandler

__mod_name__ = "𝙶-ᴛʀᴀɴ 🗞️"

__help__ = """ 
**ᴜsᴇ ᴛʜɪs ᴍᴏᴅᴜʟᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ sᴛᴜғғ!**
*ᴄᴏᴍᴍᴀɴᴅꜱ:*

❂ /tl (or /tr): ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ, ᴛʀᴀɴsʟᴀᴛᴇs ɪᴛ ᴛᴏ ᴇɴɢʟɪsʜ.

❂ /tl <lang>: ᴛʀᴀɴsʟᴀᴛᴇs ᴛᴏ <lang>

*ᴇɢ:* /tl ja: ᴛʀᴀɴsʟᴀᴛᴇs ᴛᴏ ᴊᴀᴘᴀɴᴇsᴇ.

❂ /tl <source>//<dest>: ᴛʀᴀɴsʟᴀᴛᴇs ғʀᴏᴍ <source> ᴛᴏ <lang>.

eg:  /tl ja//en: ᴛʀᴀɴsʟᴀᴛᴇs ғʀᴏᴍ ᴊᴀᴘᴀɴᴇsᴇ ᴛᴏ ᴇɴɢʟɪsʜ.

❂ /langs: ɢᴇᴛ ᴀ ʟɪsᴛ of sᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇs ғᴏʀ ᴛʀᴀɴsʟᴀᴛɪᴏɴ.

** ɪ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴛᴇxᴛ to ᴠᴏɪᴄᴇ and ᴠᴏɪᴄᴇ ᴛᴏ ᴛᴇxᴛ..**

❂ /tts <lang code>*:* ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ ᴏᴜᴛᴘᴜᴛ

❂ /stt*:* ᴛʏᴘᴇ ɪɴ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ(sᴜᴘᴘᴏʀᴛ ᴇɴɢʟɪsʜ ᴏɴʟʏ) ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴛᴇxᴛ ғʀᴏᴍ ɪᴛ.

*ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs*
 https://telegra.ph/ɪᴛs-ᴍᴇ-𒆜-Aʙɪsʜɴᴏɪ-07-30-2

"""


trans = Translator()


@pbot.on_message(filters.command(["tl", "tr"]))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ɪᴛ!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"<b>ᴛʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {source} ᴛᴏ {dest}</b>:\n"
        f"<code>{translation.text}</code>"
    )

    await message.reply_text(reply, parse_mode="html")


def languages(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text(
        "ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ᴛʜᴇ ʟɪsᴛ ᴏғ sᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs",
                        url="https://telegra.ph/ɪᴛs-ᴍᴇ-𒆜-Aʙɪsʜɴᴏɪ-07-30-2",
                    ),
                ],
            ],
            disable_web_page_preview=True,
        ),
    )


LANG_HANDLER = DisableAbleCommandHandler("langs", languages, run_async=True)

dispatcher.add_handler(LANG_HANDLER)
