import math
from pathlib import Path
from .cprintUtils import dprint, eprint, iprint  # noqa: F401


def RenameFilesInFolder(folder, FileNamePrefix=None):
    """
    Function to rename files in the folder using a prefix and
    running serial number. Folder name itself is used as prefix
    if the second parameter is not provided
    Files in the first level alone are renamed. Files under sub-folders
    (if any) are not renamed
    """
    # dprint("Welcome to RenameFilesInFolder")
    rename_list = []
    try:
        if isinstance(folder, str):
            folder = Path(folder)

        if not folder.is_dir():
            eprint(f"{folder} is not a folder")
            raise Exception(f"{folder} is not a folder")
        else:
            # dprint(f"{folder} is a folder")
            pass

        if FileNamePrefix is not None:
            prefix = FileNamePrefix
        else:
            parent = folder.absolute().parent
            prefix = str(folder.absolute().relative_to(parent))

        for root, dirs, files in folder.walk(top_down=True):
            dirs[:] = []  # don't recurse into sub-folders
            csv_fileName = root / (prefix + ".csv")
            if Path(csv_fileName).is_file():
                raise Exception("Files in this folder are already renamed")

            file_count = len(files)
            noof_digits = math.ceil(math.log(file_count, 10)) + 1

            for i, file in enumerate(files, start=1):
                old_fileName = root / file
                new_fileName = (
                    prefix + "_" + str(i).zfill(noof_digits) + old_fileName.suffix
                )
                new_fullFileName = root / new_fileName
                old_fileName.rename(new_fullFileName)
                rename_list.append((file, new_fileName))
    except Exception as e:
        eprint(str(e))
        raise e
    finally:
        # dprint("Come to finally")
        with open(root / (prefix + ".csv"), "a") as csv_file:
            for file in rename_list:
                csv_file.write(f"{file[0]}, {file[1]}\n")
