import pandas as pd
import datetime
import statistics
import matplotlib.pyplot as plt
from PIL import Image
import requests
from bs4 import BeautifulSoup
import streamlit as st
import json


def plotarGrafComp(rota):
    d_precxdata = [float(x[2]) for x in rota if x[7] != "Aviao" and x[1] != "Eucatur"]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(d_precxdata)
    if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:
        try:
            d_precxdataEucatur = [float(x[2]) for x in rota if x[1] == "Eucatur"]
            ax.violinplot(d_precxdataEucatur, widths=0.25)
            st.markdown("**Eucatur vs Concorrência**")
        except ValueError:  
            pass
    st.pyplot(fig)

def metricasConcorrencia(rota):
    col1, col2, col3 = st.columns(3)

    with col1:
        if len([float(x[2]) for x in rota if x[1] != "Eucatur"]) > 0:
            st.metric(label="Preço mínimo", value=str(round(min([float(x[2])for x in rota]),2)))
        if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:
            st.metric(label="Preço mínimo Eucatur", value=str(round(min([float(x[2]) for x in rota if x[1] == "Eucatur"]), 2)),delta= str(round(min([float(x[2]) for x in rota if x[1] == "Eucatur"]) - min([float(x[2])for x in rota]) ,2)))

    with col2:
        if len([float(x[2]) for x in rota if x[1] != "Eucatur"]) > 0:
            st.metric(label="Preço médio", value=str(round(round(statistics.mean([float(x[2])for x in rota]),2),2)))
        if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:
            st.metric(label="Preço médio Eucatur", value=str(round(statistics.mean([float(x[2]) for x in rota if x[1] == "Eucatur"]), 2)),delta= str(round(statistics.mean([float(x[2]) for x in rota if x[1] == "Eucatur"]) - statistics.mean([float(x[2])for x in rota]) ,2)))

    with col3:
        if len([float(x[2]) for x in rota if x[1] != "Eucatur"]) > 0:
            st.metric(label="Preço máximo", value=str(round(max([float(x[2])for x in rota]),2)))
        if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:
            st.metric(label="Preço máximo Eucatur", value=str(round(max([float(x[2]) for x in rota if x[1] == "Eucatur"]), 2)),delta= str(round(max([float(x[2]) for x in rota if x[1] == "Eucatur"]) - max([float(x[2])for x in rota]) ,2)))

def TabelaDados(rota):
    df = pd.DataFrame(rota, columns=["Data", 'Empresa', "Preço", "Saída", "Chegada", "Tipo de Leito", "Assentos livres","Tipo"])
    st.dataframe(df, use_container_width=True)



################## Cod do front ############################

icone = Image.open('icone.png')
st.set_page_config(
    page_title="VAM EUCATUR",
    page_icon=icone,
    layout="centered")

image = Image.open('logo.png')
st.image(image,width=250,)

st.title('VAM - Análise de Concorrência')

with open("dadosConcorrencia.json", "r") as json_file:    
    dados = json.load(json_file)


col1, col2, col3 = st.columns(3)
with col1:
    treRotas = st.selectbox( "Selecione a Rota", [x for x in dados.keys()])
with col2:
    print("")

with col3:
    date = st.date_input(
    "Data",  datetime.date.today())

if st.button('Buscar'):

    data1 = str(date)
    ano = data1[0:4]
    mes = data1[5:7]
    dia = data1[8:10]

    lisDatas = [str(datetime.date(int(ano),int(mes),int(dia)) + datetime.timedelta(days= x))  for x in range(5)]

    rota = [x[:8] for x in dados[treRotas] if x[0] in lisDatas]

    st.header(f"Dados de {lisDatas[0]} até {lisDatas[-1]}")

    metricasConcorrencia(rota)
    TabelaDados(rota)

    d_precxdata = [[float(y[2]) for y in rota if y[0] == x and y[7] != "Aviao" and y[1] != "Eucatur"] for x in lisDatas]

    fig, ax = plt.subplots(figsize = (10,6))
    ax.boxplot(d_precxdata, labels = lisDatas)

    if len([float(x[2]) for x in rota if x[1] == "Eucatur"]) > 0:

        try:
            d_precxdataEucatur = [[float(y[2]) for y in rota if y[0] == x and y[1] == "Eucatur"] for x in lisDatas]
            print(d_precxdataEucatur)
            ax.violinplot(d_precxdataEucatur,widths = 0.25)
            st.markdown("**Eucatur vs Concorrência**")            
        except ValueError:  
            pass

    st.pyplot(fig)

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
    st.image(image3,width=200,)
    st.caption("Developed by Gabriel e Rodrigo")
    st.caption("")
    st.caption("Todos os direitos reservados")

st.subheader("© 1964-2022 - v1 - EUCATUR - Empresa União Cascavel de Transportes e Turismo")
