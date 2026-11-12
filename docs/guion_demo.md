# Guion de la demo (15 a 20 minutos)

Ensayarlo completo antes de la defensa. Antes de empezar: Docker Desktop abierto, Minikube corriendo, todo desplegado, una ventana de PowerShell por persona y las evidencias de respaldo a la mano.

| Min | Quien | Que muestra | Criterio |
|---|---|---|---|
| 0-3 | Francisco | Pitch y diagrama de arquitectura (`docs/arquitectura.md`); repos, ramas, commits y README | P1-P4, D1 |
| 3-8 | Valentina | CI en GitHub Actions: ejecucion de un commit con pruebas y build; un cambio que falla y se bloquea; imagenes con etiqueta en DockerHub | D2, D3 |
| 8-10 | Valentina | Trazabilidad: del commit a la etiqueta de la imagen y al pod (`kubectl get pods -o custom-columns=...`) | D6 |
| 10-14 | Jose | Minikube: `kubectl get pods,svc,pvc -n ahorro`, ConfigMap y Secret (sin mostrar claves), probes y recursos | D4, D7 |
| 14-17 | Francisco | Flujo E2E en vivo: elegir usuario, guardar meta, buscarla, caso de error, borrar `db-0` y comprobar que los datos siguen | D5 |
| 17-20 | Jose | Diagnostico: logs, describe, falla provocada (`ImagePullBackOff`) y recuperacion con `rollout undo`; escalar a 2 replicas | D8 |
| Final | Los tres | Preguntas | D9 |

## Comandos en orden (copiar de `k8s/README.md`)
1. `kubectl get pods,svc,pvc -n ahorro`
2. `kubectl get configmap app-config -n ahorro -o yaml` (el Secret no se imprime)
3. `kubectl get pods -n ahorro -o custom-columns=POD:.metadata.name,IMAGEN:.spec.containers[*].image`
4. Pagina: guardar y buscar meta; caso de error
5. `kubectl delete pod db-0 -n ahorro` y buscar la meta otra vez
6. `kubectl logs deploy/backend -n ahorro`
7. `kubectl set image deployment/backend backend=josem1715/entrega2-backend:no-existe -n ahorro` y `kubectl get pods -n ahorro`
8. `kubectl describe pod -l app=backend -n ahorro` y explicar el `ImagePullBackOff`
9. `kubectl rollout undo deployment/backend -n ahorro`
10. `kubectl scale deployment/backend --replicas=2 -n ahorro`

## Reglas de la rubrica
- No mostrar contrasenas ni tokens.
- No acreditar flujos simulados como si fueran reales: todo en vivo.
- Si algo falla, explicar que paso y usar la evidencia de respaldo.
- Los tres deben saber explicar cualquier parte del sistema.
