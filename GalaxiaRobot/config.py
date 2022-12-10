# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
import os

from dotenv import load_dotenv

load_dotenv()


def get_user_list(config, key):
    with open("{}/GalaxiaRobot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = "11597868"  # integer value, dont use ""
    API_HASH = "326ae14ebe620f6a77277f4b979299a9"
    TOKEN = "5875229838:AAHAPQIPefiWAZx0l7bFc1ZcbLZqqZRmDww"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 5977878551  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OPENWEATHERMAP_ID = 22322
    OWNER_USERNAME = "ll_WOLVERINE_ll"
    BOT_USERNAME = ""
    SUPPORT_CHAT = "GALAXIA_X_SUPPORT"  # Your own group for support, do not add the @
    JOIN_LOGGER = (
        -1001748128104
    )  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = (
        -1001748128104
    )  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    ERROR_LOG = -1001748128104

    # RECOMMENDED
    SQLALCHEMY_DATABASE_URI = "postgres://nzjjkiqk:JwOW4Vh8ANNkjynnAkg9YnyHZ0Pl6YnV@tiny.db.elephantsql.com/nzjjkiqk"
    DATABASE_URI = "postgres://nzjjkiqk:JwOW4Vh8ANNkjynnAkg9YnyHZ0Pl6YnV@tiny.db.elephantsql.com/nzjjkiqk"
    MONGO_DB_URI = "mongodb+srv://deadterabaap09:dead@cluster0.3a4z5gq.mongodb.net/?retryWrites=true&w=majority"  # needed for any database modules
    REDIS_URL = "redis://default:imP6xyfvlFsVpzFbciK3dIx9Vde05pav@redis-17127.c239.us-east-1-2.ec2.cloud.redislabs.com:17127/default"
    ARQ_API_URL = "https://arq.hamker.in"
    ARQ_API_KEY = "NRDIAC-BMCGZV-KKUTYX-DHJNWM-ARQ"
    BOT_API_URL = "https://api.telegram.org/bot"
    LOAD = []
    NO_LOAD = ["rss"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"

    # OPTIONAL
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = get_user_list("elevated_users.json", "sudos")
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = get_user_list("elevated_users.json", "supports")
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    WORKERS = (
        8  # Number of subthreads to use. Set as number of threads your processor uses
    )
    BAN_STICKER = ""  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = (
        "awoo"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "awoo"  # Get your API key from https://timezonedb.com/api
    WALL_API = (
        "awoo"  # For wallpapers, get one from https://wall.alphacoders.com/api.php
    )
    AI_API_KEY = "awoo"  # For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    ALLOW_CHATS = None
    TEMP_DOWNLOAD_DIRECTORY = "./"
    HEROKU_APP_NAME = "siap"
    HEROKU_API_KEY = "YES"
    REM_BG_API_KEY = "yahoo"
    LASTFM_API_KEY = "yeah"
    CF_API_KEY = "jk"
    BL_CHATS = []  # List of groups that you want blacklisted.
    SESSION_STRING = "12342"
    STRING_SESSION = ""
    START_IMG = "https://telegra.ph/file/0666a84c2e3618991c15b.jpg"
    MONGO_PORT = 27017
    MONGO_DB = "AsuX"


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
