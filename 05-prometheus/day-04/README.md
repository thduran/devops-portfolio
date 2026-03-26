### Consulta de métricas (PromQL)
Serve para troubleshooting, usar nas regras de envio de alertas, criação de dashboards, integração com API.

#### Estrutura
`funcoes(metric_selector{label_selector}[range_selector])`

- funcoes: pra manipular a informação

- metric_selector: é nome da métrica

- label_selector: para filtros. Ex. quero consultar a quantidade de requisições da aplicação, mas de um determinado http_status (200)

- range_selector: para tempo, amostragem dos dados na linha do tempo. ex. 5m

É importante saber com qual métrica vamos trabalhar, qual que responde uma pergunta que estamos a fazer. Primeiro passo é olhar a documentação, também podemos ir em `/metrics`.

Vamos pegar a `flask_http_request_total` e jogar no Prometheus. Ele pode mostrar o nome da app, a instância, nome do pod. Jogando o nome da métrica pura, o Prometheus retorna o resultado do momento atual.

Normalmente iremos filtrar. Ex. para pegar só os status 200, troque o label selector:

- `flask_http_request_total{status="200"}`

- Todas exceto 200: troca `=` por `!=`

- Se quero todas que comecem com 2: `flask_http_request_total{status=~"2.."}`

- Ou 400: `flask_http_request_total{status=~"2..|4.."}`

#### Range Selector
Vamos usar o range selector agora para a métrica `flask_http_request_duration_seconds_count`:

- `flask_http_request_duration_seconds_count[5m]`

Vai mostrar uma certa quantidade de registro, essa quantidade depende do `scrape_interval`. Se menor, mais registros, se maior, menos registros. Se o `scrape_interval` for muito pequeno, pode afetar o desempenho do Prometheus e até da aplicação. É preciso balancear entre precisão e desempenho.

#### Manipulação Temporal
`offset` é usado pra pegar o valor de uma métrica em determinado momento passado.

- Ex. `flask_http_request_duration_seconds_count offset 5m`

Se pegar `pg_database_size_bytes{datname="ecommerce"}` e fizer uma compra vai ver o numero aumentar.

- Se quiser ver o quanto aumentou: `pg_database_size_bytes{datname="ecommerce"} - pg_database_size_bytes{datname="ecommerce"} offset 10m`

- Se quero ver a porcentagem que aumentou nos últimos 10min: `(pg_database_size_bytes - pg_database_size_bytes offset 10m) / pg_database_size_bytes offset 10m * 100`

Para ver de um momento especifico, posso usar a interface de calendário que tem logo abaixo de 'table'. Também posso definir direto na query atraves de `@` - insira aqui o número de segundos desde o tempo que você quer até o momento atual.

#### Operadores Aritméticos
- `pg_database_size_bytes`: informa tamanho do banco

- `pg_database_size_bytes / 1024`: em kb

- `pg_database_size_bytes / 1024 / 1024`: em mb

- `pg_stat_database_blks_hit{datname="ecommerce"} / (pg_stat_database_blks_hit{datname="ecommerce"} + pg_database_blks_read{datname="ecommerce"}) * 100`: pega a porcentagem de utilização do cache

##### Legenda:

- hit: número de blocos que foram encontrados direto no cache

- read: || no disco

#### Operadores de Comparação
- `pg_database_size_bytes / 1024 / 1024 > 1000`: retorna os bancos que tem mais que 100M

- `pg_database_size_bytes / 1024 / 1024 != 0`: bancos ativos

- `pg_stat_database_blks_hit{datname="ecommerce"} / (pg_stat_database_blks_hit{datname="ecommerce"} + pg_database_blks_read{datname="ecommerce"}) * 100 < 90`: pega os que tem menos de 90% de cache hit

- `(pg_database_size_bytes / 1024 / 1024 > 500) and (pg_stat_database_blks_hit / (pg_stat_database_blks_hit + pg_database_blks_read) * 100 < 90)`: pega os bancos maiores que 500M e com cache hit menor que 90%

#### Funções de Agregação
Lembrando a estrutura da query: `funcao(metric_selector{label_selector}[5m])`

- `sum(pg_database_size_bytes)`: pega total de bytes que todo o Postgre está usando

- `sum(flask_http_request_total) by (method)`: pega total agrupando por `method`, pode ser (status) ou os dois (status,method)

- - usando `without` no lugar do `by` remove a label do agrupamento

- `avg(flask_http_request_total)`: média da métrica

- `avg(flask_http_request_total) by (method)` ou `(instance)`

- `avg(pg_stat_user_tables_n_live_tup)`: pega a média de registros ativos nas tabelas

- `count(up{app="ecommerce-app"})`: quantidade de réplicas da aplicação - `count` não soma as métricas, mas conta os registros

- `topk(3, sum by (path) (rate(flask_http_request_duration_seconds_sum[5m])) / sum by (path) (rate(flask_http_request_duration_seconds_count[5m])))`: pega os 3 endpoints mais lentos da aplicação Flask. `bottomk` seriam os mais rápidos

- `max(pg_database_size_bytes)`: quantidade de bytes do maior banco. `min` pegaria o menor

#### Taxa e Aumento:

- `rate` é pra pegar a taxa por segundo de um range vector

- - `flask_http_request_duration_seconds_count` - pega quantidade de requisições

- - `flask_http_request_duration_seconds_count[5m]` - últimos 5min

- - `rate(flask_http_request_duration_seconds_count[5m])` - quantidade de requisições por segundo nos ultimos 5 min

- - `sum(rate(flask_http_request_duration_seconds_count[5m]))` - agora o total (de todos os endpoints)

- - posso usar um `by (path)` no final para agrupar

- `increase(flask_http_request_total[1h])` - o quanto aumentou num periodo