import math
from pathlib import Path
from .cprintUtils import dprint, eprint, iprint  # noqa: F401
from .generalUtils import render_exception


def RenameFilesInFolder(
    folder: str,
    FileNamePrefix: str = None,
    start_index: int = None,
    noof_digits: int = None,
) -> int:
    """
    Function to rename files in the folder using a prefix and
    running serial number.
    Files in the first level alone are renamed. Files under sub-folders
    (if any) are not renamed.
    Old filename and new filename are looged into a csv file with prefix as the name.
    Returns no of files renamed
    Args:
        folder (str): The path to the folder containing the files to be renamed.
        FileNamePrefix (str, optional): The prefix to be added to the new file names.
            Folder name itself is used as prefix if this is not provided.
        start_index (int, optional): The starting index for numbering the files.
            Starts at 1 if this is not provided.
            Starts from the next number, if files with same prefix are already there in the folder.
        noof_digits (int, optional): The number of digits (leading zeros) to use for the numbering.
            Guessed from the number of files if this is not provided.
    """
    rename_list = []
    try:
        if isinstance(folder, str):
            folder = Path(folder)

        if not folder.is_dir():
            eprint(f"{folder} is not a folder")
            raise Exception(f"{folder} is not a folder")
        else:
            pass

        if FileNamePrefix is not None:
            prefix = FileNamePrefix
        else:
            parent = folder.absolute().parent
            prefix = str(folder.absolute().relative_to(parent))

        for root, dirs, files in folder.walk(top_down=True):
            dirs[:] = []  # don't recurse into sub-folders
            csv_fileName = root / (prefix + ".csv")

            file_count = len(files)
            required_digits = math.ceil(math.log(file_count, 10)) + 1

            noof_digits = required_digits if noof_digits is None else noof_digits
            renamed_count = 0
            i = (
                start_index
                if start_index is not None
                else _findLastIndex(folder, prefix) + 1
            )
            for file in files:
                old_fileName = root / file
                if old_fileName.stem.startswith(prefix + "_"):
                    continue
                if old_fileName.stem == csv_fileName.stem:
                    continue
                new_fileName = (
                    prefix + "_" + str(i).zfill(noof_digits) + old_fileName.suffix
                )
                new_fullFileName = root / new_fileName
                old_fileName.rename(new_fullFileName)
                rename_list.append((file, new_fileName))
                i += 1
                renamed_count += 1

            return renamed_count
    except Exception as e:
        eprint(render_exception(e))
        raise e
    finally:
        with open(csv_fileName, "a") as csv_file:
            for file in rename_list:
                csv_file.write(f"{file[0]}, {file[1]}\n")


def _findLastIndex(folder, prefix):
    try:
        # folder and prefix are not validated since this function will be called
        #  from the main function after all the validations
        for root, dirs, files in folder.walk(top_down=True):
            dirs[:] = []  # don't recurse into sub-folders
            files.sort()
            for file in reversed(files):
                fileName = (root / file).stem
                if fileName.startswith(prefix + "_"):
                    break
            else:
                return 0  # no files starting with prefix found
            # the last renamed filename found
            index = fileName.replace(prefix + "_", "")
            return int(index)
    except Exception as e:
        raise e
