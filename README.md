# Tech Challenge - Fase 04: Sistema Preditivo de Obesidade

Este projeto foi desenvolvido para o Tech Challenge da Pós Tech em Data Analytics, com o objetivo de criar uma solução analítica e preditiva para auxiliar uma equipe médica na classificação do nível de obesidade de pacientes.

## Objetivo do projeto

Desenvolver uma pipeline de Machine Learning capaz de prever o nível de obesidade de uma pessoa com base em características físicas, hábitos alimentares, estilo de vida e histórico familiar.

Além do modelo preditivo, o projeto também conta com uma aplicação em Streamlit contendo:

- Sistema de predição individual;
- Dashboard analítico com insights sobre a base de dados;
- Visualização da probabilidade de cada classe prevista;
- Ambiente conteinerizado com Docker.

## Base de dados

A base utilizada foi o arquivo `Obesity.csv`.

A variável alvo do modelo é:

- `Obesity`: nível de obesidade.

As principais variáveis utilizadas incluem:

- Gênero;
- Idade;
- Altura;
- Peso;
- Histórico familiar de excesso de peso;
- Consumo de alimentos calóricos;
- Consumo de vegetais;
- Número de refeições principais;
- Consumo de água;
- Atividade física;
- Tempo usando dispositivos eletrônicos;
- Consumo de álcool;
- Meio de transporte.

## Modelo de Machine Learning

Foi utilizada uma pipeline com:

- Separação entre variáveis numéricas e categóricas;
- Padronização das variáveis numéricas com `StandardScaler`;
- Codificação das variáveis categóricas com `OneHotEncoder`;
- Treinamento com `RandomForestClassifier`.

A acurácia obtida foi de aproximadamente:

```txt
92,91%
```

Resultado acima do mínimo exigido de 75%.

## Tecnologias utilizadas

- Python
- Pandas
- Scikit-learn
- Joblib
- Streamlit
- Plotly
- Docker

## Como rodar o projeto localmente

Instale as dependências:

```bash
pip install -r requirements.txt
```

Treine o modelo:

```bash
python train_model.py
```

Execute a aplicação:

```bash
streamlit run app.py
```

Acesse no navegador:

```txt
http://localhost:8501
```

## Como rodar com Docker

Crie a imagem Docker:

```bash
docker build -t obesity-streamlit .
```

Execute o container:

```bash
docker run -p 8501:8501 obesity-streamlit
```

Acesse no navegador:

```txt
http://localhost:8501
```

## Estrutura do projeto

```txt
tech-challenge-obesity
├── data
│   └── Obesity.csv
├── model
│   └── obesity_model.pkl
├── app.py
├── train_model.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Visão de negócio

A aplicação pode apoiar a equipe médica como uma ferramenta auxiliar de triagem, permitindo analisar rapidamente fatores associados ao nível de obesidade de um paciente.

O sistema não substitui avaliação médica, mas contribui para uma tomada de decisão mais orientada por dados.