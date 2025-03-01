# Makefile to gather common commands

.PHONY: build check clean format help lint pipenv-dev-install publish-pypi publish-testpypi show-version-dev validate-publish version-bump version-bump-dev version-bump-patch version-bump-post version-bump-rc
.DEFAULT_GOAL := help

help: ## Show this help menu
	$(info Available make commands:)
	@grep -e '^[a-z|_|-]*:.* ##' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS=":.* ## "}; {printf "\t%-23s %s\n", $$1, $$2};'

.print-phony:
	@echo -n "\n.PHONY: "
	@grep '^[a-z|_|-]*:.* ##' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS=":.* ## "}; {printf "%s ", $$1};'
	@echo "\n"

set-up-git-hooks:
	@cp .githooks/* .git/hooks/

####### CI/CD COMMANDS #######################################################################

version-bump-dev: ## Bump blueprintflow dev-release version
	@python -m incremental.update blueprintflow --dev

version-bump-rc: ## Bump blueprintflow release candidate version
	@python -m incremental.update blueprintflow --rc

version-bump: ## Bump blueprintflow version
	@python -m incremental.update blueprintflow

version-bump-post: ## Bump blueprintflow post-release version
	@python -m incremental.update blueprintflow --post

version-bump-patch: ## Bump blueprintflow patch-release version
	@python -m incremental.update blueprintflow --patch

build: check ## Build a distribution for the package
	$(info Building distribution artifacts...)
	@rm -rf dist/
	@python -m build
	@echo Done.

validate-publish: ## Validate if the current distribution can be published
	@if find dist -type f | grep -E '\.(dev|rc)\d*'; then \
		echo "Publish Error: the distribution cannot be published to PyPI.";\
		exit 1; \
	else echo "Publish OK: the distribution can be published to PyPI."; fi

publish-testpypi: validate-publish ## Publish the dist to TestPyPI
	$(info Publishing distribution to TestPyPI...)
	@twine upload -r testpypi dist/* --verbose
	@echo Done.

publish-pypi: validate-publish ## Publish the dist to PyPI
	$(info Publishing distribution to PyPI...)
	@twine upload dist/*
	@echo Done.

show-version-dev: ## Display current dev version
	@pip show blueprintflow | grep 'Version:'

####### COMMANDS #######################################################################

check: ## Check source-code for known security vulnerabilities
	$(info Checking code for known security vulnerabilities...)
	@pipenv check
	@echo Done.

clean: ## Clean up auxiliary and temporary files from the workspace
	$(info Cleaning auxiliary and temporary files...)
	@find . -maxdepth 1 -type d -name '.mypy_cache' -exec rm -r {} +
	@find . -maxdepth 1 -type d -name '.ruff_cache' -exec rm -r {} +
	@find . -maxdepth 1 -type d -name 'build'       -exec rm -r {} +
	@find . -maxdepth 1 -type d -name 'dist'        -exec rm -r {} +
	@find . -maxdepth 2 -type d -name '*.egg-info'  -exec rm -r {} +
	@echo Done.

format: ## Format the entire codebase
	@if \
	type ruff >/dev/null 2>&1 ; then \
		echo Formatting source-code... && \
		echo Applying ruff... && \
		ruff format $(SRC) && \
		echo Done. ; \
	else echo "SKIPPED (ruff not found)" >&2 ; fi

lint: ## Perform a static code analysis
	@if \
	type ruff >/dev/null 2>&1 && \
	type mypy >/dev/null 2>&1 ; then \
		echo Linting source-code... && \
		echo Applying ruff... && \
		ruff check $(SRC) && \
		echo Applying mypy... && \
		mypy --show-error-context --show-column-numbers --pretty $(SRC) && \
		echo Done. ; \
	else echo "SKIPPED (ruff and/or mypy not found)" >&2 ; fi

pipenv-dev-install: ## Create dev venv
	@PIPENV_VERBOSITY=-1 pipenv run pip install --upgrade pip
	@if [ -f "Pipfile.lock" ] ; then \
		PIPENV_VERBOSITY=-1 pipenv install --dev --ignore-pipfile --deploy ; \
	else \
		PIPENV_VERBOSITY=-1 pipenv install --dev ; \
	fi
