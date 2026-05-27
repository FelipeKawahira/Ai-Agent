import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abspath, directory))


        valid_target_dir = os.path.commonpath([abspath, target_dir]) == abspath
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            print(f'Success: "{directory}" is within the working directory')

            try:
                items_list = []
                for item in os.listdir(target_dir):
                    item_path = os.path.join(target_dir, item)
                    items_list.append(
                        f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
                    )
                return "\n".join(items_list)
            except Exception as e:
                return f"Error: {e}"

    except Exception as e:
        return f"Error: {e}"