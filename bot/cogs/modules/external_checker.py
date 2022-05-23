import uncurl, requests


def is_live(content):
    with open('assets/live_returns.txt', encoding='UTF-8') as file:
        linhas = file.readlines()

    retorno_live = []
    for linha in linhas:
        retorno_live.append(linha.replace('\n', '').lower())

    content = str(content).replace('(', ' ').replace(')', ' ').replace('"', ' ').replace("'", ' ').replace(',', ' ').lower()

    with open('assets/die_blacklist_returns.txt', encoding='UTF-8') as file:
        linhas = file.readlines()

    retorno_die = []
    for linha in linhas:
        retorno_die.append(linha.replace('\n', ''))

    a = []
    b = []
    for item in retorno_die:
        if item in content:
            a.append('.')

    if len(a) == 0:
        for item in retorno_live:
            if item in content:
                b.append('.')
        
        if len(b) == 0:
            return False, '⚠️ - #Reprovado - Possível request inválido'
        
        else:
            return True, '✅ - #Aprovado - Request válido'

    else:
        return False, '❌ - #Reprovado - Request válido'


def curl_validate(command):
    cc = '1'
    numero = '2'
    cvv = '3'
    ano = '4'
    mes = '5'
    
    curl = command.format(cc=cc, numero=numero, cvv=cvv, ano=ano, mes=mes)
    
    if '{cc}' in command or '{numero}' in command and '{ano}' in command and '{mes}' in command and '{cvv}' in command:
        if not 'curl' in curl.lower():
            curl = 'curl '+curl

        try:
            a = str(uncurl.parse(curl))+'.text'
            return True, ''
        except:
            return False, 'Ocorreu um erro ao validar a sua URL ou Curl\n\nCertifique-se que a url seja uma url válida (com https:// ou http:// e sem espaços ou caracteres inválidos) ou o comando Curl seja um comando válido!'

    else:
        return False, "Cerifique-se de incluir as variáveis quando a CC for usada no checker!\n\n*O que são variáveis?* Nesse caso, variáveis são espaços de memória parcial ou completo da CC, que deve ser incluido na URL no lugar da CC.\n\nExemplo: `https://exemple.com/checker.php?lista={cc}`,\n`curl 'https://exemple.com/cielo?numero={numero}&mes={mes}&ano={ano}&cvv={cvv}' -H 'Content-Type: application/json'`\n\n*Variáveis*:\n\n{cc}: `CC completa em formato PIPE padrão`\n{numero}: `Número da CC`\n{mes}: `Mês de vencimento da CC`\n{ano}: `Ano de vencimento da CC (4 dígitos)`\n{cvv}: `Código de segurança de 3 a 4 dígitos da CC`"


def curl_request(command, cc):
    numero, cvv, ano, mes = cc.split('|')
    
    curl = command.format(cc=cc, numero=numero, cvv=cvv, ano=ano, mes=mes)
 
    if not 'curl' in curl.lower():
        curl = 'curl '+curl

    try:
        a = str(uncurl.parse(curl))+'.text'
        b = eval(a)
        retorno = is_live(b)
        print(b)
        return retorno[0], retorno[1] 
    
    except:
        return False, 'Possível request inválido'




