import os
import sys


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

def get_game_paths(game, steamid):
    if sys.platform.startswith("win"):
        db_file_path = os.path.expanduser(
            "~/Documents/Paradox Interactive/" + str(game) + "/launcher-v2.sqlite"
        )
        stellaris_workshop = os.path.expanduser(
            "C:/Program Files (x86)/Steam/steamapps/workshop/content/" + str(steamid)
        )  
    elif sys.platform.startswith("linux"):
        db_file_path = os.path.expanduser(
            "~/.local/share/Paradox Interactive/Stellaris/launcher-v2.sqlite"
        )
        stellaris_workshop = os.path.expanduser(
            "~/.steam/steam/steamapps/workshop/content/281990"
        ) 
    else:
        sys.exit(f"Unsupported operating system: {sys.platform}")
    return db_file_path, stellaris_workshop

def get_playsets():
    return

def get_mods(cursor):
    rows = cursor.fetchall()
    modIDList = []
    for row in rows:
        if (row[0] == playset):
            modIDList.append(row)
    # Sort the list by load order
    modIDList = sorted(modIDList, key=lambda x: x[3])

    cursor.execute("SELECT * FROM mods")
    rows = cursor.fetchall()
    modWorkshopIDList = []
    for mod in modIDList:  # For every mod in the list
        for row in rows:  # For every row in the mods table
            if row[0] == mod[1]:
                modWorkshopIDList.append(row)
    return modWorkshopIDList