# ==============================================
# THEA IA 2.0 - MAKEFILE
# ==============================================

# Variables
PYTHON = python
PIP = pip
ALEMBIC = alembic
UVICORN = uvicorn

# Targets
.PHONY: setup lint format test migrate run clean logs

setup:
	$(PYTHON) -m venv venv
	. venv/bin/activate && $(PIP) install --upgrade pip
	. venv/bin/activate && $(PIP) install -r requirements.txt

lint:
	. venv/bin/activate && flake8 src/theaia

format:
	. venv/bin/activate && black src/theaia

test:
	. venv/bin/activate && pytest --maxfail=1 --disable-warnings -q

migrate:
	. venv/bin/activate && $(ALEMBIC) upgrade head

run:
	. venv/bin/activate && $(UVICORN) theaia.main:app --host 0.0.0.0 --port 8000 --reload

logs:
	tail -f logs/theaia.log

clean:
	rm -rf __pycache__/
	rm -rf venv/
	rm -rf .pytest_cache/
