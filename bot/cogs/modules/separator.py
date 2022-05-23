def get_numbers_sequence(content):
    caracteres = str(content.replace(r'\n', '\n').replace('\n', ' '))
    sublista = []
    blacklist = ['.', ':']
    for caractere in caracteres:
        if caractere.isnumeric() or caractere in blacklist:
            sublista.append(caractere)
        
        else:
            sublista.append(' ')

    
    results = ''.join(sublista).split()
    lista = []
    
    for result in results:
        if result.isnumeric():
            lista.append(result)

    return lista



def separator(content):
    numeros = get_numbers_sequence(content.replace(' ', '|'))
    result = []
    ccs = []

    if len(numeros) >= 4:
        cc_format = []
        for numero in numeros:
            numero = numero.replace(':', '').replace('.', '')
            try:
                if len(cc_format) == 0 and len(numero) == 16 or len(numero) == 15:
                    cc_format.append(numero)
                
                elif len(cc_format) == 1 and int(numero) >= 1 and int(numero) <= 12:
                    cc_format.append(numero)
                
                elif len(cc_format) == 2 and int(numero.replace('20', '')) >= 13 and int(numero.replace('20', '')) <= 99 or len(cc_format) == 2 and int(numero) >= 13 and int(numero) <= 99:
                    if len(numero) == 2:
                        numero = '20'+numero
                        
                    cc_format.append(numero)

                elif len(cc_format) == 3 and len(numero) == 3 or len(numero) == 4:
                    cc_format.append(numero)
                    if len(cc_format) == 4:
                        
                        ccs.append((cc_format))
                        cc_format = []
                        
                    else:
                        
                        cc_format = []

                else:
                    pass

            except:
                pass
    
    for cc in ccs:
        try:
            result.append(f'{cc[0]}|{cc[1]}|{cc[2]}|{cc[3]}')

        except:
            pass

    return list(result)




