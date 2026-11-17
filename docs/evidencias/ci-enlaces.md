# Evidencias de CI y trazabilidad (Valentina)

- Pull Request con fallo controlado (replicas: uno): https://github.com/JoseM1715/entrega2/pull/1
  La validacion de manifiestos sale en rojo con 'uno' is not of type 'integer' y no se publican imagenes.
- CI en GitHub Actions: https://github.com/JoseM1715/entrega2/actions
  4 jobs en cadena: pruebas del backend, validar Kubernetes, imagenes y actualizar manifiesto.
- Imagenes en Docker Hub: https://hub.docker.com/r/josem1715/entrega2-backend/tags
  Etiqueta con el SHA del commit y latest.
- Trazabilidad: k8s/kustomization.yaml usa la misma etiqueta del commit (commit del bot con [skip ci]).
