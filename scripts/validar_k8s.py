"""Valida los manifiestos de k8s/ contra el esquema de Kubernetes 1.31.

Uso:  python scripts/validar_k8s.py
Sale con codigo 1 (y la CI se pone en rojo) si algun manifiesto es invalido.
"""
import glob
import sys

import kubernetes_validate
import yaml

VERSION = "1.31"
# secrets.example.yaml es solo un ejemplo y kustomization.yaml no es un recurso de Kubernetes.
SALTAR = {"kustomization.yaml", "secrets.example.yaml"}

errores = 0
for archivo in sorted(glob.glob("k8s/*.yaml")):
    if archivo.split("/")[-1] in SALTAR:
        continue
    for recurso in yaml.safe_load_all(open(archivo, encoding="utf-8")):
        if not recurso:
            continue
        nombre = f'{recurso.get("kind")}/{recurso.get("metadata", {}).get("name")}'
        try:
            kubernetes_validate.validate(recurso, VERSION, strict=True)
            print(f"OK    {archivo}: {nombre}")
        except Exception as error:  # noqa: BLE001
            errores += 1
            print(f"ERROR {archivo}: {nombre}: {str(error)[:300]}")

print(f"\nManifiestos con error: {errores}")
sys.exit(1 if errores else 0)
