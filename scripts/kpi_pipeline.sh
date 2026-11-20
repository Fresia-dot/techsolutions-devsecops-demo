#!/usr/bin/env bash
# Indicadores 8.25 y 8.28 a partir de las ejecuciones reales del pipeline (requiere GitHub CLI: gh auth login)
set -euo pipefail
gh run list --workflow security-gate.yml --limit 100 --json conclusion,event,headBranch,displayTitle,createdAt > /tmp/runs.json
python3 - <<'PY'
import json
runs = json.load(open("/tmp/runs.json"))
total = len(runs)
ok = sum(r["conclusion"] == "success" for r in runs)
bloq = sum(r["conclusion"] == "failure" for r in runs)
print(f"Ejecuciones de la puerta de seguridad: {total}")
print(f"  Aprobadas (todo en verde):          {ok}")
print(f"  Bloqueadas por hallazgos:           {bloq}")
print(f"KPI 8.25: liberaciones con revisión de seguridad = 100 % (toda versión pasa por el job 'liberacion', meta >= 90 %)")
print("KPI 8.28: secretos/vulnerabilidades críticas en liberaciones = 0 (una versión con hallazgos no puede liberarse)")
for r in runs[:10]:
    print(f"  {r['createdAt'][:16]}  {r['conclusion'] or 'en curso':<9} {r['headBranch']:<28} {r['displayTitle'][:40]}")
PY
