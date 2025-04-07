import random, os
from datasets import load_dataset

count = 0
i = 1
files_per_batch = 100
print("Loading dataset from HF, might take a while to download")
dataset = load_dataset("angie-chen55/javascript-github-code", split="train", streaming=True)
print("Loaded dataset, now randomly saving files from set to disk")

for each_point in dataset:
    rnd = random.random()
    if rnd < 0.2:
        continue

    batch_index = (i - 1) // files_per_batch + 1
    folder_name = f"data_cache/batch_{batch_index:05d}"
    os.makedirs(folder_name, exist_ok=True)
    code = each_point.get("code", None)
    if code:
        js_filename = f"{folder_name}/sample_{i:05d}.js"
        js_file = open(js_filename, "w", encoding="utf-8")
        js_file.write(code)
        i += 1
        print(f"Saved {i} files", end="\r")

    if i > 2e6:
        break

    