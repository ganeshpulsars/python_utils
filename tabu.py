import shutil
import os

from datetime import datetime
from pathlib import Path

from .generalUtils import get_file_hash


def tabu(fullFilename: str | os.PathLike, archive_folder: str = None, skip_if_already_backedup: bool = True) -> os.PathLike:
    """
    Timestamp And Back Up of file or folder
    Copies the file, adds Byymmdd_hhmmp string between the filename and extension(s) and
      saves it

    fullFilename : str or Path object
        The path to the file or folder that needs to be backed-up.
    archive_folder : str, optional
        The path to the folder where the newly created file should be archived.
        If not provided, file is archived in the current folder
        If folder does not already exist, a sub-folder in the current folder will be created.
    """
    try:
        if isinstance(fullFilename, str):
            fullFilename = Path(fullFilename)
        filePath = fullFilename.parent.absolute()
        suffixes = fullFilename.suffixes

        if skip_if_already_backedup:
            b_list = backups_list(fullFilename, archive_folder)
            if len(b_list) != 0:
                source_hash = get_file_hash(fullFilename)
                last_backup_hash = get_file_hash(b_list[0])
                if source_hash == last_backup_hash:
                    return b_list[0]

        fn = fullFilename.stem
        now = datetime.now()
        timeStamp = now.strftime("%y%m%d_%H%M")
        new_fn = f"{fn}_B{timeStamp}p" + "".join(suffixes)
        if archive_folder is None:
            ffn = filePath / new_fn
        else:
            arch_folder_path = filePath / archive_folder
            if not arch_folder_path.is_dir():
                Path(arch_folder_path).mkdir(exist_ok=True)
            ffn = filePath / archive_folder / new_fn
        shutil.copy2(fullFilename, ffn)
        return ffn
    except Exception as e:
        raise e


def backups_list(fullFilename: str | os.PathLike, archive_folder: str = None) -> list:
    """
    Returns a list of backup files available in the location for the given file
    """
    try:
        if isinstance(fullFilename, str):
            fullFilename = Path(fullFilename)
        filePath = fullFilename.parent.absolute()
        fileName_wo_ext = fullFilename.stem

        if archive_folder is None:
            arch_folder_path = filePath
        else:
            arch_folder_path = filePath / archive_folder

        if not arch_folder_path.is_dir():
            return []

        # files = [f for f in arch_folder_path.iterdir() if f.is_file()]
        # return files

        files = []
        for file in arch_folder_path.iterdir():
            if not file.is_file():
                continue
            if file.stem == fileName_wo_ext:
                continue
            if not file.stem.startswith(fileName_wo_ext):  # TODO: MG: Change this to re match
                continue
            files.append(file)

        files.sort(key=lambda f: f.stem, reverse=True)
        return files

    except Exception as e:
        raise e


def is_valid_backup_available(fullFilename: str | os.PathLike, archive_folder: str = None) -> bool:
    """
    Checks if a valid backup is already available by comparing the file hashes of the original file
    and the last backup file
    """
    b_list = backups_list(fullFilename, archive_folder)
    if len(b_list) == 0:
        return False
    if isinstance(fullFilename, str):
        fullFilename = Path(fullFilename)
    source_hash = get_file_hash(fullFilename)
    last_backup_hash = get_file_hash(b_list[0])
    return source_hash == last_backup_hash
