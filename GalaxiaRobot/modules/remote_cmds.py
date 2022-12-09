# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


from telegram import ChatPermissions, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler

from GalaxiaRobot import LOGGER, dispatcher
from GalaxiaRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    is_bot_admin,
    is_user_ban_protected,
    is_user_in_chat,
)
from GalaxiaRobot.modules.helper_funcs.extraction import extract_user_and_text
from GalaxiaRobot.modules.helper_funcs.filters import CustomFilters

RBAN_ERRORS = {
    "ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ",
    "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ",
    "ɴᴏᴛ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ/ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ",
    "ᴜꜱᴇʀ_ɴᴏᴛ_ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ",
    "ᴘᴇᴇʀ_ɪᴅ_ɪɴᴠᴀʟɪᴅ",
    "ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴡᴀꜱ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ",
    "ɴᴇᴇᴅ ᴛᴏ ʙᴇ ɪɴᴠɪᴛᴇʀ of a ᴜꜱᴇʀ ᴛᴏ ᴘᴜɴᴄʜ ɪᴛ ғʀᴏᴍ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ",
    "ᴄʜᴀᴛ_ᴀᴅᴍɪɴ_ʀᴇϙᴜɪʀᴇᴅ",
    "ᴏɴʟʏ ᴛʜᴇ ᴄʀᴇᴀᴛᴏʀ ᴏғ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ ᴄᴀɴ ᴘᴜɴᴄʜ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀꜱ",
    "ᴄʜᴀɴɴᴇʟ_ᴘʀɪᴠᴀᴛᴇ",
    "ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ",
}

RUNBAN_ERRORS = {
    "ᴜꜱᴇʀ is an ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ",
    "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ",
    "ɴᴏᴛ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ/ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ",
    "ᴜꜱᴇʀ_ɴᴏᴛ_ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ",
    "ᴘᴇᴇʀ_ɪᴅ_ɪɴᴠᴀʟɪᴅ",
    "ɢʀᴏᴜᴘ ᴄʜᴀᴛ was ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ",
    "ɴᴇᴇᴅ ᴛᴏ ʙᴇ ɪɴᴠɪᴛᴇʀ ᴏғ a ᴜꜱᴇʀ ᴛᴏ ᴘᴜɴᴄʜ ɪᴛ ғʀᴏᴍ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ",
    "ᴄʜᴀᴛ_ᴀᴅᴍɪɴ_ʀᴇϙᴜɪʀᴇᴅ",
    "ᴏɴʟʏ ᴛʜᴇ ᴄʀᴇᴀᴛᴏʀ of a ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ ᴄᴀɴ ᴘᴜɴᴄʜ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀꜱ",
    "ᴄʜᴀɴɴᴇʟ_ᴘʀɪᴠᴀᴛᴇ",
    "ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ",
}

RKICK_ERRORS = {
    "ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ",
    "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ",
    "ɴᴏᴛ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ/ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ",
    "ᴜꜱᴇʀ_ɴᴏᴛ_ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ",
    "ᴘᴇᴇʀ_ɪᴅ_ɪɴᴠᴀʟɪᴅ",
    "ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴡᴀꜱ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ",
    "ɴᴇᴇᴅ ᴛᴏ ʙᴇ ɪɴᴠɪᴛᴇʀ ᴏғ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴘᴜɴᴄʜ ɪᴛ ғʀᴏᴍ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ",
    "Chat_admin_required",
    "ᴏɴʟʏ ᴛʜᴇ ᴄʀᴇᴀᴛᴏʀ of ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ ᴄᴀɴ ᴘᴜɴᴄʜ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀꜱ",
    "ᴄʜᴀɴɴᴇʟ_ᴘʀɪᴠᴀᴛᴇ",
    "ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ",
}

RMUTE_ERRORS = {
    "ᴜꜱᴇʀ is ᴀɴ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ",
    "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ",
    "ɴᴏᴛ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ/ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ",
    "ᴜꜱᴇʀ_ɴᴏᴛ_ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ",
    "ᴘᴇᴇʀ_ɪᴅ_ɪɴᴠᴀʟɪᴅ",
    "ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴡᴀꜱ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ",
    "ɴᴇᴇᴅ ᴛᴏ ʙᴇ ɪɴᴠɪᴛᴇʀ ᴏғ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴘᴜɴᴄʜ ɪᴛ ғʀᴏᴍ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ",
    "ᴄʜᴀᴛ_ᴀᴅᴍɪɴ_ʀᴇϙᴜɪʀᴇᴅ",
    "ᴏɴʟʏ ᴛʜᴇ ᴄʀᴇᴀᴛᴏʀ ᴏғ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ ᴄᴀɴ ᴘᴜɴᴄʜ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀꜱ",
    "ᴄʜᴀɴɴᴇʟ_ᴘʀɪᴠᴀᴛᴇ",
    "ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ",
}

RUNMUTE_ERRORS = {
    "ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ",
    "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ",
    "ɴᴏᴛ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ/ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ",
    "ᴜꜱᴇʀ_ɴᴏᴛ_ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ",
    "ᴘᴇᴇʀ_ɪᴅ_ɪɴᴠᴀʟɪᴅ",
    "ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴡᴀꜱ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ",
    "ɴᴇᴇᴅ ᴛᴏ ʙᴇ ɪɴᴠɪᴛᴇʀ ᴏғ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴘᴜɴᴄʜ ɪᴛ ғʀᴏᴍ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ",
    "Chat_admin_required",
    "ᴏɴʟʏ ᴛʜᴇ ᴄʀᴇᴀᴛᴏʀ ᴏғ ᴀ ʙᴀꜱɪᴄ ɢʀᴏᴜᴘ ᴄᴀɴ ᴘᴜɴᴄʜ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀꜱ",
    "ᴄʜᴀɴɴᴇʟ_ᴘʀɪᴠᴀᴛᴇ",
    "ɴᴏᴛ in ᴛʜᴇ ᴄʜᴀᴛ",
}


@bot_admin
def rban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("You don't seem to be referring to a chat/user.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect..",
        )
        return
    if not chat_id:
        message.reply_text("You don't seem to be referring to a chat.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text(
                "ᴄʜᴀᴛ not found! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ a ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ I'ᴍ ᴘᴀʀᴛ ᴏғ ᴛʜᴀᴛ ᴄʜᴀᴛ.",
            )
            return
        raise

    if chat.type == "private":
        message.reply_text("I'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ!")
        return

    if (
        not is_bot_admin(chat, bot.id)
        or not chat.get_member(bot.id).can_restrict_members
    ):
        message.reply_text(
            "I ᴄᴀɴ'ᴛ ʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ I'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ʙᴀɴ ᴜꜱᴇʀꜱ.",
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "ᴜꜱᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text("I ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ")
            return
        raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("I ʀᴇᴀʟʟʏ ᴡɪꜱʜ I ᴄᴏᴜʟᴅ ʙᴀɴ ᴀᴅᴍɪɴꜱ...")
        return

    if user_id == bot.id:
        message.reply_text("I'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ BAN ᴍʏꜱᴇʟғ, ᴀʀᴇ ʏᴏᴜ ᴄᴜᴛɪʏᴀ?")
        return

    try:
        chat.ban_member(user_id)
        message.reply_text("ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴄʜᴀᴛ!")
    except BadRequest as excp:
        if excp.message == "ʀᴇᴘʟʏ ᴍᴇꜱꜱᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
            # Do not reply
            message.reply_text("ʙᴀɴɴᴇᴅ!", quote=False)
        elif excp.message in RBAN_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ᴇʀʀᴏʀ ʙᴀɴɴɪɴɢ ᴜꜱᴇʀ %s ɪɴ ᴄʜᴀᴛ %s (%s) ᴅᴜᴇ ᴛᴏ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴛʜᴀᴛ ᴜꜱᴇʀ.")


@bot_admin
def runban(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ to ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ/ᴜꜱᴇʀ.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ID ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return
    if not chat_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text(
                "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏʀ ᴇɴᴛᴇʀᴇᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ I'ᴍ ᴘᴀʀᴛ ᴏғ ᴛʜᴀᴛ ᴄʜᴀᴛ.",
            )
            return
        raise

    if chat.type == "private":
        message.reply_text("I'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ!")
        return

    if (
        not is_bot_admin(chat, bot.id)
        or not chat.get_member(bot.id).can_restrict_members
    ):
        message.reply_text(
            "I ᴄᴀɴ'ᴛ ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ I'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ᴜɴʙᴀɴ ᴜꜱᴇʀꜱ.",
        )
        return

    try:
        chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "ᴜꜱᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text("I ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ to ғɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ᴛʜᴇʀᴇ")
            return
        raise

    if is_user_in_chat(chat, user_id):
        message.reply_text(
            "ᴡʜʏ ᴀʀᴇ ʏᴏᴜ ᴛʀʏɪɴɢ ᴛᴏ ʀᴇᴍᴏᴛᴇʟʏ ᴜɴʙᴀɴ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴀᴛ ᴄʜᴀᴛ?",
        )
        return

    if user_id == bot.id:
        message.reply_text("I'm not gonna UNBAN myself, I'm an admin there!")
        return

    try:
        chat.unban_member(user_id)
        message.reply_text("Yep, this user can join that chat!")
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text("Unbanned!", quote=False)
        elif excp.message in RUNBAN_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR unbanning user %s in chat %s (%s) due to %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Well damn, I can't unban that user.")


@bot_admin
def rkick(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("You don't seem to be referring to a chat/user.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect..",
        )
        return
    if not chat_id:
        message.reply_text("You don't seem to be referring to a chat.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "Chat not found":
            message.reply_text(
                "Chat not found! Make sure you entered a valid chat ID and I'm part of that chat.",
            )
            return
        raise

    if chat.type == "private":
        message.reply_text("I'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ!")
        return

    if (
        not is_bot_admin(chat, bot.id)
        or not chat.get_member(bot.id).can_restrict_members
    ):
        message.reply_text(
            "I ᴄᴀɴ'ᴛ ʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ᴘᴜɴᴄʜ ᴜꜱᴇʀꜱ.",
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "ᴜꜱᴇʀ ɴᴏᴛ ʀᴏᴜɴᴅ":
            message.reply_text("I ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ")
            return
        raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("I ʀᴇᴀʟʟʏ ᴡɪꜱʜ ɪ ᴄᴏᴜʟᴅ ᴘᴜɴᴄʜ ᴀᴅᴍɪɴꜱ...")
        return

    if user_id == bot.id:
        message.reply_text("I'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴘᴜɴᴄʜ ᴍʏꜱᴇʟғ, ᴀʀᴇ ʏᴏᴜ ᴄʀᴀᴢʏ?")
        return

    try:
        chat.unban_member(user_id)
        message.reply_text("ᴘᴜɴᴄʜᴇᴅ ғʀᴏᴍ ᴄʜᴀʀᴛ!")
    except BadRequest as excp:
        if excp.message == "ʀᴇᴘʟʏ ᴍᴇꜱꜱᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
            # Do not reply
            message.reply_text("ᴘᴜɴᴄʜᴇᴅ!", quote=False)
        elif excp.message in RKICK_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ᴇʀʀᴏʀ ᴘᴜɴᴄʜɪɴɢ ᴜꜱᴇʀ %s ɪɴ ᴄʜᴀᴛ %s (%s) ᴅᴜᴇ ᴛᴏ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, I ᴄᴀɴ'ᴛ ᴘᴜɴᴄʜ ᴛʜᴀᴛ ᴜꜱᴇʀ.")


@bot_admin
def rmute(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ/ᴜꜱᴇʀ.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return
    if not chat_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ a ᴄʜᴀᴛ.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text(
                "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ ɪ'ᴍ ᴘᴀʀᴛ ᴏғ ᴛʜᴀᴛ ᴄʜᴀᴛ.",
            )
            return
        raise

    if chat.type == "private":
        message.reply_text("I'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ!")
        return

    if (
        not is_bot_admin(chat, bot.id)
        or not chat.get_member(bot.id).can_restrict_members
    ):
        message.reply_text(
            "I ᴄᴀɴ'ᴛ ʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ I'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ᴍᴜᴛᴇ ᴜꜱᴇʀꜱ.",
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user")
            return
        raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("I ʀᴇᴀʟʟʏ ᴡɪꜱʜ ɪ ᴄᴏᴜʟᴅ ᴍᴜᴛᴇ ᴀᴅᴍɪɴꜱ...")
        return

    if user_id == bot.id:
        message.reply_text("I'm ɴᴏᴛ ɢᴏɴɴᴀ ᴍᴜᴛᴇ ᴍʏꜱᴇʟғ, ᴀʀᴇ ʏᴏᴜ ᴄᴜᴛɪʏᴀ ?")
        return

    try:
        bot.restrict_chat_member(
            chat.id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False),
        )
        message.reply_text("ᴍᴜᴛᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ!")
    except BadRequest as excp:
        if excp.message == "ʀᴇᴘʟʏ ᴍᴇꜱꜱᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
            # Do not reply
            message.reply_text("Muted!", quote=False)
        elif excp.message in RMUTE_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ᴇʀʀᴏʀ ᴍᴜᴛᴇ ᴜꜱᴇʀ %s ɪɴ ᴄʜᴀᴛ %s (%s) ᴅᴜᴇ ᴛᴏ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴡᴇʟʟ ᴅᴀᴍɴ, ɪ ᴄᴀɴ'ᴛ ᴍᴜᴛᴇ ᴛʜᴀᴛ ᴜꜱᴇʀ.")


@bot_admin
def runmute(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    if not args:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴄʜᴀᴛ/ᴜꜱᴇʀ.")
        return

    user_id, chat_id = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(
            "You ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ a ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ID ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ..",
        )
        return
    if not chat_id:
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ a ᴄʜᴀᴛ.")
        return

    try:
        chat = bot.get_chat(chat_id.split()[0])
    except BadRequest as excp:
        if excp.message == "Chat not found":
            message.reply_text(
                "ᴄʜᴀᴛ ɴᴏᴛ ғᴏᴜɴᴅ! ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴀ ᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ ᴀɴᴅ I'm ᴘᴀʀᴛ of ᴛʜᴀᴛ ᴄʜᴀᴛ.",
            )
            return
        raise

    if chat.type == "private":
        message.reply_text("I'ᴍ ꜱᴏʀʀʏ, ʙᴜᴛ ᴛʜᴀᴛ'ꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ!")
        return

    if (
        not is_bot_admin(chat, bot.id)
        or not chat.get_member(bot.id).can_restrict_members
    ):
        message.reply_text(
            "I ᴄᴀɴ'ᴛ ᴜɴʀᴇꜱᴛʀɪᴄᴛ ᴘᴇᴏᴘʟᴇ ᴛʜᴇʀᴇ! ᴍᴀᴋᴇ ꜱᴜʀᴇ I'ᴍ ᴀᴅᴍɪɴ ᴀɴᴅ ᴄᴀɴ ᴜɴʙᴀɴ ᴜꜱᴇʀꜱ.",
        )
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "ᴜꜱᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ":
            message.reply_text("I ᴄᴀɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ғɪɴᴅ ᴛʜɪꜱ ᴜꜱᴇʀ ᴛʜᴇʀᴇ")
            return
        raise

    if is_user_in_chat(chat, user_id):
        if (
            member.can_send_messages
            and member.can_send_media_messages
            and member.can_send_other_messages
            and member.can_add_web_page_previews
        ):
            message.reply_text("ᴛʜɪꜱ ᴜꜱᴇʀ ᴀʟʀᴇᴀᴅʏ ʜᴀꜱ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ꜱᴘᴇᴀᴋ ɪɴ ᴛʜᴀᴛ ᴄʜᴀᴛ.")
            return

    if user_id == bot.id:
        message.reply_text("I'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ᴜɴᴍᴜᴛᴇ ᴍʏꜱᴇʟғ, I'ᴍ ᴀɴ ᴀᴅᴍɪɴ ᴛʜᴇʀᴇ!")
        return

    try:
        bot.restrict_chat_member(
            chat.id,
            int(user_id),
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            ),
        )
        message.reply_text("ʏᴇᴘ, ᴛʜɪꜱ ᴜꜱᴇʀ ᴄᴀɴ ᴛᴀʟᴋ ɪɴ ᴛʜᴀᴛ ᴄʜᴀᴛ!")
    except BadRequest as excp:
        if excp.message == "ʀᴇᴘʟʏ ᴍᴇꜱꜱᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
            # Do not reply
            message.reply_text("Unmuted!", quote=False)
        elif excp.message in RUNMUTE_ERRORS:
            message.reply_text(excp.message)
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ᴇʀʀᴏʀ ᴜɴᴍɴᴜᴛɪɴɢ ᴜꜱᴇʀ %s ɪɴ ᴄʜᴀᴛ %s (%s) ᴅᴜᴇ ᴛᴏ %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("ᴡᴇ'ʟʟ ᴅᴀᴍɴ, I ᴄᴀɴ'ᴛ ᴜɴᴍᴜᴛᴇ ᴛʜᴀᴛ ᴜꜱᴇʀ.")


RBAN_HANDLER = CommandHandler(
    "rban", rban, filters=CustomFilters.sudo_filter, run_async=True
)
RUNBAN_HANDLER = CommandHandler(
    "runban", runban, filters=CustomFilters.sudo_filter, run_async=True
)
RKICK_HANDLER = CommandHandler(
    "rpunch", rkick, filters=CustomFilters.sudo_filter, run_async=True
)
RMUTE_HANDLER = CommandHandler(
    "rmute", rmute, filters=CustomFilters.sudo_filter, run_async=True
)
RUNMUTE_HANDLER = CommandHandler(
    "runmute", runmute, filters=CustomFilters.sudo_filter, run_async=True
)

dispatcher.add_handler(RBAN_HANDLER)
dispatcher.add_handler(RUNBAN_HANDLER)
dispatcher.add_handler(RKICK_HANDLER)
dispatcher.add_handler(RMUTE_HANDLER)
dispatcher.add_handler(RUNMUTE_HANDLER)
