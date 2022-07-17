-include ./devops/makefiles/.env.mk
export ./devops/makefiles/.env.mk
-include ./devops/makefiles/log.mk

SUBMODULE_FOLDER := devops
SUBMODULE_ROOT_FILES_PATH := ${SUBMODULE_FOLDER}/root_files

# ============================
#   ENV
# ============================
.PHONY: venv
venv: ## Create virtualenv
	$(PYTHON) -m venv $(VENV_NAME)
	@$(MAKE) $(MAKE_TAG) venv-activate
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements/bench.txt
	$(PIP) install -r requirements/dev.txt
	$(PIP) install -e .


.PHONY: venv-activate
venv-activate: ## Activate virtual env
	$(VENV_ACTIVATE)


# ============================
#   TEST
# ============================

pytest:  ## Project pytest
	${PYTEST} -m "${mark}" ${var}
.PHONY: pytest


.PHONY: unit-test
unit-test:  ## Run a test
	$(MAKE) ${MAKE_TAG} echo-purple msg="+++unit-test:"
	@$(MAKE) ${MAKE_TAG} pytest var=${TEST_PATH} mark=ut
