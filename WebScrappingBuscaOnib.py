import datetime
import requests
from bs4 import BeautifulSoup
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


## FUNÇOES ##
def limpa_str(info_pag):
    valo_limpo = ''
    for values in info_pag:
        if values.isdigit():
            valo_limpo = f'{valo_limpo}' + f'{values}'
    return valo_limpo


def limpa_str_valor(valor):
    valor_limpo = limpa_str(valor)
    qntd_dig = len(valor_limpo) - 2
    cont = 0
    valor_menor = ''
    valor_maior = ''
    for splitad in valor_limpo:
        cont += 1
        if cont <= qntd_dig:
            valor_menor = f'{valor_menor}' + splitad
        else:
            valor_maior = f'{valor_maior}' + splitad
    valor_final = f'{valor_menor}' + '.' + f'{valor_maior}'
    return valor_final


def limpa_str_horas(valor):
    valor_limpo = limpa_str(valor)
    qntd_dig = len(valor_limpo) - 2
    cont = 0
    valor_menor = ''
    valor_maior = ''
    for splitad in valor_limpo:
        cont += 1
        if cont <= qntd_dig:
            valor_menor = f'{valor_menor}' + splitad
        else:
            valor_maior = f'{valor_maior}' + splitad
    valor_final = f'{valor_menor}' + ':' + f'{valor_maior}'
    return valor_final


def rotas_concorrentes(saida, destino, ano, mes, dia):
    ender = requests.get(f'https://www.buscaonibus.com.br/horario/{saida}/{destino}?dt={dia}/{mes}/{ano}')
    print(f'BUSCA ONIBUS {ender}')
    ender_get = ender.content
    bea = BeautifulSoup(ender_get, 'html.parser')

    # HTML DA PAGINA
    feed = bea.findAll('div', attrs={'class': 'bo-timetable-info'})

    empresas = []
    lista_paramet = []
    lista_tempo = []

    cont = 0
    for info in feed:
        cont += 1

        preco = info.find('div', attrs={'class': 'bo-timetable-price'})
        empresa = info.find('div', attrs={'class': 'bo-timetable-company-name'})
        tipo_leito = info.find('div', attrs={'class': 'bo-timetable-type'})
        hr_saida = info.find('span', attrs={'class': 'bo-timetable-departure'})
        hr_chedada = info.find('span', attrs={'class': 'bo-timetable-arrival'})
        qtd_leito = info.find('div', attrs={'class': 'bo-timetable-seats'})

        preco_limpo = limpa_str_valor(preco.text)
        hr_saida_limpo = limpa_str_horas(hr_saida.text)
        hr_chedada_limpo = limpa_str_horas(hr_chedada.text)
        qtd_leito_limpo = limpa_str(qtd_leito.text)

        lista_tempo.append(str(datetime.date(int(ano), int(mes), int(dia))))
        lista_tempo.append(empresa.text)
        lista_tempo.append(preco_limpo)
        lista_tempo.append(hr_saida_limpo)
        lista_tempo.append(hr_chedada_limpo)
        lista_tempo.append(tipo_leito.text)
        lista_tempo.append(qtd_leito_limpo)

        if empresa.text == "Skyscanner":
            lista_tempo.append("Aviao")
        elif empresa.text == "BlaBlaCar":
            lista_tempo.append("Carro")
        else:
            lista_tempo.append("Onibus")

        lista_tempo.append(saida)
        lista_tempo.append(destino)
        lista_tempo.append(saida + " - " + destino)
        lista_tempo.append(str(datetime.date.today()))

        lista_paramet = lista_tempo.copy()
        empresas.append(lista_paramet)
        lista_tempo.clear()

    return empresas


"""funcao = 'SELECT * FROM ROTAS;'
rotas = abrirBD(funcao)

CidOrigem = []
CidDestin = []
EstOrigem = []
EStDestin = []

for a in rotas:
    CidOrigem.append(a[1])
    CidDestin.append(a[2])


Lorigem = CidOrigem
Ldestino = CidDestin

dados = {}
rotaRaiz = {}

data = datetime.date.today()
cont = 0
for i in range(len(Lorigem)):
    print(f'{i}° ROTA')
    origem = Lorigem[i]
    destino = Ldestino[i]
    hoje = datetime.date(2023, 2, 3)
    '''pyautogui.press('win')'''
    for j in range(20): #QUANTIDADE DE DIAS QUE VAI RODAR
        cont += 1
        data1 = str(hoje)
        ano = int(data1[0:4])
        mes = int(data1[5:7])
        dia = int(data1[8:10])

        pyautogui.press("win")
        if cont == 1:
            r1 = rotas_concorrentes(origem, destino, ano, mes, dia)
        elif cont >= 2:
            r2 = rotas_concorrentes(origem, destino, ano, mes, dia)
            r1.extend(r2)

        hoje += datetime.timedelta(days=1)

       #pyautogui.press("win")

    cont = 0

    dados[f"{Lorigem[i]} - {Ldestino[i]}"] = r1


with open('jsons_ofertas\DadosBuscO.json', 'w') as rotas:
    json.dump(dados, rotas, indent=4)"""
