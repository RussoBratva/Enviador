from datetime import datetime


def check_expiracao(expiracao):
    n = datetime.now()
    ano_a = int(str(n.year)[2:])
    ano_b = int(expiracao[3:])

    if not ano_a > ano_b:
        return True

    else:
        return 


def check_cc(cc):
    try:
        tracos = []
        contar = 0
        contar2 = -1
        for c in cc:
            contar2 += 1
            i = c.find('|')
            if not i < 0:
                contar += 1
                tracos.append(contar2)
                

        if tracos[1] == 19:
            cc = cc[:19]+'/'+cc[19+1:]

        elif tracos[1] == 18:
            cc = cc[:18]+'/'+cc[18+1:]
            
    except:
        pass

    barras = cc.count('|')
    if barras > 1:
        corte1 = cc.find('|')
        t1 = cc[corte1+1:]
        corte2 = t1.find('|')

        numero = cc[:corte1]
        expiracao = str(t1[:corte2]).replace('20', '').replace('|', '/')
        cvv = t1[corte2+1:]
        barra = cc.find('/')
        len_numero = len(numero)
        len_expiracao = len(expiracao)
        len_cvv = len(cvv)

        if not corte2 < 0:
            if not barra < 0:
                if len_numero in [15, 16]:
                    if not len_expiracao != 5:
                        if len_cvv in [3, 4]:
                            if check_expiracao(expiracao):
                                return True, numero, expiracao, cvv
                            else:
                                return False, '', '', ''
                        else:
                            return False, '', '', ''
                    else:
                        return False, '', '', ''
                else:
                    return False, '', '', ''
            else:
                return False, '', '', ''
        else:
            return False, '', '', ''
    else:
        return False, '', '', ''


