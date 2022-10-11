# run these commands from /services directory

.PHONY: quality # runs pre-commit hooks for development purposes
UTILS_DIR = ./utilities
quality:
	@echo "Running pre-commit hooks from `pwd`"
	@echo "Ensure your files are staged to be checked"
	@cd $(UTILS_DIR) && poetry run pre-commit run

.PHONY: install # runs install-services script
install:
	./install-services.sh
