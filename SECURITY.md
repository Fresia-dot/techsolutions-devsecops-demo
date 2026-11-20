# Política de seguridad del repositorio

- Reporta vulnerabilidades a seguridad@techsolutions.example (no abras un issue público).
- Ningún secreto se guarda en el código: se usan GitHub Secrets o el gestor de secretos.
- Toda liberación pasa por la puerta de seguridad (`.github/workflows/security-gate.yml`).
