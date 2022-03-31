import os


def create_if_not_exist(file_name: str, path: str = None) -> str:
    if path is None:
        path = os.getcwd()

    file_name = f'{path}/{file_name}'

    try:
        open(file_name, 'r').close()
    except IOError:
        open(file_name, 'w').close()

    return file_name
