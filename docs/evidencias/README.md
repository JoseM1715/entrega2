# Evidencias de respaldo

Capturas de la entrega, por si algo falla en vivo durante la demo. Las del 01 al 08 son de la ejecucion de Francisco en su Minikube (17/11/2026) y la 09 es de Valentina.

| Archivo | Que muestra | Criterio |
|---|---|---|
| `01-flujo-guardar-meta.png` | Pagina: meta de 2.500.000 en 12 meses con abono de 100.000 en el mes 6; responde "Meta #3 guardada. Cuota mensual: $ 191.516,95" | D5 |
| `02-flujo-buscar-meta.png` | Busqueda de la meta #3 por su ID; devuelve la misma cuota | D5 |
| `03-flujo-error-abono-sin-mes.png` | Caso de error: abono sin mes valido; el backend explica el problema y no guarda nada | D5 |
| `04-k8s-pods-servicios-volumen.png` | `kubectl get pods,svc,pvc -n ahorro`: `db-0`, `backend` y `frontend` en `1/1`, `seed` en `Completed`, servicios y volumen `datos-db-0` en `Bound` | D4 |
| `05-k8s-borrar-pod-db0.png` | Se borra `db-0` y Kubernetes lo recrea (`kubectl get pods -w`) | D5, D8 |
| `06-persistencia-meta-tras-borrar-db0.png` | Con `db-0` ya recreado, la meta #3 sigue existiendo: los datos persisten en el volumen | D5 |
| `07-e2e-playwright-5-passed.png` | Pruebas E2E con Playwright: `5 passed` | D5, D9 |
| `08-k8s-pods-finales.png` | Estado final de los pods, todos sanos | D4 |
| `09-ci-pr-fallo-controlado.png` | Pull Request #1 con fallo controlado (`replicas: uno`): la validacion de manifiestos falla con `'uno' is not of type 'integer'` y los jobs de imagenes y manifiesto no corren | D2 |

Enlaces en vivo (CI, Pull Request, Docker Hub y trazabilidad): [ci-enlaces.md](ci-enlaces.md).

## Logs de terminal (Jose, Minikube)
Salida completa de la terminal, en texto. No contienen contrasenas: el Secret solo aparece como referencia (`<set to the key 'PG_PASSWORD' in secret 'app-secrets'>`).

| Archivo | Que muestra | Criterio |
|---|---|---|
| `logs/10-diagnostico-falla-y-rollback.txt` | Borrar `db-0` y recuperacion, `get pvc`, logs del backend y del seed, `describe` (probes, limites, Secret por referencia), eventos, falla provocada con una imagen que no existe (`ImagePullBackOff`) y `rollout undo` | D4, D5, D7, D8 |
| `logs/11-escalado-y-trazabilidad-de-imagenes.txt` | `rollout undo`, escalar el backend a 2 replicas y volver a 1, y `custom-columns` con la imagen de cada pod (etiqueta del commit) | D6, D8 |
| `logs/12-e2e-playwright-jose.txt` | Pruebas E2E con Playwright contra el frontend en Minikube | D5, D9 |
