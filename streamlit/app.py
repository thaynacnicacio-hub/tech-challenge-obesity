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

# Dicionários para exibir em português, mas enviar para a API no padrão original da base
gender_options = {
    "Feminino": "Female",
    "Masculino": "Male"
}

yes_no_options = {
    "Sim": "yes",
    "Não": "no"
}

family_history_options = {
    "Sim, há histórico familiar": "yes",
    "Não há histórico familiar": "no"
}

fcvc_options = {
    "1 - Raramente": 1,
    "2 - Às vezes": 2,
    "3 - Sempre": 3
}

ncp_options = {
    "1 - Uma refeição principal por dia": 1,
    "2 - Duas refeições principais por dia": 2,
    "3 - Três refeições principais por dia": 3,
    "4 - Quatro ou mais refeições principais por dia": 4
}

caec_options = {
    "Não consome entre as refeições": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always"
}

ch2o_options = {
    "1 - Menos de 1 L/dia": 1,
    "2 - Entre 1 e 2 L/dia": 2,
    "3 - Mais de 2 L/dia": 3
}

faf_options = {
    "0 - Nenhuma atividade física": 0,
    "1 - Aproximadamente 1 a 2 vezes por semana": 1,
    "2 - Aproximadamente 3 a 4 vezes por semana": 2,
    "3 - 5 vezes por semana ou mais": 3
}

tue_options = {
    "0 - Aproximadamente 0 a 2 horas por dia": 0,
    "1 - Aproximadamente 3 a 5 horas por dia": 1,
    "2 - Mais de 5 horas por dia": 2
}

calc_options = {
    "Não bebe": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always"
}

mtrans_options = {
    "Carro": "Automobile",
    "Moto": "Motorbike",
    "Bicicleta": "Bike",
    "Transporte público": "Public_Transportation",
    "A pé": "Walking"
}

obesity_translation = {
    "Insufficient_Weight": "Abaixo do peso",
    "Normal_Weight": "Peso normal",
    "Overweight_Level_I": "Sobrepeso I",
    "Overweight_Level_II": "Sobrepeso II",
    "Obesity_Type_I": "Obesidade I",
    "Obesity_Type_II": "Obesidade II",
    "Obesity_Type_III": "Obesidade III"
}

tab1, tab2 = st.tabs(["🔍 Predição via API", "ℹ️ Sobre a Arquitetura"])

with tab1:
    st.header("Previsão do nível de obesidade")

    st.markdown(
        """
        Preencha os dados abaixo conforme as informações do paciente.  
        As opções seguem o dicionário da base `Obesity.csv`.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        gender_label = st.selectbox("Gênero", list(gender_options.keys()))
        age = st.number_input("Idade em anos", min_value=14, max_value=100, value=25)
        height = st.number_input("Altura em metros", min_value=1.30, max_value=2.20, value=1.70)
        weight = st.number_input("Peso em kg", min_value=30.0, max_value=250.0, value=70.0)

    with col2:
        family_history_label = st.selectbox(
            "Histórico familiar de excesso de peso?",
            list(family_history_options.keys())
        )

        favc_label = st.selectbox(
            "Consome alimentos muito calóricos com frequência?",
            list(yes_no_options.keys())
        )

        fcvc_label = st.selectbox(
            "Frequência de consumo de vegetais nas refeições",
            list(fcvc_options.keys())
        )

        ncp_label = st.selectbox(
            "Número de refeições principais por dia",
            list(ncp_options.keys())
        )

    with col3:
        caec_label = st.selectbox(
            "Consumo de lanches/comes entre as refeições",
            list(caec_options.keys())
        )

        smoke_label = st.selectbox(
            "Hábito de fumar",
            ["Não fuma", "Fuma"]
        )

        ch2o_label = st.selectbox(
            "Consumo diário de água",
            list(ch2o_options.keys())
        )

        scc_label = st.selectbox(
            "Monitora a ingestão calórica diária?",
            list(yes_no_options.keys())
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        faf_label = st.selectbox(
            "Frequência semanal de atividade física",
            list(faf_options.keys())
        )

    with col5:
        tue_label = st.selectbox(
            "Tempo diário usando dispositivos eletrônicos",
            list(tue_options.keys())
        )

    with col6:
        calc_label = st.selectbox(
            "Consumo de bebida alcoólica",
            list(calc_options.keys())
        )

        mtrans_label = st.selectbox(
            "Meio de transporte habitual",
            list(mtrans_options.keys())
        )

    smoke_value = "yes" if smoke_label == "Fuma" else "no"

    input_data = {
        "Gender": gender_options[gender_label],
        "Age": age,
        "Height": height,
        "Weight": weight,
        "family_history": family_history_options[family_history_label],
        "FAVC": yes_no_options[favc_label],
        "FCVC": fcvc_options[fcvc_label],
        "NCP": ncp_options[ncp_label],
        "CAEC": caec_options[caec_label],
        "SMOKE": smoke_value,
        "CH2O": ch2o_options[ch2o_label],
        "SCC": yes_no_options[scc_label],
        "FAF": faf_options[faf_label],
        "TUE": tue_options[tue_label],
        "CALC": calc_options[calc_label],
        "MTRANS": mtrans_options[mtrans_label]
    }

    if st.button("Realizar previsão"):
        try:
            response = requests.post(API_URL, json=input_data)

            if response.status_code == 200:
                result = response.json()

                prediction = result["prediction"]
                probabilities = result["probabilities"]

                prediction_pt = obesity_translation.get(prediction, prediction)

                st.success(f"Classificação prevista: **{prediction_pt}**")

                prob_df = pd.DataFrame({
                    "Classe": [
                        obesity_translation.get(classe, classe)
                        for classe in probabilities.keys()
                    ],
                    "Probabilidade": list(probabilities.values())
                }).sort_values("Probabilidade", ascending=False)

                fig = px.bar(
                    prob_df,
                    x="Classe",
                    y="Probabilidade",
                    title="Probabilidade por classe",
                    text="Probabilidade"
                )

                fig.update_traces(texttemplate="%{text:.2%}", textposition="outside")
                fig.update_layout(yaxis_tickformat=".0%")

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