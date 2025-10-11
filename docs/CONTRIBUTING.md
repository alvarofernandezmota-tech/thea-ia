# Guía de Contribución – Thea IA 2.0

¡Gracias por tu interés en contribuir a Thea IA 2.0! Queremos construir un ecosistema de agentes inteligente, transparente y profesional.  
Esta guía te orientará para sumarte al desarrollo, reportar fallos y sugerir mejoras.

---

## 🌟 Filosofía y Valores

- Código limpio, mantenible y modular
- Documentación rigurosa y ejemplos claros
- Tests unitarios y E2E obligatorios en cada aportación
- Feedback constructivo y revisiones exhaustivas

---

## 📝 Requisitos previos

- Python 3.9 o superior, entorno virtual recomendado
- Conocer nuestra estructura de carpetas y modelos (ver README.md)
- Haber leído y entendido CHANGELOG.md y ROADMAP.md
- Familiaridad con herramientas: Git, Docker, pytest

---

   --parte 2

---

## 🚦 Flujo básico de desarrollo

1. Haz un fork del repositorio y clona en local.
2. Crea una nueva rama descriptiva, por ejemplo: `feature/nombre`.
3. Haz commits pequeños y frecuentes, siguiendo el estándar [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/).
4. Ejecuta los tests antes de cada push con:
5. Sincroniza tu rama con main antes de abrir un PR (merge/rebase).
6. Envía tu Pull Request (PR) detallando:
- **Qué y por qué** del cambio
- Impacto esperado
- Ticket o issue relacionado

---

## ⚡ Reglas para Pull Requests

- Todo PR debe incluir:
- Tests unitarios y/o E2E relevantes
- Actualización de documentación (`README.md`, diccionarios, etc.)
- Registro de cambios en `CHANGELOG.md`
- No se admitirán cambios sin revisión de otro colaborador.
- La revisión debe ser respetuosa y clara; todos los comentarios constructivos.

---
---

## ✏️ Estilo y organización de código

- Sigue PEP8 y convenciones de tipo/nombre usadas en el proyecto.
- Mantén el código modular: funciones y clases cortas, bien tipadas y con docstrings.
- Distribuye nuevas funcionalidades en los módulos adecuados (`src/theaia/agents`, `adapters`, `database`, `services`, etc.)
- Documenta toda nueva variable en `DICCIONARIO-VARIABLES.md` y campos en model/DB.
- Si refactorizas, explica en el PR la motivación y ventaja del cambio.

## 🌱 Ejemplo de commit relevante

git commit -m "feat(agents): añade nuevo agente para reuniones periódicas"
git commit -m "fix(database): corrige bug en relación Note-User"
git commit -m "docs: actualiza diccionario de variables y README"

text

---parte 3

¿Te entrego ahora la parte final con contacto, buenas prácticas y agradecimientos?**CONTRIBUTING.md – Parte 4: Contacto, buenas prácticas y cierre**

📬 Contacto y agradecimientos
Para dudas técnicas, utiliza Issues en el repositorio.

Contacto principal: Alvaro Fernandez Mota (github: alvarofernandezmota-tech)

No dudes en proponer mejoras y crear discusiones constructivas.

✅ Buenas prácticas
Mantén esta guía actualizada si trabajas nuevas ramas o amplías el equipo.

Añade ejemplos y casos de test siempre que sea posible.

Todo nuevo colaborador debe leer este documento antes de empezar.

¡Gracias por ayudar a que Thea IA 2.0 evolucione y sea cada vez más profesional!

text

Ya tienes la plantilla **CONTRIBUTING.md** lista para implementar, modularizada y alineada a las mejores prácticas. ¿Quieres seguir con FAQ, Architecture, Security o scripts?
