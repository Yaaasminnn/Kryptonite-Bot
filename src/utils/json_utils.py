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

def pretty_print(data:dict):
    print(json.dumps(data, indent=4, sort_keys=False))

def create_json(file_path):
    """
    Creates a json file.
    """
    with open(file_path, "w") as file:
        a={}
        json.dump(a, file)

def del_dict_key(dict:dict, key, index:int=None):
    """
    Deletes an item from a dict and returns the mutated dict.

    Used when mutating a dict but the user wants to keep the original version. This makes a copy of the dict, mutates
    and returns the copy.

    Takes in the dict, the key to delete and optionally the key's index if it is a list. if it is a list and the index
    is not None, we only delete the index in said key's list. otherwise, if no index is given, we only delete the key.
    """
    if index is None:
        del dict[key]
    else:
        del dict[key][index]
    return dict

def del_dict_keys(dict:dict, keys:list):
    for key in keys:
        del dict[key]
    return dict