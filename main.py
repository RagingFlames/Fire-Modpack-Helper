import json
import os
import shutil
import util
import importlib.util

DEFAULTS_PATH = os.path.join(os.path.curdir,"defaults.json")
PLUGIN_PATH = "./plugins"
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

def load_modules(directory):
    modules = {}

    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = filename[:-3]  # strip .py
            file_path = os.path.join(directory, filename)

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Require that the module has a main() function
            if hasattr(module, "main") and callable(module.main):
                modules[module_name] = module
            else:
                print(f"Warning: {filename} has no main() function. Skipping.")

    return modules

def run_module_functions(modules, func_name):

    for name, module in modules.items():
        func = getattr(module, func_name, None)

        if callable(func):
            try:
                func()
            except Exception as e:
                print(f"   ERROR running {func_name}(): {e}")
        else:
            print(f" → {name}: no {func_name}() function found.")

def help(modules):
    print("0: help")
    run_module_functions(modules, "help")

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
    modules = load_modules(PLUGIN_PATH)


    if not modules:
        print("No valid modules found in portable-libs/")

    print("\nAvailable programs:")
    print("  0. help")
    for i, name in enumerate(modules.keys(), start=1):
        print(f"  {i}. {name}")

    choice = input("\nSelect a program to run (number): ")
    if choice == "0":
        help(modules)
    else:
        try:
            index = int(choice) - 1
            module_name = list(modules.keys())[index]
            modules[module_name].main()

        except (ValueError, IndexError):
            print("Invalid choice.")
    

