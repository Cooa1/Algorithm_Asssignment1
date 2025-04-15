# Test Sorting Code

import os
import numpy as np
import time
import psutil
from basicSort import mergeSort, heapSort, bubbleSort, insertionSort, selectionSort, quickSort

# Data path
dataset_folder = './dataset'
result_folder = './result'

# Dataset
dataset_types = ['partially_sorted', 'random', 'reversed_sorted', 'sorted_asc', 'sorted_desc']

'''    'mergeSort': mergeSort,
    'heapSort': heapSort,
    'quickSort': quickSort,
    '''

# Sorting algorithms
sort_functions = {
    'selectionSort': selectionSort,
    'bubbleSort': bubbleSort,
    'insertionSort': insertionSort,
}

# Get memory usage 
process = psutil.Process(os.getpid())

# Iterate through each sorting algorithm
for sort_name, sort_func in sort_functions.items():
    time_results = {dtype: {} for dtype in dataset_types}
    memory_results = {dtype: {} for dtype in dataset_types}

    # Loop dataset
    for filename in os.listdir(dataset_folder):
        if filename.endswith('.npy'):
            dataset_type = None
            for dtype in dataset_types:
                if dtype in filename:
                    dataset_type = dtype
                    break
            if not dataset_type:
                continue

            parts = filename.split('_')
            dataset_count = int(parts[-1].split('.')[0])
            file_path = os.path.join(dataset_folder, filename)
            data = np.load(file_path)

            print(f"@️ Sort: {sort_name} | Dataset: {filename} | Size: {len(data)}")

            elapsed_times = []
            memory_usages = []

            # Run 10 rep
            for repeat in range(1):
                copied_data = data.copy()

                mem_before = process.memory_info().rss
                start_time = time.time()
                sorted_data = sort_func(copied_data)
                end_time = time.time()
                mem_after = process.memory_info().rss

                elapsed = end_time - start_time
                mem_used = max((mem_after - mem_before) / (1024 * 1024), 0)

                elapsed_times.append(elapsed)
                memory_usages.append(mem_used)

                print(f"    Run {repeat+1}/10 - Time: {elapsed:.4f} sec | Memory: {mem_used:.2f} MiB")

            avg_time = sum(elapsed_times) / len(elapsed_times)
            avg_mem = sum(memory_usages) / len(memory_usages)

            time_results[dataset_type][dataset_count] = avg_time
            memory_results[dataset_type][dataset_count] = avg_mem

            print(f" Average Time: {avg_time:.4f} sec | Average Memory: {avg_mem:.2f} MiB\n")

    result_file = os.path.join(result_folder, f'{sort_name}.txt')
    with open(result_file, 'w') as f:
        dataset_counts = sorted(list(time_results[dataset_types[0]].keys()))

        # Average time table
        f.write("=== Average Execution Time (seconds) ===\n")
        f.write('Dataset Type\t')
        for count in dataset_counts:
            f.write(f'{count}\t')
        f.write('\n')

        for dtype in dataset_types:
            f.write(f'{dtype}\t')
            for count in dataset_counts:
                time_taken = time_results[dtype].get(count, 'N/A')
                if isinstance(time_taken, float):
                    f.write(f'{time_taken:.4f}\t')
                else:
                    f.write(f'{time_taken}\t')
            f.write('\n')

        f.write('\n')

        # Average memory table
        f.write("=== Average Memory Usage (MiB) ===\n")
        f.write('Dataset Type\t')
        for count in dataset_counts:
            f.write(f'{count}\t')
        f.write('\n')

        for dtype in dataset_types:
            f.write(f'{dtype}\t')
            for count in dataset_counts:
                mem_used = memory_results[dtype].get(count, 'N/A')
                if isinstance(mem_used, float):
                    f.write(f'{mem_used:.2f}\t')
                else:
                    f.write(f'{mem_used}\t')
            f.write('\n')

    print(f" Results saved to: {result_file}\n")
