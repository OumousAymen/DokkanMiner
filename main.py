import os
import shutil
import subprocess
import gc
import traceback

# Paths
quickbms_path = "cpktools/quickbms.exe"
bms_script_path = "cpktools/cpk.bms"
base_directory = "Uncrypted_Files"
output_base = "Decrypted_Files"

counter = 0  # File counter

for root, _, files in os.walk(base_directory):
    for file in files:
        file_path = os.path.join(root, file)
        relative_path = os.path.relpath(root, base_directory)
        target_folder = os.path.join(output_base, relative_path)

        if file.lower().endswith(".cpk"):
            cpk_folder_name = os.path.splitext(file)[0]
            output_folder = os.path.join(target_folder, cpk_folder_name)

            os.makedirs(output_folder, exist_ok=True)

            print(f"Extracting {file} to {output_folder}...")

            try:
                result = subprocess.run([quickbms_path, bms_script_path, file_path, output_folder],
                                        capture_output=True, text=True, check=True, timeout=60)

                if "error" in result.stdout.lower() or "error" in result.stderr.lower():
                    print(f" Warning: QuickBMS may have encountered an issue with {file}")

                print(f" Extraction completed for {file}\n")

            except subprocess.TimeoutExpired:
                print(f"Skipping {file} (extraction took too long)")
            except subprocess.CalledProcessError as e:
                print(f" Error extracting {file}: {e}")
                traceback.print_exc()

        else:  # Move non-CPK files to the corresponding directory
            os.makedirs(target_folder, exist_ok=True)
            new_file_path = os.path.join(target_folder, file)

            try:
                shutil.move(file_path, new_file_path)
            except Exception as e:
                print(f" Error moving {file}: {e}")
                traceback.print_exc()

        counter += 1
        if counter % 10 == 0:
            gc.collect()

print(" Processing complete!")
