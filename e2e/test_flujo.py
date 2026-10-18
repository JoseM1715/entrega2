"""Pruebas Playwright de la aplicación completa (frontend -> backend -> base de datos).

Requieren el sistema corriendo:   docker compose up -d --build
Ejecutar:                         pytest e2e
"""
import os
import re

from playwright.sync_api import Page, expect

FRONTEND = os.getenv("FRONTEND_URL", "http://localhost:8080")
BACKEND = os.getenv("BACKEND_URL", "http://localhost:5000")


def llenar_meta(page: Page, meta, plazo, extra="", mes_extra=""):
    page.get_by_label("Meta (COP)", exact=True).fill(str(meta))
    page.get_by_label("Plazo (meses)", exact=True).fill(str(plazo))
    page.get_by_label("Abono extra (opcional)", exact=True).fill(str(extra))
    page.get_by_label("Mes del abono extra (opcional)", exact=True).fill(str(mes_extra))


def test_la_pagina_carga_los_usuarios_desde_la_base_de_datos(page: Page):
    page.goto(FRONTEND)
    expect(page).to_have_title("Simulador de Ahorro Programado")
    # Miguel Angel lo crea el seeding: si aparece, funcionan frontend -> backend -> BD
    expect(page.locator("#usuario")).to_contain_text("Miguel Angel")


def test_flujo_completo_calcular_guardar_y_buscar_una_meta(page: Page):
    page.goto(FRONTEND)
    expect(page.locator("#usuario")).to_contain_text("Miguel Angel")

    llenar_meta(page, 2500000, 12, 100000, 6)
    page.get_by_role("button", name="Calcular y guardar").click()

    estado = page.locator("#resultado")
    expect(estado).to_contain_text("Cuota mensual")
    expect(estado).to_contain_text("191.516,95")  # cuota calculada con la fórmula real

    id_meta = re.search(r"Meta #(\d+)", estado.inner_text()).group(1)
    page.get_by_label("ID de la meta").fill(id_meta)
    page.get_by_role("button", name="Buscar").click()
    expect(page.locator("#busqueda")).to_contain_text(f"Meta #{id_meta}")
    expect(page.locator("#busqueda")).to_contain_text("191.516,95")


def test_datos_invalidos_muestran_el_error_del_backend(page: Page):
    page.goto(FRONTEND)
    expect(page.locator("#usuario")).to_contain_text("Miguel Angel")

    llenar_meta(page, 1000000, 12, 50000, 0)  # abono sin mes
    page.get_by_role("button", name="Calcular y guardar").click()

    expect(page.get_by_role("alert")).to_contain_text("debe estar entre 1 y el plazo")


def test_buscar_una_meta_que_no_existe(page: Page):
    page.goto(FRONTEND)
    page.get_by_label("ID de la meta").fill("99999999")
    page.get_by_role("button", name="Buscar").click()
    expect(page.get_by_role("alert")).to_contain_text("No hay ninguna meta")


def test_swagger_esta_disponible_en_el_backend(page: Page):
    respuesta = page.request.get(f"{BACKEND}/openapi.json")
    assert respuesta.ok
    assert "/api/metas" in respuesta.json()["paths"]

    page.goto(f"{BACKEND}/docs", wait_until="domcontentloaded")
    expect(page).to_have_title(re.compile("Backend - Simulador de Ahorro Programado"))
