import datetime
import os
import sys
import sqlite3
from libs import paradox
import util

def main(defaults):
    # Connect to the SQLite database file (create a new file if it doesn't exist)
    formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    destination = os.path.join(os.getcwd(),formatted_datetime + "_Mod-Pack-Output")
    if sys.platform.startswith("win"):
        db_file_path = os.path.expanduser(
            "~/Documents/Paradox Interactive/Stellaris/launcher-v2.sqlite"
        )
        stellaris_workshop = os.path.expanduser(
            "C:/Program Files (x86)/Steam/steamapps/workshop/content/281990"
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
    connection = sqlite3.connect(db_file_path)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    # Get everything in the playset table
    cursor.execute("SELECT * FROM playsets")
    rows = cursor.fetchall()

    print("Found the following playsets, which playset will we use?")
    # Print the rows found
    for i in range(len(rows)):
        print("\033[1m" + str(i) + "\033[0m" + " : " + rows[i][1])
    selection = input()
    playset = rows[int(selection)][0]
    print("Using playset with ID: " + playset)

    # Get all relevant mods
    cursor.execute("SELECT * FROM playsets_mods")
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

    # Print sorted mod list
    print("The following mods will be used in this order for the modpack")
    for mod in modWorkshopIDList:
        print(mod[5])
    input("Press 'Enter' to continue")

    # Make the mod folder
    modPackName = input("What is the name for this new modpack?\n")
    modPackVersion = input("What is the version for this new modpack? (IE 3.10.1)\n")
    destination = os.path.join(destination, modPackName)
    try:
        os.makedirs(destination, exist_ok=True)
        print(f"Directory '{destination}' created successfully.")
    except FileExistsError:
        print(f"Directory '{destination}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Find the workshop mods
    workshopPath = defaults["stellaris"]
    if not os.path.basename(os.path.normpath(workshopPath)) == "281990" or not os.path.isdir(workshopPath): # A really stupid simple check for the right path
        print("It looks like we aren't looking at the correct workshop folder. Please copy and paste your workshop path.")
        while True:
            workshopPath = input("Copy paste the path to your stellaris workshop folder\n")
            if not os.path.basename(os.path.normpath(workshopPath)) == "281990": # A really stupid simple check for the right path
                print("It looks like you didn't paste the correct folder, the path should end at the '281990' folder")
            else:
                break

    # workshopPath = convert_path(workshopPath)
    # Start copying the files
    for mod in modWorkshopIDList:
        workshopModFolder = os.path.join(workshopPath, mod[2])
        util.copy_files(workshopModFolder, destination)

    # Close the cursor
    cursor.close()
    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    # Make the description files
    paradox.make_mod_file(modPackName, modPackVersion, os.path.dirname(destination))
    paradox.make_descriptor_file(modPackName, modPackVersion, destination)
    # Add additional mods
    repo_keys, repo_destinations = util.add_repo_mods(os.path.dirname(destination), modPackVersion)
    while i < len(repo_keys):
        paradox.make_mod_file(repo_keys[i], modPackVersion, destination)

def help():
    print ("Dummy help file")
