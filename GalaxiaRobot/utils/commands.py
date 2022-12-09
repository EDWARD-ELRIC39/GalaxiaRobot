from typing import List, Union

from config import COMMAND_PREFIXES
from pyrogram import filters


def command(commands: Union[str, List[str]]):
    return filters.command(commands, COMMAND_PREFIXES)
