import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory, ensuring the file path is within the permitted directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the specified file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_working_path = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(absolute_working_path, file_path))
        if not os.path.commonpath([absolute_working_path, full_file_path]) == absolute_working_path:
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory."
        if os.path.isdir(full_file_path):
            return f"Error: Cannot write to \"{file_path}\" as it is a directory."
        else:
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
            with open(full_file_path, 'w') as file:
                file.write(content)
            return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as e:
        return f"Error: {e}"