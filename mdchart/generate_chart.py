# Usage: python3 generate_chart.py bar output.png "Month" "Sales" Jan:10 Feb:15 Mar:12
import sys
import matplotlib.pyplot as plt
import os

def main():
    if len(sys.argv) < 5:
        print("Error: Not enough arguments")
        print("Usage: python3 generate_chart.py <chart_type> <output_file> <x_label> <y_label> <data_points...>")
        sys.exit(1)

    chart_type = sys.argv[1]
    output_file = sys.argv[2]
    x_label = sys.argv[3]
    y_label = sys.argv[4]
    raw_data = sys.argv[5:]

    if not raw_data:
        print("Error: No data points provided")
        sys.exit(1)

    labels = []
    values = []

    try:
        for item in raw_data:
            label, value = item.split(":")
            labels.append(label)
            values.append(float(value))
    except ValueError as e:
        print(f"Error: Invalid data format. Expected 'label:value', got '{item}'")
        sys.exit(1)

    try:
        plt.figure(figsize=(8, 6))
        if chart_type == "bar":
            plt.bar(labels, values)
        elif chart_type == "line":
            plt.plot(labels, values, marker="o")
        else:
            print(f"Error: Unsupported chart type: {chart_type}")
            sys.exit(1)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f"{chart_type.capitalize()} Chart")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Successfully generated chart: {output_file}")
    except Exception as e:
        print(f"Error generating chart: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
