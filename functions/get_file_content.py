import os
from config import CHAR_LIMIT

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abspath = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath, file_path))


        valid_target_file = os.path.commonpath([abspath, target_file]) == abspath
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:

            with open(target_file, "r") as f:
                file_content = f.read(CHAR_LIMIT)
                if f.read(1):
                    file_content += f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
            return file_content
    except Exception as e:
        return f"Error: {e}" 