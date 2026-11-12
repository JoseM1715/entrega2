# Guia para Francisco

Tu parte no depende de nadie: todo lo que necesitas esta en este repo. Haz `git pull` y sigue los pasos en orden.

**Tu parte vale 40 puntos de la nota:** el pitch (20), el diagrama de arquitectura (parte de D1, 8), el flujo E2E (14) y la organizacion de la demo (D9, 4).

## Que tienes que entregar
1. **Pitch** de 4 a 5 minutos (texto base en `docs/pitch.md`).
2. **Diagrama de arquitectura** (ya esta en `docs/arquitectura.md`; tienes que entenderlo y poder explicarlo).
3. **Flujo E2E funcionando en Minikube**: elegir usuario, guardar una meta, buscarla, ver un error y comprobar que los datos persisten.
4. **Carpeta de evidencias de respaldo** (capturas y logs) por si algo falla en la defensa.
5. **Guion de la demo** (`docs/guion_demo.md`): ensayarlo con los otros dos.

## Paso 1: instalar lo necesario (una sola vez)
Necesitas Docker Desktop abierto. En PowerShell:
```
winget install Kubernetes.minikube
winget install Kubernetes.kubectl
```
Cierra y abre PowerShell, y comprueba:
```
minikube version
kubectl version --client
```

## Paso 2: descargar el proyecto
```
git clone --recurse-submodules https://github.com/JoseM1715/entrega2.git
cd entrega2
```

## Paso 3: desplegar en tu Minikube
Sigue la seccion **1. Desplegar** de `k8s/README.md`. Resumen:
```
minikube start
kubectl apply -f k8s/00-namespace.yaml
kubectl create secret generic app-secrets -n ahorro --from-literal=PG_PASSWORD=ELIJA_UNA_CLAVE --from-literal=ADMIN_PASSWORD=ELIJA_OTRA_CLAVE
kubectl apply -k k8s/
kubectl get pods -n ahorro -w
```
Cuando `db-0`, `backend` y `frontend` esten en `1/1 Running` y `seed` en `Completed`, abre la pagina:
```
minikube service frontend -n ahorro --url
```
(deja esa ventana abierta y entra a la direccion que imprime).

## Paso 4: probar el flujo E2E a mano
1. En la pagina elige "Miguel Angel", pon meta `2500000`, plazo `12`, abono extra `100000`, mes del abono `6` y pulsa **Calcular y guardar**. Debe salir la cuota `191.516,95`.
2. Copia el numero de la meta, escribelo en **Buscar una meta** y pulsa **Buscar**.
3. **Caso de error:** pon abono extra `50000` y mes del abono `0`. Debe salir un mensaje de error y no guarda nada.
4. **Persistencia:** `kubectl delete pod db-0 -n ahorro`. Espera a que vuelva a `1/1` y busca la meta otra vez: sigue ahi.

## Paso 5: correr las pruebas automaticas (Playwright)
Ver la seccion **2** de `k8s/README.md`. Resumen: apaga Docker Compose (`docker compose down`), en una ventana `kubectl port-forward svc/backend 5000:5000 -n ahorro`, y en otra:
```
pip install -r e2e/requirements.txt
python -m playwright install chromium
$env:FRONTEND_URL="http://127.0.0.1:PUERTO"
python -m pytest e2e
```
Debe dar `5 passed`.

## Paso 6: evidencias de respaldo
Crea la carpeta `docs/evidencias/` y guarda capturas de:
- `kubectl get pods,svc,pvc -n ahorro` con todo en Running.
- La pagina con una meta guardada y la cuota.
- La busqueda de esa meta despues de borrar `db-0` (persistencia).
- El resultado `5 passed` de Playwright.
- El mensaje de error del caso inválido.

**No incluyas contraseñas ni tokens** en ninguna captura.

## Paso 7: ensayar
- Lee `docs/pitch.md` en voz alta con un cronometro: debe durar entre 4 y 5 minutos. Ajusta las frases para que suenen tuyas.
- Ensaya `docs/guion_demo.md` completo con Jose y Valentina.

## Si algo falla
Mira la tabla de problemas de `README.md` y la seccion de diagnostico de `k8s/README.md`. Si no se resuelve, copia el mensaje de error completo y pideselo a quien te este ayudando.
