import pandas as pd
import datetime
import statistics
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
import json

icone = Image.open('icone.png')
st.set_page_config(
    page_title="VAM EUCATUR",
    page_icon=icone,
    layout="centered")

with open('ROTAS.json', 'r') as rotas:
    dados = json.load(rotas)

origem_dados = [r for r in dados['Origem']]
destino_dados = [x for x in dados['Destino']]

with open('CidadeBrasil.json','r') as dado:
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

    st.subheader('''Nos ajude com o aprimoriamento do VAM!
Solicite aqui mais rotas.''')
    st.text('')
    col1, col2, col3 = st.columns(3)

    with col1:
        origem_user = st.selectbox('ORIGEM', [x for x in dic_cidades['Cidades']])

    with col2:
        destino_user = st.selectbox('DESTINO', [a for a in dic_cidades['Cidades']])

    with col3:
        st.text("")
        st.text("")
        button_lets = st.button('ENVIAR')

    if button_lets:

        print(origem_dados)
        print(destino_dados)

        ListaRotas = [f'{str(origem_dados[a]).upper()} - {str(destino_dados[a]).upper()}' for a in range(len(origem_dados))]
        print(ListaRotas)

        if f'{str(origem_user).upper()} - {str(destino_user).upper()}' not in ListaRotas:
            origem_dados.append(origem_user.upper())
            destino_dados.append(destino_user.upper())
            st.markdown(f'Encaminhada a solicitação de inclusão da rota {origem_user} x {destino_user}.')
            
            for_json = {}
            for_json['Origem'] = origem_dados
            for_json['Destino'] = destino_dados
            with open('ROTAS.json', 'w') as myjson:
                json.dump(for_json, myjson, indent=4)
                
        elif origem_user == destino_user:
            st.markdown('Origem e Destino não podem ser iguais.')
        else:
            st.markdown('Rota já inclusa ao VAM.')




    
        col1, col2, col3 = st.columns(3)

        with col2:
            image3 = Image.open('AdN.png')
            st.image(image3, width=200, )

        st.caption("<h4 style='text-align: center; color: gray;'>Todos os direitos reservados</h2>", unsafe_allow_html=True)
        st.caption(
                "<h4 style='text-align: center; color: black;'>© 1964-2022 - v1 - EUCATUR - Empresa União Cascavel de Transportes e Turismo</h2>",
                unsafe_allow_html=True)
    
    
if add_radio == 'VAM':
    def plotarGrafComp(rota):
        d_precxdata = [float(x[2]) for x in rota if x[7] != "Aviao" and x[1] != "Eucatur"]
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
        col1, col2, col3 = st.columns(3)

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
                          columns=["Data", 'Empresa', "Preço", "Saída", "Chegada", "Tipo de Leito", "Assentos livres",
                                   "Tipo"])
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


    ################## Cod do front ############################


    image = Image.open('logo.png')
    st.image(image, width=250)

    st.title('Visualização de Análise de Mercado')

    with open("dadosConcorrencia.json", "r") as json_file:
        dados = json.load(json_file)

    col1, col2, col3 = st.columns(3)
    with col1:
        treRotas = st.selectbox("Selecione a Rota", [x for x in dados.keys()])

    with col2:
        print("")

    with col3:
        date = st.date_input(
            "Data", datetime.date.today())

    data1 = str(date)
    ano = data1[0:4]
    mes = data1[5:7]
    dia = data1[8:10]

    lisDatas = [str(datetime.date(int(ano), int(mes), int(dia)) + datetime.timedelta(days=x)) for x in range(5)]

    Empresa_list = sorted(set([x[:8][1] for x in dados[treRotas] if x[0] in lisDatas]))
    options_Empresa = st.multiselect('Selecione as empresas', Empresa_list, Empresa_list)

    Leito_list = sorted(set([x[:8][5] for x in dados[treRotas] if x[0] in lisDatas and x[1] in options_Empresa]))
    options_Leito = st.multiselect('Tipo de Leito', Leito_list, Leito_list)

    horarios_list = sorted(
        set([x[:8][3] for x in dados[treRotas] if
             x[0] in lisDatas and x[1] in options_Empresa and x[5] in options_Leito]))

    options_horario_ini, options_horario_fin = st.select_slider('Horario', options=horarios_list,
                                                                value=(horarios_list[0], horarios_list[-1]))

    if st.button('Buscar'):

        rota = [x[:8] for x in dados[treRotas] if x[0] in lisDatas and
                x[1] in options_Empresa and
                x[5] in options_Leito and
                x[3] in [x for x in horarios_list if x >= options_horario_ini and x <= options_horario_fin]
                ]

        st.header(f"Dados de {lisDatas[0]} até {lisDatas[-1]}")

        metricasConcorrencia(rota)
        TabelaDados(rota)

        d_precxdata = [[float(y[2]) for y in rota if y[0] == x and y[7] != "Aviao" and y[1] != "Eucatur"] for x in
                       lisDatas]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.boxplot(d_precxdata, labels=lisDatas)

        if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:

            try:
                d_precxdataEucatur = [[float(y[2]) for y in rota if y[0] == x and y[1] == "Eucatur"] for x in lisDatas]
                print(d_precxdataEucatur)
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

    col1, col2, col3 = st.columns(3)

    with col2:
        image3 = Image.open('AdN.png')
        st.image(image3, width=200, )

    st.caption("<h4 style='text-align: center; color: gray;'>Todos os direitos reservados</h2>", unsafe_allow_html=True)
    st.caption(
        "<h4 style='text-align: center; color: black;'>© 1964-2022 - v1 - EUCATUR - Empresa União Cascavel de Transportes e Turismo</h2>",
        unsafe_allow_html=True)


