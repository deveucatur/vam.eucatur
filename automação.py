from WebScrappingBuscaOnib import rotas_concorrentes
from ScrapingClickBuss import rotasClickBuss
import datetime
import json
import mysql.connector

conexao = mysql.connector.connect(
        passwd='nineboxeucatur',
        port=3306,
        user='ninebox',
        host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
        database='Vam-Eucatur'
    )
cursor = conexao.cursor()

comando = f'SELECT origem, destino FROM ROTAS'
cursor.execute(comando)
cidades = cursor.fetchall()

comandoRotas = 'SELECT * FROM ROTAS;'
cursor.execute(comandoRotas)
rotas = cursor.fetchall()


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

dadosClick = {}
dadosBusca = {}
rotaRaiz = {}

data = datetime.date.today()
cont = 0

print('---'*30 + 'INICIO DO SCRIPPING' + '---'*30)
for i in range(len(Lorigem)):
    origem = Lorigem[i]
    destino = Ldestino[i]
    est_origem = EstOrigem[i]
    est_destin = EstDestin[i]
    hoje = datetime.date(2023, 12, 25)

    print(f'''{i}° ROTA 

{origem} - {destino}''')

    for j in range(7): #QUANTIDADE DE DIAS QUE VAI RODAR
        cont += 1
        data1 = str(hoje)
        print(hoje)
        ano = int(data1[0:4])
        mes = int(data1[5:7])
        dia = int(data1[8:10])

        #pyautogui.press("win")

        if cont == 1:
            click1 = rotasClickBuss(origem, destino, est_origem, est_destin, ano, mes, dia)
            busca1 = rotas_concorrentes(origem, destino, ano, mes, dia)
        elif cont >= 2:
            click2 = rotasClickBuss(origem, destino, est_origem, est_destin, ano, mes, dia)
            busca2 = rotas_concorrentes(origem, destino, ano, mes, dia)
            click1.extend(click2)
            busca1.extend(busca2)

        hoje += datetime.timedelta(days=1)

    cont = 0

    dadosClick[f"{origem} - {destino}"] = click1
    dadosBusca[f"{origem} - {destino}"] = busca1

    # SALVANDO AS INFORMAÇÕES EM JSONS PARA CASO OCORRA ALGUM ERRO
    with open(f'OfestasBuscaTemporario{datetime.date.today()}.json', 'w') as ofertas:
        json.dump(dadosBusca, ofertas, indent=4)
    with open(f'OfestasClickTemporario{datetime.date.today()}.json', 'w') as ofertas1:
        json.dump(dadosClick, ofertas1, indent=4)

print('------- AGORA SE INICIA O PROCESSO DE CONCATENAÇÃO -------')
rotas = [f'{x[0]} - {x[1]}'.upper() for x in cidades]

cont = 0
for a in rotas:
    cont += 1
    print(cont)
    print(a)
    if a in [x for x in dadosBusca] and a in [x for x in dadosClick]:
        list_empresa1 = []
        list_empresa2 = []
        for b in dadosBusca[a]:
            list_empresa1.append(f'{b[1]}'.upper())
        for c in dadosClick[a]:
            list_empresa2.append(f'{c[1]}'.upper())

        empresa_new = [x for x in list_empresa2 if x not in list_empresa1 and x != 'MATRIZ']

        for d in range(len(dadosClick[a])):
            empresa_da_list = f'{dadosClick[a][d][1]}'.upper()
            if empresa_da_list in empresa_new:
                print(f'EMPRESAS JSON 2 {empresa_da_list}')
                dadosBusca[a].append(dadosClick[a][d])
        print(f'NOVAS EMPRESAS {empresa_new}')


print('Arquivo json criado para caso haja problemas.')
with open(f'jsons_ofertas\OfertasConcatenadas2{datetime.date.today()}.json', 'w') as rotas:
    json.dump(dadosBusca, rotas, indent=4)

#continuar = 0
#while continuar != 1:
#    continuar = int(input('''DESEJA SEGUIR E ARMAZENAR AS INFORMAÇÕES NO BANCO DE DADOS?
#
#    [1] - PARA CONTINUAR
#
#R:'''))


print('AGORA SE INICIA O PROCESSO DE SALVAR AS ROTAS NO BANCO DE DADOS')
for rotas in dadosBusca:
    print(rotas)
    cont_ofert = 0
    for ofertas in dadosBusca[rotas]:
        cont_ofert += 1
        comando = f'insert INTO OFERTAS(data_rota, empresa, valor, hr_saida, hr_chegada, tipo_leito, qntd_leito, tipo_transpot, cidade_origem, cidade_destino, rota, data_de_atualizacao) VALUES ("{ofertas[0]}","{ofertas[1]}", {float(ofertas[2]) if len([x for x in str(ofertas[2]) if str(x).isdigit()]) > 0 else 0}, "{ofertas[3]}", "{ofertas[4]}", "{ofertas[5]}", "{ofertas[6]}", "{ofertas[7]}","{ofertas[8]}", "{ofertas[9]}", "{ofertas[10]}", "{ofertas[11]}");'

        cursor.execute(comando)
        conexao.commit()
