VENV := .venv
REPORTS := .reports

PROJECT := specifications
TESTS := tests

PY_FILES := $(shell find $(PROJECT) $(TESTS) -name "*.py")

clean:
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf $(REPORTS)
	@rm -rf $(VENV)

$(VENV):
	poetry install

$(REPORTS):
	mkdir $(REPORTS)

setup: $(VENV) $(REPORTS)

flake8: setup
	poetry run flake8 $(PROJECT) $(TESTS)

mypy: setup
	poetry run mypy $(PROJECT) $(TESTS)

bandit: setup
	poetry run bandit -qr $(PROJECT) $(TESTS) -c .bandit.yml

pylint: setup
	poetry run pylint $(PROJECT) $(TESTS) > $(REPORTS)/pylint.txt

isort: setup
	poetry run isort $(PROJECT) $(TESTS)

isort-lint: setup
	poetry run isort -c $(PROJECT) $(TESTS)

trailing-comma: setup
	@poetry run add-trailing-comma $(PY_FILES) --py36-plus --exit-zero-even-if-changed

trailing-comma-lint: setup
	@poetry run add-trailing-comma $(PY_FILES) --py36-plus

auto-pep: setup
	poetry run autopep8 -air $(PROJECT) $(TESTS)

requirements:
	poetry export -f requirements.txt --output $(REPORTS)/requirements.txt --without-hashes

cyclonedx: requirements setup
	poetry run cyclonedx-py -i $(REPORTS)/requirements.txt -o $(REPORTS)/bom.xml

test: setup
	poetry run pytest --cov=$(PROJECT)

format: isort trailing-comma auto-pep

lint: flake8 mypy bandit pylint isort-lint trailing-comma-lint cyclonedx

all: format lint test

.DEFAULT_GOAL := all
