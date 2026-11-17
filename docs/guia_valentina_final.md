# Guia final para Valentina (CI, imagenes y trazabilidad)

Esta guia completa `docs/guia_valentina.md` con lo que falta para la entrega. Tu parte es **conceptual**: Francisco ejecuta en el computador y tu explicas. Valen D2 (12), D3 (8) y D6 (10).

## 1. Tu parte de un vistazo
| Donde | Que haces |
|---|---|
| Pitch | Hablas en las diapositivas **3 (solucion), 4 (alcance) y 6 (cadena de entrega)**. Las notas de cada una dicen que decir |
| Demo, minutos 6 a 11 | Explicas la CI: ejecucion con pruebas y build, el Pull Request con fallo controlado y las imagenes en Docker Hub |
| Demo, minutos 11 a 13 | Explicas la trazabilidad: commit, CI, imagen con etiqueta, manifiesto y pod |
| Preguntas | Respondes las de CI, y como todos, cualquier pregunta del sistema (D9) |

## 2. Lo que debes dejar listo HOY
### 2.1 El Pull Request con fallo controlado (lo mas importante)
Francisco solo lo abre en la demo, asi que debe quedar **ya creado y abierto**:
```
git clone --recurse-submodules https://github.com/JoseM1715/entrega2.git
cd entrega2
git checkout -b demo-fallo
```
En `k8s/30-backend.yaml` cambia `replicas: 1` por `replicas: uno`, guarda y:
```
git commit -am "demo: manifiesto roto"
git push -u origin demo-fallo
```
En GitHub abre un **Pull Request** de `demo-fallo` hacia `main`. Debe pasar esto:
- El job **Validar manifiestos de Kubernetes** sale en **rojo** y su log dice `'uno' is not of type 'integer'`.
- El job **Construir y publicar imagenes** **no se ejecuta** (depende del anterior).
- **No cierres ni fusiones** el Pull Request: dejalo abierto para mostrarlo.
- Toma captura del rojo y del log del error.

Si `git push` da `permission denied`, falta que Jose te agregue como colaboradora (**Settings > Collaborators** del repo `entrega2`) y que aceptes la invitacion en https://github.com/notifications.

### 2.2 Comprobar lo que vas a mostrar
- [ ] Pestana **Actions**: una ejecucion verde de **CI** con sus 4 jobs.
- [ ] **Docker Hub**, `josem1715/entrega2-backend` y `entrega2-frontend` > **Tags**: la etiqueta del commit y `latest`.
- [ ] Repo, archivo `k8s/kustomization.yaml`: la misma etiqueta del commit.
- [ ] Opcional, en tu Minikube: `powershell -ExecutionPolicy Bypass -File .\scripts\desplegar.ps1` y luego `kubectl get pods -n ahorro -o custom-columns=POD:.metadata.name,IMAGEN:.spec.containers[*].image`.

## 3. Que explicas en la demo
### Minutos 6 a 11: CI en GitHub Actions
Mientras Francisco muestra la pestana Actions:
- "El workflow se dispara con cada push a `main`, con cada Pull Request y a mano con **Run workflow**."
- "Tiene 4 jobs en cadena: **pruebas del backend** (levanta PostgreSQL y corre 41 pruebas), **validar Kubernetes** (revisa los manifiestos contra el esquema de la version 1.31), **construir y publicar imagenes** y **actualizar el manifiesto**."
- "Si un job falla, los siguientes no corren: nada se publica con pruebas rotas."
- **Fallo controlado:** "Cambiamos `replicas: 1` por `replicas: uno`. La validacion sale en rojo con `'uno' is not of type 'integer'` y el job de imagenes ni se ejecuta. Ademas, en un Pull Request nunca se publica nada: el login y el push a Docker Hub solo ocurren cuando el evento no es `pull_request`."
- **Docker Hub:** "Cada imagen lleva como etiqueta el SHA corto del commit. Tambien se publica `latest` por comodidad, pero Kubernetes usa el SHA."

### Minutos 11 a 13: trazabilidad
Cadena: **commit -> CI -> imagen con etiqueta -> manifiesto -> pod**.
- "El ultimo job escribe la etiqueta en `k8s/kustomization.yaml` y la guarda con un commit del bot. Ese commit lleva `[skip ci]` para que la CI no se dispare en bucle."
- Francisco corre `kubectl get pods -n ahorro -o custom-columns=POD:.metadata.name,IMAGEN:.spec.containers[*].image` y tu senalas: "este pod corre la imagen con la etiqueta X, que es el commit X en GitHub. Asi se exactamente que codigo corre."

**Ejemplo real del repo** (confirma en GitHub cual es el mas reciente antes de la demo): el commit `09addd5` genero las imagenes con etiqueta `09addd5`, y el commit del bot `afaff21` ("ci: imagenes con etiqueta 09addd5 [skip ci]") actualizo el manifiesto.

## 4. Preguntas probables
- **Diferencia entre CI y CD?** La CI prueba y construye en cada cambio. El despliegue lo hacemos con `kubectl apply -k`. No usamos GitOps (Argo CD), pero el manifiesto en git es la fuente de verdad de que imagen debe correr.
- **Por que la etiqueta es el SHA?** Dice exactamente que codigo corre en cada pod. Una version como `1.0.0` no lo dice.
- **Donde estan las credenciales?** En los Secrets de GitHub (`DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN`), nunca en el codigo ni en las imagenes.
- **Por que en un Pull Request no se publica nada?** Porque el login y el push solo corren cuando el evento no es `pull_request`.
- **Que pasa si una prueba falla?** Los jobs siguientes no corren y no se publica nada.
- **Por que no usaron GitOps?** Es mas complejo y no hacia falta para demostrar la trazabilidad. Lo reconocemos como limitacion.
- **Que pasa si se cae la base de datos?** Kubernetes la reinicia y usa un volumen, asi que los datos no se pierden. Francisco lo demuestra borrando `db-0`.

## 5. Checklist final
- [ ] Soy colaboradora del repo y puedo hacer `git push`.
- [ ] El Pull Request `demo-fallo` esta abierto, en rojo, y tengo captura.
- [ ] Vi una ejecucion verde con los 4 jobs y las etiquetas en Docker Hub.
- [ ] Lei `docs/guion_demo.md` y las notas de mis diapositivas 3, 4 y 6.
- [ ] Ensaye mi tramo (unos 7 minutos de demo mas mi parte del pitch) con cronometro.
- [ ] Ningun token ni contrasena a la vista.
