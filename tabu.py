import shutil

from datetime import datetime
from pathlib import Path


def tabu(fullFilename, archive_folder=None):
    """
    Timestamp And Back Up of file or folder
    Adds Byymmdd_hhmmp string between the filename and extension(s) and
      saves it
    If archive_folder is given, backup is stored in that folder
    fullFilename could either be a Path object or a string
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
                # raise Exception(f"{arch_folder_path.absolute()} does not exist")
            ffn = filePath / archive_folder / new_fn
        shutil.copy2(fullFilename, ffn)
        return ffn
    except Exception as e:
        raise e
