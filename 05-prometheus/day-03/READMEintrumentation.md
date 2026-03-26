# Prometheus - Instrumentação Básica

## Visão Geral
Este repositório contém um projeto prático completo para aprender instrumentação de métricas Prometheus através de uma aplicação web e-commerce em Python (Flask) com banco de dados PostgreSQL. O código base da aplicação está localizado no diretório day-03/introducao-instrumentacao-main.

## O que é Instrumentar uma aplicação?
Significa adicionar código com um objetivo específico. Neste caso, o objetivo é expor as métricas internas da aplicação para que o Prometheus possa coletá-las e monitorá-las.

## Objetivos do Projeto
* Instrumentar aplicações com os 4 tipos de métricas nativas do Prometheus.

* Expor métricas de serviços que não as expõem nativamente, utilizando código.

* Configurar Exporters (Postgres Exporter) para coletar métricas de infraestrutura de banco de dados.

* Utilizar o Push Gateway para monitorar métricas de curta duração.

* Validar a coleta das informações através da exposição de endpoints /metrics.

* Deployar a solução completa em ambientes Docker Compose e Kubernetes.

## Tecnologias Utilizadas

* Prometheus: Coleta e armazenamento de métricas.
* prometheus_client: Biblioteca oficial Python para instrumentação.
* Postgres Exporter: Coleta de métricas do banco PostgreSQL.
* Push Gateway: Intermediário para métricas de curta duração.

## Aplicação & Infraestrutura
* Flask (Python): Framework da aplicação web e-commerce.
* PostgreSQL: Banco de dados relacional.
* Docker & Docker Compose: Containerização e ambiente local.
* Kubernetes: Orquestração (minikube, kind ou cluster real).

## Pré-requisitos
* Docker e Docker Compose instalados.
* Kubernetes configurado.
* Git.
* Python 3.8+ instalado localmente.

## Fundamentos: Tipos de Métricas no Prometheus
Antes de colocar a mão no código, precisamos definir quais métricas desejamos expor. O Prometheus trabalha com 4 tipos principais:

1. **Counter** (Contador)
Métrica cumulativa que apenas aumenta (ou reinicia do zero), sem a possibilidade de diminuir. É muito visualizada através de gráficos de barras ou de linha do tempo.

Exemplos de uso: Quantidade de requisições, total de erros retornados, quantos usuários fizeram login, total de mensagens processadas num worker, número de compras realizadas.

2. **Gauge** (Medidor)
Métrica que pode aumentar e diminuir ao longo do tempo. Serve para verificar o estado/fotografia atual de um recurso.

Exemplos de uso: Quantidade de RAM/CPU sendo consumida no momento, usuários simultâneos acessando o sistema, conexões ativas com o banco de dados, tamanho atual da fila de mensagens.

3. **Histogram** (Histograma)
Em vez de dar valores exatos únicos, o histograma agrupa os valores em faixas de distribuição (buckets). É essencial para avaliar metas de negócios como o SLO (Service Level Objective).

Por que não usar apenas a média? A média engana. Exemplo: De 100 requisições, a API respondeu 90 em 1s e 10 demoraram 10s. A média é de apenas 1.9s (parece excelente), no entanto, 10 pessoas tiveram uma experiência horrível de lentidão.

Exemplos de uso: Tempo de resposta de uma API. O histograma mostra exatamente quantas requisições foram respondidas em até 1s, quantas demoraram entre 1s e 2s, e quantas estouraram 5s.

4. **Summary** (Resumo)
Semelhante ao Histograma, mas enquanto o Histograma organiza dados em buckets predefinidos, o Summary trabalha entregando percentuais (quantiles).

Exemplo de uso: Descobrir em quanto tempo 95% das requisições foram respondidas. Se o resultado mostrar que o p95 (percentil 95) é 1s, significa que 95% dos usuários tiveram resposta em até 1 segundo.

Passo a Passo: Instrumentando a Aplicação Flask
Você pode consultar as bibliotecas oficiais em prometheus.io/docs/instrumenting/clientlibs. Para o nosso projeto Flask, usaremos a biblioteca Python: prometheus.github.io/client_python.

1. Preparando o Ambiente Local \
Primeiro, vamos isolar nosso ambiente de desenvolvimento e instalar as dependências.

```bash
# 1. Criar branch para a atividade
git checkout -b aula/instrumentacao

# 2. Criar e ativar o ambiente virtual Python
virtualenv .venv
source .venv/bin/activate

# 3. Carregar dependências atuais do projeto
pip install -r src/requirements.txt

# 4. Instalar a biblioteca do Prometheus e atualizar o requirements
pip install prometheus-client
pip freeze > src/requirements.txt
```

2. Configurando o Endpoint /metrics
No arquivo principal da aplicação (index.py), vamos importar os componentes iniciais, habilitar a rota /metrics e adicionar as informações do sistema.

Adicionar os imports em index.py:

```bash
from prometheus_client import Info, generate_latest, CONTENT_TYPE_LATEST
import sys
import platform
```
(Após os imports, adicione as linhas de código necessárias para expor a rota /metrics e inserir as informações do projeto).

3. Implementando as Métricas no Código
Para aplicar os conceitos, altere os arquivos metrics.py e index.py conforme cada objetivo abaixo.

* Dica de Validação: Após atualizar o código de cada métrica, suba o ambiente com o comando `docker compose up` e acesse a rota /metrics no navegador para confirmar se o nome da métrica e seus valores aparecem corretamente.

### Implementando o Counter: Ver Doc

Objetivo: Contar a quantidade de adições ao carrinho e a quantidade de erros no sistema.

###  Implementando o Gauge: Ver Doc

Objetivo: Medir o número atual de sessões ativas com carrinho e o uso de CPU sob demanda.

### Implementando o Histogram: Ver Doc

Objetivo: Acompanhar detalhadamente o tempo de resposta dos requests HTTP.