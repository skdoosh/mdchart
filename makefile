# Compiler and tools
CC     = gcc
LEX    = flex
YACC   = bison
PYTHON = python3

# Source files
SRC    = main.c ast.c
LEXER  = mdchart.l
PARSER = mdchart.y

# Generated files
LEX_C  = lex.yy.c
YACC_C = mdchart.tab.c
YACC_H = mdchart.tab.h

# Final executable
TARGET = md2chart

# Python dependencies
PYTHON_DEPS = matplotlib

# Default build
all: $(TARGET)

$(TARGET): $(SRC) $(YACC_C) $(LEX_C)
	$(CC) -o $(TARGET) $(SRC) $(YACC_C) $(LEX_C) -lfl

$(YACC_C) $(YACC_H): $(PARSER)
	$(YACC) -d $(PARSER)

$(LEX_C): $(LEXER)
	$(LEX) $(LEXER)

# Install Python dependencies
python-deps:
	$(PYTHON) -m pip install $(PYTHON_DEPS)

# Clean up generated files
clean:
	rm -f $(TARGET) $(LEX_C) $(YACC_C) $(YACC_H) *.o chart_*.png

# Test run
run: $(TARGET)
	./$(TARGET) < example.md > example_output.md

# View result (Linux/macOS only)
view: run
	xdg-open example_output.md || open example_output.md

.PHONY: all clean run view python-deps
