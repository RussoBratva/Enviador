from bot.cogs.modules.database import *
import asyncio


def group_list():
    grupos = asyncio.run(all_groups())
    
    return grupos



