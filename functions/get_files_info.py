import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(absolute_working_path, directory))
        if not os.path.isdir(full_path):
            return f"Error: '{full_path}' is not a directory"
        valid_full_path = os.path.commonpath([absolute_working_path, full_path]) == absolute_working_path
        if not valid_full_path:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory."
        else: 
            files = os.listdir(full_path)
            if not files:
                return f"Info: \"{directory}\" is empty."
            else:
                files_info = []
                for file in files:
                    file_path = os.path.join(full_path, file)
                    size = os.path.getsize(file_path)
                    files_info.append(f"- {file}: file_size={size} bytes, is_dir={os.path.isdir(file_path)}")
                return "\n".join(files_info)
    except Exception as e:
        return f"Error: {e}"