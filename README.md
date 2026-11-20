# TechSolutions – Implementación funcional de la Parte 4 del SGSI

Kit para **demostrar en vivo** los controles ISO/IEC 27001:2022 de la Parte 4
(6.3, 5.19, 5.23, 8.25, 8.28 y los relacionados 5.20, 5.21, 8.29, 8.33) y la mitigación de los riesgos R4.1–R4.6.

La aplicación, las dependencias y la infraestructura son **inseguras a propósito**. Las versiones corregidas están en `fixes/`.

| Demo | Control / riesgo | Qué se muestra | Archivos |
| --- | --- | --- | --- |
| 0 | Base | Repo en GitHub, rama protegida, entorno `production` con aprobación | `.github/` |
| 1 | 8.28 / **R4.1** | Hook pre-commit bloquea un secreto en tu PC; secreto movido a GitHub Secrets | `.pre-commit-config.yaml`, `.gitleaks.toml`, `.env.example` |
| 2 | 8.28 / R4.2 | SAST (Semgrep) detecta inyección SQL y debug activo; se corrige | `.semgrep/`, `app.py`, `fixes/app_seguro.py` |
| 3 | 5.21 / R4.5 | pip-audit detecta librerías con CVE; se actualizan; SBOM | `requirements.txt`, `fixes/requirements_seguro.txt` |
| 4 | 5.23 / **R4.3** | Checkov detecta bucket público, SSH abierto, IAM `*`; se corrige | `infra/main.tf`, `fixes/infra_main_seguro.tf` |
| 5 | 8.25 / R4.2 | DAST (ZAP) + puerta de liberación con aprobación + checklist de PR | `.github/workflows/security-gate.yml` |
| 6 | **Criterio de aceptación** | El pipeline bloquea un secreto aunque se salte el hook | `scripts/prueba_secreto.sh` |
| 7 | 5.19 + 5.23 / **R4.3** | Registro y evaluación de proveedores y servicios en la nube, con KPI | `terceros/` |
| 8 | 6.3 / R4.4 | Phishing simulado local (GoPhish + Mailpit) y KPI de clic/reporte | `factor_humano/` |
| 9 | Indicadores | KPI del pipeline a partir de ejecuciones reales | `scripts/kpi_pipeline.sh` |

Notas importantes:
- **No uses la clave de ejemplo de AWS `AKIAIOSFODNN7EXAMPLE`** para la prueba: Gitleaks la ignora y la prueba pasaría. `prueba_secreto.sh` genera claves falsas al azar.
- `infra/` **no se despliega**: Checkov la analiza como código. Desplegarla crearía un bucket público real.
- El laboratorio de phishing usa solo cuentas ficticias `@techsolutions.test` y Mailpit: ningún correo sale a internet.
  Una campaña con personas reales requiere autorización escrita de la dirección y aviso a RR. HH.
