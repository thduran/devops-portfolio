# TechCommerce - Push Gateway & Batch Jobs

Sistema de e-commerce com instrumentação Prometheus focado em **Push Gateway** para métricas de jobs batch e processamento efêmero.

## 📋 Visão Geral

Este projeto demonstra a implementação de **Push Gateway** do Prometheus para coletar métricas de jobs batch que executam de forma efêmera (containers que iniciam, processam e finalizam).

### Componentes

- **Aplicação E-commerce**: Flask com PostgreSQL
- **Push Gateway**: Recebe métricas de jobs batch
- **Job Batch**: Relatório de vendas diário com métricas
- **PostgreSQL Exporter**: Métricas do banco de dados

## 🎯 Objetivo do Push Gateway

O **Push Gateway** resolve o problema de coletar métricas de jobs que:
- Executam por tempo limitado
- Não têm endpoint `/metrics` permanente  
- Finalizam antes do Prometheus fazer scraping
- Rodam em agendamentos (cron, Kubernetes Jobs)

## 🚀 Executando o Projeto

### 1. Iniciar Infraestrutura Base

```bash
# Subir banco, aplicação e Push Gateway
docker-compose up -d postgres app pushgateway postgres-exporter

# Verificar serviços
docker-compose ps
```

**URLs Disponíveis:**
- **Aplicação**: http://localhost:5000
- **Push Gateway**: http://localhost:9091
- **PostgreSQL Exporter**: http://localhost:9187

### 2. Gerar Dados de Vendas

Acesse a aplicação e faça alguns pedidos para gerar dados:

```bash
# Abrir aplicação no navegador
open http://localhost:5000

# Ou usar curl para adicionar produtos
curl -X POST http://localhost:5000/add_to_cart \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### 3. Executar Job Batch

```bash
# Relatório do dia atual
docker-compose run --rm batch

# Relatório de ontem
REPORT_DATE=yesterday docker-compose run --rm batch

# Data específica
REPORT_DATE=2025-09-21 docker-compose run --rm batch
```

### 4. Verificar Métricas

```bash
# Ver métricas no Push Gateway
curl http://localhost:9091/metrics

# Ou acessar interface web
open http://localhost:9091
```

## 📊 Métricas do Job Batch

### Métricas de Negócio

```promql
# Faturamento total do dia
daily_sales_revenue_total

# Quantidade de pedidos
daily_sales_orders_count  

# Ticket médio
daily_sales_avg_ticket_amount

# Receita do produto mais vendido
daily_sales_top_product_revenue
```

### Métricas Técnicas

```promql
# Duração total da geração
report_generation_duration_seconds

# Tamanho do PDF gerado
report_pdf_size_kilobytes

# Timestamp da última execução
report_last_run_timestamp

# Tempo de queries no banco
report_database_query_duration_seconds

# Tempo de geração do PDF
report_pdf_generation_duration_seconds
```

### Métricas do Processo Batch

O job batch também reporta métricas específicas do **processo de execução**:

#### Status e Controle
```promql
# Indica se o job está em execução (1) ou parado (0)
batch_job_running{job="daily-sales-report", instance="<hostname>"}

# Timestamp da última execução bem-sucedida
batch_job_last_success_timestamp{job="daily-sales-report"}

# Timestamp da última falha
batch_job_last_failure_timestamp{job="daily-sales-report"}

# Contador de execuções totais
batch_job_executions_total{job="daily-sales-report", status="success|failure"}
```

#### Performance do Sistema
```promql
# Uso de CPU durante execução (%)
batch_job_cpu_usage_percent{job="daily-sales-report"}

# Uso de memória em MB
batch_job_memory_usage_mb{job="daily-sales-report"}

# Número de conexões de banco abertas
batch_job_database_connections{job="daily-sales-report"}

# Taxa de throughput de dados processados
batch_job_data_throughput_records_per_second{job="daily-sales-report"}
```

#### Métricas de Erro e Debug
```promql
# Contador de erros por tipo
batch_job_errors_total{job="daily-sales-report", error_type="database|pdf|network"}

# Número de tentativas de retry
batch_job_retries_total{job="daily-sales-report", operation="database_query|push_metrics"}

# Tamanho da fila de processamento
batch_job_queue_size{job="daily-sales-report"}

# Latência de operações individuais
batch_job_operation_duration_seconds{job="daily-sales-report", operation="query|render|export"}
```

#### Labels Disponíveis

Todas as métricas incluem labels para filtragem e agrupamento:

```promql
# Labels padrão em todas as métricas batch
{
  job="daily-sales-report",           # Nome do job
  instance="<hostname>",              # Hostname/container ID
  report_date="2025-09-22",          # Data do relatório processado
  version="1.0.0",                   # Versão do job
  environment="production|staging"    # Ambiente de execução
}
```

#### Exemplo de Alertas Prometheus

```yaml
# alerts.yml
groups:
- name: batch-jobs
  rules:
  # Alerta se job não executou nas últimas 25 horas
  - alert: BatchJobNotExecuted
    expr: time() - batch_job_last_success_timestamp > 25 * 60 * 60
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Job batch não executou nas últimas 25 horas"
      
  # Alerta se duração do job excede 10 minutos
  - alert: BatchJobTooSlow
    expr: report_generation_duration_seconds > 600
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: "Job batch demorou mais que 10 minutos"
      
  # Alerta se falhas consecutivas
  - alert: BatchJobConsecutiveFailures
    expr: increase(batch_job_executions_total{status="failure"}[1h]) >= 3
    for: 0m
    labels:
      severity: critical
    annotations:
      summary: "Job batch falhando consecutivamente"
```

## 🔧 Configuração do Job Batch

### Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|---------|-----------|
| `DB_HOST` | `postgres` | Host do PostgreSQL |
| `DB_USER` | `ecommerce` | Usuário do banco |
| `DB_PASSWORD` | `Pg1234` | Senha do banco |
| `DB_NAME` | `ecommerce` | Nome do banco |
| `PUSHGATEWAY_URL` | `http://pushgateway:9091` | URL do Push Gateway |
| `REPORT_DATE` | `today` | Data: `yesterday`, `today`, `YYYY-MM-DD` |
| `LOG_LEVEL` | `INFO` | Nível de log |

### Customização da Data

```bash
# Relatório de ontem
REPORT_DATE=yesterday docker-compose run --rm batch

# Data específica  
REPORT_DATE=2025-09-20 docker-compose run --rm batch

# Hoje (padrão)
REPORT_DATE=today docker-compose run --rm batch
```

## 📁 Arquivos Gerados

Os relatórios PDF são salvos em:
- **Container**: `/app/reports/`
- **Volume**: `.docker_volumes/batch_reports/`
- **Formato**: `daily-sales-YYYY-MM-DD.pdf`

```bash
# Listar relatórios gerados
ls -la .docker_volumes/batch_reports/

# Visualizar relatório mais recente
open .docker_volumes/batch_reports/daily-sales-$(date +%Y-%m-%d).pdf
```

## 🏗️ Arquitetura do Job Batch

```
batch/
├── main.py              # Entry point principal
├── config/
│   └── settings.py      # Configurações centralizadas
├── database/
│   ├── connection.py    # Conexão SQLAlchemy
│   └── queries.py       # Repositório de dados
├── metrics/
│   ├── definitions.py   # Métricas Prometheus
│   └── publisher.py     # Publisher Push Gateway
├── reports/
│   ├── generator.py     # Orquestrador principal
│   └── pdf_engine.py    # Engine de PDF
└── templates/
    └── daily_sales.html # Template do relatório
```

## 🔍 Monitoramento e Debug

### Logs do Job Batch

```bash
# Ver logs em tempo real
docker-compose run --rm batch

# Debug detalhado
LOG_LEVEL=DEBUG docker-compose run --rm batch
```

### Verificar Push Gateway

```bash
# Status dos jobs
curl http://localhost:9091/api/v1/metrics

# Interface web com métricas
open http://localhost:9091

# Limpar métricas específicas (se necessário)
curl -X DELETE http://localhost:9091/metrics/job/daily-sales-report
```

### Validação de Dados

```bash
# Conectar no PostgreSQL para verificar dados
docker-compose exec postgres psql -U ecommerce -d ecommerce

# Ver pedidos recentes
SELECT created_at, total_price FROM orders WHERE is_open = false ORDER BY created_at DESC LIMIT 10;
```

## 🚨 Troubleshooting

### Job Falha - Sem Dados

```
❌ Falha na geração do relatório: Nenhum pedido encontrado no sistema
```

**Solução**: Acesse a aplicação e faça alguns pedidos primeiro.

### Push Gateway Não Acessível

```
⚠️ Push Gateway não acessível, mas continuando execução
```

**Verificação**:
```bash
# Verificar se Push Gateway está rodando
docker-compose ps pushgateway

# Testar conectividade
curl http://localhost:9091/metrics
```

### Erro de Conexão com Banco

```
❌ Erro ao buscar resumo diário: connection failed
```

**Verificação**:
```bash
# Verificar PostgreSQL
docker-compose ps postgres

# Testar conexão
docker-compose exec postgres pg_isready -U ecommerce
```

## 📈 Exemplo de Query Prometheus

Após configurar o Prometheus para scraping do Push Gateway:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'pushgateway'
    static_configs:
      - targets: ['pushgateway:9091']
```

**Queries úteis**:
```promql
# Faturamento dos últimos relatórios
daily_sales_revenue_total

# Comparar performance de geração
rate(report_generation_duration_seconds[1h])

# Últimas execuções do job
report_last_run_timestamp
```

## 💡 Casos de Uso

- **Relatórios diários** automatizados
- **Análise de performance** de jobs batch
- **Monitoramento de dados** de negócio
- **Alertas baseados** em métricas de vendas
- **Tracking de SLA** de processamento

---

**Autor**: TechCommerce DevOps Team  
**Versão**: 1.0  
**Última Atualização**: Setembro 2025