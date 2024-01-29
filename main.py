import os
import shutil
import sqlite3


def is_admin():
    try:
        return os.getuid() == 0
    except:
        return False


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


def main_help():
    print("0: Rename mod folders")
    print(
        "You can use this to rename the stellaris workshop folder sto something human readable. First copy everything in your stellaris workshop folder to a" +
        "temporary directory. Then run the script from that directory, or point the script at that directory. This will make a copy of all your stellaris mod" +
        " folders with relevant names. For example '1121692237' would be renamed to 'Gigastructural Engineering & More '")
    print("1: Create modpack")
    print("A guided process to create a new modpack using an existing playset from the stellaris launcher. Make sure the mods in the playlist are already in "+
          "the proper mod load order.")
    print("9: Help")
    print("This is help")


def rename_folders():
    current_directory = os.getcwd()
    print("Would you like to use the current directory: (y/n)")
    print(current_directory)
    if yes_or_no():
        directory = current_directory
    else:
        directory = convert_path(input("Please enter or paste the path you want to use"))
        print("Using")
        print(directory)

    # rename and copy
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)

        if os.path.isdir(folder_path):
            descriptor_file_path = os.path.join(folder_path, "descriptor.mod")

            if os.path.exists(descriptor_file_path):
                try:
                    with open(descriptor_file_path, 'r') as descriptor_file:
                        for line in descriptor_file:
                            if line.startswith("name="):
                                new_name = line.split("=")[1].strip().strip('"')
                                new_folder_path = os.path.join(directory, new_name)

                                # Create a new folder and copy everything preserving structure
                                shutil.copytree(folder_path, new_folder_path)

                                print(f'Created folder: {new_folder_path}')
                                break
                except Exception as e:
                    print(f"Error processing folder {folder_path}: {e}")
    input("Press enter to continue")

def sort_mods(e):
    return e[3]


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

def create_modpack():
    # Connect to the SQLite database file (create a new file if it doesn't exist)
    destination = os.getcwd()
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

    # Get all relavent mods
    cursor.execute("SELECT * FROM playsets_mods")
    rows = cursor.fetchall()
    modIDList = []
    for row in rows:
        if(row[0] == playset):
            modIDList.append(row)
    # Sort the list by load order
    modIDList = sorted(modIDList, key=lambda x:x[3])

    cursor.execute("SELECT * FROM mods")
    rows = cursor.fetchall()
    modWorkshopIDList = []
    for mod in modIDList: # For every mod in the list
        for row in rows: # For every row in the mods table
            if row[0] == mod[1]:
                modWorkshopIDList.append(row)

    # Print sorted mod list
    print("The following mods will be used in this order for the modpack")
    for mod in modWorkshopIDList:
        print(mod[5])
    input("Press 'Enter' to continue")



    # Make the mod folder
    modPackName = input("What is the name for this new modpack?")
    destination = os.path.join(destination, modPackName)
    try:
        os.mkdir(destination)
        print(f"Directory '{destination}' created successfully.")
    except FileExistsError:
        print(f"Directory '{destination}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


    # Find the workshop mods
    workshopPath = ""
    while True:
        workshopPath = input("Copy paste the path to your stellaris workshop folder")
        if not workshopPath.rsplit("\\", 1)[-1] == "281990":
            print("It looks like yu didn't paste the correct folder, the path should end at the '281990' folder")
        else:
            break

    #workshopPath = convert_path(workshopPath)
    workshopMods = [f for f in os.listdir(workshopPath) if os.path.isdir(os.path.join(workshopPath, f))] #List of every folder in the workshop path
    # Start copying the files
    for mod in modWorkshopIDList:
        workshopModFolder = os.path.join(workshopPath, mod[2])
        copy_files(workshopModFolder, destination)




    # Close the cursor
    cursor.close()
    # Commit the changes and close the connection
    connection.commit()
    connection.close()


if __name__ == '__main__':

    print("This is a multi tool script, Please type the number for what you would like to do:")
    print("0: Rename mod folders")
    print("1: Create modpack")
    selection = input("9: help")
    while True:

        match selection:
            case "0":
                rename_folders()
                break
            case "1":
                create_modpack()
                break
            case "9":
                main_help()
                break
            case _:
                print("Please retype answer")
