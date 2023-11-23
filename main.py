import pandas as pd
import datetime
import statistics
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
import json
import mysql.connector

icone = Image.open('icone.png')
st.set_page_config(
    page_title="VAM EUCATUR",
    page_icon=icone,
    layout="wide")

conexao = mysql.connector.connect(
        passwd='nineboxeucatur',
        port=3306,
        user='ninebox',
        host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
        database='Vam-Eucatur'
    )

cursor = conexao.cursor()

comando = f'SELECT origem, destino FROM ROTAS;'
cursor.execute(comando)
rotas = cursor.fetchall()


ListaRotas = list(set(f'{str(x[0]).strip()} - {str(x[1]).strip()}' for x in rotas))

with open('CidadeBrasil.json', 'r') as dado:
    dic_cidades = json.load(dado)


with st.sidebar:
    st.title('MAIS OPÇÕES')

    add_radio = st.radio('Escolha um metodo',
                         ("VAM", "Inclusão de rotas")
                         )

if add_radio == 'Inclusão de rotas':
    image = Image.open('logo.png')

    st.image(image, width=250)


    st.title('INCLUSÃO DE ROTAS')

    with st.form("my_form"): 
        
        st.subheader('''Nos ajude com o aprimoriamento do VAM!
Solicite aqui mais rotas.''')
        st.text('')
        col1, col2 = st.columns(2)

        with col1:
            origem_user = st.selectbox('CIDADE ORIGEM', [x for x in dic_cidades['Cidades']])
            st.text('')
            destino_user = st.selectbox('CIDADE DESTINO', [a for a in dic_cidades['Cidades']])
            st.text("")
            st.text("")

        with col2:
            ESTADorigem = st.selectbox('ESTADO ORIGEM', [a for a in dic_cidades['Estados']])
            st.text('')
            ESTADestino = st.selectbox('ESTADO DESTINO', [b for b in dic_cidades['Estados']])

        submitted = st.form_submit_button("ENVIAR")
        if submitted:

            if f'{str(origem_user).upper()} - {str(destino_user).upper()}' not in ListaRotas and origem_user != destino_user:
                st.markdown(f'Encaminhada a solicitação de inclusão da rota {origem_user} x {destino_user}. \nA sua rota estará inclusa na próxima atualização do VAM.')

                conexao = mysql.connector.connect(
                    host='database-2.cwv7wd2g4l5m.sa-east-1.rds.amazonaws.com',
                    user='root',
                    password='ArqProcess0s',
                    database='OFERTAS_CONCORRENTES')
                cursor = conexao.cursor()

                comando = f'insert INTO ROTAS(origem, destino, estado_origem, estado_destino) VALUES ("{origem_user}","{destino_user}", "{ESTADorigem}", "{ESTADestino}");'
                cursor.execute(comando)
                conexao.commit()

                cursor.close()
                conexao.close()

            elif origem_user == destino_user:
                st.markdown('Origem e Destino não podem ser iguais.')
            else:
                st.markdown('Rota já solicitada ou já inclusa ao VAM.')

    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.caption("<h4 style='text-align: center; color: gray;'>Todos os direitos reservados</h2>", unsafe_allow_html=True)
    st.caption(
            "<h4 style='text-align: center; color: black;'>© 1964-2022 - v1 - EUCATUR - Empresa União Cascavel de Transportes e Turismo</h2>",
            unsafe_allow_html=True)

if add_radio == 'VAM':
    def plotarGrafComp(rota):
        d_precxdata = [float(x[2]) for x in rota if x[6] != "Aviao" and x[1] != "Eucatur"]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.boxplot(d_precxdata)
        if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:
            try:
                d_precxdataEucatur = [float(x[2]) for x in rota if x[1] == "Eucatur"]
                ax.violinplot(d_precxdataEucatur, widths=0.125)
                st.markdown("**Eucatur vs Concorrência**")
            except ValueError:
                pass
        st.pyplot(fig)


    def metricasConcorrencia(rota):
        col1, colaux, col2, colaux1, col3 = st.columns(5)

        with col1:
            if len([float(x[2]) for x in rota if x[1] != "Eucatur"]) > 0:
                st.metric(label="Preço mínimo", value=str(round(min([float(x[2]) for x in rota]), 2)))
            if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:
                st.metric(label="Preço mínimo Eucatur",
                          value=str(round(min([float(x[2]) for x in rota if x[1] == "Eucatur"]), 2)), delta=str(
                        round(min([float(x[2]) for x in rota if x[1] == "Eucatur"]) - min([float(x[2]) for x in rota]),
                              2)))

        with col2:
            if len([float(x[2]) for x in rota if x[1] != "Eucatur"]) > 0:
                st.metric(label="Preço médio",
                          value=str(round(round(statistics.mean([float(x[2]) for x in rota]), 2), 2)))
            if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:
                st.metric(label="Preço médio Eucatur",
                          value=str(round(statistics.mean([float(x[2]) for x in rota if x[1] == "Eucatur"]), 2)),
                          delta=str(
                              round(statistics.mean([float(x[2]) for x in rota if x[1] == "Eucatur"]) - statistics.mean(
                                  [float(x[2]) for x in rota]), 2)))

        with col3:
            if len([float(x[2]) for x in rota if x[1] != "Eucatur"]) > 0:
                st.metric(label="Preço máximo", value=str(round(max([float(x[2]) for x in rota]), 2)))
            if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:
                st.metric(label="Preço máximo Eucatur",
                          value=str(round(max([float(x[2]) for x in rota if x[1] == "Eucatur"]), 2)), delta=str(
                        round(max([float(x[2]) for x in rota if x[1] == "Eucatur"]) - max([float(x[2]) for x in rota]),
                              2)))


    def TabelaDados(rota):
        df = pd.DataFrame(rota,
                          columns=["Data", 'Empresa', "Preço", "Saída", "Chegada", "Tipo de Leito", "Tipo"])
        st.dataframe(df, use_container_width=True)


    def expliGraf():
        with st.expander("Ver explicação do gráfico"):
            col1, col2 = st.columns(2)
            with col1:
                st.header("CONCORRÊNCIA")
                imag_BOX = Image.open("BOXPLOT1.jpg")
                st.image(imag_BOX, width=315)
                st.write("""
                            GRÁFICO BOX PLOT

                            O diagrama identifica onde estão localizados 50% dos valores mais prováveis, a mediana e os valores extremos.

                            OUTLIER – Valores discrepantes ou extremos se comparado com outros.

                            MÁXIMO - Maior valor encontrado. (exceto Outliers)

                            MÍNIMO - Menor valor encotrado. (exceto Outliers)

                            TERCEIRO QUARTIL - A terceira linha de cima para baixo do retângulo central.

                            SEGUNDA QUARTIL OU MEDIANA - Segunda linha de cima para baixo do retângulo central.

                            PRIMEIRO QUARTIL - Primeira linha de cima para baixo do retângulo central.
                        """)

            with col2:
                st.header("EUCATUR")
                imag_VIOLI = Image.open("VIOLION1.png")
                st.image(imag_VIOLI, width=315)
                st.write("""
                    GRÁFICO VIOLINO

                    Os gráficos de violino são semelhantes aos gráficos box plot, exceto que eles também mostram a densidade de probabilidade dos dados em valores diferentes, geralmente suavizados por um estimador de densidade do kernel.

                    FUNCIONALIDADE:
                    É avaliado onde está localizado os preços da EUCATUR com o volume da direita para a esquerda do gráfico.
                    Quanto maior o volume,  maior ali a localização de valores naquele dia.


                """)


    def comer2digtHoras(hora):
        var = hora[:-3]
        return var


    ################## Cod do front ############################

    image = Image.open('logo.png')
    st.image(image, width=250)

    st.title('Visualização de Análise de Mercado')

    


    col1, col2, col3 = st.columns(3)
    with col1:
        treRotas = st.selectbox("Selecione a Rota", ListaRotas)

    with col2:
        print("")

    with col3:
        date = st.date_input(
            "Data", datetime.date.today())

    data1 = str(date)
    ano = data1[0:4]
    mes = data1[5:7]
    dia = data1[8:10]

    data2 = str(date + datetime.timedelta(days=5))
    ano2 = data2[0:4]
    mes2 = data2[5:7]
    dia2 = data2[8:10]

    with st.form("my_form1"): 
        lisDatas = [str(datetime.date(int(ano), int(mes), int(dia)) + datetime.timedelta(days=x)) for x in range(5)]
        try:
            comandaEmpresa = f'SELECT DISTINCT empresa, tipo_leito, hr_saida, hr_chegada FROM OFERTAS WHERE (rota = "{treRotas}") AND (data_rota >= "{ano}-{mes}-{dia}") AND (data_rota <= "{ano2}-{mes2}-{dia2}");'
            
            cursor.execute(comandaEmpresa)
            empresasBD = cursor.fetchall()

            Empresa_list = sorted(set(str(x[0]) for x in empresasBD))
            options_Empresa = st.multiselect('Selecione as empresas', Empresa_list, Empresa_list)

            leito_list = sorted(set([str(x[1]) for x in empresasBD]))
            options_Leito = st.multiselect('Tipo de Leito', leito_list, leito_list)

            #horarios_list1 = [str(x[2]) for x in empresasBD]
            #horarios_list2 = [str(x[3]) for x in empresasBD]
            #horarios_list = sorted(set(horarios_list1 + horarios_list2))
            
            #options_horario_ini, options_horario_fin = st.select_slider('Horario', options=horarios_list,  value=(horarios_list[0], horarios_list[-1]))
        except:
            st.text("Não existe nenhuma informação referente a essa rota.")
        

        botao = st.form_submit_button("PROCURAR")
        if botao:
            rota = []
            listaTemp = []
            listaOfic = []

            lista_Ofertas = []
            for a in options_Empresa:
                for b in options_Leito:
                    comandoOfertas = f'SELECT data_rota, empresa, valor, hr_saida, hr_chegada, tipo_leito, tipo_transpot FROM OFERTAS WHERE (empresa = "{a}") AND (tipo_leito = "{b}") AND (data_rota >= "{ano}-{mes}-{dia}") AND (data_rota <= "{ano2}-{mes2}-{dia2}") AND (rota = "{treRotas}");'
                    cursor.execute(comandoOfertas)
                    var = cursor.fetchall()

                    for info in range(len(var)):
                        list_temp = []
                        for vari in var[info]:
                            list_temp.append(str(vari))
                            lista_Ofertas.append(list_temp)

            rota = []
            for a in range(len(lista_Ofertas)):
                if lista_Ofertas[a] not in rota:
                    rota.append(lista_Ofertas[a])


            st.header(f"Dados de {lisDatas[0]} até {lisDatas[-1]}")

            metricasConcorrencia(rota)
            TabelaDados(rota)

            d_precxdata = [[float(y[2]) for y in rota if y[0] == x and y[6] != "Aviao" and y[1] != "Eucatur"] for x in
                        lisDatas]

            fig, ax = plt.subplots(figsize=(16, 12))
            ax.boxplot(d_precxdata, labels=lisDatas)

            if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:

                try:
                    d_precxdataEucatur = [[float(y[2]) for y in rota if y[0] == x and y[1] == "Eucatur"] for x in lisDatas]
                    ax.violinplot(d_precxdataEucatur, widths=0.25)
                    st.markdown("**Eucatur vs Concorrência**")
                except ValueError:
                    pass

            st.pyplot(fig)

            expliGraf()

            st.header("Dados por dia ")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(lisDatas)

            with tab1:
                rota1 = [x for x in rota if x[0] == lisDatas[0]]
                st.header(lisDatas[0])

                metricasConcorrencia(rota1)
                TabelaDados(rota1)
                plotarGrafComp(rota1)

            with tab2:
                rota2 = [x for x in rota if x[0] == lisDatas[1]]
                st.header(lisDatas[1])

                metricasConcorrencia(rota2)
                TabelaDados(rota2)
                plotarGrafComp(rota2)

            with tab3:
                rota3 = [x for x in rota if x[0] == lisDatas[2]]
                st.header(lisDatas[2])

                metricasConcorrencia(rota3)
                TabelaDados(rota3)
                plotarGrafComp(rota3)

            with tab4:
                rota4 = [x for x in rota if x[0] == lisDatas[3]]
                st.header(lisDatas[3])

                metricasConcorrencia(rota4)
                TabelaDados(rota4)
                plotarGrafComp(rota4)

            with tab5:
                rota5 = [x for x in rota if x[0] == lisDatas[4]]
                st.header(lisDatas[4])

                metricasConcorrencia(rota5)
                TabelaDados(rota5)
                plotarGrafComp(rota5)


    st.caption("<h4 style='text-align: center; color: gray;'>Todos os direitos reservados</h2>", unsafe_allow_html=True)
    st.caption(
        "<h4 style='text-align: center; color: black;'>© 1964-2023 - v1 - EUCATUR - Empresa União Cascavel de Transportes e Turismo</h2>",
        unsafe_allow_html=True)


