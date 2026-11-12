"""Cambia la etiqueta (newTag) de las imagenes en k8s/kustomization.yaml.

Uso:  python scripts/actualizar_etiquetas.py <etiqueta>
La CI lo ejecuta con el SHA corto del commit: asi el manifiesto declara que imagen exacta debe correr.
"""
import re
import sys

if len(sys.argv) != 2 or not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", sys.argv[1]):
    sys.exit("Uso: python scripts/actualizar_etiquetas.py <etiqueta>")

RUTA = "k8s/kustomization.yaml"
texto = open(RUTA, encoding="utf-8").read()
nuevo, cambios = re.subn(r"(newTag:\s*)\S+", rf"\g<1>{sys.argv[1]}", texto)
if cambios != 2:
    sys.exit(f"Se esperaban 2 etiquetas en {RUTA} y se encontraron {cambios}")
open(RUTA, "w", encoding="utf-8").write(nuevo)
print(f"{RUTA}: {cambios} imagenes ahora usan la etiqueta {sys.argv[1]}")
