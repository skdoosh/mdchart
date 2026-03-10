%{
#include "mdchart.tab.h"
#include <string.h>
#include <stdlib.h>

#define MAX_INPUT_SIZE 65536

void yyerror(const char *s);
extern char input_buffer[];
extern int input_size;

// Function to append text to input buffer
void append_to_buffer(const char *text) {
    int len = strlen(text);
    if (input_size + len < MAX_INPUT_SIZE - 1) {
        strcpy(input_buffer + input_size, text);
        input_size += len;
    }
}

// Clear the input buffer
void clear_input_buffer() {
    input_buffer[0] = '\0';
    input_size = 0;
}
%}

%x CHART_BLOCK

%%

"```chart"[ \t]*\n { 
    BEGIN(CHART_BLOCK); 
    return CHART_START; 
}

<CHART_BLOCK>"```"[ \t]*\n { 
    BEGIN(INITIAL); 
    return CHART_END; 
}

<CHART_BLOCK>{
    "type"            { return TYPE; }
    "x"               { return X; }
    "y"               { return Y; }
    "data"            { return DATA; }

    "="               { return EQUALS; }
    ";"               { return SEMI; }
    ","               { return COMMA; }
    ":"               { return COLON; }
    "["               { return LBRACK; }
    "]"               { return RBRACK; }

    [a-zA-Z_][a-zA-Z0-9_]* {
        yylval.str = strdup(yytext);
        return IDENTIFIER;
    }

    [0-9]+            {
        yylval.num = atoi(yytext);
        return NUMBER;
    }

    [ \t\r\n]+        { /* skip whitespace */ }

    .                 { /* ignore unknown characters in CHART_BLOCK */ }
}

.|\n              { /* ignore non-chart content */ }

%%

int yywrap() { return 1; }
