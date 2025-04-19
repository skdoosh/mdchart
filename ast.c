#include "ast.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 8
int chart_id_counter = 0;  // Global counter for chart IDs

ChartSpec *create_chart_spec(const char *type, const char *x, const char *y, DataPointList *data) {
    ChartSpec *c = malloc(sizeof(ChartSpec));
    c->type = strdup(type);
    c->x_field = strdup(x);
    c->y_field = strdup(y);
    c->data = data;
    c->id = chart_id_counter++;  // Assign a unique ID to this chart
    return c;
}

DataPoint *create_data_point(const char *label, int value) {
    DataPoint *d = malloc(sizeof(DataPoint));
    d->label = strdup(label);
    d->value = value;
    return d;
}

DataPointList *create_data_list(DataPoint *first) {
    DataPointList *list = malloc(sizeof(DataPointList));
    list->count = 1;
    list->capacity = INITIAL_CAPACITY;
    list->items = malloc(sizeof(DataPoint *) * list->capacity);
    list->items[0] = first;
    return list;
}

DataPointList *append_data_list(DataPointList *list, DataPoint *point) {
    if (list->count >= list->capacity) {
        list->capacity *= 2;
        list->items = realloc(list->items, sizeof(DataPoint *) * list->capacity);
    }
    list->items[list->count++] = point;
    return list;
}

// Generate a PNG chart using the Python script
void generate_chart_png(const ChartSpec *c) {
    // Create the command to call the Python script
    char cmd[4096];
    char filename[32];
    
    // Format the filename with the chart ID
    snprintf(filename, sizeof(filename), "chart_%03d.png", c->id);
    
    // Start building the command
    snprintf(cmd, sizeof(cmd), "python3 generate_chart.py %s %s \"%s\" \"%s\"", 
             c->type, filename, c->x_field, c->y_field);
    
    // Add data points to the command
    for (int i = 0; i < c->data->count; i++) {
        char data_point[64];
        snprintf(data_point, sizeof(data_point), " %s:%d", 
                 c->data->items[i]->label, c->data->items[i]->value);
        strcat(cmd, data_point);
    }
    
    // Execute the command
    system(cmd);
}

// Get the Markdown image link for a chart
char *get_chart_image_markdown(const ChartSpec *c) {
    char *markdown = malloc(256);
    char filename[32];
    
    // Format the filename with the chart ID
    snprintf(filename, sizeof(filename), "chart_%03d.png", c->id);
    
    // Create the Markdown image link
    snprintf(markdown, 256, "![Chart](%s \"Generated Chart\")", filename);
    
    return markdown;
}

void free_chart_spec(ChartSpec *c) {
    if (!c) return;
    free(c->type);
    free(c->x_field);
    free(c->y_field);
    for (int i = 0; i < c->data->count; i++) {
        free(c->data->items[i]->label);
        free(c->data->items[i]);
    }
    free(c->data->items);
    free(c->data);
    free(c);
}
