UTILS_DIR = ./services/utilities

.PHONY: quality # runs pre-commit hooks for development purposes
quality:
	@echo "Running pre-commit hooks from `pwd`"
	@echo "Ensure your files are staged to be checked"
	@cd $(UTILS_DIR) && poetry run pre-commit run

.PHONY: install # runs install-services script
install:
	@cd $(UTILS_DIR) && ./install-services.sh && poetry run pre-commit install
