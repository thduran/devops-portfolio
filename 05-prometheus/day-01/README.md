1. Pilares da Observabilidade
Métricas: Valores numéricos sobre software/infra.

Ex: CPU, nº de requisições, nº de instâncias.

Logs: Info sobre eventos do app/infra.

Tracing: Rastro do fluxo de eventos ao longo dos microserviços.

Ferramentas
Prometheus: Métricas

Loki e Fluentbit: Log

Jaeger: Tracing

Grafana: Visualização

Classificação de Métricas
As métricas se dividem em métricas de sistema e de negócio.

Sistema: APIs mais acessadas, nº de erros.

Negócio: Nº de usuários, nº de compras.

Tipos de Métricas
Counter: Só aumenta.

Gauge: Aumenta e diminui.

Histogram: Gráfico - amostragem de valor, frequência.

Summary: Gráfico - porcentagem.

2. Arquitetura do Prometheus
Prometheus Server
Tem o storage do TSDB, retrieval e o PromQL.

TSDB (Time Series Database)

Armazena bloco de dados armazenados de 2 em 2h.

Pode configurar quando apagar/compactar os dados.

Ao compactar ganha espaço mas perde precisão.

Devido a isso métricas de negocio é recomendado armazenar em outro lugar e não no prometheus, que pode ficar so com as métricas de sistema.

Adapter: Permite armazenar os dados em outros lugares, como o Elasticsearch, OpenTSDB. Ele pode ser somente leitura, somente escrita ou escrita e leitura.

Retrieval

Parte de coleta das métricas.

A aplicação não envia as métricas, o Prometheus que coleta ativamente, a app só abre um endpoint pro Prometheus coletar.

PromQL

Linguagem para executar queries.

Componentes do Ecossistema
Bibliotecas: São para facilitar a exposição e coleta de métricas como OpenTelemetry, AppMetrics, Micrometer.

Exporter: Serve como intermediário para coletar métrica de ferramentas que não têm suporte nativo ao Prometheus, como Jenkins, MySQL.

Push Gateway: Para processos de curta duração, armazena as métricas em cache.

Service Discovery: São para quando há elasticidade.

Alertas: Alertmanager checa se a regra é cumprida e manda pro Slack/Email/Telegram, etc.

3. Instalação do Prometheus via Docker
Comandos iniciais:

Bash

docker-compose up -d
docker container ls
Teste da API:

Browser teste: localhost:8080/swagger

Clica em get produto execute

post produto try it out, tira linha execute

No get produto execute

Teste: localhost:8080/metrics

Adicionando Prometheus no Docker Compose
(linhas 26 a 33)

Pra saber o nome da imagem certa: hub.docker.com.

Pesquisa prometheus, é o prom/prometheus by prom.

Pega a tag com a última versão sem ser a latest.

Executa:

Bash

docker-compose up -d
docker container ls
(pra ver se subiu)

Endpoints de verificação: Teste localhost:9090

/graph: consulta promql

/alerts

/status: runtime, build infos

/tsbd_status: infos do tsdb, métricas armazenadas

/flags: configuração de linha de comando

/config: estrutura de config do prom atual

/rules

/targets: endpoints que estão sendo coletados métricas

4. Configurando Scrape (Coleta)
Scrape da API
No momento só tá scrapando o Prometheus, mas pra scrapar minha api:

Crio prometheus.yaml (até linha 17).

Mapeio volume no docker-compose.yaml (linha 21).

Executa:

Bash

docker compose up -d
docker container ls
Dando um F5 em /config e /targets poderá ver as atualizações.

Coletando do MongoDB (Exporter)
Pra coletar do MongoDB também, vamos usar um exporter (linhas 28 a 37 compose.yaml).

Adc tb no prom.yaml (linhas 19 a 24).

Executa:

Bash

docker-compose up -d
docker container ls
Testa localhost:9216/metrics.

Pega uma das métricas tipo http_request_duration_seconds_sum e joga no /graph.

5. Instalação via Kubernetes (Helm)
Será com Helm.

Instalar metric server, kubectl top pods.

Teremos deployment.yaml e service.yaml da API e deployment.yaml e service.yaml pro MongoDB.

Comandos:

Bash

kubectl apply -f .\ -R
kubectl get all
kubectl top pods --all-namespaces
Pega o external ip/swagger do api-service e testa browser.

Clica get produto try it out execute.

Testa /metrics.

Instalação do Prometheus (ArtifactHUB)
artifacthub.io pesquisa prometheus e instala seguindo o manual "get helm info".

helm repo list prometheus-community deve aparecer.

helm search repo prometheus.

Configuração do Values:

helm inspect values prometheus-community/prometheus > values.yaml.

Edições no arquivo:

alertmanager: coloca false

persistentVolume: false

service/type: bota loadbalancer

pushgatway: false

Salva.

Instalação:

Bash

kubectl create ns prometheus
helm upgrade --install prometheus prometheus-community/prometheus --values ./values.yaml --namespace prometheus

kubectl get pods -n prometheus
kubectl get svc -n prometheus
Pega o ip e joga no browser.

Vai no /config só pra ver.

/targets vai ver que não ta coletando do pod.

Configurando Coleta (Annotations): Pra passar a coletar, precisa de annotations (k8s/api/deploy.yaml linhas 12 a 15).

Bash

kubect apply -f ./api/deployment.yaml
/targets pra ver se o pod tá sendo scrapado.

Muda qtd de réplicas aplica e vê /targets.

Coleta do MongoDB em K8s (Sidecar)
Para coleta do MongoDB em k8s vamos usar um sidecar, que é um container auxiliar usado para requisitos não funcionais (linhas 26 a 33).

Declara que deve ser scrapado com annotation (linhas 11 a 14).

Executa:

Bash

kubectl apply -f ./mongodb/deployment.yaml
kubectl get pods
/targets precisa ter a qtd de replica + 1 que é o sidecar.

/graph: mongodb_up execute.

6. PromQL (Querying)
Primeiro passo é ver qual métrica que eu quero lá pelo /metrics.

Exemplo 1: HTTP Requests Vamos testar http_request_received_total execute. Mostra qtd agrupado por code (200, 404 etc) e controller.

Pra simular requisições, abre terminal:

Bash

while true; do curl http://localhost:8080/produto; sleep 1; done;
Em Table dá pra colocar espaço de tempo.

Em Graph aparece um gráfico.

Filtros:

Ele tá me retornando vários valores, dá pra filtrar pelo code 200: http_requests_received_total(code="200")

Pelo method: http_requests_received_total(method="GET")

Exemplo 2: MongoDB Vamos ver outra métrica, agora do mongodb: mongodb_op_counters_total (número de comandos de consulta que fiz no mongodb) agrupado por type.

Tb posso filtrar, p ex. pelo type: mongodb_op_counters_total(type="query") (mostra só as consultas).

Operadores:

Negação: PromQL aceita negação. mongodb_op_counters_total(type!="query") (mostra todos diferentes de query: delete, insert etc).

Expressões Regulares: mongodb_op_counters_total(type=~"query|command") (mostra todos com type query e command).

Vetores e Tempo: Trabalhamos com instant vector, agora vamos range vector pra pegar em certo tempo.

mongodb_op_counters_total[1m]: pega só do último minuto.

Se aparecer várias amostras é devido ao scrape_interval. Se aparecer 12 amostras no ultimo 1minuto é pq o scrape interval tá 5s.

Adicionando [1m:5s]: na parte do 5s é recomendado colocar o mesmo valor do scrape interval para não dar valor quebrado.

Funções: Pra subir o nível do estudo, podemos usar funções (prometheus.io/docs/prometheus/latest/querying/functions). As mais usadas são rate() (calcula média de chamadas/s) e sum() (soma os valores).

Exemplos:

rate(http_requests_received_total[1m]): vai mostrar agrupado.

Mas queremos soma de tudo mesmo, então: sum(rate(http_requests_received_total[1m]))

Agregação (Group By): Se eu quiser fazer tipo um group by do SQL eu posso colocar by (job) no final da última query acima. Aí vai mostrar a soma de cada job, cada linha será a soma de um job.

Mais um exemplo: sum(rate(mongodb_op_counters_total[1m])) by (type) Vai mostrar a soma de cada tipo (update, delete etc).

7. Alertmanager
Setup do Prometheus no K8s com Alertas
Usaremos Helm. Vamos alterar os values de configuração do helm e vou aplicar configurando os alert groups.

Preparação:

Bash

kubectl apply -f ./k8s -R
kubectl get all
kubectl port-forward svc/api-service 8080:80
localhost:8080/swagger try it out execute

/metrics

Configuração do Helm:

artifacthub.io pesquisa prometheus pega o prometheus-community.

Comandos:

Bash

helm repo list
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add kube-state-metrics https://kubernetes.github.io/kube-state-metrics
helm repo update
helm repo list
helm show values prometheus-community/prometheus > values.yaml
Na linha 1267 alerting_rules.yml: pega o conteúdo do alert.rules.yaml e cola.

Na linha 1244 alertmanagerFiles: pega o conteúdo dos routes de alertmanager.yml e cola no lugar certo, a mesma coisa com os receivers.

Instalação e Testes:

Bash

kubectl create ns monitoramento
helm install prometheus prometheus-community/prometheus --namespace=monitoramento --values ./values.yaml
kubectl get all -n monitoramento
Port-Forwarding:

Bash

kubectl port-forward svc/prometheus-server 8181:80 -n monitoramento
kubectl port-forward svc/prometheus-alertmanager 8282:80 -n monitoramento
kubectl port-forward svc/api-service 8080:80
Gerar Alertas: Aumentar requisições:

Bash

while true; do curl http://localhost:8080/produto; sleep 0.5; done
Em localhost:8181/alerts vai mostrar os alertas em pending depois firing.

Em localhost:8282/alerts vai mostrar o alerta ativo.

Posso ir em /config pra ver a notificação ativa.

8. Conceitos e Regras do Alertmanager
O Alertmanager que tem as regras de manipulação de alertas que o Prometheus manda pra ele. As configurações de alerta vão no alert.rules.yaml.

Estágios do alerta:

Inactive: Quando a regra ainda não foi atingida.

Pending: Regra foi atingida mas o tempo do for não foi atingido.

Firing: Regra e tempo foram atingidos.

No firing o Prometheus envia o alerta pro Alertmanager. Posso silenciar, inibir ou agrupar alertas.

9. Alertmanager no Docker
Vamos criar as regras -> alert.rules.yaml.

Em prometheus.yaml coloca rule_files (linha 6) e no compose linha 43 mapeio como volume.

Executa:

Bash

docker-compose up -d
docker containenr ls
Check: localhost:9090/alerts.

Adicionando Alertmanager ao Compose
Coloco como serviço no compose linha 51.

No prometheus.yaml adiciono alerting linha 29.

Executa:

Bash

docker-compose down
docker-compose up -d
docker container ls
localhost:9090/config: vai ver o campo alerting.

Check: localhost:9093.

Configuração Final e Teste
Agora é configurar o Alertmanager (alertmanager.yaml) e mapear no service do alertmanager no compose linhas 55 a 58.

Executa:

Bash

docker-compose up -d
Checa 9093/status.

Mandar requisições:

Bash

while true; do curl http://localhost:8080/produto; sleep 0.5; done
9090/alerts vai entrar em pending e firing.

No alertmanager 9093/alerts os alertas vão aparecer.

No heroku vai aparecer o alerta.