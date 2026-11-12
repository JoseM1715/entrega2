# Guia para Valentina

Tu parte son la **CI con GitHub Actions** y la **trazabilidad** (del commit a la imagen y al pod). Valen 30 puntos: D2 (12), D3 (8) y D6 (10).
El workflow ya esta escrito en `.github/workflows/ci.yml`. Tu trabajo es dejarlo funcionando, entender cada paso y poder demostrarlo en vivo.

## Que hace el workflow
```
commit -> [Pruebas del backend] + [Validar Kubernetes] -> [Construir y publicar imagenes] -> [Actualizar etiquetas en el manifiesto]
```
| Job | Que hace |
|---|---|
| `pruebas-backend` | Levanta PostgreSQL y corre las 41 pruebas del backend |
| `validar-kubernetes` | Valida los manifiestos de `k8s/` contra el esquema de Kubernetes 1.31 |
| `imagenes` | Construye backend y frontend y los sube a DockerHub con la etiqueta = **SHA corto del commit** |
| `actualizar-manifiesto` | Escribe esa etiqueta en `k8s/kustomization.yaml` y la guarda en git |

Si un job falla, los siguientes **no corren**: nada se publica con pruebas rotas.
Los disparadores son: `push` a `main`, `pull_request` y el boton **Run workflow** (`workflow_dispatch`).

## Paso 1: acceso al repo
Jose te agrega como colaboradora del repo `entrega2` (**Settings > Collaborators**). Aceptas la invitacion en https://github.com/notifications.

## Paso 2: crear un token de DockerHub
1. Entra a hub.docker.com con la cuenta `josem1715` (Jose te lo hace o te presta la sesion; **no se comparte la contraseña**).
2. Foto de perfil > **Account settings** > **Personal access tokens** > **Generate new token**.
3. Nombre `github-actions`, permisos **Read & Write**. Copia el token (solo se ve una vez).

## Paso 3: guardar los secretos en GitHub
En el repo `entrega2`: **Settings > Secrets and variables > Actions > New repository secret**. Crea dos:
| Nombre | Valor |
|---|---|
| `DOCKERHUB_USERNAME` | `josem1715` |
| `DOCKERHUB_TOKEN` | el token del paso 2 |

**El token nunca se pega en el chat, en el codigo ni en capturas.**

## Paso 4: permitir que la CI guarde el manifiesto
**Settings > Actions > General > Workflow permissions > Read and write permissions > Save.**

## Paso 5: ejecutar la CI
1. Entra a la pestaña **Actions** del repo.
2. Elige el workflow **CI** y pulsa **Run workflow** (rama `main`).
3. Espera a que los 4 jobs salgan en verde. Abre cada uno y mira los logs.

## Paso 6: comprobar la trazabilidad
1. En DockerHub, `entrega2-backend` y `entrega2-frontend` tienen una etiqueta nueva igual al SHA corto del commit (mismo valor que ves en la ejecucion).
2. En el repo hay un commit nuevo `ci: imagenes con etiqueta ... [skip ci]` que cambia `k8s/kustomization.yaml`.
3. Haz `git pull` y despliega: `kubectl apply -k k8s/`
4. Muestra que el pod usa esa imagen:
```
kubectl get pods -n ahorro -o custom-columns=POD:.metadata.name,IMAGEN:.spec.containers[*].image
```
La cadena que debes poder explicar: **commit -> CI -> imagen con etiqueta -> manifiesto -> pod**.

## Paso 7: fallo controlado (para la demo)
Muestra que un error **impide avanzar**:
1. Crea una rama: `git checkout -b demo-fallo`
2. En `k8s/30-backend.yaml` cambia `replicas: 1` por `replicas: uno`.
3. `git commit -am "demo: manifiesto roto"` y `git push -u origin demo-fallo`.
4. En GitHub abre un **Pull Request** hacia `main`. El job **Validar manifiestos de Kubernetes** sale en rojo y el job de imagenes **no se ejecuta**. Abre el log: dice `'uno' is not of type 'integer'`.
5. Corrige (`replicas: 1`), haz commit y push: ahora todo sale en verde.
6. Cierra el Pull Request sin fusionar (**Close pull request**) o fusionalo ya corregido.

## Que debes saber explicar (preguntas probables)
- **Diferencia entre CI y CD:** la CI prueba y construye en cada cambio; el despliegue (CD) aqui lo hace `kubectl apply -k`. No usamos GitOps (Argo CD), pero el manifiesto en git es la fuente de verdad de que imagen debe correr.
- **Por que la etiqueta es el SHA:** para saber exactamente que codigo corre en cada pod; `1.0.0` no dice nada del commit.
- **Donde estan las credenciales:** en los Secrets de GitHub, no en el codigo.
- **Por que en un Pull Request no se publica nada:** el paso de subir imagenes solo corre en `push` a `main`.

## Si algo falla
- **`unauthorized` o `denied` en el job de imagenes:** revisa que `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN` existan con esos nombres exactos y que el token sea Read & Write.
- **El job `actualizar-manifiesto` falla al hacer push:** falta el Paso 4 (permisos de escritura).
- **El job de pruebas falla:** abre el log y copia el error completo para consultarlo.
