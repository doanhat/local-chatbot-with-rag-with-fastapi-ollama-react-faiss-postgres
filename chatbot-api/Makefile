PACKAGE := api
PACKAGES := $(PACKAGE) tests
FAILURES := .pytest_cache/v/cache/lastfailed
install: .install .cache ## Install project dependencies

.install: poetry.lock
	poetry install
	poetry check
	@touch $@

poetry.lock: pyproject.toml
	poetry lock
	@touch $@

.cache:
	@mkdir -p .cache

.PHONY: requirements.txt
requirements.txt: install ## Generate requirements.txt
	@mkdir -p dist
	@poetry export --without-hashes -f requirements.txt > dist/requirements.txt
	@gsed -i '1d' dist/requirements.txt


.PHONY: check
check: install ## Run linters and static analysis
	poetry run isort $(PACKAGES)
	poetry run ruff format $(PACKAGES)
	poetry run ruff check $(PACKAGE) --fix
	poetry run mypy --show-error-codes --ignore-missing-imports --config-file pyproject.toml $(PACKAGE)

.PHONY: test
test: install ## Run unit tests
	@if test -e $(FAILURES); then poetry run pytest tests --last-failed --exitfirst; fi
	@rm -rf $(FAILURES)
	poetry run pytest