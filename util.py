import os
import shutil
from git import Repo
import json

GIT_REPOS_PATH = os.path.join(os.path.curdir,"repo-mods.json")

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

def add_repo_mods(destination, modPackVersion):
    # Load repo data
    try:
        if os.path.exists(GIT_REPOS_PATH):
            with open(GIT_REPOS_PATH, "r") as file:
                try:
                    repos = json.load(file)
                except json.JSONDecodeError:
                    print("Error decoding JSON")
        else:
            print(f"Config file not found.")
            return
    except Exception as e:
        print("An error occurred:", str(e))
        return

   
    repo_keys = list(repos.keys())
    selected = set()
    message = "If you want additional git repo based mods to be added, add them now."
    while True:
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # Print options
        print(message)
        print("Select a repo (enter number). Type 0 to finish.\n")
        message = ""
        for i, key in enumerate(repo_keys, start=1):
            prefix = "+" if i in selected else " "
            print(f"{prefix} {i}: {key}")

        selection = input("\nEnter number: ").strip()
        # Selection logic
        if selection == "0":
            break

        if selection.isdigit():
            selection = int(selection)
            if 1 <= selection <= len(repo_keys):
                if selection in selected:
                    selected.remove(selection)
                else:
                    selected.add(selection)
            else:
                message = "Invalid number."
        else:
            message = "Invalid input."

    # Clone the repos
    for i in sorted(selected):
        repo_destination=os.path.join(destination,repo_keys[i-1])
        Repo.clone_from(repos[repo_keys[i-1]],repo_destination)
        make_mod_file(repo_keys[i-1], modPackVersion, destination)

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
    with open(file_path, "w") as file: # Name the file the same name as the folder plus the .mod extension
        file.write(content)

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

