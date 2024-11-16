import importlib.util
import importlib

def run_command(command_name):
    """
    Dynamically load the command module and run it.
    """
    module_name = f"commands.{command_name}"
    spec = importlib.util.find_spec(module_name)
    
    if spec is None:
        print(f"Command '{command_name}' not found.")
        return

    command_module = importlib.import_module(module_name)
    
    if hasattr(command_module, 'run'):
        command_module.run()
    else:
        print(f"Command '{command_name}' does not have a 'run' function.")
