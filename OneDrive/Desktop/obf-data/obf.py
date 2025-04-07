import os, subprocess, threading

error_files = []
global_file_counter = 0

def run_single_obfuscation(filepath: str, outpath: str):
    command = f'npx javascript-obfuscator {filepath} --output {outpath}'
    try:
        _ = subprocess.check_output(command, text=True, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        error_files.append(filepath)


def run_batch_obfuscation(start_index: int):
    global global_file_counter
    data_path = 'data_cache'
    all_batches = os.listdir(data_path)
    all_batches.sort()
    split_batch = all_batches[start_index:start_index+100]

    for each_batch in split_batch:
        all_files_in_batch = os.listdir(f"{data_path}/{each_batch}/")
        for each_file in all_files_in_batch:
            run_single_obfuscation(f"{data_path}/{each_batch}/{each_file}", f"{data_path}_obf/{each_batch}/{each_file.replace(".js", ".obf.js")}")
            global_file_counter += 1
            print(f"Obfuscated {global_file_counter} files", end='\r')


if __name__ == "__main__":
    threads = []
    for i in range(0, 2000, 100):
        t1 = threading.Thread(target=run_batch_obfuscation, args=[i])
        threads.append(t1)
    
    for each_thread in threads:
        each_thread.start()

    for each_thread in threads:
        each_thread.join()
