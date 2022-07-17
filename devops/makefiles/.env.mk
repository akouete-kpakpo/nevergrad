# Makefile variables
# ------------------
MAKE_TAG := --no-print-directory

# Default configuration
SHELL := /bin/bash
PYTHON := python3
PIP := ${PYTHON} -m pip
CI_FILE := .github/workflows/devops-ci.yml
_VERBOSE ?= -vvv
_COLOR ?= --color=yes
PYTEST := RUN_BY_PYTEST=True ${PYTHON} -m pytest ${_VERBOSE} ${_COLOR}
TEST_PATH := nevergrad
DEFAULT_BRANCH := pcse

# Virtual env
VENV_NAME = venv
VENV_ACTIVATE := source $(VENV_NAME)/bin/activate
