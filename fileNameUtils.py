import os

from pathlib import Path
from datetime import datetime
from termcolor import cprint


def timestamp():
    # TODO: MG: Move to an appropriate file
    return datetime.now().strftime("%y%m%d_%H%M%S")


def change_extension(fileName, new_extension):
    """
    input fileName: lib/readme.txt, new_extension: md
    output: lib/readme.md
    """
    path = Path(fileName)
    new_fileName = path.with_suffix("." + new_extension)
    # path.rename(new_file_path)
    return new_fileName


def inject_extension(fileName, extension):
    """
    input fileName: lib/readme.txt, extension: modified
    output: lib/readme.modified.txt
    """
    full_fileName = Path(fileName)
    new_fileName = f"{Path(full_fileName).stem}.{extension}{Path(full_fileName).suffix}"
    return Path(full_fileName.parent / new_fileName)


def add_extension(fileName, extension):
    """
    input fileName: lib/readme.txt, extension: modified
    output: lib/readme.txt.modified
    """
    full_fileName = Path(fileName)
    new_fileName = f"{Path(full_fileName).stem}{Path(full_fileName).suffix}.{extension}"
    return Path(full_fileName.parent / new_fileName)


def append_fileName(fileName, appended_str):
    """
    input fileName: lib/readme.txt, appended_str: highlighted
    output: lib/readme_highlighted.txt
    """
    full_fileName = Path(fileName)
    full_fileName_with_app = f"{Path(full_fileName).stem}{appended_str}"
    new_fileName = f"{full_fileName_with_app}{Path(full_fileName).suffix}"
    return Path(full_fileName.parent / new_fileName)


def backup_fileName(fileName):
    """
    input fileName: lib/readme.txt
    output: lib/readme_B240825_1512p.txt
    """
    # full_fileName = Path(fileName)
    # full_fileName_with_ts = f"{Path(full_fileName).stem}_B{timestamp()}p"
    # new_fileName = f"{full_fileName_with_ts}{Path(full_fileName).suffix}"
    # return Path(full_fileName.parent / new_fileName)

    appended_str = f"B{timestamp()}p"
    return append_fileName(fileName, appended_str)


def db_fileName(folder: str | os.PathLike) -> os.PathLike:
    """
    input folder name: manhole_image
    output: manhole_image/manhole_image.db
    """
    try:
        folder = Path(folder)
        # TODO: MG: raise exception if folder is not a directory
        parent = folder.absolute().parent
        prefix = str(folder.absolute().relative_to(parent))
        return folder / (prefix + ".db")
    except Exception as e:
        raise e


def file_names_in_folder(folder: os.PathLike) -> [str]:
    """
    Returns a list of filenames in the folder
    """
    try:
        if not folder.is_dir():
            raise FileNotFoundError(f"{folder} does not exist")
        for root, dirs, files in folder.walk(top_down=True):
            dirs[:] = []  # don't recurse into sub-folders
        return files
    except Exception as e:
        raise e


if __name__ == "__main__":
    test_fileName = "../utils.txt"

    new_path = change_extension(test_fileName, "original")
    cprint(f"change_extension: {new_path}", "green")

    new_path = inject_extension(test_fileName, "original")
    cprint(f"inject_extension: {new_path}", "green")

    new_path = add_extension(test_fileName, "original")
    cprint(f"add_extension: {new_path}", "green")

    backupFileName = backup_fileName(test_fileName)
    cprint(f"{backupFileName=}", "green")

    dbFileName = db_fileName("manhole_image")
    cprint(f"{dbFileName=}", "green")

    for file_name in file_names_in_folder(Path("")):
        cprint(file_name, "yellow")
