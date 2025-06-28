import os
import shutil


def copy_files(src_folder, dest_folder):
    # Walk through the source folder
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            src_path = os.path.join(root, file)

            # Preserve the relative path structure in the destination folder
            relative_path = os.path.relpath(src_path, src_folder)
            dest_path = os.path.join(dest_folder, relative_path)

            # Create the necessary directories in the destination folder
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Copy the file, overwriting if it already exists
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {src_path} to {dest_path}")


def yes_or_no():
    while True:
        user_input = input().lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def convert_path(clipboard_path):
    # Replace backslashes with double backslashes
    formatted_path = clipboard_path.replace("\\", "\\\\")

    # If the path contains a drive letter, add 'r' prefix to make it a raw string
    if ":" in formatted_path:
        formatted_path = "r'" + formatted_path + "'"

    return formatted_path

def make_mod_file(name, version, destination):
    ## The mod file template
    content = f'''name="{name}"
version="{version}"
tags={{
    "Gameplay"
}}
picture="thumbnail.png"
supported_version="{version}"
path="mod/{name}"'''
    ## Writing to disk
    file_path = os.path.join(destination, name+".mod")
    with open(name+".mod", "w") as file: # Name the file the same name as the folder plus the .mod extension
        file.write(content)
    print("Content has been written to mod_info.txt")

def make_descriptor_file(name, version, destination):
    # Define the content string using the provided template
    content = f'''name="{name}"
version="{version}"
tags={{
    "Gameplay"
}}
picture="thumbnail.png"
supported_version="{version}"'''

    # Specify the file path
    file_path = os.path.join(destination, "descriptor.mod")

    # Write content to the specified file path
    with open(file_path, "w") as file:
        file.write(content)

    print(f"Content has been written to {file_path}")

