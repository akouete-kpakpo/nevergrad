-include ./devops/makefiles/Makefile


test-all:  ## Run all tests
	@$(MAKE) ${MAKE_TAG} echo-cyan msg="2.1. Unit tests"
	@$(MAKE) ${MAKE_TAG} unit-test
.PHONY: test-all
