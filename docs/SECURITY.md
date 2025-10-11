# Guía de Seguridad – Thea IA 2.0

Este documento recoge las buenas prácticas y políticas mínimas para garantizar un despliegue y desarrollo seguro en Thea IA 2.0.

---

## 🔒 Principios clave

- Nunca guardar claves ni passwords en el código fuente.
- Usar variables de entorno (`.env`) para toda información sensible.
- Revisar y actualizar dependencias regularmente.
- Seguir el principio de privilegio mínimo en base de datos y servicios externos.
- Usar HTTPS siempre en producción y para webhooks.

---

¿Quieres que te pase la parte de gestión de credenciales, roles y protección de endpoints?**SECURITY.md – Parte 2: Gestión de credenciales, roles y protección**

🗝️ Gestión de credenciales
Claves, tokens y contraseñas deben estar en .env y nunca en el código.

Protege los archivos sensibles (.env, credenciales/*) con .gitignore.

👥 Roles y permisos
Limita el acceso a datos críticos a los agentes y servicios necesarios.

Configura roles y privilegios en la base de datos.

🛡️ Protección de endpoints
Usa autenticación para todas las rutas críticas en la API.

Configura tiempo de expiración y refresh en tokens JWT.

Rate-Limit y validación extra para endpoints públicos o webhook.

---

## 🕵️ Auditoría y reporting

- Audita dependencias con herramientas automáticas (`pip-audit`, `safety`, etc.) cada mes.
- Documenta y corrige cualquier vulnerabilidad detectada en CHANGELOG.md.
- Emplea logs con rotación y backup para trayectorias de acceso y errores.

## 🔄 Actualización y monitorización

- Actualiza todos los módulos, dependencias y contenedores con regularidad.
- Configura monitorización básica (logs, healthcheck, alertas) para detectar anomalías.
- Revisa SECURITY.md siempre antes de cada release importante.

---

*Todos los cambios de seguridad relevantes deben documentarse en CHANGELOG.md y ser comunicados a los colaboradores activos.*
