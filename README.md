# Tech Challenge - Fase 04: Sistema Preditivo de Obesidade

Este projeto foi desenvolvido para o Tech Challenge da Pós Tech em Data Analytics, com o objetivo de criar uma solução analítica e preditiva para auxiliar uma equipe médica na classificação do nível de obesidade de pacientes.
### Links do projeto

- Aplicação publicada no Streamlit Cloud: https://tech-challenge-obesity.streamlit.app
- Repositório GitHub: https://github.com/thaynacnicacio-hub/tech-challenge-obesity

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

## Arquitetura com Docker Compose, Flask e Streamlit

Além da versão publicada no Streamlit Cloud, o projeto também possui uma arquitetura containerizada, estruturada com três componentes principais:

```txt
train/      -> responsável pelo treinamento do modelo
api/        -> API Flask responsável por expor o endpoint de predição
streamlit/  -> interface web que consome a API Flask
Fluxo da solução

O fluxo da aplicação é organizado da seguinte forma:

Obesity.csv
   ↓
Container de treinamento
   ↓
Modelo treinado salvo em volume Docker
   ↓
API Flask carrega o modelo
   ↓
Streamlit envia os dados para a API
   ↓
API retorna a classificação prevista
Componentes da arquitetura
1. Treinamento do modelo

A pasta train/ contém o script responsável por carregar a base de dados, realizar o pré-processamento, treinar o modelo de Machine Learning e salvar o arquivo obesity_model.pkl.

O modelo utilizado foi o RandomForestClassifier, com pipeline contendo:

Padronização das variáveis numéricas;
One-Hot Encoding das variáveis categóricas;
Classificação multiclasse da variável alvo Obesity.

O modelo alcançou acurácia de aproximadamente 92,91% na base de teste.

2. API Flask

A pasta api/ contém uma API desenvolvida com Flask.

A API possui o endpoint:

POST /predict

Esse endpoint recebe os dados do usuário em formato JSON, aplica o mesmo padrão de tratamento utilizado no treinamento e retorna:

Classe prevista de obesidade;
Probabilidades associadas a cada classe.
3. Interface Streamlit

A pasta streamlit/ contém a interface web da aplicação.

Essa interface coleta os dados informados pelo usuário, envia uma requisição para a API Flask e exibe o resultado da previsão de forma visual e interativa.

4. Docker Compose

O arquivo docker-compose.yml é responsável por orquestrar os três serviços:

trainer   -> executa o treinamento do modelo
api       -> sobe a API Flask
streamlit -> sobe a interface web

O modelo treinado é salvo em um volume Docker compartilhado, permitindo que a API acesse o arquivo gerado pelo container de treinamento.

Como executar com Docker Compose

Para rodar a arquitetura completa localmente, execute:

docker compose up --build

Após a inicialização dos containers, acesse a aplicação em:

http://localhost:8501

A API Flask também ficará disponível em:

http://localhost:5000
Observação sobre o deploy

A versão publicada no Streamlit Cloud utiliza o arquivo app.py da raiz do projeto.

Já a arquitetura com Docker Compose utiliza a estrutura separada em train/, api/ e streamlit/, simulando um fluxo mais próximo de uma aplicação em produção.