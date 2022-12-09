# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""
import os
import time

import psutil

from GalaxiaRobot import StartTime

# Stats Callback


async def bot_sys_stats():
    bot_uptime = int(time.time() - StartTime)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
------------------
ᴜᴘᴛɪᴍᴇ: {formatter.get_readable_time(bot_uptime)}
ʙᴏᴛ: {round(process.memory_info()[0] / 1024 ** 2)} MB
ᴄᴘᴜ: {cpu}%
ʀᴀᴍ: {mem}%
ᴅɪsᴋ: {disk}%
------------------
"""
    return stats
