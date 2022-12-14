SERVICES_DIR := ./services
UTILS_DIR = $(SERVICES_DIR)/utilities
FRONTEND_DIR := ./frontend

.PHONY: quality # runs pre-commit hooks for development purposes
quality:
	@echo "Running pre-commit hooks from `pwd`"
	@echo "Ensure your files are staged to be checked"
	@cd $(UTILS_DIR) && poetry run pre-commit run

.PHONY: install # runs install-services script
install:
	@cd $(SERVICES_DIR) && ./install-services.sh
	@cd $(UTILS_DIR) && poetry run pre-commit install

.PHONY: build
build: install
	@cd $(FRONTEND_DIR) && npm install
	@cd $(FRONTEND_DIR) && npm run build
	@cd $(SERVICES_DIR)/prediction-api/prediction_api && poetry run main.py
