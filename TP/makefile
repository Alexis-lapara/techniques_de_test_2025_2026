# Makefile pour projet Triangulator

# Variables
PYTEST = pytest
COVERAGE = coverage
RUFF = ruff
PDOC = python -m pdoc
SRC = .

# -------------------------
# Targets principales
# -------------------------

.PHONY: all test unit_test perf_test coverage lint doc clean

all: test

# Lance tous les tests
test:
	$(PYTEST) $(SRC)

# Lance tous les tests sauf les tests de performance
unit_test:
	$(PYTEST) -m "not performance" $(SRC)

# Lance uniquement les tests de performance
perf_test:
	$(PYTEST) -m performance $(SRC)

# Génère le rapport de couverture
coverage:
	$(COVERAGE) run -m pytest $(SRC)
	$(COVERAGE) report -m
	$(COVERAGE) html

# Vérifie la qualité du code avec ruff
lint:
	$(RUFF) check $(SRC)

# Génère la documentation en HTML avec pdoc3
doc:
	$(PDOC) -o docs test_triangulation.py test_triangulation_encoding.py test_PointSet_encoding.py test_performance.py test_server.py Triangulator.py encoding.py triangulator_server.py

# Nettoyage des fichiers temporaires et du coverage HTML
clean:
	python -c "import shutil, os; \
[shutil.rmtree(d, ignore_errors=True) for d in ('__pycache__', '.pytest_cache', '.mypy_cache', 'htmlcov', 'docs')]; \
[os.remove(f) for f in ('coverage.xml',) if os.path.exists(f)]"
