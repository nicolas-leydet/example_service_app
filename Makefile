.PHONY: clean clean-test clean-pyc help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-pyc clean-test ## remove all test, coverage and Python artifacts

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove pytest and coverage artifacts
	rm -fr .cache/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 knogget tests

test: ## run tests using pytest
	pytest

load-test: ## start load tests
	locust -f tests/load/scenario.py --host=http://localhost:5000

coverage: ## check code coverage with pytest and display report
	pytest --cov knogget --cov-report=html
	$(BROWSER) htmlcov/index.html

run: ## run application locally
	python -m knogget.server

ldeploy: docker-stop-all docker-build docker-mongo-start docker-service-start

docker-build:
	docker build . -t knogget_api

docker-service-start:
	docker run -d --name knogget_api -p 5000:5000 --link simple_mongo knogget_api

docker-mongo-start:
	docker run -d --name simple_mongo -p 27017:27017 mongo

docker-stop-all:
	docker stop knogget_api || true
	docker rm knogget_api || true
	docker stop simple_mongo || true
	docker rm simple_mongo || true
