import os
import random
import numpy as np

DATA_DIR = "D:/ass1/dataset"

def generate_input_sizes(count=20, min_size=1000, max_size=1000000):
    sizes = random.sample(range(min_size + 1, max_size - 1), count - 2)
    sizes.extend([min_size, max_size])
    return sorted(sizes)

def generate_and_save_datasets(input_sizes):
    os.makedirs(DATA_DIR, exist_ok=True)

    for size in input_sizes:
        base = list(range(size))
        datasets = {
            "sorted_asc": base,
            "sorted_desc": base[::-1],
            "random": random.sample(base, len(base)),
            "reversed_sorted": base[::-1],
            "partially_sorted": base[:size // 2] + random.sample(base[size // 2:], size - size // 2),
        }

        for dtype, data in datasets.items():
            filename = f"{DATA_DIR}/{dtype}_{size:07d}.npy"
            np.save(filename, np.array(data))
            print(f"Saved: {filename}")

if __name__ == "__main__":
    input_sizes = generate_input_sizes()
    print("Input sizes:", input_sizes)
    generate_and_save_datasets(input_sizes)
