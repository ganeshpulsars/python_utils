import shutil
import os

from datetime import datetime
from pathlib import Path


def tabu(fullFilename: str | os.PathLike, archive_folder: str = None) -> bool:
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
