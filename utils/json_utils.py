"""
JSON utilities.

Currently consists of loading and updating json files
"""
import json

def load_json(file_path):
    """
    Loads in a json file.
    """
    with open(file_path, "r") as file:
        return json.load(file)

def update_json(file_path, file_data, operation="w"):
    """
    Update a json file with the given data.

    :file_path: path of the file we want to write to
    :file_data: the data we want to write
    :operation: whether we want to overwrite ot add to the file. can be "w" or "a"

    Examples:
        >>>data = {"example":"data"}
        >>>update_json("example.json", data)
        WRITES to the json

        >>>update_json("example.json", data, operation="a")
        APPENDS to the json

    todo:
        allow for all types of writing operations
    """
    with open(file_path, operation) as file:
        file.write(json.dumps(file_data, indent=4, sort_keys=False))

def create_json(file_path):
    """
    Creates a json file.
    """
    with open(file_path, "w") as file:
        a={}
        json.dump(a, file)
