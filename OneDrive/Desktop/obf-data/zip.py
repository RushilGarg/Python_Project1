import os
import zipfile

def zip_folder_contents(folder_path):
    folder_name = os.path.basename(folder_path)
    zip_filename = f"{folder_name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, folder_path))

def main():
    all_batches = os.listdir("data_cache_obf")
    for each_batch in all_batches:
        with zipfile.ZipFile(f"data_zipped/{each_batch}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(f"data_cache_obf/{each_batch}"):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, arcname=os.path.relpath(file_path, "data_cache_obf"))
                    except:
                        print("something failed, rip bozo")


if __name__ == "__main__":
    main()