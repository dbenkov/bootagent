import subprocess
import os

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file relative to the working directory, with optional command-line arguments, ensuring the file path is within the permitted directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to the Python file to execute, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file",
                },
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        absolute_working_path = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(absolute_working_path, file_path))
        if not os.path.commonpath([absolute_working_path, full_file_path]) == absolute_working_path:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory."
        if not os.path.isfile(full_file_path):
            return f"Error: \"{file_path}\" does not exist or is not a regular file."
        if not full_file_path.endswith('.py'):
            return f"Error: \"{file_path}\" is not a Python file."
        command = ["python", full_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command, 
            cwd=absolute_working_path,
            capture_output=True, 
            text=True,
            timeout=30,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"