from bs4 import BeautifulSoup
import requests
from datetime import date
import unidecode
import mysql.connector


def abrirBD(funcao):
    conexao = mysql.connector.connect(
        passwd='nineboxeucatur',
        port=3306,
        user='ninebox',
        host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
        database='Vam-Eucatur'
    )
    cursor = conexao.cursor()

    comando = f'{funcao}'
    cursor.execute(comando)
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado


def limpaValor(valor):
    cont = 0
    digit = ''
    PosVirg = ''
    for a in valor:
        qnt = len(valor) - 3
        cont += 1
        if cont <= qnt:
            digit += a
        elif cont > qnt + 1:
            PosVirg += a
    numFinal = f'{digit}.{PosVirg}'
    return(numFinal)


def isdigit(texto):
    numero = ''
    for a in str(texto.strip()):
        if a.isdigit():
            numero = numero + a
    return numero


def rotasClickBuss(origem, destino, est_origem,est_destin, ano, mes, dia):
    if int(mes) < 10:
        mes = f'0{int(mes)}'
    if int(dia) < 10:
        dia = f'0{dia}'

    origem_tratada = unidecode.unidecode(origem).lower().strip()
    destino_tratado = unidecode.unidecode(destino).lower().strip()

    origem_final = origem_tratada.replace(' ', '-')
    destino_final = destino_tratado.replace(' ', '-')

    estOrigemTratad = str(f"{est_origem}").lower()
    estdestinTratad = str(f"{est_destin}").lower()


    city_todos = ['sao-paulo', 'rio-de-janeiro', 'belo-horizonte', 'recife', 'maceio', 'brasilia', 'fortaleza',
                  'vitoria', 'campinas', 'sao-jose-do-rio-preto', 'juiz-de-fora', 'sao-jose-dos-campos',
                  'campos-dos-goytacazes', 'joao-pessoa', 'teresina', 'natal', 'nova-friburgo',
                  'porto-alegre', 'aracaju']

    SemiLeitos = ['Semileito - C/ AR', 'Semileito - DD', 'Semileito - Space']
    Execut = ['Executivo - DD', 'Convencional -  DD', 'Convencional']
    Cama = ['Cama - Cabine']
    Leito = ['Leito - Total']

    if origem_final in city_todos:
        url = requests.get(f'https://www.clickbus.com.br/onibus/{origem_final}-{estOrigemTratad}-todos/{destino_final}-{estdestinTratad}?departureDate={ano}-{mes}-{dia}')
        print(f'CLICK BUSS {url}')

        if destino_final in city_todos:
            url = requests.get(f'https://www.clickbus.com.br/onibus/{origem_final}-{estOrigemTratad}-todos/{destino_final}-{estdestinTratad}-todos?departureDate={ano}-{mes}-{dia}')
            print(f'CLICK BUSS {url}')

    elif destino_final in city_todos:
        url = requests.get(f'https://www.clickbus.com.br/onibus/{origem_final}-{estOrigemTratad}/{destino_final}-{estdestinTratad}-todos?departureDate={ano}-{mes}-{dia}')
        print(f'CLICK BUSS {url}')

    else:
        url = requests.get(f'https://www.clickbus.com.br/onibus/{origem_final}-{estOrigemTratad}/{destino_final}-{estdestinTratad}?departureDate={ano}-{mes}-{dia}')
        print(f'CLICK BUSS {url}')

    ender = url.content
    bea = BeautifulSoup(ender, 'html.parser')

    fedd = bea.findAll('div', attrs={'class': 'search-result-item valign-wrapper'})

    lista_ofestas = []
    listDelist = []
    listacopy = []
    for info in fedd:
        preco = info.find('span', attrs={'class': 'price-value'})
        empresas = info.find('div', attrs={'class': 'company'})
        tipo_leito = info.find('div', attrs={'class': 'service-class'})
        hr_saida = info.find('time', attrs={'class': 'departure-time'})
        hr_chegada = info.find('time', attrs={'class': 'return-time'})
        qtd_leito = info.find('small', attrs={'class': 'available-seats'})
        data = hr_saida['data-date']

        leitotexto = str(qtd_leito.text)
        var = isdigit(leitotexto)
        print(leitotexto)
        print(var)

        leito = str(tipo_leito['content'])
        if leito in SemiLeitos:
            leito = 'SEMI-LEITO'
        elif leito in Execut:
            leito = 'EXECUTIVO'
        elif leito in Cama:
            leito = 'CAMA'
        elif leito in Leito:
            leito = 'LEITO'

        valor = str(preco.text)[2:]
        valorlimpo = limpaValor(valor)

        lista_ofestas.append(data)
        lista_ofestas.append(empresas['data-name'])
        lista_ofestas.append(valorlimpo)
        lista_ofestas.append(hr_saida.text)
        lista_ofestas.append(hr_chegada.text)
        lista_ofestas.append(leito.upper())
        lista_ofestas.append(var)
        lista_ofestas.append('Onibus')
        lista_ofestas.append(f'{origem}')
        lista_ofestas.append(f'{destino}')
        lista_ofestas.append(f'{origem} - {destino}')
        lista_ofestas.append(str(date.today()))

        listacopy = lista_ofestas.copy()
        listDelist.append(listacopy)
        lista_ofestas.clear()

    return listDelist


"""funcao = 'SELECT * FROM ROTAS;'
rotas = abrirBD(funcao)

CidOrigem = []
CidDestin = []
EstOrigem = []
EstDestin = []

for a in rotas:
    CidOrigem.append(a[1])
    CidDestin.append(a[2])
    EstOrigem.append(a[3])
    EstDestin.append(a[4])

Lorigem = CidOrigem
Ldestino = CidDestin

dados = {}
rotaRaiz = {}

data = date.today()
cont = 0
for i in range(len(Lorigem)):
    print(f'{i}° ROTA')
    origem = Lorigem[i]
    destino = Ldestino[i]
    est_origem = EstOrigem[i]
    est_destin = EstDestin[i]
    hoje = date(2023, 2, 3)
    for j in range(20): #QUANTIDADE DE DIAS QUE VAI RODAR
        cont += 1
        data1 = str(hoje)
        ano = int(data1[0:4])
        mes = int(data1[5:7])
        dia = int(data1[8:10])

        #pyautogui.press("win")

        if cont == 1:
            rot1 = rotasClickBuss(origem, destino, est_origem, est_destin, ano, mes, dia)
        elif cont >= 2:
            rot2 = rotasClickBuss(origem, destino, est_origem, est_destin, ano, mes, dia)
            rot1.extend(rot2)

        hoje += datetime.timedelta(days=1)

    cont = 0

    dados[f"{origem} - {destino}"] = rot1


with open('jsons_ofertas\OfertasClickBussTESTE.json', 'w') as mijson:
    json.dump(dados, mijson, indent=4)"""
