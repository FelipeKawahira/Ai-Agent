import os
import subprocess
from google.genai import types

# Actual function
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abspath = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath, file_path))

        valid_target_file = os.path.commonpath([abspath, target_file]) == abspath
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_file]
            if args != None:
                command.extend(args)
            completed_process = subprocess.run(command, capture_output=True, timeout=30, text=True)
            
            output_list = []
            if completed_process.returncode != 0:
                output_list.append(f"Process exited with code {completed_process.returncode}")
            if not completed_process.stdout and not completed_process.stderr:
                output_list.append("No output produced")
            if completed_process.stdout:
                output_list.append(f"STDOUT: {completed_process.stdout}")
            if completed_process.stderr:
                output_list.append(f"STDERR: {completed_process.stderr}")
            return "\n".join(output_list)

    except Exception as e:
        return f"Error: executing Python file: {e}"     

# Describe function to LLM
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a .py file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of strings to be added to the command list",
            )
        },
    ),
)