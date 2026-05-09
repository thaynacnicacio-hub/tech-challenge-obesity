import streamlit as st
import pandas as pd
import plotly.express as px
import requests


API_URL = "http://api:5000/predict"

st.set_page_config(
    page_title="Sistema Preditivo de Obesidade",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Sistema Preditivo de Obesidade")

st.markdown(
    """
    Aplicação desenvolvida para auxiliar a equipe médica na classificação do nível de obesidade,
    utilizando uma arquitetura com **modelo de Machine Learning**, **API Flask**, **Streamlit** e **Docker Compose**.
    """
)

tab1, tab2 = st.tabs(["🔍 Predição via API", "ℹ️ Sobre a Arquitetura"])

with tab1:
    st.header("Previsão do nível de obesidade")

    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gênero", ["Female", "Male"])
        age = st.number_input("Idade", min_value=14, max_value=100, value=25)
        height = st.number_input("Altura em metros", min_value=1.30, max_value=2.20, value=1.70)
        weight = st.number_input("Peso em kg", min_value=30.0, max_value=250.0, value=70.0)

    with col2:
        family_history = st.selectbox("Histórico familiar de sobrepeso?", ["yes", "no"])
        favc = st.selectbox("Consome alimentos calóricos com frequência?", ["yes", "no"])
        fcvc = st.selectbox("Frequência de consumo de vegetais", [1, 2, 3])
        ncp = st.selectbox("Número de refeições principais por dia", [1, 2, 3, 4])

    with col3:
        caec = st.selectbox("Come entre as refeições?", ["no", "Sometimes", "Frequently", "Always"])
        smoke = st.selectbox("Fuma?", ["yes", "no"])
        ch2o = st.selectbox("Consumo diário de água", [1, 2, 3])
        scc = st.selectbox("Monitora calorias?", ["yes", "no"])

    col4, col5, col6 = st.columns(3)

    with col4:
        faf = st.selectbox("Frequência de atividade física", [0, 1, 2, 3])

    with col5:
        tue = st.selectbox("Tempo usando dispositivos eletrônicos", [0, 1, 2])

    with col6:
        calc = st.selectbox("Consumo de álcool", ["no", "Sometimes", "Frequently", "Always"])
        mtrans = st.selectbox(
            "Meio de transporte",
            [
                "Automobile",
                "Motorbike",
                "Bike",
                "Public_Transportation",
                "Walking"
            ]
        )

    input_data = {
        "Gender": gender,
        "Age": age,
        "Height": height,
        "Weight": weight,
        "family_history": family_history,
        "FAVC": favc,
        "FCVC": fcvc,
        "NCP": ncp,
        "CAEC": caec,
        "SMOKE": smoke,
        "CH2O": ch2o,
        "SCC": scc,
        "FAF": faf,
        "TUE": tue,
        "CALC": calc,
        "MTRANS": mtrans
    }

    if st.button("Realizar previsão"):
        try:
            response = requests.post(API_URL, json=input_data)

            if response.status_code == 200:
                result = response.json()

                prediction = result["prediction"]
                probabilities = result["probabilities"]

                st.success(f"Classificação prevista: **{prediction}**")

                prob_df = pd.DataFrame({
                    "Classe": list(probabilities.keys()),
                    "Probabilidade": list(probabilities.values())
                }).sort_values("Probabilidade", ascending=False)

                fig = px.bar(
                    prob_df,
                    x="Classe",
                    y="Probabilidade",
                    title="Probabilidade por classe"
                )

                st.plotly_chart(fig, use_container_width=True)

            else:
                st.error("Erro ao realizar previsão.")
                st.write(response.json())

        except Exception as error:
            st.error("Não foi possível conectar com a API Flask.")
            st.write(error)

with tab2:
    st.header("Arquitetura da solução")

    st.markdown(
        """
        Esta versão utiliza uma arquitetura mais próxima de produção:

        **1. Container de treinamento**
        
        Responsável por carregar a base `Obesity.csv`, treinar o modelo de Machine Learning e salvar o modelo treinado.

        **2. API Flask**
        
        Responsável por carregar o modelo treinado e expor um endpoint `/predict` para receber os dados e retornar a previsão.

        **3. Interface Streamlit**
        
        Responsável por exibir a aplicação para o usuário final e consumir a API Flask.

        **4. Docker Compose**
        
        Responsável por orquestrar os containers de treinamento, API e Streamlit.
        """
    )