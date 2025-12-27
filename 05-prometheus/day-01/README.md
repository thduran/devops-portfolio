pilares da observabilidade

métricas: valores umérico sobre software/infra.
Ex. cpu, n de requisições, de instancias

logs: info sobre eventos do app/infra

tracing: rastro do fluxo de eventos ao longo dos
microserviços

--

ferramentas: prometheus (métricas), loki e
fluentbit (log), Jaeger (tracing), grafana pro visual

--

métricas se divide em métricas de sistema e de negócio

sistema: APIs + acessadas, n de erros
negócio: n de usuários, de compras

tipos de métricas couter, gauge, histogram,summary

counter: só aumenta
gauge: aumenta e diminui
histogram: grafico - amostragem de valor, frequência
summary: gráfico - porcentage

---

arquitetura do prometheus

prommetheus server:
tem o storage do tsdb, retrieval e o promql

tsdb
armazena bloco de  dados armazenados de 2 em 2h
pode configurar quando apagar/compactar os dados
ao compactar ganha espaço mas perde precisao

devido a isso métricas de negocio é recomendado armazenar em outro lugar e não no prometheus, que pode ficar so com as métricas de sistema

adapter permite armazenar os dados em outros lugares, como o elasticsearch,opentsdb
ele ode ser somente leitura, somente escrita ou escrita e leitura

--

retrieval:parte de coleta das métricas 
a aplicação nao envia as métricas, o prometheus que coleta ativamente, a app so abre um endpoint pro prometheus coletar

--

promql: linguagem para execitar queries

--

bibliotecas são para facilitar a exposição e coleta de métricas como opentelemetry, appmettrics, micrometer

exporter serve como intermediario para coletar métrica de  ferramentas que não tem suporte nativo aoo prometheus, como Jenkins, mysql

para processos de curta duração há o push gateway que armazena as métricas em cache

servisse Discovery são para quando há elasticidade

alertas: alertmanager checa se a regra é cumprida e manda pro slack/email/telegrama etc

---

instalação prometheus via docker

docker-compose up -d
docker container ls 
browser teste localhost:8080/swagger

clica em get produto execute
post produto try it out, tira linha execute
no get produto execute

teste localhost:8080/metrics

--

adicionando prometheus no docker compose
(linhas 26 a 33 )
pra saber o nome da imagem certa hub.docker.com
pesquisa prometheus, é o prom/prmoetheus by prom
pega a tag com a ultima versao sem ser a latest

dá um docker-compose up -d, docker container ls
pra ver se subiu

teste localhost:9090

/graph consulta promql
/alerts
/status runtime,build infos
/tsbd_status infos do tsdb, metricas armazenadas
/flags configuracao de linha de comando
/config estrutura de config do prom atual
/rules
/targets endpoints que estao sendo coletados metricas

--

no momento so ta scrapando o prometheus, mas pra scrapar minha api, crio prometheus.yaml (ate linha 17) e mapeio volume no docker-compose.yaml (linha 21)

docker compose up -d, docker container ls

dando um f5 em /config e /targets podera ver as atualzicoes

--

pra coletar do mongodb tambem, vamos usar um exporter (linhas 28 a 37 compose.yaml)

adc tb no prom.yaml (linhas 19 a 24)

docker-compose up -d, docker container ls

testa localhost:9216/metrics
pega uma das metricas tipo http_request_duration_seconds_sum e joga no /graph

---

agora instalação via kubernetes
será com helm

instalar metric server, kubectl top pods

teremos deployment.yaml e service.yaml da api e deployment.yaml e service.yaml pro mongodb

kubectl apply -f .\ -R, kubectl get all, kubectl top pods --all-namespaces

pega o external ip/swagger do api-service e testa browser

clica get produto try it out execute

testa /metrics

---

actifacthub.io pesquisa prometheus
e instala seguindo o manual "get helm info"
helm repo list prometheus-community deve aparecer
helm search repo prometheus

helm inspect values prometheus-community/prometheus > values.yaml

alertmanager coloca false
persistentVolume false
em service/type bota loadbalancer
pushgatway false
salva

kubectl create ns prometheus
helm upgrade --install prometheus prometheus-community/prometheus --values ./values.yaml --namespace prometheus

kubectl get pods -n prometheus
kubectl get svc -n prometheus
pega o ip e joga no browser
vai no /config so pra ver
/targets vai ver que nao ta coletando do pod
pra passar a coletar, precisa de annotations (k8s/api/deploy.yaml linhas 12 a 15)

kubect apply -f ./api/deployment.yaml

/targets pra ver se o pod ta sendo scrapado
muda qtd de replicas aplica e ve /targets

--

para coleta do mongodb em k8s vamos usar um sidecar, que é um container auxiliar usado para requisitos nao funcionais (linhas 26 a 33)

declara que deve ser scrapado com annotation (linhas 11 a 14)

kubectl apply -f ./mongodb/deployment.yaml
kubectl get pods
/targets precisa ter a qtd de replica + 1 que é o sidecar

/graph mongodb_up execute

---

promql

primeiro passo é ver qual metrica que eu quero la pelo /metrics

vamos testar http_request_received_total execute
mostra qtd agrupado por code (200, 404 etc) e controller 

pra simular requisicoes, abre terminal while true; do curl http://localhost:8080/produto; sleep 1; done;

em table da pra colocar espaço de tempo
em graph aparece um grafico

ele ta me retornando varios valores, da pra filtrar pelo code 200
http_requests_received_total(code="200")
pelo method
http_requests_received_total(method="GET")

vamos ver outra metrica, agora do mongodb
mongodb_op_counters_total (numero de comandos de consulta que fiz no mongodb) agrupado por type 

tb posso filtrar, p ex. pelo type.
mongodb_op_counters_total(type="query")
mostra só as consultas

promql aceita negacao
mongodb_op_counters_total(type!="query")
mostra todos diferentes de query (delete, insert etc)

promql tb aceita expressoes regulares
mongodb_op_counters_total(type=~"query|command")
mostra todos com type query e command

trabalhamos com instanct vector, agora vamos range vector pra pegar em certo tempo
mongodb_op_counters_total[1m] pega só do ultimo minuto
> se aparecer varias amostras é devido ao scrape_interval. se aparecer 12 amostras no ultimo 1minuto é pq o scrape interval tá 5s 

adicionando [1m:5s] - na parte do 5s é recomendado colocar o mesmo valor do scrape interval para nao dar valor quebrado

pra subir o nivel do estudo, podemos usar funções
(prometheus.io/docs/prometheus/latest/querying/functions)
as mais usadas são rate() - calcula media de chamadas /s; sum() - soma os valores

exemplos:
rate(http_requests_received_total[1m])
vai mostrar agrupado, mas queremos soma de tudo mesmo, entao
sum(rate(http_requests_received_total[1m]))

se eu quiser fazer tipo um group by do sql eu posso colocar by (job) no final da ultima query acima
aí vai mostrar a soma de cada job, cada linha sera a soma de um job, mais um exemplo:

sum(rate(mongodb_op_counters_total[1m])) by (type)
vai mostrar a soma de cada tipo (update, delete etc)

--

alertmanageer

pra fazer o setup do prometheus no k8s usaremos helm. vamos alterar os values de configuração do helm e vou aplicar configurando os alert groups

kubectl apply -f ./k8s -R
kubectl get all
kubectl port-forward svc/api-service 8080:80
localhost:8080/swagger try it out execute
/metrics

artifacthub.io pesquisa prometheus pega o prometheus-community
helm repo list
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add kube-state-metrics https://kubernetes.github.io/kube-state-metrics
helm repo update
helm repo list
helm show values prometheus-community/prometheus > values.yaml

na linha 1267 alerting_rules.yml, pega o conteudo do alert.rules.yaml e cola
na linha 1244 alertmanagerFiles, pega o conteudo dos routes de alertmanager.yml e cola no lugar certo, a mesma coisa com os receivers

kubectl create ns monitoramento

helm install prometheus prometheus-community/prometheus --namespace=monitoramento --values ./values.yaml

kubectl get all -n monitoramento

kubectl port-forward svc/prometheus-server 8181:80 -n monitoramento

kubectl port-forward svc/prometheus-alertmanager 8282:80 -n monitoramento

kubectl port-forward svc/api-service 8080:80

aumentar requisicoes:
while true; do curl http://localhost:8080/produto; sleep 0.5; done

em localhost:8181/alerts vai mostrar os alertas em pending depois fiiring

em localhost:8282/alerts vai mostrar o alerta ativo

posso ir em /config pra ver a notificacao ativa

---

o alertmanager que tem as regras de manipulação de alertas que o prometheus manda pra ele

as configurações de alerta vao no alert.rules.yaml

estagios do alerta:
inactive: quando a regra ainda nao foi atingida
pending: regra foi atingida mas o tempo do for não foi atingido
firing: regra e tempo foram atingidos

no firing o prometheus envia o alerta pro alertmanager

posso silenciar, inibir ou agrupar alertas

---

alertmanager no docker

vamos criar as regras -> alert.rules.yaml
em prometheus.yaml coloca rule_files (linha 6) e no compose linha 43 mapeio como volume

docker-compose up -d, docker containenr ls

localhost:9090/alerts

---

adicionando alertmanager, coloco como serviço no compose linha 51
e no prometheus.yaml adiciono alerting linha 29

docker-compose down
docker-compose up -d
docker container ls

localhost:9090/config
> vai ver o campo alerting

localhost:9093

---

agora é configurar o alertmanager (alertmanager.yaml) e mapear no service do alertmanager no compose linhas 55 a 58

docker-compose up -d
checa 9093/status

mandar requisicoes
while true; do curl http://localhost:8080/produto; sleep 0.5; done

9090/alerts vai entrar em pending e firing
no alertmanager 9093/alerts os alertas vao aparecer

no heroku vai aparecer o alerta