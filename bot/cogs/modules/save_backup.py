import sqlite3, os


row_ccs = ['cc_id', 'numero', 'expiracao', 'cvv', 'tipo', 'bandeira', 'categoria', 'banco', 'pais', 'cpf', 'nome', 'comprador', 'hora']
row_users = ['id_user', 'saldo', 'nome', 'hora']
row_recargas = ['id_user', 'saldo_adicionado', 'order_id', 'hora']
row_categoria = ['categoria', 'preco']
row_afiliado = ['afiliado', 'indicado', 'hora']
row_configuracao = ['variavel', 'condicao']
row_mix = ['quantidade', 'preco']
row_adms = ['id_user']
row_gift = ['gift', 'valor', 'id_user', 'hora']
row_grupos = ['id_group', 'hora']
row_chk_rate = ['id_user', 'rate']
row_chk_ccs = ['numero', 'expiracao', 'cvv', 'tipo', 'bandeira', 'categoria', 'banco', 'pais', 'nome', 'result', 'retorno', 'hora']


def register(lista, coluna, path):
    conn_a = sqlite3.connect('database.db', check_same_thread=False, isolation_level=None, timeout=30000)
    cur_a = conn_a.cursor()
    
    conn_b = sqlite3.connect(path, check_same_thread=False, isolation_level=None, timeout=30000)
    cur_b = conn_b.cursor()
    
    lista2 = []
    
    cur_a.execute("PRAGMA table_info('%s');" % coluna)
    results = cur_b.fetchall()
    for row in results:
        lista2.append(row[1])
    
    rows = []
    sql = 'SELECT * FROM {0}'.format(coluna)
    row2 = cur_b.execute(sql)
    for row in row2:
        rows.append(row)
        row2 = cur_b.fetchone()

    if len(rows) >= 2:
        index = 1
    else:
        index = 0

    def pesquisar(tabela, pesquisar):
        try:
            sql = 'SELECT * FROM {0} WHERE {1} = {2}'.format(tabela, lista[index], pesquisar)
            row = cur_a.execute(sql)
            row = cur_a.fetchone()
            return row

        except:
            return None

    def inserir(tabela, nomes_rows, rows):
        try:
            nr = ', '.join(nomes_rows)
            r = ', '.join(rows)
            sql = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(tabela, nr, r)
            print(sql)
            cur_a.execute(sql)
            conn_a.commit()
            return True

        except:
            return False

    erros = 0
    contador = 0
    if lista == lista2:
        for row in rows:
            row = row[index]

            result = pesquisar(coluna, row)
            if result is None:
                contador += 1
                inserido = inserir(coluna, lista, result)
                if not inserido:
                    erros += 1
                
            else:
                pass
        
        conn_a.rollback()
        conn_a.close()
       
        conn_b.rollback()
        conn_b.close()
        
        return contador, erros

    else:
        return 0, erros


def extract_rows(available_table):
    tables = []
    for row in available_table:
        for table in row:
            tables.append(table)
    
    return tables


def install_backup(path):
    tables_bsbot = ['administrador', 'afiliados', 'cc', 'cc_chk', 'configs', 'gifts', 'grupos', 'limit_chk', 'mix', 'precos', 'recarga', 'usuarios']

    if os.path.isfile(path):
        print('Salve')
        conn_b = sqlite3.connect(path, check_same_thread=False, isolation_level=None, timeout=30000)
        cur_b = conn_b.cursor()
        cur_b.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        available_table = (cur_b.fetchall())

        aproved_tables = []
        tables = extract_rows(available_table)

        for table in tables:
            if table in tables_bsbot:
                aproved_tables.append(table)

        ccs = 0
        usuarios = 0
        recarga = 0
        precos = 0
        afiliados = 0
        mix = 0
        administrador = 0
        gifts = 0
        grupos = 0
        limit_chk = 0
        erros = 0

        if 'cc' in aproved_tables:
            ccs = register(row_ccs, 'cc', path)
            erros = erros + ccs[1]
            ccs = ccs[0]

        if 'usuarios' in aproved_tables:
            usuarios = register(row_users, 'usuarios', path)
            erros = erros + usuarios[1]
            usuarios = usuarios[0]

        if 'recarga' in aproved_tables:
            recarga = register(row_recargas, 'recarga', path)
            erros = erros + recarga[1]
            recarga = recarga[0]

        if 'precos' in aproved_tables:
            precos = register(row_categoria, 'precos', path)
            erros = erros + precos[1]
            precos = precos[0]
            
        if 'afiliados' in aproved_tables:
            afiliados = register(row_afiliado, 'afiliados', path)
            erros = erros + afiliados[1]
            afiliados = afiliados[0]

        if 'mix' in aproved_tables:
            mix = register(row_mix, 'mix', path)
            erros = erros + mix[1]
            mix = mix[0]

        if 'administrador' in aproved_tables:
            administrador = register(row_adms, 'administrador', path)
            erros = erros + administrador[1]
            administrador = administrador[0]

        if 'gifts' in aproved_tables:
            gifts = register(row_gift, 'gifts', path)
            erros = erros + gifts[1]
            gifts = gifts[0]

        if 'grupos' in aproved_tables:
            grupos = register(row_grupos, 'grupos', path)
            erros = erros + grupos[1]
            grupos = grupos[0]

        if 'limit_chk' in aproved_tables:
            limit_chk = register(row_chk_rate, 'limit_chk', path)
            erros = erros + limit_chk[1]
            limit_chk = limit_chk[0]

        conn_b.rollback()
        conn_b.close()

        os.remove(path)
        return True, ccs, usuarios, recarga, precos, afiliados, mix, administrador, gifts, grupos, limit_chk, erros

    else:
        return False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0





