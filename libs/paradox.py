import os


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