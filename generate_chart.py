# Usage: python3 generate_chart.py bar output.png "Month" "Sales" Jan:10 Feb:15 Mar:12
import sys
import matplotlib.pyplot as plt

def main():
    chart_type = sys.argv[1]
    output_file = sys.argv[2]
    x_label = sys.argv[3]
    y_label = sys.argv[4]
    raw_data = sys.argv[5:]

    labels = []
    values = []

    for item in raw_data:
        label, value = item.split(":")
        labels.append(label)
        values.append(float(value))

    plt.figure(figsize=(6,4))
    if chart_type == "bar":
        plt.bar(labels, values)
    elif chart_type == "line":
        plt.plot(labels, values, marker="o")
    else:
        print("Unsupported chart type:", chart_type)
        return

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"{chart_type.capitalize()} Chart")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    main()
