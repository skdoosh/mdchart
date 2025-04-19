#ifndef AST_H
#define AST_H

typedef struct DataPoint {
    char *label;
    int value;
} DataPoint;

typedef struct DataPointList {
    DataPoint **items;
    int count;
    int capacity;
} DataPointList;

typedef struct ChartSpec {
    char *type;
    char *x_field;
    char *y_field;
    DataPointList *data;
    int id;  // Added chart ID for unique filenames
} ChartSpec;

// Global counter for chart IDs
extern int chart_id_counter;

// Constructors
ChartSpec *create_chart_spec(const char *type, const char *x, const char *y, DataPointList *data);
DataPoint *create_data_point(const char *label, int value);
DataPointList *create_data_list(DataPoint *first);
DataPointList *append_data_list(DataPointList *list, DataPoint *point);

// Chart generation
void generate_chart_png(const ChartSpec *c);
char *get_chart_image_markdown(const ChartSpec *c);

// Emitter
void emit_chart_html(const ChartSpec *c);

// Cleanup
void free_chart_spec(ChartSpec *c);

#endif
