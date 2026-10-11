import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get the file content of a specified file relative to the working directory, with a maximum character limit",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to read the file from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_working_path = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(absolute_working_path, file_path))
        if not os.path.isfile(full_file_path):
            return f"Error: File not found or is not a regular file: \"{full_file_path}\""
        valid_full_file_path = os.path.commonpath([absolute_working_path, full_file_path]) == absolute_working_path
        if not valid_full_file_path:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory."
        else:
            with open(full_file_path, 'r') as file:
                content = file.read(MAX_CHARS)
                if file.read(1):
                    content += f'[... File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"