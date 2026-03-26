# Monitoramento PostgreSQL

## Visão Geral
Ainda utilizando a estrutura do projeto day-03, o objetivo agora é expandir a observabilidade para monitorar também o banco de dados PostgreSQL.

Como o PostgreSQL não disponibiliza um endpoint de métricas nativamente, utilizaremos o Postgres Exporter (Repositório Oficial: http://github.com/prometheus-community/postgres_exporter). Ele atua como um intermediário (middleware) entre o banco de dados e o Prometheus.

## O Que Já Temos (Métricas de Aplicação)
* Counter: ecommerce_cart_additions_total - Adições ao carrinho.
* Counter: ecommerce_errors_total - Erros no sistema.
* Gauge: ecommerce_active_sessions - Sessões ativas.
* Histogram: ecommerce_request_duration_seconds - Tempo de resposta HTTP.

## O Que Está Faltando (Métricas de Banco)
* Cache Performance: Hit ratio por tabela (explicar por que a tabela products é mais rápida que a order_items).
* Operações CRUD: INSERTs e UPDATEs rastreados diretamente no banco.
* Correlação Direta: Entender que 1 adição ao carrinho resulta em 1 INSERT na tabela order_items.
* Impacto no Cache: Como operações com alta taxa de escrita (write-heavy) afetam a performance geral.
* Padrões de Acesso: Diferenciar workloads focados em leitura (read-heavy) versus escrita (write-heavy).

---

## Solução: PostgreSQL Exporter

Por Que Usar um Exporter?
Diferente da aplicação Flask (onde inserimos o código Python diretamente), o PostgreSQL não suporta o Prometheus de forma nativa. O exporter externo resolve isso pois:

* Conecta no PostgreSQL via string de conexão.

* Executa queries em views internas do sistema (ex: pg_stat_*).

* Expõe as métricas traduzidas para o formato que o Prometheus entende.

* Roda como serviço separado, em um container independente.

## Arquitetura

* **E-commerce Stack (Componentes Locais):**
    * **Flask App:** É a nossa aplicação principal. Ela se conecta ao banco de dados para funcionar e expõe suas próprias métricas de software no endpoint `:5000/metrics`.
    * **PostgreSQL Database:** Nosso banco de dados relacional, rodando na porta padrão `:5432`.
    * **postgres_exporter:** O serviço auxiliar. Ele se conecta diretamente ao PostgreSQL para ler os dados do sistema e expõe essas métricas traduzidas no endpoint `:9187/metrics`.

* **Coleta de Métricas:**
    * **Prometheus:** O servidor central de monitoramento. Ele acessa ativamente a Flask App (para buscar métricas de código) e o postgres_exporter (para buscar métricas do banco) e consolida tudo em um só lugar.

---

## As 3 Métricas Integradas

### 1. Hit Ratio por Tabela - O Indicador de Performance
Conceito: É o percentual de dados que foram encontrados no cache (memória) em comparação com os dados que precisaram ser lidos do disco, medido para cada tabela específica.

#### PromQL:
```bash
Hit Ratio = (blocos em cache / (blocos em cache + blocos do disco)) × 100
(
  pg_statio_user_tables_heap_blks_hit{relname="products"} /
  (pg_statio_user_tables_heap_blks_hit{relname="products"} + pg_statio_user_tables_heap_blks_read{relname="products"})
) * 100
```

#### Padrões Esperados por Tipo de Workload:

- Read-Heavy (tabela products): 90-95% - Predominância de dados estáticos e muitas consultas. O Hit Ratio se mantém alto.
- Write-Heavy (tabela order_items): 60-80% - Inserção constante de dados novos (INSERTs).
- Mixed (tabela orders): 70-90% - Mistura de consultas ao histórico e entrada de novos pedidos.

#### Por Que Varia?
INSERTs frequentes significam dados novos, o que gera um cache miss inicial. Já em tabelas estáticas, os dados permanecem no cache por mais tempo. Além disso, muita atividade geral causa pressão no buffer pool, removendo dados antigos da memória.

### 2. INSERTs por Tabela - Correlação Perfeita
Métrica: `pg_stat_user_tables_n_tup_ins{relname="order_items"}`

#### Correlação Direta com a Aplicação:
Existe uma correlação de 1:1 entre a métrica da aplicação e a do banco:

```bash
rate(ecommerce_cart_additions_total[5m]) 
rate(pg_stat_user_tables_n_tup_ins{relname="order_items"}[5m])
```

#### Impacto no Hit Ratio:
Cada INSERT adiciona um novo bloco de dados, causando um cache miss inicial e diminuindo temporariamente o hit ratio da tabela afetada. Em contraste, tabelas que sofrem apenas SELECTs mantêm o hit ratio alto.

* Cenário Prático: Usuário adiciona produto -> INSERT em order_items -> Hit ratio de order_items cai. Usuário navega pelo catálogo -> SELECT em products -> Hit ratio de products se mantém alto.

### 3. UPDATEs por Tabela - Finalização do Processo
Métrica: `pg_stat_user_tables_n_tup_upd{relname="orders"}`

### Correlação com Checkout:
O momento de checkout reflete um UPDATE na tabela de pedidos (mudando o status de aberto para fechado).

```bash
Checkout = UPDATE na tabela orders (is_open=false)
rate(pg_stat_user_tables_n_tup_upd{relname="orders"}[5m])
```

#### Impacto no Cache:
UPDATEs podem invalidar o cache da linha que foi atualizada, mas o impacto no desempenho geral é menor quando comparado aos INSERTs, pois o bloco de dados já existe.

#### Métrica Bônus: DELETEs
Métrica: `pg_stat_user_tables_n_tup_del{relname="order_items"}`

* Cenário: Remoção de um item do carrinho.
* Conceito: Gera "dead tuples" no banco, que posteriormente precisarão ser limpas pelo processo de VACUUM. Complementa o rastreamento do ciclo CRUD.

---

## Sinergia das Métricas no E-commerce
Essas métricas se complementam para contar a história completa da aplicação. O Hit Ratio revela o impacto das operações na infraestrutura (cache), os INSERTs possuem ligação perfeita com as ações ativas dos usuários e os UPDATEs indicam a conclusão de fluxos de negócio.

### Ciclo Completo do Carrinho na Visão de Métricas:

1. Navegação (Read-Heavy): Gera SELECTs em products. Hit ratio de products fica acima de 95%. Nenhum INSERT/UPDATE.
2. Adicionar ao Carrinho (Write-Heavy): Gera INSERT em order_items. Correlação: 1 cart_addition = 1 INSERT. Hit ratio de order_items diminui devido aos dados novos.
3. Alterar Quantidade: Gera UPDATE em order_items. Hit ratio continua baixo por invalidação localizada do cache.
4. Finalizar Checkout: Gera UPDATE em orders (is_open=false). O checkout finaliza a transação.
5. Análise Final: products tem Hit ratio alto, order_items tem Hit ratio baixo, e orders mantém Hit ratio médio.

---

## Implementação e Deploy

**No Docker**
Siga a documentação do repositório oficial para configurar o serviço no arquivo compose.

1. Execute docker compose up -d.
2. Valide a execução com docker container ls. Você deve visualizar 3 containers rodando: a aplicação Flask, o banco PostgreSQL e o Postgres Exporter.

**No Kubernetes**
A implementação no K8s usa o padrão de arquitetura Sidecar.

1. O exporter é configurado como um container secundário (sidecar) dentro do mesmo Pod do banco de dados PostgreSQL (revisar linha 33 do manifesto).
2. As annotations do Prometheus devem ser adicionadas para permitir o scrape automático.
3. Aplique as configurações com: kubectl apply -f 01/k8s/deploy.yaml.
4. Acesse através do respectivo Service criado.

---

## Critérios de Sucesso e Validação
Para garantir que a implementação foi concluída corretamente, verifique os seguintes pontos testando os endpoints:

Comandos de Teste:
```bash
# Verificar métricas da aplicação Flask
curl http://localhost:5000/metrics
# Verificar métricas do PostgreSQL via Exporter
curl http://localhost:9187/metrics
```

### O que você deve encontrar:

* Os endpoints estão respondendo corretamente e expondo os dados no formato de texto do Prometheus.
* A infraestrutura está funcional tanto via Docker Compose quanto via Kubernetes.
* O Prometheus está conseguindo raspar (scrape) essas métricas automaticamente.
* Os valores das métricas incrementam conforme você interage com a aplicação (adicionando itens, navegando).

### Checklist de Métricas Essenciais Expostas:

* Flask: ecommerce_cart_additions_total, ecommerce_active_sessions, ecommerce_request_duration_seconds.
* PostgreSQL (via Exporter): `pg_stat_user_tables_n_tup_ins` (INSERTs), `pg_stat_user_tables_n_tup_upd` (UPDATEs), `pg_statio_user_tables_heap_blks_hit` (Hit ratio por tabela para avaliar a performance do cache).