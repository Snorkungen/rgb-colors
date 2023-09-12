from os import path, mkdir
from typing import Final
import sys
import subprocess

OUT_DIR: Final = "data"


def ensure_file_exists(filename: str, producer_args: list[str]) -> None:
    filepath = path.join(OUT_DIR, filename)

    # first ensure that OUT_DIR Exists
    if not path.exists(OUT_DIR):
        mkdir(OUT_DIR)

    if path.exists(filepath):
        return

    if len(producer_args) < 1:
        raise ValueError("Producer lacks arguments")

    if path.splitext(producer_args[0])[1] == ".py":
        producer_args = [sys.executable] + producer_args

    subprocess.run(" ".join(producer_args), shell=True)

    if not path.exists(filepath):
        raise RuntimeError(f"{filepath}: not found after running producer")
