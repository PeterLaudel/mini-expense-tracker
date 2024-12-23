VENV_DIR := $(shell poetry env info --path || echo .venv)
VENV_BIN := $(VENV_DIR)/bin

.PHONY: test
test:
	ENV=test $(VENV_BIN)/pytest --durations=10 -s test

.PHONY: mypy
mypy:
	$(VENV_BIN)/mypy .
