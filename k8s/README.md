# Despliegue en Minikube (Kubernetes)

Todo el sistema (base de datos, seeding, backend y frontend) se despliega en el namespace `ahorro`.

| Archivo | Que crea |
|---|---|
| `00-namespace.yaml` | Namespace `ahorro` |
| `01-configmap.yaml` | Configuracion no secreta (host, puerto, nombre de la BD y usuario) |
| `secrets.example.yaml` | Solo la **forma** del Secret. El Secret real se crea con `kubectl create secret` y **no se guarda en git** |
| `10-db.yaml` | PostgreSQL como StatefulSet con volumen persistente (1 Gi), probes y recursos |
| `20-seed-job.yaml` | Job que crea las tablas y carga los datos iniciales; espera a que la BD este lista |
| `30-backend.yaml` | Deployment del backend (probes en `/health`) y Service `backend` (5000) |
| `40-frontend.yaml` | Deployment del frontend y Service `frontend` (NodePort 30080) |
| `kustomization.yaml` | Junta todo y fija la **etiqueta de cada imagen** (`images:`) |

## 1. Desplegar
Requisitos: Docker Desktop abierto, `minikube` y `kubectl`. Desde la carpeta del monorepo (PowerShell):

```
minikube start
kubectl apply -f k8s/00-namespace.yaml
kubectl create secret generic app-secrets -n ahorro --from-literal=PG_PASSWORD=ELIJA_UNA_CLAVE --from-literal=ADMIN_PASSWORD=ELIJA_OTRA_CLAVE
kubectl apply -k k8s/
kubectl get pods -n ahorro -w
```

Espere a ver `db-0`, `backend` y `frontend` en `Running` y `1/1`, y el pod `seed` en `Completed` (Ctrl+C para salir del `-w`).

Para abrir la pagina (deje esa ventana abierta, imprime la direccion):
```
minikube service frontend -n ahorro --url
```

## 2. Flujo E2E y pruebas Playwright en Minikube
Apague antes el Docker Compose (`docker compose down`) para liberar el puerto 5000. En una ventana:
```
kubectl port-forward svc/backend 5000:5000 -n ahorro
```
En otra, con la direccion que imprimio `minikube service` (ejemplo `http://127.0.0.1:54321`):
```
$env:FRONTEND_URL="http://127.0.0.1:54321"
python -m pytest e2e
```
Debe dar `5 passed`.

## 3. Persistencia (los datos sobreviven al reinicio de la BD)
1. En la pagina, guarde una meta y anote su ID.
2. `kubectl delete pod db-0 -n ahorro` (Kubernetes lo recrea solo).
3. Cuando `db-0` vuelva a `1/1`, busque la meta por su ID: sigue ahi.

## 4. Observabilidad y diagnostico
```
kubectl get pods,svc,pvc -n ahorro
kubectl describe pod -l app=backend -n ahorro
kubectl logs deploy/backend -n ahorro
kubectl logs job/seed -n ahorro
kubectl get events -n ahorro --sort-by=.lastTimestamp
```

### Falla provocada y recuperacion
```
kubectl set image deployment/backend backend=josem1715/entrega2-backend:no-existe -n ahorro
kubectl get pods -n ahorro
kubectl describe pod -l app=backend -n ahorro
kubectl rollout undo deployment/backend -n ahorro
kubectl rollout status deployment/backend -n ahorro
```
Se ve `ImagePullBackOff` (la etiqueta no existe), la pagina sigue funcionando porque el pod anterior no se apaga hasta que el nuevo este listo, y `rollout undo` vuelve a la version buena.

### Escalar
```
kubectl scale deployment/backend --replicas=2 -n ahorro
kubectl get pods -n ahorro
```

## 5. Trazabilidad
Que imagen exacta corre en cada pod:
```
kubectl get pods -n ahorro -o custom-columns=POD:.metadata.name,IMAGEN:.spec.containers[*].image
```
La etiqueta sale de `k8s/kustomization.yaml`, que la CI actualiza con el SHA del commit.

## 6. Secretos
- Las contrasenas viven solo en el Secret `app-secrets` (creado con `kubectl create secret`), nunca en git ni en las imagenes.
- En la demo no se imprimen: no use `kubectl get secret -o yaml`.

## 7. Reiniciar desde cero
```
kubectl delete namespace ahorro
```
Borra todo, incluida la base de datos. Luego repita el paso 1.
