def sanitize(file_name: str):
    if file_name[0].isnumeric():
        file_name = '_$' + file_name
    file_name = file_name.replace(' ', '_0')
    return file_name
