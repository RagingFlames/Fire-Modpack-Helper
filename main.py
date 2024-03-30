import os
import shutil
from util import yes_or_no, convert_path
import createStellarisPack
import createBarotraumaPack
import util


def is_admin():
    try:
        return os.getuid() == 0
    except:
        return False

def sort_mods(e):
    return e[3]

def main_help():
    print("0: Rename mod folders")
    print(
        "You can use this to rename the stellaris workshop folder sto something human readable. First copy everything in your stellaris workshop folder to a" +
        "temporary directory. Then run the script from that directory, or point the script at that directory. This will make a copy of all your stellaris mod" +
        " folders with relevant names. For example '1121692237' would be renamed to 'Gigastructural Engineering & More '")
    print("1: Create modpack")
    print("A guided process for creating modpacks for a variety of games")
    print("9: Help")
    print("This is help")

def create_modpack_help():
    print("Stellaris:")
    print("A guided process to create a new modpack using an existing playset from the stellaris launcher. Make sure the mods in the playlist are already in "+
          "the proper mod load order.")

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



def createModpack():
    print("Which game is this modpack for?")
    print("0: Barotrauma")
    selection = input("9: Stellaris\n")
    while True:

        match selection:
            case "0":
                rename_folders()
                break
            case "1": #Barotrauma
                createBarotraumaPack.create_modpack()
                break
            case "9": #Stellaris
                createStellarisPack.create_modpack()
                break
            case _:
                print("Please retype answer")

if __name__ == '__main__':

    print("This is a multi tool script, Please type the number for what you would like to do:")
    print("0: Rename mod folders")
    print("1: Create modpack")
    selection = input("9: help\n")
    while True:

        match selection:
            case "0":
                rename_folders()
                break
            case "1":
                createModpack()
                break
            case "9":
                main_help()
                break
            case _:
                print("Please retype answer")
