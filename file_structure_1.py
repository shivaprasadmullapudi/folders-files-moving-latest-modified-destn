import os
import shutil

def get_latest_files(folder):
    """
    Traverse 'folder' recursively, grouping files by their filename.
    For each filename, store a tuple (relative_path, full_path, modification_time)
    for the file with the latest modification time.
    """
    latest_files = {}
    for dirpath, _, filenames in os.walk(folder):
        # Compute relative directory path
        rel_dir = os.path.relpath(dirpath, folder)
        if rel_dir == ".":
            rel_dir = ""
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            mod_time = os.path.getmtime(full_path)
            # Build relative path (preserving folder structure)
            rel_path = os.path.join(rel_dir, filename) if rel_dir else filename
            
            # If this filename is new or the file is newer than the stored one, update it.
            if filename not in latest_files or mod_time > latest_files[filename][2]:
                latest_files[filename] = (rel_path, full_path, mod_time)
    return latest_files

def merge_latest_files(folder1, folder2, dest_folder):
    """
    Merge files from folder1 and folder2 into dest_folder:
      - For each filename present in either folder, copy only the file with the latest modification time.
      - Preserve the folder structure based on the relative path of the latest file.
    """
    # Get the latest file for each filename from both source folders.
    latest_files_1 = get_latest_files(folder1)
    latest_files_2 = get_latest_files(folder2)
    
    # Merge the two dictionaries (grouping by filename)
    merged_files = {}
    all_filenames = set(latest_files_1.keys()).union(latest_files_2.keys())
    
    for filename in all_filenames:
        file_info1 = latest_files_1.get(filename)
        file_info2 = latest_files_2.get(filename)
        
        if file_info1 and file_info2:
            # If file exists in both, choose the one with the later modification time.
            merged_files[filename] = file_info1 if file_info1[2] >= file_info2[2] else file_info2
        elif file_info1:
            merged_files[filename] = file_info1
        elif file_info2:
            merged_files[filename] = file_info2

    # Copy each selected file to the destination folder, preserving its relative folder structure.
    for filename, (rel_path, full_path, mod_time) in merged_files.items():
        dest_file_path = os.path.join(dest_folder, rel_path)
        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        print(f"Copying '{full_path}' to '{dest_file_path}'")
        shutil.copy2(full_path, dest_file_path)
    
    print("\nMerge complete! Latest files have been copied to:", dest_folder)

if __name__ == "__main__":
    folder1 = input("Enter the path for the first folder: ").strip()
    folder2 = input("Enter the path for the second folder: ").strip()
    dest_folder = input("Enter the destination folder path: ").strip()

    # Validate the source folders.
    if not os.path.isdir(folder1):
        print(f"Error: '{folder1}' is not a valid directory.")
        exit(1)
    if not os.path.isdir(folder2):
        print(f"Error: '{folder2}' is not a valid directory.")
        exit(1)
    
    # Create the destination folder if it doesn't exist.
    os.makedirs(dest_folder, exist_ok=True)
    
    merge_latest_files(folder1, folder2, dest_folder)
