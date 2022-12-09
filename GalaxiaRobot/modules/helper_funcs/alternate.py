# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

from functools import wraps

from telegram import ChatAction, error


def send_message(message, text, *args, **kwargs):
    try:
        return message.reply_text(text, *args, **kwargs)
    except error.BadRequest as err:
        if str(err) == "ʀᴇᴘʟʏ ᴍᴇssᴀɢᴇ ɴᴏᴛ ғᴏᴜɴᴅ":
            return message.reply_text(text, quote=False, *args, **kwargs)


def typing_action(func):
    """sᴇɴᴅs ᴛʏᴘɪɴɢ ᴀᴄᴛɪᴏɴ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ғᴜɴᴄ ᴄᴏᴍᴍᴀɴᴅ."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func


def send_action(action):
    """sᴇɴᴅs `action` ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ғᴜɴᴄ ᴄᴏᴍᴍᴀɴᴅ."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(
                chat_id=update.effective_chat.id, action=action
            )
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator
