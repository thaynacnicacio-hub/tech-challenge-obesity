# Tech Challenge - Fase 04: Sistema Preditivo de Obesidade

Este projeto foi desenvolvido para o Tech Challenge da Pós Tech em Data Analytics, com o objetivo de criar uma solução analítica e preditiva para auxiliar uma equipe médica na classificação do nível de obesidade de pacientes.
### Links do projeto

- Aplicação publicada no Streamlit Cloud: https://tech-challenge-obesity.streamlit.app
- Repositório GitHub: https://github.com/thaynacnicacio-hub/tech-challenge-obesity

## Objetivo do projeto

Construir uma solução completa de dados e Machine Learning para apoiar uma equipe médica na avaliação do nível de obesidade de pacientes.

O projeto contempla:

- Treinamento de modelo de classificação multiclasse;
- Interface de predição em português;
- Dashboard analítico com métricas e visualizações;
- Fluxo de produção com Docker Compose, API Flask e Streamlit.

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

### Opção 1: Docker tradicional (versão simples)

Esta opção executa apenas a aplicação Streamlit com o modelo treinado localmente.

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

### Opção 2: Docker Compose (arquitetura completa)

Use esta opção para rodar o fluxo completo com treinamento, API Flask e interface Streamlit separados.

```bash
docker compose up --build
```

Após a inicialização, acesse:

- Streamlit: http://localhost:8501
- API Flask: http://localhost:5000

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

Este projeto oferece duas formas de execução:

1. **Versão Streamlit Cloud** — utilizando `app.py` na raiz do projeto, ideal para deploy rápido e visualização online.
2. **Versão Docker Compose** — arquitetura containerizada com treinamento, API e interface separados.

### Componentes da arquitetura Docker Compose

- `train/` — container de treinamento que carrega `Obesity.csv`, pré-processa os dados, treina o modelo e salva `obesity_model.pkl`.
- `api/` — API Flask que carrega o modelo e expõe o endpoint `POST /predict`.
- `streamlit/` — interface Streamlit que envia os dados para a API e exibe a previsão.

### Fluxo da solução

1. O container de treinamento lê a base de dados e treina o modelo.
2. O modelo treinado é salvo em um volume Docker compartilhado.
3. A API Flask carrega o modelo desse volume e fica disponível para requisições.
4. A interface Streamlit envia os dados do usuário para a API e recebe a previsão.

### O que a API retorna

- Classe prevista de obesidade;
- Probabilidades de cada classe;
- Resultado em JSON para uso em front-end ou outros serviços.

### Benefícios dessa arquitetura

- Separação clara entre treinamento, inferência e interface;
- Melhor aproximação a um fluxo de produção;
- Reutilização do modelo por diferentes consumidores;
- Facilita testes e deploy em ambientes conteinerizados.

### Como executar com Docker Compose

```bash
docker compose up --build
```

Após a inicialização, acesse:

- Streamlit: http://localhost:8501
- API Flask: http://localhost:5000

### Deploy e versões

- A versão publicada no Streamlit Cloud utiliza `app.py` da raiz do projeto.
- A versão Docker Compose utiliza `streamlit/app.py` para a interface, consumindo a API Flask.

Isso permite mostrar tanto uma implantação simples em Streamlit quanto uma arquitetura mais robusta e modular para produção.