[english below]

### Deployments

## Deployment vs. replicaset

* Ao contrário do `replicaset`, o `deployment` garante atualização dos pods automaticamente e sem downtime, utilizando a estratégia `rolling update`.
* O `deployment` atua acima do `replicaset`, gerenciando-os. A cada atualização, um novo `replicaset` é criado.
* O `replicaset` da versão antiga não é excluído, apenas desativado, pra permitir um rollback rápido pra versão anterior, caso precise.

---

## Comandos

Criar ou atualizar deploy

`kubectl apply -f deployment.yaml`

Detalhar deploy

`kubectl describe deploy mydeployment`

Observar atualização dos pods

`kubectl apply -f deployment.yaml && watch 'kubectl get po'`

Acessar

`kubectl port-forward pod/mydeployment-64f86fc94c-rfnc5 8080:80`

Verificar `replicaset` anterior > Útil pra verificar que a imagem do `rs` antigo é diferente e que o `rs` já não tem mais pods, pois a imagem foi alterada.

`kubectl describe replicaset mydeployment-64f86fc94c`

Ver histórico de atualizações

`kubectl rollout history deployment mydeployment`

Aplicar e ver atualizações

`kubectl apply -f deployment.yaml && watch 'kubectl get deploy,rs,pod'`

Rollback

`kubectl rollout undo deploy mydeployment && watch 'kubectl get deploy,rs,pod'`

Escalar

`kubectl scale deploy meudeployment --replicas=5`

---

[english]

### Deployments

## Deployment vs. replicaset

* Unlike `replicaset`, the `deployment` guarantees pod update automatically with no downtime, using `rolling update` strategy.
* The `deployment` remains above `replicaset`, managing them. Each update generates a new `replicaset`.
* The old version `replicaset` is not deleted, just deactivated, allowing a quick rollback to an older version, if needed.

---

## Commands

Create or update deploy

`kubectl apply -f deployment.yaml`

Detail deploy

`kubectl describe deploy mydeployment`

Observe pods update

`kubectl apply -f deployment.yaml && watch 'kubectl get po'`

Access

`kubectl port-forward pod/mydeployment-64f86fc94c-rfnc5 8080:80`

Check previous `replicaset` --> Useful to see that the previous `rs` image is different and that this `rs` has no longer pods, because the image was changed.

`kubectl describe replicaset mydeployment-64f86fc94c`

See update history

`kubectl rollout history deployment mydeployment`

Apply e check updates

`kubectl apply -f deployment.yaml && watch 'kubectl get deploy,rs,pod'`

Rollback

`kubectl rollout undo deploy mydeployment && watch 'kubectl get deploy,rs,pod'`

Scale

`kubectl scale deploy meudeployment --replicas=5`