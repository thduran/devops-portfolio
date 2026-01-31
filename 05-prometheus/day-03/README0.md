Veremos: como usar codigo para instrumentar a aplicação, os tipos de métricas que podemos usar no Prometheus, como trabalhar com exporters para coletar métricas de BD e serviços que não expões as métricas nativamente e o push gateway para métricas de curta duração

Instrumentara a aplicação: adicionar código para um objetio. No caso, expor as métricas de uma aplicação

A aplicação está em day-03/introducao-instrumentacao-main (aplicacao python)

Primeiro passo: definir quais  métricas desejamos expor, depois adicionar a biblioteca do prometheus no projeto

antes, criamos uma branch aula/instrumentacao
sobre a biblioteca, descobrimos qual é lá em prometheus.io/docs/instrumenting/clientlibs
usaremos python pois a app é em flask (prometheus.github.io/client_python)

vamos criar o ambiente virtual (venv python):
virtualenv .venv
source .venv/bin/activate

carregar dependencias atuais do projeto: pip install -r src/requirements.txt
adicionar a biblioteca do link no projeto: pip install prometheus-client
adc lib ao requirements.txt pip freeze > src/requirements.txt

vamos adicionar os componentes iniciais da lib do prometheus (index.py): (linhas x,x x)
from prometheus_client import Info, generate_latest, CONTENT_TYPE_LATEST
import sys
import platform

agora vamos habilitar o /metrics e adc algumas infos do projeto no /metrics (linhas 17 x a x) e x a x final cod

tipos de metricas
counter: cumulativa, apenas aumenta, sem possibilidade de diminuir
quantdd requisicoes, erros retornar, qts uusarios fizeram logins, qts mssgs processadar num worker, qts compras realizadas
costuma ser graficos de barra, de linha do tempo
gauge: pode aumentar e diminuir ao longo do tempo, pra verificar o estado atual de algo
qtd de memoria/cpu sendo consumida no momento, qtd usuarios acessando no momento, qtd conexoes ao BD ativas, tamanho atual da fila de msgs
histogram: não dá valores exatos, agrupa os valores em faixas (buckets)
tempo de resposta de uma api > histogram mostra quantas requisições foram respondidas em até 1s, quantas demoraram entre 1s e 2s, quantas passaram de 5s. Você não tem apenas a média, podendo entender melhor o comportamento da applicação. Essencial para avaliar o SLO - service level objective
A média pode enganar. ex. De 100 requisições, a API respondeu 90em 1s, 10 demoraram 10s. Média 1.9s. Mesmo que a média esteja ok, 10 pessoas tiveram uma experiência muito ruim
summary: o histogram organiza os dados em buckets, o summary trabalha com percentuais. ex: em quanto tempo 95% das requisições foram respondidas; se o resultado mostrar que o b95 é 1s, quer dizer que  95% das requisições foram respondidas em até 1s. 

implementando counter no projeto (prometheus.github.io/client_python/instrumenting/counter)
- qtd adições ao carrinho
- qtd erros no sistema

após atualizar metrics.py e index.py, dá um compose up e no /metrics vai ver o nome das metricas que adc

implementando gauge no projeto (prometheus.github.io/client_python/instrumenting/gauge)
- sessoes ativas com carrinho
- uso de cpu sob demanda

após atualizar metrics.py e index.py, dá um compose up e no /metrics vai ver o nome das metricas que adc

implementando histogram no projeto (https://prometheus.github.io/client_python/instrumenting/histogram/)
- tempo de resposta de requests http

após atualizar metrics.py e index.py, dá um compose up e no /metrics vai ver o nome das metricas que adc

# 📊 Curso Prometheus - Instrumentação Básica

## Visão Geral

Este repositório contém um **projeto prático completo** para aprender instrumentação de métricas Prometheus através de uma aplicação e-commerce.

> 🎓 **Este projeto faz parte da [Formação DevOps Pro](https://devopspro.com.br)**.

## 🎯 Objetivos do Curso

- **Instrumentar aplicações** com os 4 tipos de métricas Prometheus
- **Configurar Postgres Exporter** para métricas de infraestrutura
- **Validar coleta** de métricas via endpoints `/metrics`
- **Deployar em Docker e Kubernetes** com monitoramento

## 📁 Estrutura do Projeto

### **01-projeto-inicial/**
Aplicação e-commerce **original** sem instrumentação Prometheus - ponto de partida da aula.

### **00-documentacao/**
Material didático completo:
- **[METRICAS_PROMETHEUS.md](./00-documentacao/METRICAS_PROMETHEUS.md)**: Objetivos e conceitos da aula
- **[DESAFIO_INSTRUMENTACAO.md](./00-documentacao/DESAFIO_INSTRUMENTACAO.md)**: Desafio prático step-by-step

## 📚 Projeto: E-commerce Fake Shop

### 📖 **Instrumentação Completa**
- **Aplicação**: Flask + PostgreSQL
- **Métricas**: Counter, Gauge, Histogram, Summary
- **Exporter**: Postgres Exporter para métricas de banco
- **Ambientes**: Docker Compose e Kubernetes

## 🚀 Como Começar

### Pré-requisitos
- **Docker** e **Docker Compose**
- **Kubernetes** (minikube, kind, ou cluster)
- **Git**
- **Python 3.8+** (para módulos específicos)

### Quick Start

#### 📖 **Começar pelos Fundamentos**
```bash
# Ler objetivos e conceitos
cat 00-documentacao/METRICAS_PROMETHEUS.md

# Entender o desafio
cat 00-documentacao/DESAFIO_INSTRUMENTACAO.md
```

#### 🚀 **Executar Projeto Original**
```bash
# Navegar para aplicação base
cd 01-projeto-inicial

# Executar com Docker Compose
docker-compose up -d

# Acessar: http://localhost:5000
```

#### ⚡ **Implementar Instrumentação**
```bash
# Trabalhar na versão instrumentada
cd src

# Seguir instruções no CLAUDE.md
```

## 🛠️ Tecnologias Utilizadas

### **Core Stack**
- **Prometheus**: Coleta e armazenamento de métricas
- **prometheus_client**: Biblioteca Python para instrumentação
- **Postgres Exporter**: Métricas de banco PostgreSQL

### **Aplicação**
- **Flask** (Python): Aplicação web e-commerce
- **PostgreSQL**: Banco de dados para monitoramento

### **Infraestrutura**
- **Docker**: Containerização
- **Kubernetes**: Orquestração
- **Docker Compose**: Ambiente local

## 📚 Documentação

- **[Objetivos da Aula](./00-documentacao/METRICAS_PROMETHEUS.md)**: Fundamentos e conceitos
- **[Desafio Prático](./00-documentacao/DESAFIO_INSTRUMENTACAO.md)**: Implementação step-by-step
- **[Instruções Detalhadas](./CLAUDE.md)**: Comandos e configurações específicas
