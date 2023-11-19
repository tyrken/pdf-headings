VENV_DIR:=.venv
APP_NAME:=repo-fixer
APP_FOLDER:=src/repo_fixer

# Equivalent also in .envrc for direct tool usage
export PATH:=$(CURDIR)/$(VENV_DIR)/bin:$(PATH)

help: ## Prints this help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Delete virtual env
	rm -rf $(VENV_DIR)
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

$(VENV_DIR)/poetry.done: poetry.lock
	poetry install --no-ansi
	echo 'done' > $(VENV_DIR)/poetry.done

$(VENV_DIR): $(VENV_DIR)/poetry.done ## Create/update virtualenv

setup: $(VENV_DIR) ## Setup virtualenv

update: ## Force poetry update
	poetry update
	poetry install
	echo 'done' > $(VENV_DIR)/poetry.done

format: $(VENV_DIR) ## Check formatting
	ruff format src/ tests/
	ruff check src/ tests/ --fix

lint: $(VENV_DIR) ## Check lint
	bin/lint-ruff
	# Re-enable later
	# bin/lint-mypy

test: $(VENV_DIR) ## Run tests
	pytest -vv $(PYTEST_OPTS)

local-install: $(VENV_DIR) ## Install app from repo clone to ~/.local/bin
	rm -f ~/.local/bin/$(APP_NAME)
	ABSOLUTE_VENV_DIR=$$(python -c 'import os,sys;print(os.path.realpath("$(VENV_DIR)"))') &&\
	ln -s $$ABSOLUTE_VENV_DIR/bin/$(APP_NAME) ~/.local/bin

publish: ## Publish package to Lyst package server
	poetry version -s > $(APP_FOLDER)/VERSION
	rm -rf dist
	poetry build
	ls -al dist
	twine upload --non-interactive --repository-url https://packages.lystit.com/lyst/dev \
		--username "lyst" --password "" --disable-progress-bar --skip-existing dist/*
