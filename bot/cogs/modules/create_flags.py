from bot.cogs.modules.database import *
import asyncio



lista = [
    ['manutencao', '0'],
    ['checker', '1'],
    ['pix', '1'],
    ['afiliado', '1'],
    ['pesquisar_bandeira', '1'],
    ['pesquisar_banco', '1'],
    ['pesquisar_bin', '1'],
    ['chk', '1'],
    ['checker_publico', '0'],
    ['auto_live', '1'],
    ['qrcode', '0'],
    ['troca', '0']
]


def create_flags():
    for item in lista:
        variavel = item[0]
        condicao = item[1]
        asyncio.run(add_config(variavel, condicao))

