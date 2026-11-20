"""Evaluación de proveedores (control 5.19) y servicios en la nube (control 5.23) de TechSolutions.

Uso:  python evaluar_terceros.py
Lee proveedores.csv y servicios_nube.csv (en esta misma carpeta) y genera reporte_terceros.html
con la criticidad, el puntaje, el estado y los indicadores de la Parte 4. Solo usa la biblioteca estándar.
"""
import csv
import html
from datetime import date
from pathlib import Path

AQUI = Path(__file__).parent
AREAS = ["certificaciones", "accesos_mfa", "cifrado", "continuidad", "incidentes",
         "desarrollo_seguro", "subcontratistas", "datos_personales"]
MAXIMOS = [15, 15, 10, 15, 15, 10, 10, 10]  # suman 100 (Anexo 2 del documento)
PUNTAJE_MINIMO = 70


def criticidad(p):
    """Anexo 2: clasificación por acceso a datos, impacto en el servicio y acceso a sistemas."""
    if p["acceso_datos_clientes"] == "si" and p["impacto_si_falla"] == "alto":
        return "Crítico"
    if p["acceso_sistemas_o_codigo"] == "si" or p["acceso_datos_clientes"] == "si":
        return "Alto"
    if p["impacto_si_falla"] == "medio":
        return "Medio"
    return "Bajo"


def evaluar_proveedor(p):
    p["criticidad"] = criticidad(p)
    valores = [p[a].strip() for a in AREAS]
    if all(v == "" for v in valores):
        p["puntaje"] = None
        p["estado"] = "Pendiente de evaluación" if p["criticidad"] in ("Crítico", "Alto") else "No requiere cuestionario completo"
        return p
    puntos = [min(int(v or 0), m) for v, m in zip(valores, MAXIMOS)]
    p["puntaje"] = sum(puntos)
    if p["puntaje"] >= PUNTAJE_MINIMO and p["acuerdo_seguridad_firmado"] == "si":
        p["estado"] = "Aprobado"
    elif p["puntaje"] >= PUNTAJE_MINIMO:
        p["estado"] = "Aprobado: falta firmar cláusulas"
    else:
        p["estado"] = "No aprobado: plan de acción"
    return p


def evaluar_servicio(s):
    problemas = []
    if not s["responsable"].strip():
        problemas.append("sin responsable")
    if s["mfa_cuenta_admin"] != "si":
        problemas.append("sin MFA en la cuenta admin")
    if s["almacenamiento_publico"] == "si":
        problemas.append("almacenamiento público")
    if s["cifrado_activo"] != "si":
        problemas.append("sin cifrado")
    if s["registros_auditoria"] != "si":
        problemas.append("sin registros de auditoría")
    s["problemas"] = problemas
    s["revisado"] = bool(s["responsable"].strip() and s["fecha_ultima_revision"].strip())
    s["estado"] = "Conforme" if not problemas else "No conforme"
    return s


def pct(a, b):
    return 0 if b == 0 else round(100 * a / b)


def main():
    with open(AQUI / "proveedores.csv", encoding="utf-8") as f:
        provs = [evaluar_proveedor(r) for r in csv.DictReader(f)]
    with open(AQUI / "servicios_nube.csv", encoding="utf-8") as f:
        servs = [evaluar_servicio(r) for r in csv.DictReader(f)]

    criticos = [p for p in provs if p["criticidad"] == "Crítico"]
    criticos_ok = [p for p in criticos if p["puntaje"] is not None and p["acuerdo_seguridad_firmado"] == "si"]
    kpi_519 = pct(len(criticos_ok), len(criticos))
    kpi_523 = pct(sum(s["revisado"] for s in servs), len(servs))
    hallazgos_criticos = sum(1 for s in servs for x in s["problemas"] if x in ("almacenamiento público", "sin MFA en la cuenta admin"))

    print("=== Proveedores (5.19) ===")
    for p in provs:
        print(f"  {p['proveedor']:<22} {p['criticidad']:<8} puntaje={p['puntaje'] if p['puntaje'] is not None else '-':<4} {p['estado']}")
    print("=== Servicios en la nube (5.23) ===")
    for s in servs:
        print(f"  {s['servicio']:<26} {s['estado']:<12} {', '.join(s['problemas'])}")
    print(f"\nKPI 5.19 Proveedores críticos evaluados con acuerdo: {kpi_519} % (meta 100 %)")
    print(f"KPI 5.23 Servicios en la nube revisados:            {kpi_523} % (meta >= 90 %)")
    print(f"Hallazgos críticos de configuración en la nube:     {hallazgos_criticos} (meta 0)")

    e = html.escape
    color = {"Aprobado": "#c6efce", "Conforme": "#c6efce"}
    filas_p = "".join(
        f"<tr><td>{e(p['proveedor'])}</td><td>{e(p['servicio'])}</td><td>{p['criticidad']}</td>"
        f"<td>{p['puntaje'] if p['puntaje'] is not None else '—'}</td><td>{e(p['acuerdo_seguridad_firmado'])}</td>"
        f"<td style='background:{color.get(p['estado'], '#ffeb9c' if 'falta' in p['estado'] else '#ffc7ce')}'>{e(p['estado'])}</td>"
        f"<td>{e(p['fecha_evaluacion'] or '—')}</td><td>{e(p['responsable'])}</td></tr>" for p in provs)
    filas_s = "".join(
        f"<tr><td>{e(s['servicio'])}</td><td>{e(s['responsable'] or '— SIN RESPONSABLE —')}</td>"
        f"<td style='background:{color.get(s['estado'], '#ffc7ce')}'>{s['estado']}</td>"
        f"<td>{e(', '.join(s['problemas']) or 'Sin observaciones')}</td><td>{e(s['fecha_ultima_revision'] or '—')}</td></tr>" for s in servs)
    reporte = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>Reporte de terceros - TechSolutions</title>
<style>body{{font-family:Arial,sans-serif;margin:32px;color:#222}}table{{border-collapse:collapse;width:100%;margin:12px 0 28px}}
th,td{{border:1px solid #bbb;padding:6px 8px;font-size:13px;text-align:left}}th{{background:#1f3864;color:#fff}}
.kpi{{display:inline-block;border:1px solid #bbb;border-radius:8px;padding:12px 18px;margin:0 12px 12px 0}}.kpi b{{font-size:24px;display:block}}</style>
<h1>Registro de proveedores evaluados y servicios en la nube</h1>
<p>TechSolutions · ISO/IEC 27001:2022, controles 5.19 y 5.23 · generado el {date.today():%d/%m/%Y} · puntaje mínimo para proveedores críticos: {PUNTAJE_MINIMO}/100</p>
<div class="kpi">Proveedores críticos evaluados con acuerdo (5.19)<b>{kpi_519} %</b>meta 100 %</div>
<div class="kpi">Servicios en la nube revisados (5.23)<b>{kpi_523} %</b>meta ≥ 90 %</div>
<div class="kpi">Hallazgos críticos de configuración<b>{hallazgos_criticos}</b>meta 0</div>
<h2>Proveedores (5.19)</h2><table><tr><th>Proveedor</th><th>Servicio</th><th>Criticidad</th><th>Puntaje</th><th>Acuerdo firmado</th><th>Estado</th><th>Evaluado</th><th>Responsable</th></tr>{filas_p}</table>
<h2>Servicios en la nube (5.23)</h2><table><tr><th>Servicio</th><th>Responsable</th><th>Estado</th><th>Observaciones</th><th>Última revisión</th></tr>{filas_s}</table>
</html>"""
    (AQUI / "reporte_terceros.html").write_text(reporte, encoding="utf-8")
    print("\nReporte generado: terceros/reporte_terceros.html")


if __name__ == "__main__":
    main()
