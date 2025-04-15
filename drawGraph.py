# Drawing Graph

import os
import matplotlib.pyplot as plt

# Set path
file_path = os.path.join("result", "quickSort.txt")

input_sizes = []
execution_times = {}
memory_usages = {}

# Read and parse
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Flags to determine which section is being parsed
parsing_exec = False
parsing_mem = False
dataset_types = []

for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith("==="):
        if "Execution Time" in line:
            parsing_exec = True
            parsing_mem = False
        elif "Memory Usage" in line:
            parsing_exec = False
            parsing_mem = True
        continue

    if line.startswith("Dataset Type"):
        # Extract input sizes from the header line
        parts = line.split("\t")
        input_sizes = [int(x) for x in parts[1:]]
        continue

    # Split the line into dataset type and corresponding values
    parts = line.split("\t")
    dtype = parts[0]
    values = [float(x) for x in parts[1:]]

    # Store the values in the appropriate dictionary
    if parsing_exec:
        execution_times[dtype] = values
        if dtype not in dataset_types:
            dataset_types.append(dtype)
    elif parsing_mem:
        memory_usages[dtype] = values

# Plot the average execution time graph
plt.figure(figsize=(12, 6))
for dtype in dataset_types:
    plt.plot(input_sizes, execution_times[dtype], marker='o', label=dtype)
plt.title("Average Execution Time vs Input Size (quickSort)")
plt.xlabel("Input Size")
plt.ylabel("Execution Time (seconds)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot the average memory usage graph
plt.figure(figsize=(12, 6))
for dtype in dataset_types:
    plt.plot(input_sizes, memory_usages[dtype], marker='x', label=dtype)
plt.title("Average Memory Usage vs Input Size (quickSort)")
plt.xlabel("Input Size")
plt.ylabel("Memory Usage (MiB)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
