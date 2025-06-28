import json
import os
import shutil
from util import yes_or_no, convert_path
import createStellarisPack
import util

DEFAULTS_PATH = os.path.join(os.path.curdir,"defaults.json")

def read_config_file(): 
    # Check if the file exists
    try:
        if os.path.exists(DEFAULTS_PATH):
            with open(DEFAULTS_PATH, "r") as file:
                try:
                    defaults = json.load(file)
                except json.JSONDecodeError:
                    print("Error decoding JSON")
        else:
            print(f"Config file not found.")
    except Exception as e:
        print("An error occurred:", str(e))
    return defaults

def is_admin():
    try:
        return os.getuid() == 0
    except:
        return False

def sort_mods(e):
    return e[3]

def main_help():
    print("0: Create modpack")
    print("A guided process for creating modpacks for a variety of games")
    print("9: Help")
    print("This is help")

def create_modpack_help():
    print("Stellaris:")
    print("A guided process to create a new modpack using an existing playset from the stellaris launcher. Make sure the mods in the playlist are already in "+
          "the proper mod load order.")

def createModpack(defaults):
    print("Which game is this modpack for?")
    selection = input("0: Stellaris\n")
    while True:
        match selection:
            case "0": #Stellaris
                createStellarisPack.create_modpack(defaults)
                break
            case _:
                print("Please retype answer")
                break

if __name__ == '__main__':
    # Load any default data
    defaults = read_config_file()

    print("Please type the number for what you would like to do:")
    print("0: Create modpack")
    selection = input("9: help\n")
    while True:

        match selection:
            case "0":
                createModpack(defaults)
                break
            case "9":
                main_help()
                break
            case _:
                print("Please retype answer")

