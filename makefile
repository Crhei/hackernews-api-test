.DEFAULT_GOAL = help
VENV ?= . venv/bin/activate;

.PHONY: help
help: ## List the available targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z%_-]+:.*?## / {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

ensure-bash: ## check that the correct shell is configured for make
	@( /bin/sh --version | grep bash > /dev/null) || \
	  (echo 'This makefile requires Bash. Please run "ln -fs `which bash` /bin/sh"' && exit 1)

.PHONY: install
install: venv ensure-bash ## create venv, install requirements and pre-commit hooks
	@echo "\n...\nDone! Activate venv by running 'source venv/bin/activate'"
venv: venv/touchfile ## create venv, install requirements
venv/touchfile: requirements.txt # Only re-install venv if requirements have changed
	test -d venv || python3.12 -m venv venv
	$(VENV)python3.12 -m pip install --upgrade pip
	$(VENV)pip install -Ur requirements.txt
	touch venv/touchfile

.PHONY: pylint pylint-all
pylint: ensure-bash ## run `pylint core tests` on changed files, all messages
	@export changes=$$(git diff --name-only --diff-filter=d HEAD | grep '\.py$$'); \
	  if [ ! -z "$$changes" ] ; then \
	    $(VENV)echo "$$changes" | xargs pylint ; \
	  fi
pylint-all: ## run `pylint core tests` on all files, all messages
	@$(VENV)pylint core tests

.PHONY: format logs clean cleanup
logs: ## tail test logs
	@tail -f output/test.log
clean: ## remove venv and compiled python files
	@rm -rf venv
	@find . -iname "*.pyc" -delete
cleanup: ## remove tmp dirs and test artifacts
	@find . -name "output" -type d -print -exec rm -rv "{}" +
