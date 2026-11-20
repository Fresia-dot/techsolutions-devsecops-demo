#!/usr/bin/env bash
# Prueba controlada del criterio de aceptación: el pipeline debe BLOQUEAR un secreto expuesto.
# IMPORTANTE: NO uses la clave de ejemplo de AWS (AKIAIOSFODNN7EXAMPLE): Gitleaks la ignora a propósito
# y la prueba "pasaría". Este script genera una clave FALSA al azar con formato válido (no sirve en AWS).
set -euo pipefail
RAMA="test/secret-gate-$(date +%H%M%S)"
git checkout -b "$RAMA"
set +o pipefail   # tr | head corta la tubería a propósito
KEY="AKIA$(LC_ALL=C tr -dc 'A-Z2-7' </dev/urandom | head -c16)"
SEC="$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c40)"
TOK="ts_live_$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c32)"
set -o pipefail
cat > config_prueba.py <<PY
# Archivo de PRUEBA: secretos falsos generados al azar para demostrar el bloqueo
AWS_ACCESS_KEY_ID = "$KEY"
AWS_SECRET_ACCESS_KEY = "$SEC"
TECHSOL_API_KEY = "$TOK"
PY
git add config_prueba.py
# --no-verify salta el hook local para simular a alguien que lo evita: el pipeline debe atraparlo igual
git commit --no-verify -m "test: secreto de prueba (debe ser bloqueado)"
git push -u origin "$RAMA"
echo
echo "Listo. Abre un Pull Request de $RAMA hacia main y verifica que el job 'Detección de secretos' falla"
echo "y que el botón Merge queda bloqueado. Toma capturas para el acta."
