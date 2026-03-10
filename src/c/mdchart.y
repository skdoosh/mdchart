%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

extern int yylex();
void yyerror(const char *s);

// External variables for input/output
extern FILE *yyin;
extern FILE *yyout;
extern char input_buffer[];
extern int input_size;

// Function to replace a chart block with an image link
void replace_chart_block(int start_pos, int end_pos, const char *image_link) {
    // Calculate the length of the replacement
    int link_len = strlen(image_link);
    int block_len = end_pos - start_pos;
    
    // Create a new buffer for the modified content
    char *new_buffer = malloc(input_size + link_len - block_len + 1);
    
    // Copy the content before the chart block
    strncpy(new_buffer, input_buffer, start_pos);
    new_buffer[start_pos] = '\0';
    
    // Copy the image link
    strcat(new_buffer, image_link);
    strcat(new_buffer, "\n");
    
    // Copy the content after the chart block
    strcat(new_buffer, input_buffer + end_pos);
    
    // Update the input buffer
    strcpy(input_buffer, new_buffer);
    input_size = strlen(new_buffer);
    
    // Free the temporary buffer
    free(new_buffer);
}

// Function to find the position of a chart block
int find_chart_block_start() {
    char *start = strstr(input_buffer, "```chart");
    if (start) {
        return start - input_buffer;
    }
    return -1;
}

int find_chart_block_end() {
    char *end = strstr(input_buffer, "```\n");
    if (end) {
        return end - input_buffer + 4;  // Include the newline after ```
    }
    return -1;
}

ChartSpec *parsed_chart;
%}

%code requires {
    #include "ast.h"
}

%union {
    int num;
    char *str;               // For strings (e.g., IDENTIFIER, chart_type, field_name)
    DataPoint *point;        // For a single data point
    DataPointList *list;     // For a list of data points (data_list)
    ChartSpec *spec;         // For chart specifications
}

%token <str> IDENTIFIER
%token <num> NUMBER

%token TYPE X Y DATA
%token EQUALS SEMI COMMA COLON LBRACK RBRACK
%token CHART_START CHART_END

%type <str> chart_type field_name
%type <list> data_list
%type <point> data_pair
%type <spec> chart_body
%type <str> type_decl x_decl y_decl
%type <list> data_decl

%%

input:
    /* empty */
  | input chart_block
  ;

chart_block:
    CHART_START chart_body CHART_END
    {
        // Generate the PNG chart
        generate_chart_png($2);
        
        // Get the Markdown image link
        char *image_link = get_chart_image_markdown($2);
        
        // Find the chart block in the input
        int start_pos = find_chart_block_start();
        int end_pos = find_chart_block_end();
        
        if (start_pos >= 0 && end_pos >= 0) {
            // Replace the chart block with the image link
            replace_chart_block(start_pos, end_pos, image_link);
        }
        
        // Free the image link
        free(image_link);
        
        // Free the chart spec
        free_chart_spec($2);
    }
    ;

chart_body:
    type_decl x_decl y_decl data_decl
    {
        // Create the ChartSpec
        $$ = create_chart_spec($1, $2, $3, $4); 
    }
    ;

type_decl:
    TYPE EQUALS chart_type SEMI { $$ = $3; }
    ;

x_decl:
    X EQUALS field_name SEMI { $$ = $3; }
    ;

y_decl:
    Y EQUALS field_name SEMI { $$ = $3; }
    ;

data_decl:
    DATA EQUALS LBRACK data_list RBRACK SEMI { $$ = $4; }
    ;

chart_type:
    IDENTIFIER { $$ = $1; }  // Store the chart type as a string
    ;

field_name:
    IDENTIFIER { $$ = $1; }  // Store the field name as a string
    ;

data_list:
    data_pair                 { $$ = create_data_list($1); }  // Create a data list from one data point
  | data_list COMMA data_pair { $$ = append_data_list($1, $3); } // Append new data points to the list
    ;

data_pair:
    IDENTIFIER COLON NUMBER  { $$ = create_data_point($1, $3); }  // Create a data point with label and value
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Parse error: %s\n", s);
}
