import asyncio, aiosqlite, time, random, string, os, platform
from concurrent.futures import ThreadPoolExecutor
from bot.cogs.modules.bin_checker import bin_checker


database_name = '/root/BratvaV14/main.db'

if platform.system() == 'Linux':
    cmd = f"sudo fuser -k {database_name}"
    os.system(cmd)

elif platform.system() == 'Windows':
    cmd = f'for /f "skip=4 tokens=3" %i in ("handle {database_name}\") do taskkill /pid %i'
    os.system(cmd)


async def get_conn():
    conn = await aiosqlite.connect(f'{database_name}')
    return conn


async def create_database():
    await conn.execute("CREATE TABLE IF NOT EXISTS cc (cc_id text, numero text, expiracao text, cvv text, tipo text, bandeira text, categoria text, banco text, pais text, cpf text, nome_user text, comprador text, hora text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS compradas (cc_id text, numero text, expiracao text, cvv text, tipo text, bandeira text, categoria text, banco text, pais text, cpf text, nome_user text, comprador text, hora text, preco text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS users (id text, balance text, nome_user text, hora text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS recarga (id text, balance_adicionado text, order_id text, hora text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS precos (categoria text, preco text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS afiliados (afiliado text, indicado text, hora text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS configs (variavel text, condicao text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS mix (quantidade text, preco text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS administrador (id text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS gifts (gift text, valor text, id text, hora text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS grupos (id_group, hora text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS cc_die (cc text, hora text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS banned (id text,hora text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS checker_pagarme (api_key text, hora text, is_default text, is_redundance text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS checker_cielo (merchantid text, merchantkey text, hora text, is_default text, is_redundance text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS checker_getnet (client_id text, secret_id text, seller_id text, hora text, is_default text, is_redundance text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS checker_erede (pv text, token text, hora text, is_default text, is_redundance text);")
    await conn.execute("CREATE TABLE IF NOT EXISTS checker_external (curl text, hora text, is_default text, is_redundance text);")


conn = asyncio.run(get_conn())
asyncio.run(create_database())


async def registrar_checker(tipo, content):
    id_checker = str(random.randint(111111111, 999999999))
    is_default = '0'
    is_redundance = '0'
    hora = str(time.time())
    
    if tipo == 'pagarme':
        await conn.execute(f'INSERT INTO checker_pagarme (id, api_key, hora) VALUES (?,?,?,?,?)', (id_checker, content, hora, is_default, is_redundance,))
        await conn.commit()

    elif tipo == 'external':
        await conn.execute(f'INSERT INTO checker_external (id, curl, hora) VALUES (?,?,?,?,?)', (id_checker, content, hora, is_default, is_redundance,))
        await conn.commit()

    elif tipo == 'cielo':
        merchantid, merchantkey = content.split('|')
        await conn.execute(f'INSERT INTO checker_cielo (id, merchantid, merchantkey, hora) VALUES (?,?,?,?,?,?)', (id_checker, merchantid, merchantkey, hora, is_default, is_redundance,))
        await conn.commit()

    elif tipo == 'erede':
        pv, token = content.split('|')
        await conn.execute(f'INSERT INTO checker_erede (id, pv, token, hora) VALUES (?,?,?,?,?,?)', (id_checker, pv, token, hora, is_default, is_redundance,))
        await conn.commit()

    elif tipo == 'getnet':
        client_id, client_secret, seller_id = content.split('|')
        await conn.execute(f'INSERT INTO checker_getnet (id, client_id, client_secret, seller_id, hora) VALUES (?,?,?,?,?,?,?)', (id_checker, client_id, client_secret, seller_id, hora, is_default, is_redundance,))
        await conn.commit()


async def pesquisar_ban(pesquisar):
    try:
        sql = 'SELECT * FROM banned WHERE id = ?'
        row = await conn.execute(sql,  (pesquisar,))
        row = await row.fetchone()
        return row

    except:
        return None


async def registrar_ban(id):
    pesquisa = await pesquisar_ban(id)
    if pesquisa == None:
        hora = str(time.time())
        await conn.execute(f'INSERT INTO banned (id, hora) VALUES (?,?)', (id, hora,))
        await conn.commit()


async def check_comprada_id(pesquisar):
    sql = 'SELECT * FROM compradas WHERE cc_id = ?'
    row = await conn.execute(sql,  (pesquisar,))
    row = await row.fetchone()

    if row is None:
        return False, []
    
    else:
        return True, row



async def remove_ban(id):
    try:
        pesquisa = await pesquisar_ban(id)
        if not pesquisa == None:
            sql = 'DELETE FROM banned WHERE id = ?'
            await conn.execute(sql,  (id,))
            await conn.commit()
            
            return True

        else:
            return False

    except:
        return False


async def check_config(pesquisar):
    try:
        sql = 'SELECT * FROM configs WHERE variavel = ?'
        row = await conn.execute(sql,  (pesquisar,))
        row = await row.fetchone()

    except Exception as e:
        print('Erro:',)
        row = ['', '1']
        
    return row


async def add_config(variavel, condicao):
    check = await check_config(variavel)
    if check is None:
        await conn.execute(f'INSERT INTO configs (variavel, condicao) VALUES (?,?)', (variavel, condicao))
        await conn.commit()



async def check_group(pesquisar):
    sql = 'SELECT * FROM grupos WHERE id_group = ?'
    row = await conn.execute(sql,  (pesquisar,))
    row = await row.fetchone()

    return row


async def check_comprada(pesquisar):
    sql = 'SELECT * FROM compradas WHERE numero = ?'
    row = await conn.execute(sql,  (pesquisar,))
    row = await row.fetchone()

    if row is None:
        return True
    
    else:
        await remove_cc(pesquisar, False)
        return False


async def add_group(id_group):
    check = await check_group(id_group)
    if check is None:
        hora = str(time.time())
        await conn.execute(f'INSERT INTO grupos (id_group, hora) VALUES (?,?)', (id_group, hora,))
        await conn.commit()
        
        return True
    
    else:
        return False


async def config_change(variavel, condicao):
    await conn.execute(
        "UPDATE configs SET condicao = (?)"
        "WHERE variavel = (?)", (condicao, variavel,))

    await conn.commit()


async def check_cc_database(pesquisar):
    try:
        sql = 'SELECT * FROM cc WHERE numero = ?'
        row = await conn.execute(sql,  (pesquisar,))
        row = await row.fetchone()
        return row
    
    except:
        return None


async def level_price(pesquisar):
    try:
        sql = 'SELECT * FROM precos WHERE categoria = ?'
        row = await conn.execute(sql,  (pesquisar.upper(),))
        row = await row.fetchone()
        if row == None:
            return None

        else:
            if row[1] == 'None':
                return 'Não especificado'
            
            else:
                return row[1]
    except:
        return 'Não especificado'


async def price_change(level, preco):
    await conn.execute(
        "UPDATE precos SET preco = (?)"
        "WHERE categoria = (?)", (preco, level.upper(),))

    await conn.commit()


async def add_level(level):
    sql = 'SELECT * FROM precos WHERE categoria = ?'
    row = await conn.execute(sql,  (level,))
    row = await row.fetchone()
    if row == None:
        preco = 'None'
        await conn.execute(f'INSERT INTO precos (categoria, preco) VALUES (?,?)', (level, preco))
        await conn.commit()


async def check_level():
    try:
        results= []
        async with conn.execute("""select * from "precos";""") as cursor:
            async for row in cursor:
                preco = row[1]
                if preco == 'None':
                    results.append(preco)

        return len(results)

    except Exception as e:
        print('Erro:', e)
        return 0


async def name_update(id, nome_atual):
    try:
        sql = 'SELECT * FROM users WHERE id = ?'
        row = await conn.execute(sql,  (id,))
        row = await row.fetchone()
        if row is not None:
            nome_registrado = row[2]
            if nome_registrado == nome_atual.strip():
                pass

            else:
                await conn.execute(
                    "UPDATE users SET nome_user = (?)"
                    "WHERE id = (?)", (nome_atual.strip(), id,))

    except:
        pass


async def pesquisar_adm(pesquisar):
    try:
        pesquisa = await pesquisar_ban(pesquisar)
        if not pesquisa is None:
            sql = 'SELECT * FROM administrador WHERE id = ?'
            row = await conn.execute(sql,  (pesquisar,))
            row = await row.fetchone()
            return row

        else:
            return None

    except:
        return None



async def registrar_adm(id):
    pesquisa = await pesquisar_adm(id)
    if pesquisa == None:
        await conn.execute(f'INSERT INTO administrador (id) VALUES (?)', (id,))
        await conn.commit()


async def remove_adm(id):
    try:
        pesquisa = await pesquisar_adm(id)
        if not pesquisa == None:
            sql = 'DELETE FROM administrador WHERE id = ?'
            await conn.execute(sql,  (id,))
            await conn.commit()
            
            return True

        else:
            return False

    except:
        return False


async def remove_cc(numero, die=True):
    try:
        sql = 'SELECT * FROM cc WHERE numero = ?'
        row = await conn.execute(sql,  (numero,))
        row = await row.fetchone()
        expiracao = str(row[2]).replace('/', '|20')
        cvv = row[3]
        
        cc = f'{numero}|{expiracao}|{cvv}'
        
        sql = 'DELETE FROM cc WHERE numero = ?'
        await conn.execute(sql,  (numero,))
        await conn.commit()
        
        if die:
            hora = str(time.time())
            await conn.execute(f'INSERT INTO cc_die (cc, hora) VALUES (?,?)', (cc, hora))
            await conn.commit()

        sql = 'DELETE FROM cc WHERE numero = ?'
        await conn.execute(sql,  (numero,))
        await conn.commit()

        return True
    except:
        return False


async def all_gifts():
    results= []
    
    try:
        async with conn.execute("""select * from "gifts";""") as cursor:
            async for row in cursor:
                results.append(row)

    except:
        pass
    
    return results


async def all_groups():
    results= []
    
    try:
        async with conn.execute("""select * from "grupos";""") as cursor:
            async for row in cursor:
                results.append(row[0])

    except:
        pass
    
    return results


async def all_adms():
    results= []
    
    try:
        async with conn.execute("""select * from "administrador";""") as cursor:
            async for row in cursor:
                results.append(row[0])
        
    except:
        pass

    return results



async def pesquisar_id(pesquisar):
    contador = 0
    while True:
        contador += 1
        if not contador >5:
            try:
                sql = 'SELECT * FROM users WHERE id = ?'
                row = await conn.execute(sql,  (pesquisar,))
                row = await row.fetchone()
                break
            except:
                pass
        
        else:
            row = None
            break
    
    return row


async def registrar_usuario(id, nome_user):
    pesquisa = await pesquisar_id(id)
    if pesquisa == None:
        balance = '0'
        hora = str(time.time())
        await conn.execute(f'INSERT INTO users (id, balance, nome_user, hora) VALUES (?,?,?,?)', (id, balance, nome_user, hora))
        await conn.commit()


async def registrar_recarga(id, balance, order_id):
    pesquisa = await pesquisar_id(id)
    if not pesquisa == None:
        hora = str(time.time())
        await conn.execute(f'INSERT INTO recarga (id, balance_adicionado, order_id, hora) VALUES (?,?,?,?)', (id, balance, order_id, hora))
        await conn.commit()


async def ccs_comprados(id):
    try:
        results1= []
        results2= []
        
        async with conn.execute('SELECT * FROM cc WHERE comprador = ?',  (id,)) as cursor:
            async for row in cursor:
                results1.append(row)
 
        async with conn.execute('SELECT * FROM compradas WHERE comprador = ?',  (id,)) as cursor:
            async for row in cursor:
                results2.append(row)
        
        results = results1+results2
        
        return len(results)

    except:
        return 0


async def pesquisar_recarga(pesquisar):
    try:
        pesquisa = await pesquisar_ban(pesquisar)
        if not pesquisa is None:
            sql = 'SELECT * FROM recarga WHERE order_id = ?'
            row = await conn.execute(sql,  (pesquisar,))
            row = await row.fetchone()
            return row

        else:
            return None

    except:
        return None
    
    
async def recargas(id):
    try:
        sql = 'SELECT * FROM recarga WHERE id = ?'
        results= []
        async with await conn.execute(sql,  (id,)) as cursor:
            async for row in cursor:
                results.append(row)

        return len(results)

    except:
        return 0


async def add_balance(id, balance):
    balance_atual = await pesquisar_id(id)
    if balance_atual is not None:
        soma = str(int(balance_atual[1])+int(balance))
        await conn.execute("UPDATE users SET balance = (?)""WHERE id = (?)", (soma, id,))
        await conn.commit()


async def subtrair_balance(id, balance):
    balance_atual = await pesquisar_id(id)
    if balance_atual is not None:
        if not int(balance_atual[1]) < int(balance):
            subtracao = str(int(balance_atual[1])-int(balance))
        else:
            subtracao = '0'

        await conn.execute("UPDATE users SET balance = (?)""WHERE id = (?)", (subtracao, id,))
        await conn.commit()


async def rate_limit_chk(id, reset=False):
    check = await pesquisar_id(id)
    if not reset:
        if check is not None:
            sql = 'SELECT * FROM limit_chk WHERE id = ?'
            row = await conn.execute(sql,  (id,))
            row = await row.fetchone()
            if row is None:
                rate_init = '0'
                await conn.execute(f'INSERT INTO limit_chk (id, rate) VALUES (?,?)', (id, rate_init,))
                await conn.commit()
                
                return False
            
            else:
                if int(row[1]) >= 4:
                    rate = str(int(row[1]) + 1)
                    await conn.execute("UPDATE limit_chk SET rate = (?)""WHERE id = (?)", (rate, id,))
                    await conn.commit()
                    return False
                
                else:
                    rate = '0'
                    await conn.execute("UPDATE limit_chk SET rate = (?)""WHERE id = (?)", (rate, id,))
                    await conn.commit()
                    return True
    else:
        rate = '0'
        await conn.execute("UPDATE limit_chk SET rate = (?)""WHERE id = (?)", (rate, id,))
        await conn.commit()
        return False


async def cadastrar_cartao(cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome_user, comprador, data):
    sql = 'SELECT * FROM compradas WHERE numero = ?'
    row = await conn.execute(sql,  (numero,))
    row = await row.fetchone()
    cc = f'{numero}|{expiracao.replace("/", "|20")}|{cvv}'
    if row is None:
        await conn.execute(f'INSERT INTO cc (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome_user, comprador, hora) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome_user, comprador, data,))
        await conn.commit()
        print('CC cadastrada')
    else:
        print('CC não cadastrada')


async def all_precos():
    results= []
    
    try:
        async with conn.execute("""select * from "precos";""") as cursor:
            async for row in cursor:
                results.append(row)

    except:
        pass

    return results


async def pesquisar_categoria(categoria):
    results = []
    
    try:
        ccs = await all_ccs()
        
        for row in ccs:
            comprador = row[11]
            hora = row[12]
            if categoria == row[6]:
                results.append(row)
    
    except:
        pass

    return results


async def pesquisar_cc_id(cc_id):
    try:
        sql = 'SELECT * FROM cc WHERE cc_id = ?'
        row = await conn.execute(sql,  (cc_id,))
        row = await row.fetchone()
        
        return row
    
    except:
        return None


async def check_afiliado(id_user_indicado):
    sql = 'SELECT * FROM afiliados WHERE indicado = ?'
    row = await conn.execute(sql,  (id_user_indicado,))
    row = await row.fetchone()

    if not row == None:
        return row[0]

    else:
        return None


async def add_afiliado(id_user_afiliado, id_user_indicado):
    row = await pesquisar_id(id_user_afiliado)
    
    if not row == None:
        if not id_user_indicado == id_user_afiliado:
            check = await check_afiliado(id_user_indicado)
            if check == None:
                check2 = await pesquisar_id(id_user_indicado)
                if check2 is None:
                    hora = str(time.time())
                    await conn.execute(f'INSERT INTO afiliados (afiliado, indicado, hora) VALUES (?,?,?)', (id_user_afiliado, id_user_indicado, hora))
                    await conn.commit()


async def comissao(id, balance):
    afiliado = await check_afiliado(id)
    if not afiliado == None:
        calculo = int(balance) - int(int(balance) * (1 - 10 / 100))
        await add_balance(str(afiliado), calculo)
        
        return True
    
    else:
        return False


async def lista_indicados(id_user_afiliado):
    try:
        sql = 'SELECT * FROM afiliados WHERE afiliado = ?'

        results= []
        async with conn.execute(sql,  (id_user_afiliado,)) as cursor:
            async for row in cursor:
                indicado = row[1]
                results.append(indicado)

        return len(results)

    except:
        return 0


async def update_cartao(cc_id, id, hora):
    try:
        id = str(id)
        cc_id = str(cc_id)
        hora = str(hora)
        row = await pesquisar_cc_id(cc_id)
        numero = row[1]
        await remove_cc(numero)
        expiracao = row[2]
        cvv = row[3]
        tipo = row[4]
        bandeira = row[5]
        categoria = row[6]
        banco = row[7]
        pais = row[8]
        cpf = row[9]
        nome_user = row[10]
        comprador = id
        hora = str(time.time())
        preco = await precos(categoria)
        
        await conn.execute(f'INSERT INTO compradas (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome_user, comprador, hora) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome_user, id, hora, preco,))
        await conn.commit()

        return True

    except:
        return False


async def precos(tipo):
    try:
        sql = 'SELECT * FROM precos WHERE categoria = ?'
        row = await conn.execute(sql,  (tipo,))
        row = await row.fetchone()
        return row[1]
    
    except:
        return 'Indefinido'


def buscar_preco(categoria, lista):
    def corte_preco(c):
        contador = -1
        n = 0
        for l in c:
            contador += 1
            if l.isnumeric():
                n = contador
                break
            
        return n

    for c in lista:
        if not c.find(categoria.upper().strip()) == -1:
            corte = corte_preco(c)
            return c[corte:]


async def precos_inline():
    try:
        results = []
        async with conn.execute('SELECT * FROM precos') as cursor:
            async for row in cursor:
                if not row[1] == 'None':
                    results.append(row[0]+' '+row[1])
            
        return results
    
    except:
        return []


async def all_ccs_compradas():
    try:
        results = []
        async with conn.execute('SELECT * FROM compradas') as cursor:
            async for row in cursor:
                results.append(row)

        return results

    except Exception as e:
        print(e)
        return []



async def all_ccs():
    try:
        precos = await precos_inline()
        lista = list(precos)

        comprador = 'None'
        sql = 'SELECT * FROM cc WHERE comprador = ?'

        results = []
        async with conn.execute(sql,  (str(comprador),)) as cursor:
            async for row in cursor:
                categoria = row[6]
                p = buscar_preco(categoria, lista)
                if not p == None:
                    results.append(row)
            
        return results

    except Exception as e:
        print(e)
        return []




async def all_ccs_added():
    precos = await precos_inline()
    lista = list(precos)

    results = []
    async with conn.execute('SELECT * FROM cc') as cursor:
        async for row in cursor:
            categoria = row[6]
            if not row[12]=='None':
                p = buscar_preco(categoria, lista)
                if not p == None:
                    results.append(row)
            
    return results


async def all_dies():
    results = []
    async with conn.execute('SELECT * FROM cc_die') as cursor:
        async for row in cursor:
            results.append(row)
            
    return results


async def pesquisar_info_categoria(categoria):
    try:
        sql = 'SELECT * FROM precos WHERE categoria = ?'
        row = await conn.execute(sql,  (categoria,))
        row = await row.fetchone()
        
        return row

    except:
        return None


async def pesquisar_comprador(id):
    try:
        sql = 'SELECT * FROM compradas WHERE comprador = ?'
        cartoes = []
        async with conn.execute(sql,  (id,)) as cursor:
            async for row in cursor:
                cartoes.append(row)

        return cartoes

    except:
        return []


async def pesquisar_recargas(id):
    try:
        sql = 'SELECT * FROM recarga WHERE id = ?'
        recargas = []
        async with conn.execute(sql,  (id,)) as cursor:
            async for row in cursor:
                recargas.append(row)

        return recargas

    except:
        return []


async def excluir_conta(id):
    try:
        sql = "DELETE FROM users WHERE id = ?"
        await conn.execute(sql,  (id,))
        await conn.commit()
        
        rows = await pesquisar_recargas(id)
        for row in rows:
            order_id = row[2]
            sql = "DELETE FROM recarga WHERE order_id = ?"
            await conn.execute(sql,  (order_id,))
            await conn.commit()
        
        rows = await pesquisar_comprador(id)
        for row in rows:
            cc_id = row[0]
            sql = "DELETE FROM cc WHERE cc_id = ?"
            await conn.execute(sql,  (cc_id,))
            await conn.commit()
            
        sql = 'DELETE FROM afiliados WHERE indicado = ?'
        await conn.execute(sql,  (id,))
        await conn.commit()

        sql = 'DELETE * FROM afiliados WHERE afiliado = ?'
        await conn.execute(sql,  (id,))
        await conn.commit()

        sql = 'DELETE * FROM gifts WHERE id = ?'
        await conn.execute(sql,  (id,))
        await conn.commit()

        sql = "DELETE FROM users WHERE id = ?"
        await conn.execute(sql,  (id,))
        await conn.commit()
        return True

    except:
        return False


async def gen_gift(valor):
    usuario = 'None'
    hora = 'None'
    strings = []
    for c in range(0, 5):
        random_string = random.sample(string.ascii_lowercase+string.digits,5)
        strings.append(''.join(random_string))

    gift = '-'.join(strings)

    await conn.execute(f'INSERT INTO gifts (gift, valor, id, hora) VALUES (?,?,?,?)', (str(gift,), str(valor), str(usuario), str(hora)))
    await conn.commit()
    
    return gift


async def pesquisar_gift(pesquisar):
    try:
        sql = 'SELECT * FROM gifts WHERE gift = ?'
        row = await conn.execute(sql,  (pesquisar,))
        row = await row.fetchone()
        return row

    except:
        return None


async def pesquisar_gifts_resgatados(pesquisar):
    try:
        results = []
        sql = 'SELECT * FROM gifts WHERE id = ?'

        async with conn.execute(sql,  (pesquisar,)) as cursor:
            async for row in cursor:
                results.append(row)
                
        return results

    except:
        return []


async def resgatar_gift(gift, id):
    p_gift = await pesquisar_gift(gift)

    if p_gift is not None:
        user = p_gift[2]
        valor = p_gift[1]
        
        if user == 'None':
            hora = str(time.time())
            await add_balance(id, valor)
            await conn.execute("UPDATE gifts SET id = (?)""WHERE gift = (?)", (id, gift,))
            await conn.commit()
            await conn.execute("UPDATE gifts SET hora = (?)""WHERE gift = (?)", (hora, gift,))
            await conn.commit()
            return True, ''

        else:
            return False, '1'

    else:
        return False, '2'


async def pesquisar_mix(quantidade):
    try:
        sql = 'SELECT * FROM mix WHERE quantidade = ?'
        row = await conn.execute(sql,  (quantidade,))
        row = await row.fetchone()
        return row

    except:
        return None


async def registrar_mix(quantidade, valor):
    pesquisa = await pesquisar_mix(quantidade)
    if pesquisa is None:
        await conn.execute(f'INSERT INTO mix (quantidade, preco) VALUES (?,?)', (quantidade, valor))
        await conn.commit()



async def all_recargas():
    try:
        results = []
        async with conn.execute('SELECT * FROM recarga') as cursor:
            async for row in cursor:
                results.append(row)

        return results

    except:
        return []


async def all_mix():
    try:
        results = []
        async with conn.execute('SELECT * FROM mix') as cursor:
            async for row in cursor:
                results.append(row)

        return results

    except:
        return []


async def editar_valor_mix(quantidade, valor):
    await conn.execute(
        "UPDATE mix SET preco = (?)"
        "WHERE quantidade = (?)", (valor, quantidade,))

    await conn.commit()


async def deletar_mix(quantidade):
    sql = "DELETE FROM mix WHERE quantidade = ?"
    await conn.execute(sql,  (quantidade,))
    await conn.commit()


async def all_users_id():
    try:
        results= []
        async with conn.execute("""select * from "users";""") as cursor:
            async for row in cursor:
                results.append(row[0])

        return results

    except:
        return []


async def all_users():
    try:
        results= []
        async with conn.execute("""select * from "users";""") as cursor:
            async for row in cursor:
                results.append(row)

        return results

    except:
        return []


async def fix_compradas():
    try:
        async with conn.execute("""select * from "cc_comprada";""") as cursor:
            async for row in cursor:
                try:
                    preco = await precos(row[6])
                    await conn.execute(f'INSERT INTO compradas (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome_user, comprador, hora, preco) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], preco,))
                except: pass

        await conn.execute(f'DROP TABLE cc_comprada')
        await conn.commit()

    except: pass


async def fix_bin(row):
    cc_id = row[0]
    numero = row[1]
    expiracao = row[2]
    cvv = row[3]
    bin_info = bin_checker(numero[:6])
    print(f'Realocando os leveis das ccs: ID: {cc_id}: {row[6]} -> {bin_info[2]}')

    tipo = bin_info[1]
    bandeira = bin_info[0]
    categoria = bin_info[2]
    banco = bin_info[3]
    pais = bin_info[4]
    cpf = row[9]
    nome_user = row[10]
    comprador = 'None'
    data = 'None'

    await remove_cc(numero, die=False)
    await cadastrar_cartao(cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome_user, comprador, data)


def convert_fix_bin(row):
    asyncio.run(fix_bin(row))


async def fix_bins():
    a = await check_config('ccs_level_changed')
    if a is None:
        ccs = await all_ccs()
        with ThreadPoolExecutor(max_workers=50) as pool:
            results = list(pool.map(convert_fix_bin,ccs))

        await add_config('ccs_level_changed', '1')



