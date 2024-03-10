import os
import sys
import time
import shutil


def sync_folders(source_folder, replica_folder, log_file):
    # Ensure source folder exists
    if not os.path.exists(source_folder):
        print(f'Source folder {source_folder} does not exist.')
        return

    # Ensure replica folder exists, create if not
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # Iterate through all files and subdirectories in the source folder
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.join(root.replace(source_folder, replica_folder, 1), file)

            # Copy the file from source to replica
            shutil.copy2(source_file_path, replica_file_path)
            print(f'Copied {source_file_path} to {replica_file_path}.')
            log_file.write(f'Copied {source_file_path} to {replica_file_path}.\n')

        for subdir in dirs:
            replica_dir_path = os.path.join(root.replace(source_folder, replica_folder, 1), subdir)

            # Ensure directory exists in replica
            if not os.path.exists(replica_dir_path):
                os.makedirs(replica_dir_path)
                print(f'Created directory {replica_dir_path}.')
                log_file.write(f'Created directory {replica_dir_path}.\n')

    # Remove any files or directories in replica that do not exist in source
    for root, dirs, files in os.walk(replica_folder):
        for file in files:
            replica_file_path = os.path.join(root, file)
            source_file_path = os.path.join(root.replace(replica_folder, source_folder, 1), file)

            if not os.path.exists(source_file_path):
                os.remove(replica_file_path)
                print(f'Removed {replica_file_path}.')
                log_file.write(f'Removed {replica_file_path}.\n')

        for subdir in dirs:
            replica_dir_path = os.path.join(root, subdir)
            source_dir_path = os.path.join(root.replace(replica_folder, source_folder, 1), subdir)

            if not os.path.exists(source_dir_path):
                shutil.rmtree(replica_dir_path)
                print(f'Removed directory {replica_dir_path}.')
                log_file.write(f'Removed directory {replica_dir_path}.\n')

        log_file.flush()


if __name__ == "__main__":
    # Check if all command line arguments are provided
    if len(sys.argv) != 4:
        print('Usage: python sync_folders.py <source_folder> <replica_folder> <log_file>')
        sys.exit(1)

    source_folder_arg = sys.argv[1]
    replica_folder_arg = sys.argv[2]
    log_file_path_arg = sys.argv[3]

    # Open log file for writing
    with open(log_file_path_arg, 'a') as log_file:
        while True:
            sync_folders(source_folder_arg, replica_folder_arg, log_file)
            print('Synchronization complete !')
            print('Sleeping for 30 seconds !')

            # Synchronize every 30 seconds
            time.sleep(30)
