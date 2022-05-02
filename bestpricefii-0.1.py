# importar as bibliotecas necessárias
import yahoo_fin
from yahoo_fin import stock_info as si
import requests
from bs4 import BeautifulSoup
import threading
from threading import Thread, Lock
vet = []
totalvet = []
ValDivedendos = []
vetorDividendo = []
titulos=["VRTA11","MXRF11","BCRI11","FLMA11","HTMX11","MFII11","RBRF11","RECT11","HFOF11","MAXR11","RBVA11","TGAR11","XPLG11","XPHT11"]
mutex = Lock()
def chama(titulo):
    response = requests.get('https://www.fundsexplorer.com.br/funds/'+titulo)
    content = response.content
    site = BeautifulSoup(content, 'html.parser')
    classes = site.findAll('span', attrs={'class': 'indicator-value'})
    historico_dividendo = site.findAll('script',)
    #dividendo = float(str(classes[1]).split('R$ ')[1].split('</span>')[0].replace(',','.'))
    string_lista = (str(historico_dividendo).split('Dividendos","data":')[1].split(',"backgroundColor":')[0].split("[")[1].split("]")[0])
    divisor_virgula = int(string_lista.count(','))
    for i in range(0,divisor_virgula):
        ValDivedendos.append(float(string_lista.split(",")[i]))
    vetorDividendo = sum(ValDivedendos[-7:-1])/len(ValDivedendos[-7:-1])
    dividendo=vetorDividendo
    #print(vetorDividendo)
    #print(dividendo)
    preco = float(round(si.get_live_price(titulo+".SA"),2))
#print(si.get_live_price("MXRF11.SA"))
    div_tit=dividendo/preco
    print(titulo)
    print(div_tit)
    mutex.acquire()
    vet.append(titulo)
    vet.append(div_tit)
    mutex.release()

for titulo in titulos:
    # chama(titulo)
    titulo = threading.Thread(target=chama,args=(titulo,))
    titulo.start()
    

