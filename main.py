import os
import shutil


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
    print("0: Rename mod folders")
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


if __name__ == '__main__':

    print("This is a multi tool script, Please type the number for what you would like to do:")
    print("0: Rename mod folders")
    selection = input("9: help")
    while True:

        match selection:
            case "0":
                rename_folders()
                break
            case "9":
                main_help()
                break
            case _:
                print("Please retype answer")
