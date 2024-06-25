import json
import os
import typing

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
                "`.sdfmpy.json` is already populated or empty. Overwrite? [Y/n]: "
            )

    with open(".sdfmpy.json", "w") as file:
        if overwrite.lower() != "y" or overwrite.lower != "":
            file.write("[]")
        else:
            print("Keeping file contents. Cannot proceed.")
            exit()

    print("Initialized sdfmpy in directory")


@app.command()
def add(
    file: Annotated[str, typer.Argument(help="The file to add and track with sdfmpy")]
):
    pass


app()
