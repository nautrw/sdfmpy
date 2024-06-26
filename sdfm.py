import json
import os
import shutil
import typing
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

    if not os.path.exists(path):
        exit("Invalid path. Cannot proceed.")

    with open(".sdfmpy.json", "r") as file:
        data = json.load(file)
        data.append(path)

    with open(".sdfmpy.json", "w") as file:
        json.dump(data, file, indent=2)

    path_obj = Path(path)
    target_dir = Path.cwd() / path_obj.name

    if path_obj.is_dir():
        shutil.copytree(path, target_dir)
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, target_dir)

    print(f"Added {path} to sdfmpy and cloned it to {target_dir}")


app()
