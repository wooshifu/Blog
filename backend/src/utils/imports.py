from pathlib import Path


def import_all_file_under_current_dir(file: str,
                                      from_=None, import_=None, as_=None,
                                      suffixes_=('.py',), ignore_files_=('__init__.py',)) -> None:
    """
    used for import all file under a package

    :param from_: from where
    :param file: usually it's a package __init__ file
    :param import_: import what
    :param as_: as what
    :param suffixes_: file suffix
    :param ignore_files_: ignore files
    :return: None
    """
    current_dir = Path(file).parent

    for file in current_dir.iterdir():
        if file.is_file() and file.suffix in suffixes_ and file.name not in ignore_files_:
            exec(f'from {from_ or current_dir.name} import {import_ or file.stem} {"as " + as_ if as_ else ""}')
