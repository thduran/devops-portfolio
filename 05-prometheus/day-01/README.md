## 1. Pilares da Observabilidade

### Métricas: Valores numéricos sobre software/infra.

Ex: CPU, nº de requisições, nº de instâncias.

### Logs: Info sobre eventos do app/infra.

### Tracing: Rastro do fluxo de eventos ao longo dos microserviços.

## Ferramentas

* Prometheus: Métricas
* Loki e Fluentbit: Log
* Jaeger: Tracing
* Grafana: Visualização

## Classificação de Métricas
As métricas se dividem em métricas de sistema e de negócio.

* Sistema: APIs mais acessadas, nº de erros.
* Negócio: Nº de usuários, nº de compras.

### Tipos de Métricas
* Counter: Só aumenta.
* Gauge: Aumenta e diminui.
* Histogram: Gráfico - amostragem de valor, frequência.
* Summary: Gráfico - porcentagem.

## 2. Arquitetura do Prometheus

* Prometheus Server
Tem o storage do TSDB, retrieval e o PromQL.

* TSDB (Time Series Database)
Armazena bloco de dados armazenados de 2 em 2h.
Pode configurar quando apagar/compactar os dados.
Ao compactar ganha espaço mas perde precisão.
Devido a isso métricas de negocio é recomendado armazenar em outro lugar e não no prometheus, que pode ficar so com as métricas de sistema.

* Adapter: Permite armazenar os dados em outros lugares, como o Elasticsearch, OpenTSDB. Ele pode ser somente leitura, somente escrita ou escrita e leitura.

* Retrieval
Parte de coleta das métricas.
A aplicação não envia as métricas, o Prometheus que coleta ativamente, a app só abre um endpoint pro Prometheus coletar.

* PromQL
Linguagem para executar queries.

### Componentes do Ecossistema

* Bibliotecas: São para facilitar a exposição e coleta de métricas como OpenTelemetry, AppMetrics, Micrometer.
* Exporter: Serve como intermediário para coletar métrica de ferramentas que não têm suporte nativo ao Prometheus, como Jenkins, MySQL.
* Push Gateway: Para processos de curta duração, armazena as métricas em cache.
* Service Discovery: São para quando há elasticidade.
* Alertas: Alertmanager checa se a regra é cumprida e manda pro Slack/Email/Telegram, etc.

## 3. Instalação do Prometheus via Docker

Comandos iniciais:

```bash
docker-compose up -d
docker container ls
Teste da API:
```

Browser teste:
localhost:8080/swagger

Clicar em GET produto, execute. Depois em POST produto, try it out, tira linha execute. No GET produto, execute

Teste: localhost:8080/metrics

---

## Hands-on:

Adicionando Prometheus no Docker Compose
(linhas 26 a 33)

Pra saber o nome da imagem certa: hub.docker.com.
Pesquisar prometheus, é o prom/prometheus by prom.
Usar a tag com a última versão sem ser a latest.

```bash
docker-compose up -d
docker container ls
```

Teste localhost:9090
* /graph: consulta promql
* /alerts
* /status: runtime, build infos
* /tsbd_status: infos do tsdb, métricas armazenadas
* /flags: configuração de linha de comando
* /config: estrutura de config do prom atual
* /rules
* /targets: endpoints que estão sendo coletados métricas

## 4. Configurando Scrape (Coleta)


4.1 No momento só tá coletando métricas do Prometheus, mas pra coletar da api:

Crio prometheus.yaml (até linha 17).
Mapeio volume no docker-compose.yaml (linha 21).

```bash
docker compose up -d
docker container ls
```
Dando um F5 em /config e /targets poderá ver as atualizações.

4.2 Coletando do MongoDB (Exporter)
Pra coletar do MongoDB também, vamos usar um exporter (linhas 28 a 37 do docker-compose.yaml).

Deve adicionar também no prometheus.yaml (linhas 19 a 24).

```bash
docker-compose up -d
docker container ls
```

Teste localhost:9216/metrics. Pegue http_request_duration_seconds_sum e joga no /graph.

## 5. Instalação via Kubernetes (Helm)

Primeiro deve instalar metric server. Teste com kubectl top pods.
Teremos deployment.yaml e service.yaml da API e deployment.yaml e service.yaml pro MongoDB.

```bash
kubectl apply -f .\ -R
kubectl get all
kubectl top pods --all-namespaces
```

Pegue o external IP do api-service e teste no browser. Ex. xx.xx.xx/swagger
Clicar GET produto, try it out, execute.
Testar /metrics.

Instalação do Prometheus (ArtifactHUB)
artifacthub.io > pesquisar prometheus e instalar seguindo o manual "get helm info".

`helm repo list prometheus-community` deve aparecer.
`helm search repo prometheus`

Configuração dos values:
`helm inspect values prometheus-community/prometheus > values.yaml`
Edições no arquivo values.yaml:
alertmanager: false
persistentVolume: false
service/type: loadbalancer
pushgatway: false

Salve o arquivo.

Instalação:
```bash
kubectl create ns prometheus
helm upgrade --install prometheus prometheus-community/prometheus --values ./values.yaml --namespace prometheus
kubectl get pods -n prometheus
kubectl get svc -n prometheus
```

Testar IP no browser.
Ir no /config só pra verificar.
/targets vai ver que não tá coletando do pod.

---

## Configurando Coleta (annotations)
Pra passar a coletar, precisa de annotations (k8s/api/deploy.yaml linhas 12 a 15).

`kubect apply -f ./api/deployment.yaml`
/targets pra ver se o pod tá sendo visto.

Teste: mudar quantidade de réplicas, aplica e ver /targets.

## Coleta do MongoDB em K8s (Sidecar)
Para coleta do MongoDB em k8s vamos usar um sidecar, que é um container auxiliar usado para requisitos não funcionais (linhas 26 a 33).

Declara que deve ser coletado com annotation (linhas 11 a 14).

```bash
kubectl apply -f ./mongodb/deployment.yaml
kubectl get pods
```

Ao checar /targets, ele terá a quantidade de réplicas + 1, que é o sidecar.
/graph: mongodb_up > execute.

## 6. PromQL (Querying)
Primeiro passo é ver qual métrica usar pelo /metrics.

### Exemplo 1: HTTP Requests
Vamos testar http_request_received_total > execute
Mostra quantidade agrupada por code (200, 404 etc), controller, entre outros.

Pra simular requisições, abre terminal:

```bash
while true; do curl http://localhost:8080/produto; sleep 1; done;
```

Em Table dá pra colocar espaço de tempo.
Em Graph aparece um gráfico.

Filtros:
Ele tá me retornando vários valores, dá pra filtrar pelo code 200: http_requests_received_total(code="200")
Pelo method: http_requests_received_total(method="GET")

### Exemplo 2: MongoDB Vamos ver outra métrica, agora do mongodb: mongodb_op_counters_total (número de comandos de consulta feitas no mongodb) agrupado por type.
Também posso filtrar, por exemplo, pelo type: mongodb_op_counters_total(type="query") (mostra só as consultas).

#### Operadores:
* Negação: PromQL aceita negação. mongodb_op_counters_total(type!="query") (mostra todos diferentes de query: delete, insert etc).
* Expressões Regulares: mongodb_op_counters_total(type=~"query|command") (mostra todos com type query e command).

Vetores e Tempo: Trabalhamos com instant vector, agora vamos ver range vector para usar métricas de certo tempo.
mongodb_op_counters_total[1m]: métricas do último minuto.

Se aparecer várias amostras, é devido ao scrape_interval. Se aparecer 12 amostras no ultimo minuto é o scrape interval que tá 5s (5x12=60s).

Adicionando [1m:5s]: na parte do 5s é recomendado colocar o mesmo valor do scrape interval para não resultar valor quebrado.

* Funções: Pra subir o nível do estudo, podemos usar funções (prometheus.io/docs/prometheus/latest/querying/functions).
As mais usadas são rate() (calcula média de chamadas/s) e sum() (soma os valores).

#### Exemplos:

* rate(http_requests_received_total[1m])
Vai mostrar agrupado. Mas queremos soma de tudo mesmo, então: sum(rate(http_requests_received_total[1m]))

Agregação: Se eu quiser fazer tipo um "group by" do SQL eu posso colocar "by (job)" no final da última query acima. Vai mostrar a soma de cada job, cada linha será a soma de um job.

* sum(rate(mongodb_op_counters_total[1m])) by (type)
Vai mostrar a soma de cada tipo (update, delete etc).

## 7. Alertmanager
Para o setup do Prometheus no K8s com alertas usaremos Helm.
Vamos alterar os values de configuração do helm e aplicar configurando os alert groups.

```bash
kubectl apply -f ./k8s -R
kubectl get all
kubectl port-forward svc/api-service 8080:80
```

Teste: localhost:8080/swagger > try it out, execute; Teste /metrics

Configuração do Helm:
artifacthub.io > pesquisar prometheus. Usar o prometheus-community.

```bash
helm repo list
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add kube-state-metrics https://kubernetes.github.io/kube-state-metrics
helm repo update
helm repo list
helm show values prometheus-community/prometheus > values.yaml
```

Na linha 1267 alerting_rules.yml: pega o conteúdo do alert.rules.yaml e cola.
Na linha 1244 alertmanagerFiles: pega o conteúdo dos routes de alertmanager.yml e cola no lugar certo, a mesma coisa com os receivers.

Instalação e Testes:
```bash
kubectl create ns monitoramento
helm install prometheus prometheus-community/prometheus --namespace=monitoramento --values ./values.yaml
kubectl get all -n monitoramento
```

Port-Forwarding:
```bash
kubectl port-forward svc/prometheus-server 8181:80 -n monitoramento
kubectl port-forward svc/prometheus-alertmanager 8282:80 -n monitoramento
kubectl port-forward svc/api-service 8080:80
```

Aumentar requisições para gerar alertas:

```bash
while true; do curl http://localhost:8080/produto; sleep 0.5; done
```

Em localhost:8181/alerts vai mostrar os alertas em "pending" depois "firing".
Em localhost:8282/alerts vai mostrar o alerta ativo.
Em /config verei a notificação ativa.

## 8. Conceitos e Regras do Alertmanager
O Alertmanager que tem as regras de manipulação de alertas que o Prometheus manda pra ele.
As configurações de alerta vão no alert.rules.yaml.

* Inactive: Quando a regra ainda não foi atingida.
* Pending: Regra foi atingida mas o tempo do "for" não foi atingido.
* Firing: Regra e tempo foram atingidos.

No firing, o Prometheus envia o alerta pro Alertmanager.
Posso silenciar, inibir ou agrupar alertas.

## 9. Alertmanager no Docker
Vamos criar as regras -> alert.rules.yaml.
Em prometheus.yaml, colocar rule_files (linha 6) e no docker-compose.yaml linha 43 mapear como volume.

```bash
docker-compose up -d
docker containenr ls
```

Teste: localhost:9090/alerts.

### Adicionando Alertmanager ao Compose
Coloco como serviço no docker-compose.yaml - linha 51.
No prometheus.yaml adiciono alerting - linha 29.

```bash
docker-compose down
docker-compose up -d
docker container ls
```

Teste: localhost:9090/config > vai ter o campo alerting.
Teste: localhost:9093

### Configuração Final e Teste
Agora é configurar o Alertmanager (alertmanager.yaml) e mapear no service do alertmanager - docker-compose.yaml linhas 55 a 58.
 
```bash
docker-compose up -d
```

Teste localhost:9093/status

Aumentar requisições para gerar alertas:
```bash
while true; do curl http://localhost:8080/produto; sleep 0.5; done
```

Teste:
localhost:9090/alerts > vai entrar em pending e firing.
No alertmanager (localhost:9093/alerts), os alertas vão aparecer.
No heroku vai aparecer o aledssrta.