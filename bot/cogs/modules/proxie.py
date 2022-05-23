from bs4 import BeautifulSoup
import urllib.request
import requests


def ip_check(ip):
    r = requests.get('http://ip-api.com/json/'+ip).json()
    
    return r['country'], r['city']+' - '+r['regionName'], r['as']


def makesoup(url):
    page=requests.get(url)
    print(url + ' scraped successfully')
    return BeautifulSoup(page.text,"html.parser")


def proxyscrape(table):
    proxies = set()
    for row in table.findAll('tr'):
        fields = row.findAll('td')
        count = 0
        proxy = ""
        for cell in row.findAll('td'):
            if count == 1:
                proxy += ":" + cell.text.replace('&nbsp;', '')
                proxies.add(proxy)
                break
            proxy += cell.text.replace('&nbsp;', '')
            count += 1
    return proxies


def scrapeproxies(url):
    soup=makesoup(url)
    result = proxyscrape(table = soup.find('table', attrs={'class': 'table table-striped table-bordered'}))
    proxies = set()
    proxies.update(result)
    
    return proxies


def checker(i, proxyType):
    proxy = proxyType + '://' + i
    proxy_support = urllib.request.ProxyHandler({proxyType: proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    req = urllib.request.Request(proxyType + '://' + 'google.com')

    try:
        urllib.request.urlopen(req, timeout=10)
        return True

    except:
        return False


def proxies(proxy='https'):
    lista = []
    if proxy == 'https':
        proxy_list = list(scrapeproxies('http://sslproxies.org',))
        contador = 0
        print(f'Proxies achadas: {len(proxy_list)}')
        while True:
            try:
                if not contador >= len(proxy_list):
                    check = checker(proxy_list[contador], proxy)
                    
                    if check == True:
                        return proxy_list[contador]
                
                else:
                    break
                
                contador+=1
            
            except: pass

        with open('proxies.txt', 'a', encoding='UTF-8') as file:
            file.write('\n'.join(lista))
        
        print(f'Proxies aprovadas: {len(lista)}')
        
        return lista

    elif proxy == 'http':
        proxy_list = list(scrapeproxies('http://free-proxy-list.net',))
        if len(proxy_list) == 0:
            proxy_list = list(scrapeproxies('http://us-proxy.org',))

        contador = 0
        print(f'Proxies achadas: {len(proxy_list)}')
        while True:
            check = checker(proxy_list[contador], proxy)
            data = ip_check(proxy_list[contador])
            
            if check == True:
                print(f'{proxy_list[contador]} - Proxy boa! - {data[0]} | {data[1]} | {data[2]}')
                return proxy_list[contador]
            
            else:
                print(f'{proxy_list[contador]} - Proxy ruim! - {data[0]} | {data[1]} | {data[2]}')
            
            if contador >= len(proxy_list):
                break
            
            contador+=1
        
        with open('proxies.txt', 'a', encoding='UTF-8') as file:
            file.write('\n'.join(lista))
        
        print(f'Proxies aprovadas: {len(lista)}')
        
"""        return lista
        
    else:
        return lista
"""

def proxie(proxy='https'):
    return proxies()




