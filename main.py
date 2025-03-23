import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List
from rich.console import Console
from rich.prompt import Prompt
from rich.spinner import Spinner
from InquirerPy import inquirer

APP_NAME = "scriptswift"
CONFIG_FILE = Path.home() / f".{APP_NAME}_config.json"
console = Console()

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def add_script():
    name = Prompt.ask("Enter a shorthand name for your script")
    script_type = inquirer.select(message="Choose script type:", choices=["python", "bash", "node"]).execute()
    path = Prompt.ask("Enter full path to the script")

    if not Path(path).exists():
        console.print("[red]Error:[/] Path does not exist.")
        return

    config = load_config()
    config[name] = {"type": script_type, "path": path}
    save_config(config)
    console.print(f"[green]Added '{name}' successfully![/]")

def remove_script():
    config = load_config()
    if not config:
        console.print("[red]No scripts to remove.[/]")
        return

    name = inquirer.select(message="Select script to remove:", choices=list(config.keys())).execute()
    del config[name]
    save_config(config)
    console.print(f"[green]Removed '{name}' successfully![/]")

def run_script(name):
    config = load_config()
    script = config.get(name)
    if not script:
        console.print(f"[red]No script found with name '{name}'[/]")
        return

    path = script["path"]
    base_cmd = []

    if script["type"] == "python":
        base_cmd = ["python3", path]
    elif script["type"] == "bash":
        base_cmd = ["bash", path]
    elif script["type"] == "node":
        base_cmd = ["node", path]

    # Prompt for optional args
    user_args = Prompt.ask("Enter any arguments (leave blank for none)", default="").strip()
    args = user_args.split() if user_args else []

    full_cmd = base_cmd + args

    with console.status(f"[blue]Running {name}...[/]", spinner="dots"):
        subprocess.run(full_cmd)

def run_picker():
    config = load_config()
    if not config:
        console.print("[red]No apps found. Add one first.[/]")
        return

    name = inquirer.select(message="Your apps:", choices=list(config.keys())).execute()
    run_script(name)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-a", "--app"] and len(sys.argv) > 2:
            run_script(sys.argv[2])
            return

    action = inquirer.select(
        message="What do you want to do?",
        choices=["Run app", "Add app", "Remove app", "Exit"]
    ).execute()

    if action == "Run app":
        run_picker()
    elif action == "Add app":
        add_script()
    elif action == "Remove app":
        remove_script()

if __name__ == "__main__":
    main()
