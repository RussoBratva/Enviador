from bot.cogs.modules.database import *
import asyncio
import json


def adm_list():
    with open('config/config.json', 'r') as file:
        try:
            config = json.loads(file.read())
            donos = config['donos']

        except:
            donos = []

    db_adms = asyncio.run(all_adms())
    
    adms = db_adms+donos

    return adms







