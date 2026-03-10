PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

SRC_C_DIR := src/c
BUILD_DIR := build
TARGET := $(BUILD_DIR)/md2chart

LEXER := $(SRC_C_DIR)/mdchart.l
PARSER := $(SRC_C_DIR)/mdchart.y
LEX_C := $(BUILD_DIR)/lex.yy.c
YACC_C := $(BUILD_DIR)/mdchart.tab.c
YACC_H := $(BUILD_DIR)/mdchart.tab.h
C_SRC := $(SRC_C_DIR)/main.c $(SRC_C_DIR)/ast.c

.DEFAULT_GOAL := help

help:
	@echo "Targets:"
	@echo "  install        Install package and dev deps"
	@echo "  test           Run pytest suite"
	@echo "  api            Run FastAPI dev server"
	@echo "  legacy-build   Build legacy C/Flex/Bison binary"
	@echo "  legacy-run     Run legacy binary using examples/example.md"
	@echo "  clean          Remove generated artifacts"

install:
	$(PIP) install -e '.[dev]'

test:
	$(PYTHON) -m pytest

api:
	uvicorn apps.api.main:app --reload

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(YACC_C) $(YACC_H): $(PARSER) | $(BUILD_DIR)
	bison -d -o $(YACC_C) $(PARSER)

$(LEX_C): $(LEXER) $(YACC_H) | $(BUILD_DIR)
	flex -o $(LEX_C) $(LEXER)

$(TARGET): $(C_SRC) $(YACC_C) $(LEX_C)
	gcc -I$(SRC_C_DIR) -I$(BUILD_DIR) -o $(TARGET) $(C_SRC) $(YACC_C) $(LEX_C)

legacy-build: $(TARGET)

legacy-run: legacy-build
	MDCHART_PYTHON=$$(if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi) \
	./$(TARGET) < examples/example.md > examples/example_output.md

clean:
	rm -rf $(BUILD_DIR) .pytest_cache chart_*.png

.PHONY: help install test api legacy-build legacy-run clean
