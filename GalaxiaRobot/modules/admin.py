# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.utils.helpers import mention_html

from GalaxiaRobot import DRAGONS, SUPPORT_CHAT, dispatcher
from GalaxiaRobot.modules.disable import DisableAbleCommandHandler
from GalaxiaRobot.modules.helper_funcs.admin_rights import user_can_changeinfo
from GalaxiaRobot.modules.helper_funcs.alternate import send_message
from GalaxiaRobot.modules.helper_funcs.chat_status import (
    ADMIN_CACHE,
    bot_admin,
    can_pin,
    can_promote,
    connection_status,
    user_admin,
)
from GalaxiaRobot.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from GalaxiaRobot.modules.log_channel import loggable


@bot_admin
@user_admin
def set_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("ʏᴏᴜ'ʀᴇ ᴍɪꜱꜱɪɴɢ ʀɪɢʜᴛꜱ ᴛᴏ ᴄʜᴀɴɢᴇ ᴄʜᴀᴛ ɪɴғᴏ!🤧")

    if msg.reply_to_message:
        if not msg.reply_to_message.sticker:
            return msg.reply_text(
                "ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ꜱᴏᴍᴇ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ꜱᴇᴛ ᴄʜᴀᴛ ꜱᴛɪᴄᴋᴇʀ ꜱᴇᴛ😏 !"
            )
        stkr = msg.reply_to_message.sticker.set_name
        try:
            context.bot.set_chat_sticker_set(chat.id, stkr)
            msg.reply_text(f"ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ set ɴᴇᴡ ɢʀᴏᴜᴘ ꜱᴛɪᴄᴋᴇʀꜱ ɪɴ {chat.title}!😙")
        except BadRequest as excp:
            if excp.message == "Participants_too_few":
                return msg.reply_text(
                    "ꜱᴏʀʀʏ, ᴅᴜᴇ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ʀᴇꜱᴛʀɪᴄᴛɪᴏɴꜱ ᴄʜᴀᴛ ɴᴇᴇᴅꜱ ᴛᴏ ʜᴀᴠᴇ ᴍɪɴɪᴍᴜᴍ 100 ᴍᴇᴍʙᴇʀꜱ ʙᴇғᴏʀᴇ ᴛʜᴇʏ ᴄᴀɴ ʜᴀᴠᴇ ɢʀᴏᴜᴘ ꜱᴛɪᴄᴋᴇʀꜱ🤐!"
                )
            msg.reply_text(f"Error! {excp.message}.")
    else:
        msg.reply_text("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ꜱᴏᴍᴇ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ꜱᴇᴛ ᴄʜᴀᴛ ꜱᴛɪᴄᴋᴇʀ ꜱᴇᴛ. 🤭!")


@bot_admin
@user_admin
def setchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("ʏᴏᴜ ᴀʀᴇ ᴍɪꜱꜱɪɴɢ ʀɪɢʜᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴғᴏ! 🤧")
        return

    if msg.reply_to_message:
        if msg.reply_to_message.photo:
            pic_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            pic_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ꜱᴇᴛ ꜱᴏᴍᴇ ᴘʜᴏᴛᴏ ᴀꜱ ᴄʜᴀᴛ ᴘɪᴄ 🧐!")
            return
        dlmsg = msg.reply_text("Just a sec...")
        tpic = context.bot.get_file(pic_id)
        tpic.download("gpic.png")
        try:
            with open("gpic.png", "rb") as chatp:
                context.bot.set_chat_photo(int(chat.id), photo=chatp)
                msg.reply_text("ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ꜱᴇᴛ ɴᴇᴡ ᴄʜᴀᴛᴘɪᴄ! ✌️")
        except BadRequest as excp:
            msg.reply_text(f"Error! {excp.message}")
        finally:
            dlmsg.delete()
            if os.path.isfile("gpic.png"):
                os.remove("gpic.png")
    else:
        msg.reply_text("ʀᴇᴘʟʏ ᴛᴏ ꜱᴏᴍᴇ ᴘʜᴏᴛᴏ ᴏʀ ғɪʟᴇ ᴛᴏ ꜱᴇᴛ ɴᴇᴡ ᴄʜᴀᴛ ᴘɪᴄ 🙆‍♂️!")


@bot_admin
@user_admin
def rmchatpic(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ 👴")
        return
    try:
        context.bot.delete_chat_photo(int(chat.id))
        msg.reply_text("ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴄʜᴀᴛ'ꜱ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ 🙎‍♂️!")
    except BadRequest as excp:
        msg.reply_text(f"Error! {excp.message}.")
        return


@bot_admin
@user_admin
def set_desc(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        return msg.reply_text("ʏᴏᴜ'ʀᴇ ᴍɪꜱꜱɪɴɢ ʀɪɢʜᴛꜱ ᴛᴏ ᴄʜᴀɴɢᴇ ᴄʜᴀᴛ ɪɴғᴏ 😬!")

    tesc = msg.text.split(None, 1)
    if len(tesc) >= 2:
        desc = tesc[1]
    else:
        return msg.reply_text("ꜱᴇᴛᴛɪɴɢ ᴇᴍᴘᴛʏ ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ ᴡᴏɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ!")
    try:
        if len(desc) > 255:
            return msg.reply_text(
                "ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ ᴍᴜꜱᴛ ɴᴇᴇᴅꜱ ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ 255 ᴄʜᴀʀᴀᴄᴛᴇʀ'ꜱ 🥴!"
            )
        context.bot.set_chat_description(chat.id, desc)
        msg.reply_text(f"ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴜᴘᴅᴀᴛᴇᴅ ᴄʜᴀᴛ ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ ɪɴ {chat.title} 🤓!")
    except BadRequest as excp:
        msg.reply_text(f"ᴇʀʀᴏʀ ☹️! {excp.message}.")


@bot_admin
@user_admin
def setchat_title(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    args = context.args

    if user_can_changeinfo(chat, user, context.bot.id) is False:
        msg.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ʀɪɢʜᴛꜱ ᴛᴏ ᴄʜᴀɴɢᴇ ᴄʜᴀᴛ ɪɴғᴏ 🤓!")
        return

    title = " ".join(args)
    if not title:
        msg.reply_text("ᴇɴᴛᴇʀ ꜱᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ꜱᴇᴛ ɴᴇᴡ ᴛɪᴛʟᴇ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ 😎!")
        return

    try:
        context.bot.set_chat_title(int(chat.id), str(title))
        msg.reply_text(
            f"ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ꜱᴇᴛ <b>{title}</b> ᴀꜱ ɴᴇᴡ ᴄʜᴀᴛ ᴛɪᴛʟᴇ 🙋‍♂️!",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest as excp:
        msg.reply_text(f"ᴇʀʀᴏʀ 😔! {excp.message}.")
        return


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def promote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇꜱꜱᴀʀʏ ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ 😏!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ.🙄.",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ("administrator", "creator"):
        message.reply_text(
            "ʜᴏᴡ ᴀᴍ ɪ ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ? 🙃"
        )
        return

    if user_id == bot.id:
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴍʏꜱᴇʟғ ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ғᴏʀ ᴍᴇ 🥰.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴡʜᴏ ɪꜱɴ'ᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.. 🤭")
        else:
            message.reply_text("An error occured while promoting.")
        return

    bot.sendMessage(
        chat.id,
        f"ᴘʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜꜱᴇʀ ɪɴ <b>{chat.title}</b>\n\nᴜꜱᴇʀ: {mention_html(user_member.user.id, user_member.user.first_name)}\nᴀᴅᴍɪɴ: {mention_html(user.id, user.first_name)}",
        parse_mode=ParseMode.HTML,
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#PROMOTED\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def lowpromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ᴛʜᴇ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇꜱꜱᴀʀʏ ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ 😑!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ɪᴅ ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ.🤭.",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ("administrator", "creator"):
        message.reply_text(
            "ʜᴏᴡ ᴀᴍ ɪ ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ? 🤔"
        )
        return

    if user_id == bot.id:
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴍʏ ꜱᴇʟғ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ғᴏʀ ᴍᴇ. 🥰 .")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_pin_messages=bot_member.can_pin_messages,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴡʜᴏ ɪꜱɴ'ᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ. 🤭.")
        else:
            message.reply_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴍᴏᴛɪɴɢ.")
        return

    bot.sendMessage(
        chat.id,
        f"ʟᴏᴡ ᴘʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜꜱᴇʀ ɪɴ <b>{chat.title}<b>\n\nᴜꜱᴇʀ: {mention_html(user_member.user.id, user_member.user.first_name)}\nᴀᴅᴍɪɴ: {mention_html(user.id, user.first_name)}",
        parse_mode=ParseMode.HTML,
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#LOWPROMOTED\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def fullpromote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    promoter = chat.get_member(user.id)

    if (
        not (promoter.can_promote_members or promoter.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇꜱꜱᴀʀʏ ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ 🙃!")
        return

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ID ꜱᴘᴇᴄɪғɪᴇᴅ is incorrect..",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status in ("administrator", "creator"):
        message.reply_text(
            "ʜᴏᴡ ᴀᴍ ɪ ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ? 😦"
        )
        return

    if user_id == bot.id:
        message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ᴍʏ ꜱᴇʟғ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ғᴏʀ ᴍᴇ 🥰.")
        return

    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = chat.get_member(bot.id)

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
        )
    except BadRequest as err:
        if err.message == "User_not_mutual_contact":
            message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴡʜᴏ ɪꜱɴ'ᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ 😐.")
        else:
            message.reply_text("An error occured while promoting.")
        return

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ᴅᴇᴍᴏᴛᴇ", callback_data="demote_({})".format(user_member.user.id)
                )
            ]
        ]
    )

    bot.sendMessage(
        chat.id,
        f"ғᴜʟʟ ᴘʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜꜱᴇʀ ɪɴ <b>{chat.title}</b>\n\n<b>ᴜꜱᴇʀ: {mention_html(user_member.user.id, user_member.user.first_name)}</b>\n<b>ᴘʀᴏᴍᴏᴛᴇʀ: {mention_html(user.id, user.first_name)}</b>",
        parse_mode=ParseMode.HTML,
    )

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#FULLPROMOTED\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@bot_admin
@can_promote
@user_admin
@loggable
def demote(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ᴛʜᴇ ID ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ .🙄.",
        )
        return

    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if user_member.status == "creator":
        message.reply_text("ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ CREATED ᴛʜᴇ chat, ʜᴏᴡ ᴡᴏᴜʟᴅ I ᴅᴇᴍᴏᴛᴇ ᴛʜᴇᴍ ʙᴄ 😖")
        return

    if not user_member.status == "administrator":
        message.reply_text("ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴡʜᴀᴛ ᴡᴀꜱɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇᴅ! 🤫")
        return

    if user_id == bot.id:
        message.reply_text("ɪ ᴄᴀɴ'ᴛ demote ᴍʏ ꜱᴇʟғ! ɢᴇᴛ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴅᴏ ɪᴛ ғᴏʀ ᴍᴇ.🙃.")
        return

    try:
        bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_voice_chats=False,
        )

        bot.sendMessage(
            chat.id,
            f"ꜱᴜᴄᴇꜱꜱғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ ᴀ ᴀᴅᴍɪɴꜱ ɪɴ <b>{chat.title}</b>\n\nᴀᴅᴍɪɴ: <b>{mention_html(user_member.user.id, user_member.user.first_name)}</b>\nᴅᴇᴍᴏᴛᴇʀ: {mention_html(user.id, user.first_name)}",
            parse_mode=ParseMode.HTML,
        )

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#DEMOTED\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>ᴜꜱᴇʀ:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
        )

        return log_message
    except BadRequest:
        message.reply_text(
            "ᴄᴏᴜʟᴅ ɴᴏᴛ ᴅᴇᴍᴏᴛᴇ. ɪ ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀᴅᴍɪɴ, ᴏʀ ᴛʜᴇ ᴀᴅᴍɪɴ ꜱᴛᴀᴛᴜꜱ ᴡᴀꜱ ᴀᴘᴘᴏɪɴᴛᴇᴅ ʙʏ ᴀɴᴏᴛʜᴇʀ"
            " ᴜꜱᴇʀ, ꜱᴏ ɪ ᴄᴀɴ'ᴛ ᴀᴄᴛ ᴜᴘᴏɴ ᴛʜᴇᴍ!",
        )
        return


@user_admin
def refresh_admin(update, _):
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass

    update.effective_message.reply_text(" 🥰 ᴀᴅᴍɪɴꜱ ᴄᴀᴄʜᴇ ʀᴇғʀᴇꜱʜᴇᴅ ʙᴀʙʏ 🥰!")


@connection_status
@bot_admin
@can_promote
@user_admin
def set_title(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message

    user_id, title = extract_user_and_text(message, args)
    try:
        user_member = chat.get_member(user_id)
    except:
        return

    if not user_id:
        message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ꜱᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜꜱᴇʀ or the ɪᴅ ꜱᴘᴇᴄɪғɪᴇᴅ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛ.🙄.",
        )
        return

    if user_member.status == "creator":
        message.reply_text(
            "ᴛʜɪꜱ ᴘᴇʀꜱᴏɴ CREATED ᴛʜᴇ ᴄʜᴀᴛ, ʜᴏᴡ ᴄᴀɴ i ꜱᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴛɪᴛʟᴇ ғᴏʀ ʜɪᴍ? 😉",
        )
        return

    if user_member.status != "administrator":
        message.reply_text(
            "ᴄᴀɴ'ᴛ ꜱᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ ɴᴏɴ-ᴀᴅᴍɪɴꜱ!\nᴘʀᴏᴍᴏᴛᴇ ᴛʜᴇᴍ ғɪʀꜱᴛ ᴛᴏ ꜱᴇᴛ ᴄᴜꜱᴛᴏᴍ ᴛɪᴛʟᴇ 😇!",
        )
        return

    if user_id == bot.id:
        message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ꜱᴇᴛ ᴍʏ ᴏᴡɴ ᴛɪᴛʟᴇ ᴍʏꜱᴇʟғ! ɢᴇᴛ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴍᴀᴅᴇ ᴍᴇ admin ᴛᴏ ᴅᴏ ɪᴛ for ᴍᴇ.🤩",
        )
        return

    if not title:
        message.reply_text("ꜱᴇᴛᴛɪɴɢ ʙʟᴀɴᴋ ᴛɪᴛʟᴇ ᴅᴏᴇꜱɴ'ᴛ ᴅᴏ ᴀɴʏᴛʜɪɴɢ!")
        return

    if len(title) > 16:
        message.reply_text(
            "ᴛʜᴇ ᴛɪᴛʟᴇ ʟᴇɴɢᴛʜ ɪꜱ ʟᴏɴɢᴇʀ ᴛʜᴀɴ 16 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ.\nᴛʀᴜɴᴄᴀᴛɪɴɢ ɪᴛ ᴛᴏ 16 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ 😊.",
        )

    try:
        bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
    except BadRequest:
        message.reply_text(
            "ᴇɪᴛʜᴇʀ ᴛʜᴇʏ ᴀʀᴇɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ ʙʏ ᴏʀ ʏᴏᴜ ꜱᴇᴛ ᴀ ᴛɪᴛʟᴇ ᴛᴇxᴛ ᴛʜᴀᴛ ɪꜱ ɪᴍᴘᴏꜱꜱɪʙʟᴇ ᴛᴏ ꜱᴇᴛ. 😉"
        )
        return

    bot.sendMessage(
        chat.id,
        f"ꜱᴜᴄᴇꜱꜱғᴜʟʟʏ ꜱᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ <code>{user_member.user.first_name or user_id}</code> "
        f"to <code>{html.escape(title[:16])}</code>!",
        parse_mode=ParseMode.HTML,
    )


@bot_admin
@can_pin
@user_admin
@loggable
def pin(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    user = update.effective_user
    chat = update.effective_chat
    msg = update.effective_message
    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id

    if msg.chat.username:
        # If chat has a username, use this format
        link_chat_id = msg.chat.username
        message_link = f"https://t.me/{link_chat_id}/{msg_id}"
    elif (str(msg.chat.id)).startswith("-100"):
        # If chat does not have a username, use this
        link_chat_id = (str(msg.chat.id)).replace("-100", "")
        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}"

    is_group = chat.type not in ("private", "channel")
    prev_message = update.effective_message.reply_to_message

    if prev_message is None:
        msg.reply_text("Reply a message to pin it!")
        return

    is_silent = True
    if len(args) >= 1:
        is_silent = (
            args[0].lower() != "notify"
            or args[0].lower() == "loud"
            or args[0].lower() == "violent"
        )

    if prev_message and is_group:
        try:
            bot.pinChatMessage(
                chat.id, prev_message.message_id, disable_notification=is_silent
            )
            msg.reply_text(
                f"ɪ ʜᴀᴠᴇ ᴘɪɴɴᴇᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ 👍.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✦ ɢᴏ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ ✦", url=f"{message_link}")]]
                ),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except BadRequest as excp:
            if excp.message != "Chat_not_modified":
                raise

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"MESSAGE-PINNED-SUCCESSFULLY\n"
            f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

        return log_message


@bot_admin
@can_pin
@user_admin
@loggable
def unpin(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message
    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id
    unpinner = chat.get_member(user.id)

    if (
        not (unpinner.can_pin_messages or unpinner.status == "creator")
        and user.id not in DRAGONS
    ):
        message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇꜱꜱᴀʀʏ ʀɪɢʜᴛꜱ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ ✊!")
        return

    if msg.chat.username:
        # If chat has a username, use this format
        link_chat_id = msg.chat.username
        message_link = f"https://t.me/{link_chat_id}/{msg_id}"
    elif (str(msg.chat.id)).startswith("-100"):
        # If chat does not have a username, use this
        link_chat_id = (str(msg.chat.id)).replace("-100", "")
        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}"

    is_group = chat.type not in ("private", "channel")
    prev_message = update.effective_message.reply_to_message

    if prev_message and is_group:
        try:
            context.bot.unpinChatMessage(chat.id, prev_message.message_id)
            msg.reply_text(
                f"ᴜɴᴘɪɴɴᴇᴅ <a href='{message_link}'>this message</a>.",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except BadRequest as excp:
            if excp.message != "Chat_not_modified":
                raise

    if not prev_message and is_group:
        try:
            context.bot.unpinChatMessage(chat.id)
            msg.reply_text("ᴜɴᴘɪɴɴᴇᴅ ᴛʜᴇ ʟᴀꜱᴛ ᴘɪɴɴᴇᴅ ᴍᴇꜱꜱᴀɢᴇ.")
        except BadRequest as excp:
            if excp.message == "ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴜɴᴘɪɴ ɴᴏᴛ ғᴏᴜɴᴅ":
                msg.reply_text(
                    "ɪ ᴄᴀɴ'ᴛ ꜱᴇᴇ ᴘɪɴɴᴇᴅ ᴍᴇꜱꜱᴀɢᴇ, ᴍᴀʏʙᴇ ᴀʟʀᴇᴀᴅʏ ᴜɴᴘɪɴᴇᴅ, ᴏʀ ᴘɪɴ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴏʟᴅ 🙂"
                )
            else:
                raise

    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"MESSAGE-UNPINNED-SUCCESSFULLY\n"
        f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, html.escape(user.first_name))}"
    )

    return log_message


@bot_admin
def pinned(update: Update, context: CallbackContext) -> str:
    bot = context.bot
    msg = update.effective_message
    msg_id = (
        update.effective_message.reply_to_message.message_id
        if update.effective_message.reply_to_message
        else update.effective_message.message_id
    )

    chat = bot.getChat(chat_id=msg.chat.id)
    if chat.pinned_message:
        pinned_id = chat.pinned_message.message_id
        if msg.chat.username:
            link_chat_id = msg.chat.username
            message_link = f"https://t.me/{link_chat_id}/{pinned_id}"
        elif (str(msg.chat.id)).startswith("-100"):
            link_chat_id = (str(msg.chat.id)).replace("-100", "")
            message_link = f"https://t.me/c/{link_chat_id}/{pinned_id}"

        msg.reply_text(
            f"↬ ᴘɪɴɴᴇᴅ ᴏɴ {html.escape(chat.title)}.",
            reply_to_message_id=msg_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="✦ ɢᴏ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ ✦",
                            url=f"https://t.me/{link_chat_id}/{pinned_id}",
                        )
                    ]
                ]
            ),
        )

    else:
        msg.reply_text(
            f"ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴘɪɴɴᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ɪɴ <b>{html.escape(chat.title)}!</b>",
            parse_mode=ParseMode.HTML,
        )


@bot_admin
@user_admin
@connection_status
def invite(update: Update, context: CallbackContext):
    bot = context.bot
    chat = update.effective_chat

    if chat.username:
        update.effective_message.reply_text(f"https://t.me/{chat.username}")
    elif chat.type in [chat.SUPERGROUP, chat.CHANNEL]:
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = bot.exportChatInviteLink(chat.id)
            update.effective_message.reply_text(invitelink)
        else:
            update.effective_message.reply_text(
                "ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴛʜᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋ, ᴛʀʏ ᴄʜᴀɴɢɪɴɢ ᴍʏ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ 👊!",
            )
    else:
        update.effective_message.reply_text(
            "ɪ ᴄᴀɴ ᴏɴʟʏ ɢɪᴠᴇ ʏᴏᴜ ɪɴᴠɪᴛᴇ ʟɪɴᴋꜱ ғᴏʀ ꜱᴜᴘᴇʀɢʀᴏᴜᴘꜱ ᴀɴᴅ ᴄʜᴀɴɴᴇʟꜱ, ꜱᴏʀʀʏ 🙄!",
        )


@connection_status
def adminlist(update, context):
    chat = update.effective_chat  # type: Optional[Chat] -> unused variable
    user = update.effective_user  # type: Optional[User]
    args = context.args  # -> unused variable
    bot = context.bot

    if update.effective_message.chat.type == "private":
        send_message(update.effective_message, "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋꜱ ɪɴ ɢʀᴏᴜᴘꜱ 😉.")
        return

    update.effective_chat
    chat_id = update.effective_chat.id
    chat_name = update.effective_message.chat.title  # -> unused variable

    try:
        msg = update.effective_message.reply_text(
            "ғᴇᴛᴄʜɪɴɢ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ...",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest:
        msg = update.effective_message.reply_text(
            "ғᴇᴛᴄʜɪɴɢ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ...",
            quote=False,
            parse_mode=ParseMode.HTML,
        )

    administrators = bot.getChatAdministrators(chat_id)
    text = "ᴀᴅᴍɪɴꜱ ɪɴ <b>{}</b>:".format(html.escape(update.effective_chat.title))

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == "":
            name = "☠ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(user.first_name + " " + (user.last_name or "")),
                ),
            )

        if user.is_bot:
            administrators.remove(admin)
            continue

        # if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "creator":
            text += "\n ↬ ᴄʀᴇᴀᴛᴏʀ:"
            text += "\n\n<code> • </code>{}\n\n".format(name)

            if custom_title:
                text += f"<code> ┗━ {html.escape(custom_title)}</code>\n\n"

    text += "\n\n➳ ᴀᴅᴍɪɴꜱ:"

    custom_admin_list = {}
    normal_admin_list = []

    for admin in administrators:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title

        if user.first_name == "":
            name = "☠ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ"
        else:
            name = "{}".format(
                mention_html(
                    user.id,
                    html.escape(user.first_name + " " + (user.last_name or "")),
                ),
            )
        # if user.username:
        #    name = escape_markdown("@" + user.username)
        if status == "administrator":
            if custom_title:
                try:
                    custom_admin_list[custom_title].append(name)
                except KeyError:
                    custom_admin_list.update({custom_title: [name]})
            else:
                normal_admin_list.append(name)

    for admin in normal_admin_list:
        text += "\n\n<code> • </code>{}\n".format(admin)

    for admin_group in custom_admin_list.copy():
        if len(custom_admin_list[admin_group]) == 1:
            text += "\n<code> • </code>{} | <code>{}</code>\n".format(
                custom_admin_list[admin_group][0],
                html.escape(admin_group),
            )
            custom_admin_list.pop(admin_group)

    text += "\n"
    for admin_group, value in custom_admin_list.items():
        text += "\n🚨 <code>{}</code>\n".format(admin_group)
        for admin in value:
            text += "\n<code> • </code>{}\n".format(admin)
        text += "\n\n"

    try:
        msg.edit_text(text, parse_mode=ParseMode.HTML)
    except BadRequest:  # if original message is deleted
        return


@bot_admin
@can_promote
@user_admin
@loggable
def button(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    bot: Optional[Bot] = context.bot
    match = re.match(r"demote_\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        member = chat.get_member(user_id)
        bot_member = chat.get_member(bot.id)
        bot_permissions = promoteChatMember(
            chat.id,
            user_id,
            can_change_info=bot_member.can_change_info,
            can_post_messages=bot_member.can_post_messages,
            can_edit_messages=bot_member.can_edit_messages,
            can_delete_messages=bot_member.can_delete_messages,
            can_invite_users=bot_member.can_invite_users,
            can_promote_members=bot_member.can_promote_members,
            can_restrict_members=bot_member.can_restrict_members,
            can_pin_messages=bot_member.can_pin_messages,
            can_manage_voice_chats=bot_member.can_manage_voice_chats,
        )
        demoted = bot.promoteChatMember(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_voice_chats=False,
        )
        if demoted:
            update.effective_message.edit_text(
                f"ᴀᴅᴍɪɴ {mention_html(user.id, user.first_name)} \nᴅᴇᴍᴏᴛᴇᴅ {mention_html(member.user.id, member.user.first_name)}!",
                parse_mode=ParseMode.HTML,
            )
            query.answer("ᴅᴇᴍᴏᴛᴇᴅ!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#DEMOTE\n"
                f"<b>ᴀᴅᴍɪɴ:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>ᴜꜱᴇʀ:</b> {mention_html(member.user.id, member.user.first_name)}"
            )
    else:
        update.effective_message.edit_text(
            "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴘʀᴏᴍᴏᴛᴇᴅ ᴏʀ ʜᴀꜱ ʟᴇғᴛ ᴛʜᴇ ɢʀᴏᴜᴘ 🤫!"
        )
        return ""


@connection_status
def bug_reporting(update: Update, _: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    update.effective_user
    bot = dispatcher.bot
    invitelink = bot.exportChatInviteLink(chat.id)
    puki = msg.text.split(None, 1)
    if len(puki) >= 2:
        bugnya = puki[1]
    else:
        msg.reply_text(
            "❌ <b>ʏᴏᴜ ᴍᴜꜱᴛ ꜱᴘᴇᴄɪғʏ ᴛʜᴇ ʙᴜɢ ᴛᴏ ʀᴇᴘᴏʀᴛ.</b>\n • ᴇxᴀᴍᴘʟᴇ: <code>/bug ᴛʜᴇɴ ᴡʜᴀᴛ ᴀ ᴇʀʀᴏʀ .</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    try:
        if len(bugnya) > 100:
            return msg.reply_text("ʙᴜɢ ᴍᴜꜱᴛ ɴᴇᴇᴅꜱ ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ 100 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ 😉!")
        bot.sendMessage(
            chat.id,
            f"✅ ʏᴏᴜʀ ʙᴜɢ ᴡᴀꜱ ꜱᴜʙᴍɪᴛᴛᴇᴅ ᴛᴏ <b>ʙᴏᴛ ᴀᴅᴍɪɴꜱ</b>. ᴛʜᴀɴᴋꜱ ғᴏʀ ʀᴇᴘᴏʀᴛɪɴɢ ᴛʜᴇ ʙᴜɢ. \nʟᴏᴠᴇ ғʀᴏᴍ @Abishnoi1M.",
            parse_mode=ParseMode.HTML,
        )
        if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
            try:
                bot.sendMessage(
                    f"@{SUPPORT_CHAT}",
                    f"📣 <b>ɴᴇᴡ ʙᴜɢ ʀᴇᴘᴏʀᴛᴇᴅ.</b>\n\n<b>Chat:</b> <a href='{invitelink}'>{chat.title}</a>\n<b>ɴᴀᴍᴇ:</b> <a href='tg://user?id={msg.from_user.id}'>{mention_html(msg.from_user.id, msg.from_user.first_name)}</a>\n<b>ᴜꜱᴇʀ ID:</b> <code>{msg.from_user.id}</code>\n<b>Chat id:</b> <code>{chat.id}</code>\n\nᴄᴏɴᴛᴇɴᴛ ᴏғ ᴛʜᴇ ʀᴇᴘᴏʀᴛ:\n{bugnya}",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("✦ ɢᴏ ᴛᴏ ᴍᴇꜱᴀᴀɢᴇ ✦", url=f"{msg.link}")]]
                    ),
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Unauthorized:
                LOGGER.warning(
                    "ʙᴏᴛ ɪꜱɴ'ᴛ ᴀʙʟᴇ ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ support_chat, ɢᴏ ᴀɴᴅ ᴄʜᴇᴄᴋ !"
                )
            except BadRequest as e:
                LOGGER.warning(e.message)
    except BadRequest:
        pass


SET_DESC_HANDLER = CommandHandler(
    "setdesc", set_desc, filters=Filters.chat_type.groups, run_async=True
)
SET_STICKER_HANDLER = CommandHandler(
    "setsticker", set_sticker, filters=Filters.chat_type.groups, run_async=True
)
SETCHATPIC_HANDLER = CommandHandler(
    "setgpic", setchatpic, filters=Filters.chat_type.groups, run_async=True
)
RMCHATPIC_HANDLER = CommandHandler(
    "delgpic", rmchatpic, filters=Filters.chat_type.groups, run_async=True
)
SETCHAT_TITLE_HANDLER = CommandHandler(
    "setgtitle", setchat_title, filters=Filters.chat_type.groups, run_async=True
)

ADMINLIST_HANDLER = DisableAbleCommandHandler(
    ["admins", "adminlist"], adminlist, run_async=True
)
BUG_HANDLER = DisableAbleCommandHandler("bug", bug_reporting, run_async=True)

PIN_HANDLER = CommandHandler(
    "pin", pin, filters=Filters.chat_type.groups, run_async=True
)
UNPIN_HANDLER = CommandHandler(
    "unpin", unpin, filters=Filters.chat_type.groups, run_async=True
)
PINNED_HANDLER = CommandHandler(
    "pinned", pinned, filters=Filters.chat_type.groups, run_async=True
)

INVITE_HANDLER = DisableAbleCommandHandler(
    ["invitelink", "link"], invite, run_async=True
)

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote, run_async=True)
FULLPROMOTE_HANDLER = DisableAbleCommandHandler(
    "fullpromote", fullpromote, run_async=True
)
LOW_PROMOTE_HANDLER = DisableAbleCommandHandler(
    ["lowpromote", "spromote"], lowpromote, run_async=True
)
DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote, run_async=True)

SET_TITLE_HANDLER = CommandHandler("title", set_title, run_async=True)
ADMIN_REFRESH_HANDLER = CommandHandler(
    ["admincache", "reload"],
    refresh_admin,
    filters=Filters.chat_type.groups,
    run_async=True,
)

dispatcher.add_handler(SET_DESC_HANDLER)
dispatcher.add_handler(SET_STICKER_HANDLER)
dispatcher.add_handler(SETCHATPIC_HANDLER)
dispatcher.add_handler(RMCHATPIC_HANDLER)
dispatcher.add_handler(SETCHAT_TITLE_HANDLER)
dispatcher.add_handler(ADMINLIST_HANDLER)
dispatcher.add_handler(PIN_HANDLER)
dispatcher.add_handler(UNPIN_HANDLER)
dispatcher.add_handler(BUG_HANDLER)
dispatcher.add_handler(PINNED_HANDLER)
dispatcher.add_handler(INVITE_HANDLER)
dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(FULLPROMOTE_HANDLER)
dispatcher.add_handler(LOW_PROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(SET_TITLE_HANDLER)
dispatcher.add_handler(ADMIN_REFRESH_HANDLER)


__mod_name__ = "𝙰ᴅᴍɪɴs 😎"

__help__ = """
*ᴜꜱᴇʀ ᴄᴏᴍᴍᴀɴᴅꜱ*:
❂ /admins*:* ʟɪꜱᴛ ᴏғ ᴀᴅᴍɪɴꜱ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ

❂ /pinned*:* ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘɪɴɴᴇᴅ ᴍᴇꜱꜱᴀɢᴇ.

*ᴀᴅᴍɪɴꜱ ᴏɴʟʏ:* 
❂ /pin*:* ꜱɪʟᴇɴᴛʟʏ ᴘɪɴꜱ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ - ᴀᴅᴅ 'loud' ᴏʀ 'notify' ᴛᴏ ɢɪᴠᴇ ɴᴏᴛɪғꜱ ᴛᴏ ᴜꜱᴇʀꜱ

❂ /unpin*:* ᴜɴᴘɪɴꜱ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴘɪɴɴᴇᴅ ᴍᴇꜱꜱᴀɢᴇ

❂ /invitelink*:* ɢᴇᴛꜱ ɪɴᴠɪᴛᴇʟɪɴᴋ

❂ /promote*:* ᴘʀᴏᴍᴏᴛᴇꜱ ᴛʜᴇ ᴜꜱᴇʀ ʀᴇᴘʟɪᴇᴅ ᴛᴏ

❂ /fullpromote*:* ᴘʀᴏᴍᴏᴛᴇꜱ ᴛʜᴇ ᴜꜱᴇʀ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴡɪᴛʜ ғᴜʟʟ ʀɪɢʜᴛꜱ

❂ /demote*:* ᴅᴇᴍᴏᴛᴇꜱ ᴛʜᴇ ᴜꜱᴇʀ ʀᴇᴘʟɪᴇᴅ ᴛᴏ

❂ /title <title here>*:* ꜱᴇᴛꜱ ᴀ ᴄᴜꜱᴛᴏᴍ ᴛɪᴛʟᴇ ғᴏʀ ᴀɴ ᴀᴅᴍɪɴ ᴛʜᴀᴛ ᴛʜᴇ ʙᴏᴛ ᴘʀᴏᴍᴏᴛᴇᴅ

❂ /admincache*:* ғᴏʀᴄᴇ ʀᴇғʀᴇꜱʜ ᴛʜᴇ ᴀᴅᴍɪɴꜱ ʟɪꜱᴛ

❂ /del*:* ᴅᴇʟᴇᴛᴇꜱ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ʏᴏᴜ ʀᴇᴘʟɪᴇᴅ ᴛᴏ

❂ /purge*:* ᴅᴇʟᴇᴛᴇꜱ ᴀʟʟ ᴍᴇꜱꜱᴀɢᴇꜱ ʙᴇᴛᴡᴇᴇɴ ᴛʜɪꜱ ᴀɴᴅ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴍᴇꜱꜱᴀɢᴇ.

❂ /purge <integer X>*:* ᴅᴇʟᴇᴛᴇꜱ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ, ᴀɴᴅ X ᴍᴇꜱꜱᴀɢᴇꜱ ғᴏʟʟᴏᴡɪɴɢ ɪᴛ ɪғ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ.

❂ /setgtitle <text>*:* ꜱᴇᴛ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ

❂ /setgpic*:* ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ ᴛᴏ ꜱᴇᴛ ᴀꜱ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ

❂ /setdesc*:* ꜱᴇᴛ ɢʀᴏᴜᴘ ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ

❂ /setsticker*:* ꜱᴇᴛ ɢʀᴏᴜᴘ ꜱᴛɪᴄᴋᴇʀ

➻ 
"""


__command_list__ = [
    "setdesc" "setsticker" "setgpic" "delgpic" "setgtitle" "adminlist",
    "admins",
    "invitelink",
    "promote",
    "fullpromote",
    "lowpromote",
    "demote",
    "admincache",
]
__handlers__ = [
    SET_DESC_HANDLER,
    SET_STICKER_HANDLER,
    SETCHATPIC_HANDLER,
    RMCHATPIC_HANDLER,
    SETCHAT_TITLE_HANDLER,
    ADMINLIST_HANDLER,
    PIN_HANDLER,
    UNPIN_HANDLER,
    PINNED_HANDLER,
    INVITE_HANDLER,
    BUG_HANDLER,
    PROMOTE_HANDLER,
    FULLPROMOTE_HANDLER,
    LOW_PROMOTE_HANDLER,
    DEMOTE_HANDLER,
    SET_TITLE_HANDLER,
    ADMIN_REFRESH_HANDLER,
]
