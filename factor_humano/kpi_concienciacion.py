"""Indicadores del control 6.3 a partir de la exportación de resultados de GoPhish.

Uso:  python kpi_concienciacion.py resultados_gophish.csv [registro_capacitacion.csv]
(En GoPhish: Campaigns > tu campaña > Export CSV > Results)
"""
import csv
import sys

if len(sys.argv) < 2:
    sys.exit("Uso: python kpi_concienciacion.py resultados_gophish.csv [registro_capacitacion.csv]")

with open(sys.argv[1], encoding="utf-8") as f:
    filas = list(csv.DictReader(f))

total = len(filas)
clic = [r for r in filas if r["status"] in ("Clicked Link", "Submitted Data")]
reporto = [r for r in filas if str(r.get("reported", "")).lower() == "true"]
abrio = [r for r in filas if r["status"] in ("Email Opened", "Clicked Link", "Submitted Data")]


def pct(a):
    return 0 if total == 0 else 100 * len(a) / total


print(f"Personas evaluadas:            {total}")
print(f"Abrieron el correo:            {len(abrio)} ({pct(abrio):.0f} %)")
print(f"Tasa de clic (KPI 6.3):        {len(clic)} ({pct(clic):.0f} %)   meta <= 5 %  -> {'CUMPLE' if pct(clic) <= 5 else 'NO CUMPLE'}")
print(f"Tasa de reporte:               {len(reporto)} ({pct(reporto):.0f} %)   meta >= 60 % -> {'CUMPLE' if pct(reporto) >= 60 else 'NO CUMPLE'}")
print("\nRequieren microcapacitación (hicieron clic):")
for r in clic:
    print(f"  - {r['first_name']} {r['last_name']} <{r['email']}> ({r.get('position', '')})")

if len(sys.argv) > 2:
    with open(sys.argv[2], encoding="utf-8") as f:
        reg = list(csv.DictReader(f))
    aprobados = [r for r in reg if float(r["nota"]) >= 80]
    print(f"\nCobertura de capacitación:     {len(aprobados)}/{len(reg)} ({100 * len(aprobados) / len(reg):.0f} %)   meta >= 95 %")
