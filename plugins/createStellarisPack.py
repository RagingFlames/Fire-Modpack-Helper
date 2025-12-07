import datetime
import os
import sqlite3
import util

def main(defaults):
    # Connect to the SQLite database file (create a new file if it doesn't exist)
    formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    destination = os.path.join(os.getcwd(),formatted_datetime + "_Mod-Pack-Output")
    db_file_path = os.path.join(os.path.expanduser("~"), "Documents", "Paradox Interactive", "Stellaris", "launcher-v2.sqlite")
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
        os.mkdir(destination)
        print(f"Directory '{destination}' created successfully.")
    except FileExistsError:
        print(f"Directory '{destination}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Find the workshop mods
    workshopPath = defaults["stellaris"]
    if not workshopPath.rsplit("\\", 1)[-1] == "281990": # A really stupid simple check for the right path
        print("It looks like yu didn't paste the correct folder, the path should end at the '281990' folder")
    else: 
        while True:
            workshopPath = input("Copy paste the path to your stellaris workshop folder\n")
            if not workshopPath.rsplit("\\", 1)[-1] == "281990": # A really stupid simple check for the right path
                print("It looks like yu didn't paste the correct folder, the path should end at the '281990' folder")
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
    util.make_mod_file(modPackName, modPackVersion, os.path.dirname(destination))
    util.make_descriptor_file(modPackName, modPackVersion, destination)
    util.add_repo_mods(os.path.dirname(destination), modPackVersion)


def help():
    print ("Dummy help file")
