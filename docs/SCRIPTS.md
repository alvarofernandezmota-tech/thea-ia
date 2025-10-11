# Scripts de Automatización – Thea IA 2.0

Este documento describe el propósito y ejemplo de uso de los scripts incluidos en el proyecto, organizados en la carpeta `/scripts/`.

---

## 📁 Ubicación

- Todos los scripts están en `/scripts/`
- Solo deben ejecutarse dentro de un entorno virtual con dependencias instaladas

---

## 📜 ¿Qué scripts hay disponibles?

- `setup.sh`: Inicializa entorno, instala dependencias y crea archivos base.
- `deploy.sh`: Automatiza el despliegue en producción o servidores.
- `migrate.sh`: Ejecuta migraciones de la base de datos (vía Alembic).
- `lint.sh`: Ejecuta linters y formateadores sobre el código.
- `entrypoint.sh`: Script de entrada para Docker.

---parte 2

---

## 🚀 Ejemplo de uso

### Inicializar entorno
bash scripts/setup.sh

text

### Migrar la base de datos
bash scripts/migrate.sh

text

### Desplegar el proyecto
bash scripts/deploy.sh

text

### Ejecutar linter y formateador
bash scripts/lint.sh

text

---

## 🌱 Recomendaciones y ampliación

- Añade nuevos scripts con nombre explícito y docstring inicial explicando el propósito.
- Documenta cada paso relevante en este archivo al añadir o modificar scripts.
- Revisa permisos de ejecución y rutas de acceso antes de subir cambios.
- Toda automatización nueva debe tener ejemplo de uso al menos para una plataforma.

---parte 3 

---

## 🎯 Propósito principal de la carpeta /scripts

La carpeta `/scripts` centraliza toda la automatización, despliegue, migración y testing del proyecto.  
Sirve para facilitar tareas repetitivas, preparar entornos, mejorar la productividad y la consistencia del equipo.

---

## ✨ Estándares y buenas prácticas

- Todo script debe tener nombre descriptivo (`setup.sh`, `lint.sh`, `test_e2e.sh`, etc.).
- Incluir un bloque de ayuda/uso (`usage`) al inicio de cada script para orientación rápida.
- Documentar dependencias externas (herramientas, binarios, servicios) y pre-requisitos.
- Usar rutas relativas y variables de entorno para mejor portabilidad.

---

## 🗂️ Tipos de scripts recomendados

- **Instalación**: preparar el entorno, instalar dependencias, levantar contenedores.
- **Migración BD**: crear/actualizar el esquema de base de datos y migrar modelos.
- **Testing**: lanzar tests unitarios, coverage y E2E.
- **Linting/Format**: validar estilo y formato de código.
- **Despliegue**: automatizar despliegues productivos/staging.
- **Mantenimiento**: rotación de logs, backups, limpieza temporal, salud del sistema.

---

## 🛠️ Ejemplo de bloque de ayuda en Bash

if [ "$1" == "--help" ]; then
echo "Uso: setup.sh [opciones]

Instala dependencias y configura entorno para Thea IA 2.0

Opciones disponibles:
--dev: instala dependencias de desarrollo
--lint: ejecuta linters después de setup
"
exit 0
fi

text

---

## 🔗 Integración con documentación técnica

- Documenta cada nuevo script en este archivo con propósito y ejemplo.
- Actualiza README.md cuando añadas automatizaciones clave.

---

*Mantén la carpeta /scripts y SCRIPTS.md alineados para garantizar reproducibilidad y onboarding ágil de todo el equipo.*