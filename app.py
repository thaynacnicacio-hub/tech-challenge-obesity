import streamlit as st
import pandas as pd
import joblib
import plotly.express as px


st.set_page_config(
    page_title="Sistema Preditivo de Obesidade",
    page_icon="🏥",
    layout="wide"
)


@st.cache_data
def load_data():
    df = pd.read_csv("data/Obesity.csv")

    cols_to_round = ["FCVC", "NCP", "CH2O", "FAF", "TUE"]
    for col in cols_to_round:
        df[col] = df[col].round()

    return df


@st.cache_resource
def load_model():
    return joblib.load("model/obesity_model.pkl")


df = load_data()
model = load_model()

st.title("🏥 Sistema Preditivo de Obesidade")

st.markdown(
    """
    Aplicação desenvolvida para auxiliar a equipe médica na análise de risco 
    e classificação do nível de obesidade com base em características físicas, 
    hábitos alimentares e estilo de vida.
    """
)

tab1, tab2, tab3 = st.tabs(
    ["🔍 Predição", "📊 Dashboard Analítico", "ℹ️ Sobre o Projeto"]
)

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

    input_data = pd.DataFrame({
        "Gender": [gender],
        "Age": [age],
        "Height": [height],
        "Weight": [weight],
        "family_history": [family_history],
        "FAVC": [favc],
        "FCVC": [fcvc],
        "NCP": [ncp],
        "CAEC": [caec],
        "SMOKE": [smoke],
        "CH2O": [ch2o],
        "SCC": [scc],
        "FAF": [faf],
        "TUE": [tue],
        "CALC": [calc],
        "MTRANS": [mtrans]
    })

    if st.button("Realizar previsão"):
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        classes = model.classes_

        st.success(f"Classificação prevista: **{prediction}**")

        prob_df = pd.DataFrame({
            "Classe": classes,
            "Probabilidade": probabilities
        }).sort_values("Probabilidade", ascending=False)

        fig = px.bar(
            prob_df,
            x="Classe",
            y="Probabilidade",
            title="Probabilidade por classe"
        )

        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("📊 Dashboard Analítico")

    st.markdown(
        """
        Esta visão analítica tem como objetivo apoiar a equipe médica na compreensão dos principais
        fatores associados aos diferentes níveis de obesidade presentes na base de dados.
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de pacientes", len(df))

    with col2:
        st.metric("Idade média", f"{df['Age'].mean():.1f} anos")

    with col3:
        st.metric("Peso médio", f"{df['Weight'].mean():.1f} kg")

    with col4:
        st.metric("Altura média", f"{df['Height'].mean():.2f} m")

    st.divider()

    st.subheader("Distribuição dos níveis de obesidade")

    obesity_count = df["Obesity"].value_counts().reset_index()
    obesity_count.columns = ["Nível de obesidade", "Quantidade"]

    fig_obesity = px.bar(
        obesity_count,
        x="Nível de obesidade",
        y="Quantidade",
        title="Quantidade de pacientes por nível de obesidade",
        text="Quantidade"
    )

    st.plotly_chart(fig_obesity, use_container_width=True)

    st.info(
        "Insight: a distribuição dos níveis de obesidade permite identificar quais grupos são mais frequentes na base, "
        "ajudando a equipe médica a direcionar ações preventivas e estratégias de acompanhamento."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Peso x Altura por nível de obesidade")

        fig_scatter = px.scatter(
            df,
            x="Height",
            y="Weight",
            color="Obesity",
            title="Relação entre altura, peso e nível de obesidade",
            labels={
                "Height": "Altura",
                "Weight": "Peso",
                "Obesity": "Nível de obesidade"
            }
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        st.info(
            "Insight: pacientes com maior peso em relação à altura tendem a se concentrar em classes mais elevadas "
            "de obesidade, reforçando a importância desses indicadores na triagem médica."
        )

    with col2:
        st.subheader("Histórico familiar x nível de obesidade")

        family_obesity = (
            df.groupby(["family_history", "Obesity"])
            .size()
            .reset_index(name="Quantidade")
        )

        fig_family = px.bar(
            family_obesity,
            x="family_history",
            y="Quantidade",
            color="Obesity",
            barmode="group",
            title="Histórico familiar de sobrepeso por nível de obesidade",
            labels={
                "family_history": "Histórico familiar",
                "Obesity": "Nível de obesidade"
            }
        )

        st.plotly_chart(fig_family, use_container_width=True)

        st.info(
            "Insight: o histórico familiar pode indicar maior predisposição ao excesso de peso, sendo uma variável "
            "relevante para avaliação preventiva."
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Atividade física x nível de obesidade")

        activity_obesity = (
            df.groupby(["FAF", "Obesity"])
            .size()
            .reset_index(name="Quantidade")
        )

        fig_activity = px.bar(
            activity_obesity,
            x="FAF",
            y="Quantidade",
            color="Obesity",
            barmode="group",
            title="Frequência de atividade física por nível de obesidade",
            labels={
                "FAF": "Frequência de atividade física",
                "Obesity": "Nível de obesidade"
            }
        )

        st.plotly_chart(fig_activity, use_container_width=True)

        st.info(
            "Insight: a frequência de atividade física ajuda a observar padrões comportamentais associados aos "
            "diferentes níveis de obesidade."
        )

    with col4:
        st.subheader("Consumo de alimentos calóricos x nível de obesidade")

        favc_obesity = (
            df.groupby(["FAVC", "Obesity"])
            .size()
            .reset_index(name="Quantidade")
        )

        fig_favc = px.bar(
            favc_obesity,
            x="FAVC",
            y="Quantidade",
            color="Obesity",
            barmode="group",
            title="Consumo frequente de alimentos calóricos por nível de obesidade",
            labels={
                "FAVC": "Consome alimentos calóricos?",
                "Obesity": "Nível de obesidade"
            }
        )

        st.plotly_chart(fig_favc, use_container_width=True)

        st.info(
            "Insight: o consumo frequente de alimentos altamente calóricos é um fator comportamental importante "
            "para análise de risco e orientação médica."
        )

    st.divider()

    st.subheader("Principais conclusões para a equipe médica")

    st.markdown(
        """
        - O peso e a altura são variáveis centrais para diferenciar os níveis de obesidade.
        - O histórico familiar aparece como um fator importante para avaliação preventiva.
        - Hábitos como consumo de alimentos calóricos, prática de atividade física e ingestão de água ajudam a compor uma visão mais completa do paciente.
        - O modelo preditivo pode apoiar a triagem inicial, mas não substitui a avaliação clínica realizada por profissionais da saúde.
        """
    )

with tab3:
    st.header("Sobre o projeto")

    st.markdown(
        """
        Este projeto utiliza uma base de dados sobre obesidade para construir 
        uma solução analítica e preditiva voltada ao apoio da tomada de decisão médica.

        A aplicação contempla:

        - Tratamento e preparação dos dados;
        - Feature engineering;
        - Treinamento de modelo de Machine Learning;
        - Sistema preditivo em Streamlit;
        - Dashboard com principais insights analíticos;
        - Ambiente conteinerizado com Docker.
        """
    )