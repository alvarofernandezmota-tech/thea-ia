# 🧠 Thea IA Framework 3.0

Bienvenido a **Thea IA**, una plataforma modular de inteligencia artificial construida sobre **FastAPI**, **FSM (Finite State Machines)** y agentes inteligentes de conversación.

---

### 🔧 Instalación rápida

pip install -r requirements.txt
bash scripts/setup_env.sh

text

---

### 🚀 Inicio rápido

uvicorn src.theaia.api.main:app --reload

text

**Servidor corriendo:**  
http://localhost:8000/docs

---

### 📘 Documentación técnica

La guía completa, arquitectura FSM, agentes y configuraciones detalladas se encuentran en:

➡️ [docs/README.md](docs/README.md)  
➡️ [docs/architecture.md](docs/architecture.md)

---

### 🧩 Tests y migraciones

pytest src/theaia/tests/integration
alembic upgrade head

text

---

**© Thea IA 3.0 — Proyecto modular desarrollado por Álvaro Fernández Mota**
