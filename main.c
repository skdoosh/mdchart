#include <stdio.h>
#include <string.h>
#include "ast.h"

extern int yyparse();
extern FILE *yyin;
extern FILE *yyout;

// Buffer to store the input Markdown
#define MAX_INPUT_SIZE 65536
char input_buffer[MAX_INPUT_SIZE];
char temp_buffer[MAX_INPUT_SIZE];
int input_size = 0;

// Function to read the entire input into a buffer
void read_input() {
    int c;
    while ((c = getchar()) != EOF && input_size < MAX_INPUT_SIZE - 1) {
        input_buffer[input_size++] = c;
    }
    input_buffer[input_size] = '\0';
}

// Function to output the modified Markdown
void output_markdown() {
    printf("%s", input_buffer);
}

// External function to clear the input buffer
extern void clear_input_buffer();

int main(void) {
    // Clear the input buffer
    clear_input_buffer();
    
    // Read the entire input into a buffer
    read_input();
    
    // Make a copy of the original input
    strcpy(temp_buffer, input_buffer);
    
    // Set up input and output for the lexer/parser
    yyin = fmemopen(temp_buffer, strlen(temp_buffer), "r");
    yyout = stdout;
    
    // Parse input and generate charts
    yyparse();
    
    // Close the input file
    fclose(yyin);
    
    // Output the modified Markdown
    output_markdown();
    
    return 0;
}
