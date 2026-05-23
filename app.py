import streamlit as st
import pandas as pd
import joblib
import plotly.express as px


st.set_page_config(
    page_title="Sistema Preditivo de Obesidade",
    page_icon="🏥",
    layout="wide"
)

# Dicionários para exibir em português, mas enviar para o modelo no padrão original da base
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

smoke_options = {
    "Não": "no",
    "Sim": "yes"
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
    "1 - < 1 L/dia": 1,
    "2 - 1-2 L/dia": 2,
    "3 - > 2 L/dia": 3
}

faf_options = {
    "0 - Nenhuma": 0,
    "1 - ~1-2×/sem": 1,
    "2 - ~3-4×/sem": 2,
    "3 - 5×/sem ou mais": 3
}

tue_options = {
    "0 - ~0-2 h/dia": 0,
    "1 - ~3-5 h/dia": 1,
    "2 - > 5 h/dia": 2
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

df_display = df.copy()
df_display["Obesity"] = df_display["Obesity"].map(obesity_translation)

def translate_column(column, mapping):
    return column.map(mapping).fillna(column)

df_display["family_history"] = translate_column(df_display["family_history"], {v: k for k, v in family_history_options.items()})
df_display["FAVC"] = translate_column(df_display["FAVC"], {v: k for k, v in yes_no_options.items()})
df_display["CAEC"] = translate_column(df_display["CAEC"], {v: k for k, v in caec_options.items()})
df_display["CALC"] = translate_column(df_display["CALC"], {v: k for k, v in calc_options.items()})
df_display["MTRANS"] = translate_column(df_display["MTRANS"], {v: k for k, v in mtrans_options.items()})

df_display["Gender"] = translate_column(df_display["Gender"], {v: k for k, v in gender_options.items()})

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
            "Consumo de lanches entre as refeições",
            list(caec_options.keys())
        )

        smoke_label = st.selectbox(
            "Hábito de fumar",
            list(smoke_options.keys())
        )

        ch2o_label = st.selectbox(
            "Consumo diário de água",
            list(ch2o_options.keys())
        )

        scc_label = st.selectbox(
            "Monitora ingestão calórica",
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

    input_data = pd.DataFrame({
        "Gender": [gender_options[gender_label]],
        "Age": [age],
        "Height": [height],
        "Weight": [weight],
        "family_history": [family_history_options[family_history_label]],
        "FAVC": [yes_no_options[favc_label]],
        "FCVC": [fcvc_options[fcvc_label]],
        "NCP": [ncp_options[ncp_label]],
        "CAEC": [caec_options[caec_label]],
        "SMOKE": [smoke_options[smoke_label]],
        "CH2O": [ch2o_options[ch2o_label]],
        "SCC": [yes_no_options[scc_label]],
        "FAF": [faf_options[faf_label]],
        "TUE": [tue_options[tue_label]],
        "CALC": [calc_options[calc_label]],
        "MTRANS": [mtrans_options[mtrans_label]]
    })

    if st.button("Realizar previsão"):
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        classes = model.classes_

        prediction_pt = obesity_translation.get(prediction, prediction)
        st.success(f"Classificação prevista: **{prediction_pt}**")

        prob_df = pd.DataFrame({
            "Classe": [obesity_translation.get(classe, classe) for classe in classes],
            "Probabilidade": probabilities
        }).sort_values("Probabilidade", ascending=False)

        fig = px.bar(
            prob_df,
            x="Classe",
            y="Probabilidade",
            title="Distribuição de Probabilidades por Classe",
            labels={
                "Classe": "Classe de Peso",
                "Probabilidade": "Probabilidade (%)"
            },
            text="Probabilidade"
        )

        fig.update_traces(texttemplate="%{text:.2%}", textposition="outside")
        fig.update_layout(
            yaxis_tickformat=".0%",
            xaxis_title="Classe de Peso",
            yaxis_title="Probabilidade (%)",
            showlegend=False
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
        st.metric("Total de pacientes", len(df_display))

    with col2:
        st.metric("Idade média", f"{df_display['Age'].mean():.1f} anos")

    with col3:
        st.metric("Peso médio", f"{df_display['Weight'].mean():.1f} kg")

    with col4:
        st.metric("Altura média", f"{df_display['Height'].mean():.2f} m")

    st.divider()

    st.subheader("Distribuição dos níveis de obesidade")

    obesity_count = df_display["Obesity"].value_counts().reset_index()
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
            df_display,
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
            df_display.groupby(["family_history", "Obesity"])
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
            df_display.groupby(["FAF", "Obesity"])
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
                "Obesity": "Nível de obesidade",
                "Quantidade": "Quantidade"
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
            df_display.groupby(["FAVC", "Obesity"])
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
                "Obesity": "Nível de obesidade",
                "Quantidade": "Quantidade"
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
        Esta versão em Streamlit Cloud oferece uma experiência direta para análise e predição de obesidade.

        O aplicativo permite:

        - Inserir dados do paciente em português;
        - Gerar previsão do nível de obesidade;
        - Visualizar probabilidades por classe;
        - Acessar insights de variáveis importantes como peso, altura, hábitos alimentares e atividade física.

        O objetivo é apoiar a triagem inicial, tornando a análise mais rápida e acessível, sem substituir a avaliação clínica.

        A estrutura inclui:

        - pré-processamento dos dados;
        - modelo RandomForest treinado;
        - interface simples e interativa;
        - dashboard com métricas e gráficos.
        """
    )