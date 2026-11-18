# Guion de la demo (15 a 20 minutos)

## Reparto
- **Francisco** es quien mas explica: ejecuta toda la parte practica en vivo (teclado y pantalla) y explica lo tecnico (arquitectura, CI y trazabilidad, Kubernetes, flujo y diagnostico).
- **Valentina** complementa la parte conceptual de CI, imagenes y trazabilidad y habla en el pitch (solucion y alcance).
- **Jose** habla en el pitch (portada, problema y cierre), complementa lo conceptual y responde preguntas.
- En el **pitch**: Jose (portada, problema y cierre), Valentina (solucion y alcance) y Francisco (arquitectura, cadena de entrega, practicas, parte practica y decisiones). Las notas de cada diapositiva dicen quien habla.
- La demo corre en **un solo computador** (el de Francisco, con su Minikube ya desplegado).
- Los tres deben saber explicar cualquier parte del sistema y responder cualquier pregunta.

## Antes de empezar (checklist)
- [ ] Docker Desktop abierto, Minikube corriendo y todo desplegado (`kubectl get pods -n ahorro`: `db-0`, `backend`, `frontend` en `1/1`, `seed` en `Completed`).
- [ ] Ventana 1 de PowerShell: `minikube service frontend -n ahorro --url` abierta (no cerrar) y la direccion abierta en el navegador.
- [ ] Ventana 2 de PowerShell: lista para los comandos, dentro de la carpeta del repo.
- [ ] Pestanas del navegador listas: repo en GitHub, pestana **Actions**, el Pull Request del fallo controlado, Docker Hub (etiquetas) y la presentacion.
- [ ] Carpeta de evidencias de respaldo abierta.
- [ ] Nada de contrasenas ni tokens a la vista.

## Linea de tiempo
| Min | Ejecuta | Explica | Que se muestra | Criterio |
|---|---|---|---|---|
| 0-4 | Francisco pasa las diapositivas | Los tres (cada uno sus diapositivas) | Pitch | P1-P4 |
| 4-6 | Francisco | Francisco (Jose complementa) | Repos, ramas, commits, README y diagrama (`docs/arquitectura.md`) | D1 |
| 6-11 | Francisco | Francisco (Valentina complementa) | CI en GitHub Actions: ejecucion con pruebas y build; Pull Request con fallo controlado (rojo, no publica); imagenes con etiqueta en Docker Hub | D2, D3 |
| 11-13 | Francisco | Francisco (Valentina complementa) | Trazabilidad: commit, etiqueta de la imagen, manifiesto y pod | D6 |
| 13-16 | Francisco | Francisco (Jose complementa) | Minikube: pods, servicios, volumen, ConfigMap y Secret (sin mostrar claves), probes y recursos | D4, D7 |
| 16-18 | Francisco | Francisco (Jose complementa) | Flujo en la pagina: guardar meta, buscarla, caso de error; borrar `db-0` y comprobar que los datos siguen | D5 |
| 18-21 | Francisco | Francisco (Jose complementa) | Diagnostico: logs, `describe`, falla provocada (`ImagePullBackOff`) y `rollout undo`; escalar a 2 replicas | D8 |
| Final | Los tres | Los tres | Preguntas | D9 |

## Comandos en orden (los ejecuta Francisco)
1. `kubectl get pods,svc,pvc -n ahorro`
2. `kubectl get configmap app-config -n ahorro -o yaml` (el Secret **no** se imprime)
3. `kubectl get pods -n ahorro -o custom-columns=POD:.metadata.name,IMAGEN:.spec.containers[*].image`
4. `kubectl describe pod -l app=backend -n ahorro` (mostrar probes, limites y `PG_PASSWORD` como referencia al Secret)
5. Pagina: guardar una meta (por ejemplo usuario Jose Angel, 2500000, 12 meses, extra 100000, mes 6; debe dar 191.516,95), anotar el ID y buscarla; luego un caso de error (un abono sin mes)
6. `kubectl delete pod db-0 -n ahorro`, `kubectl get pods -n ahorro -w` (Ctrl+C cuando `db-0` vuelva a `1/1`) y buscar la meta otra vez
7. `kubectl logs deploy/backend -n ahorro --tail=20`
8. `kubectl set image deployment/backend backend=josem1715/entrega2-backend:no-existe -n ahorro`
9. Esperar unos 30 segundos y `kubectl get pods -n ahorro` (aparece `ImagePullBackOff`; el backend anterior sigue `1/1`)
10. `kubectl describe pod NOMBRE_DEL_POD_MALO -n ahorro` y senalar en `Events` el `Failed to pull image ... not found`
11. `kubectl rollout undo deployment/backend -n ahorro` y `kubectl rollout status deployment/backend -n ahorro`
12. `kubectl scale deployment/backend --replicas=2 -n ahorro`, esperar y `kubectl get pods -n ahorro`; luego volver a `--replicas=1`

## Si algo falla en vivo
- Explicar con calma que paso y mostrar la captura de respaldo de ese paso.
- Si la pagina no abre, revisar que la ventana de `minikube service` siga abierta (el puerto cambia si se reinicia).
- Para empezar de cero: `powershell -ExecutionPolicy Bypass -File .\scripts\desplegar.ps1`.

## Reglas de la rubrica
- No mostrar contrasenas ni tokens.
- No acreditar flujos simulados como si fueran reales: todo en vivo.
- Si algo falla, explicar que paso y usar la evidencia de respaldo.
- Los tres deben saber explicar cualquier parte del sistema.
