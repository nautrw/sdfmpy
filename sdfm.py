import json
import os
import shutil
from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def init():
    """
    Initialize sdfmpy
    """

    if not os.path.isfile(".sdfmpy.json"):
        with open(".sdfmpy.json", "w") as file:
            file.write("[]")

    with open(".sdfmpy.json", "r") as file:
        file_content = file.read()

    if file_content != "[]":
        overwrite = input(
            "`.sdfmpy.json` is either already populated or empty. Overwrite? [Y/n]: "
        )

    with open(".sdfmpy.json", "w") as file:
        if overwrite.lower() != "y" or overwrite.lower != "":
            file.write("[]")
        else:
            exit("Keeping file contents. Cannot proceed.")

    print("Initialized sdfmpy in directory")


@app.command()
def add(path: Annotated[str, typer.Argument(help="The path to add")]):
    """Adds a path to sdfmpy"""

    if not os.path.isfile(".sdfmpy.json"):
        exit("sdfmpy.json file not found. Cannot proceed. Run 'sdfmpy init' first.")

    home_directory = Path.home()
    target_path = Path(path)

    if not target_path.exists():
        exit("Path given does not exist. Cannot proceed.")

    relative_path = target_path.relative_to(home_directory)

    with open(".sdfmpy.json", "r") as file:
        data = json.load(file)

    if str(relative_path) in data:
        exit("Path is already added. Cannot proceed.")

    data.append(str(relative_path))

    with open(".sdfmpy.json", "w") as file:
        json.dump(data, file, indent=2)

    destination_directory = Path.cwd() / relative_path.parent
    destination_directory.mkdir(parents=True, exist_ok=True)

    if target_path.is_dir():
        shutil.copytree(target_path, destination_directory / target_path.name)
    else:
        shutil.copy2(target_path, destination_directory)

    print("Added path to sdfmpy")


app()
