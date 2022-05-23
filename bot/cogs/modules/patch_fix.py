from bot.cogs.modules.database import *
from bot.cogs.modules.bin_checker import *
import asyncio


def move_ccs():
    ccs = asyncio.run(all_ccs_added())
    for row in ccs:
        cc_id = row[0]
        comprador = row[11]
        hora = row[12]

        if not comprador == 'None' or hora == 'None':
            update_cartao(cc_id, comprador, hora)



def verify_ccs():
    ccs = asyncio.run(all_ccs())
    for cc in ccs:
        check = asyncio.run(check_comprada(cc[1]))
        if not check:
            asyncio.run(remove_cc(cc[1]))


