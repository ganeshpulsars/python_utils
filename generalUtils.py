import sys
import traceback

from pathlib import Path


class FolderNotFoundError(FileNotFoundError):
    pass


def render_exception(e, html=False):
    strOut = "Error : \n"
    for arg in e.args:
        strOut += str(arg) + "\n"
    strOut += traceback.format_exc()
    if html:
        strOut = strOut.replace("\n", "<br>").replace('"', "")
    return strOut


def is_content_html(obj: [str, object]) -> bool:
    """
    Function to test the response for content-type html
    """
    if type(obj) == str:
        return obj.startswith("<!DOCTYPE html>")
    else:
        try:
            return "html" in obj.headers.get("content-type", "")
        except Exception:
            raise TypeError(f"Invalid type {type(obj)}")
def get_folder_name_from_argv(index=None):
    """
    Helper function for receiving folder name as a command line argument.
    TODO: MG: 1. create if it does not exist using create=True arguement
              2. Ask user if input=True or inputPrompt="Please enter the folder name to process: "
    """
    index = 1 if index is None else index
    if len(sys.argv) > index:
        folder_name = sys.argv[index]
    else:
        raise Exception(f"Please specify the foldername as {index} arguement")

    folder = Path(folder_name)
    if not folder.exists():
        raise FolderNotFoundError(f"{folder_name} does not exist")
    elif not folder.is_dir():
        raise Exception(f"{folder_name} is not a folder")

    return folder

