from datetime import timedelta
from bot.cogs.modules.database import *
from bot.cogs.modules.adm_list import adm_list
import time, asyncio


asyncio.run(fix_compradas())

def time_diference(start_time):
    try:
        start_time = float(start_time)
        elapsed_time_secs = time.time() - start_time

        msg = str(timedelta(seconds=round(elapsed_time_secs))).split(':')

        horas_dias = msg[0]

        if horas_dias.isnumeric() == True:
            return '0'
        
        elif 'days' in horas_dias.lower():
            return horas_dias.split()[0]
        
        else:
            return 'erro'
    
    except Exception as e:
        return 'erro'


def stats():
    donos = adm_list()

    hoje = []
    doisdias = []
    tresdias = []
    quatrodias = []
    cincodias = []
    seisdias = []
    setedias = []
    quinzedias = []
    trintadias = []

    try:
        users = asyncio.run(all_users())
        for user in users:
            date = user[3]
            if user[0] not in donos:
                check = time_diference(date)
                if not check.lower() == 'erro':
                    dias = check
                    if int(dias) <= 30:
                        trintadias.append('.')

                        if int(dias) <= 15:
                            quinzedias.append('.')

                            if int(dias) <= 7:
                                setedias.append('.')

                                if int(dias) <= 6:
                                    seisdias.append('.')

                                    if int(dias) <= 5:
                                        cincodias.append('.')

                                        if int(dias) <= 4:
                                            quatrodias.append('.')

                                            if int(dias) <= 3:
                                                tresdias.append('.')
                                                
                                                if int(dias) <= 2:
                                                    doisdias.append('.')

                                                    if int(dias) == 0:
                                                        hoje.append('.')

    except: pass

    users_result = {"quantidade": {"1": len(hoje), "2": len(doisdias), "3": len(tresdias), "4": len(quatrodias), "5": len(cincodias), "6": len(seisdias), "7": len(setedias), "15": len(quinzedias), "30": len(trintadias)}}


    hoje = []
    doisdias = []
    tresdias = []
    quatrodias = []
    cincodias = []
    seisdias = []
    setedias = []
    quinzedias = []
    trintadias = []

    hojeccs = 0
    doisdiasccs = 0
    tresdiasccs = 0
    quatrodiasccs = 0
    cincodiasccs = 0
    seisdiasccs = 0
    setediasccs = 0
    quinzediasccs = 0
    trintadiasccs = 0

    try:
        ccs = asyncio.run(all_ccs_compradas())
        for cc in ccs:
            date = cc[12]
            preco = cc[13]
            if cc[11] not in donos:
                check = time_diference(date)
                if not check.lower() == 'erro':
                    dias = check
                    if int(dias) <= 30:
                        trintadias.append('.')
                        trintadiasccs = trintadiasccs+int(preco)

                        if int(dias) <= 15:
                            quinzedias.append('.')
                            quinzediasccs = quinzediasccs+int(preco)

                            if int(dias) <= 7:
                                setedias.append('.')
                                setediasccs = setediasccs+int(preco)

                                if int(dias) <= 6:
                                    seisdias.append('.')
                                    seisdiasccs = seisdiasccs+int(preco)

                                    if int(dias) <= 5:
                                        cincodias.append('.')
                                        cincodiasccs = cincodiasccs+int(preco)

                                        if int(dias) <= 4:
                                            quatrodias.append('.')
                                            quatrodiasccs = quatrodiasccs+int(preco)

                                            if int(dias) <= 3:
                                                tresdias.append('.')
                                                tresdiasccs = tresdiasccs+int(preco)
                                                
                                                if int(dias) <= 2:
                                                    doisdias.append('.')
                                                    doisdiasccs = doisdiasccs+int(preco)
                                                    
                                                    if int(dias) == 0:
                                                        hoje.append('.')
                                                        hojeccs = hojeccs+int(preco)
        
    except: pass

    ccs_result = {"quantidade": {"1": len(hoje), "2": len(doisdias), "3": len(tresdias), "4": len(quatrodias), "5": len(cincodias), "6": len(seisdias), "7": len(setedias), "15": len(quinzedias), "30": len(trintadias)}, "ganho": {"1": 'R$'+str(hojeccs)+',00', "2": 'R$'+str(doisdiasccs)+',00', "3": 'R$'+str(tresdiasccs)+',00', "4": 'R$'+str(quatrodiasccs)+',00', "5": 'R$'+str(cincodiasccs)+',00', "6": 'R$'+str(seisdiasccs)+',00', "7": 'R$'+str(setediasccs)+',00', "15": 'R$'+str(quinzediasccs)+',00', "30": 'R$'+str(trintadiasccs)+',00'}}

    hoje = []
    doisdias = []
    tresdias = []
    quatrodias = []
    cincodias = []
    seisdias = []
    setedias = []
    quinzedias = []
    trintadias = []

    hojerecargas = 0
    doisdiasrecargas = 0
    tresdiasrecargas = 0
    quatrodiasrecargas = 0
    cincodiasrecargas = 0
    seisdiasrecargas = 0
    setediasrecargas = 0
    quinzediasrecargas = 0
    trintadiasrecargas = 0

    try:
        recargas = asyncio.run(all_recargas())
        for recarga in recargas:
            date = recarga[3]
            if recarga[0] not in donos:
                check = time_diference(date)
                if not check.lower() == 'erro':
                    dias = check
                    if int(dias) <= 30:
                        trintadias.append(int(recarga[1]))
                        trintadiasrecargas = trintadiasrecargas+int(recarga[1])

                        if int(dias) <= 15:
                            quinzedias.append(int(recarga[1]))
                            quinzediasrecargas = quinzediasrecargas+int(recarga[1])

                            if int(dias) <= 7:
                                setedias.append(int(recarga[1]))
                                setediasrecargas = setediasrecargas+int(recarga[1])

                                if int(dias) <= 6:
                                    seisdias.append(int(recarga[1]))
                                    seisdiasrecargas = seisdiasrecargas+int(recarga[1])

                                    if int(dias) <= 5:
                                        cincodias.append(int(recarga[1]))
                                        cincodiasrecargas = cincodiasrecargas+int(recarga[1])

                                        if int(dias) <= 4:
                                            quatrodias.append(int(recarga[1]))
                                            quatrodiasrecargas = quatrodiasrecargas+int(recarga[1])

                                            if int(dias) <= 3:
                                                tresdias.append(int(recarga[1]))
                                                tresdiasrecargas = tresdiasrecargas+int(recarga[1])

                                                if int(dias) <= 2:
                                                    doisdias.append(int(recarga[1]))
                                                    doisdiasrecargas = doisdiasrecargas+int(recarga[1])
                                                    
                                                    if int(dias) == 0:
                                                        hoje.append(int(recarga[1]))
                                                        hojerecargas = hojerecargas+int(recarga[1])

    except: pass

    recargas_result = {"quantidade": {"1": len(hoje), "2": len(doisdias), "3": len(tresdias), "4": len(quatrodias), "5": len(cincodias), "6": len(seisdias), "7": len(setedias), "15": len(quinzedias), "30": len(trintadias)}, "ganho": {"1": 'R$'+str(hojerecargas)+',00', "2": 'R$'+str(doisdiasrecargas)+',00', "3": 'R$'+str(tresdiasrecargas)+',00', "4": 'R$'+str(quatrodiasrecargas)+',00', "5": 'R$'+str(cincodiasrecargas)+',00', "6": 'R$'+str(seisdiasrecargas)+',00', "7": 'R$'+str(setediasrecargas)+',00', "15": 'R$'+str(quinzediasrecargas)+',00', "30": 'R$'+str(trintadiasrecargas)+',00'}}

    hoje = []
    doisdias = []
    tresdias = []
    quatrodias = []
    cincodias = []
    seisdias = []
    setedias = []
    quinzedias = []
    trintadias = []

    hojegifts = 0
    doisdiasgifts = 0
    tresdiasgifts = 0
    quatrodiasgifts = 0
    cincodiasgifts = 0
    seisdiasgifts = 0
    setediasgifts = 0
    quinzediasgifts = 0
    trintadiasgifts = 0
    
    try:
        gifts = asyncio.run(all_gifts())
        for gift in gifts:
            date = gift[3]
            check = time_diference(date)
            if not check.lower() == 'erro':
                dias = check
                
                if gift[2] not in donos:
                    if int(dias) <= 30:
                        trintadias.append(int(gift[1]))
                        trintadiasgifts = trintadiasgifts+int(gift[1])

                        if int(dias) <= 15:
                            quinzedias.append(int(gift[1]))
                            quinzediasgifts = quinzediasgifts+int(gift[1])

                            if int(dias) <= 7:
                                setedias.append(int(gift[1]))
                                setediasgifts = setediasgifts+int(gift[1])

                                if int(dias) <= 6:
                                    seisdias.append(int(gift[1]))
                                    seisdiasgifts = seisdiasgifts+int(gift[1])

                                    if int(dias) <= 5:
                                        cincodias.append(int(gift[1]))
                                        cincodiasgifts = cincodiasgifts+int(gift[1])

                                        if int(dias) <= 4:
                                            quatrodias.append(int(gift[1]))
                                            quatrodiasgifts = quatrodiasgifts+int(gift[1])

                                            if int(dias) <= 3:
                                                tresdias.append(int(gift[1]))
                                                tresdiasgifts = tresdiasgifts+int(gift[1])

                                                if int(dias) <= 2:
                                                    doisdias.append(int(gift[1]))
                                                    doisdiasgifts = doisdiasgifts+int(gift[1])
                                                    
                                                    if int(dias) == 0:
                                                        hoje.append(int(gift[1]))
                                                        hojegifts = hojegifts+int(gift[1])
    except: pass

    gifts_result = {"quantidade": {"1": len(hoje), "2": len(doisdias), "3": len(tresdias), "4": len(quatrodias), "5": len(cincodias), "6": len(seisdias), "7": len(setedias), "15": len(quinzedias), "30": len(trintadias)}, "ganho": {"1": 'R$'+str(hojegifts)+',00', "2": 'R$'+str(doisdiasgifts)+',00', "3": 'R$'+str(tresdiasgifts)+',00', "4": 'R$'+str(quatrodiasgifts)+',00', "5": 'R$'+str(cincodiasgifts)+',00', "6": 'R$'+str(seisdiasgifts)+',00', "7": 'R$'+str(setediasgifts)+',00', "15": 'R$'+str(quinzediasgifts)+',00', "30": 'R$'+str(trintadiasgifts)+',00'}}

    return {"relatorio": {"usuarios": users_result, "ccs": ccs_result, "recargas": recargas_result, "gifts": gifts_result}}


