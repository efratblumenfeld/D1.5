import pandas as pd
import matplotlib.pyplot as plt
import os

# Get the Excel file path from user input
file_path = input("Please enter the path to the Excel file: ")

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Prepare the plot
fig, ax = plt.subplots()

# Iterate over each sheet in the Excel file
for sheet_name in xls.sheet_names:
    # Read data from the current sheet
    data = pd.read_excel(xls, sheet_name=sheet_name)
    # Plot data (assumes data in column 'G' are x-values and data in column 'H' are y-values)
    ax.plot(data['X axis'], data['Largest our of all'], label=sheet_name)

# Set the labels and title for the axes
ax.set_xlabel('Total Number of Nodes')
ax.set_ylabel('Giant component')
ax.set_title('Giant Component vs. % of Removed Nodes')
ax.legend()

# Save the graph in the same folder as the Excel file
output_path = os.path.join(os.path.dirname(file_path), "graph_giant.png")
plt.savefig(output_path)
plt.close()

print(f"Graph saved successfully at {output_path}")
