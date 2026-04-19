from deepdiff import DeepDiff

def compareJson(json1, json2):
    """
    Compares two JSON objects and returns the differences.

    Args:
        json1 (dict): The first JSON object.
        json2 (dict): The second JSON object.
    Returns:
        dict: A dictionary containing the differences between the two JSON objects.

    """
    diff = DeepDiff(json1, json2, verbose_level=2)
    return diff

def diff_parser(diff):
    """
        Converts a DeepDiff-style dictionary into a structured list of normalized change records.
        
        The function iterates through change categories (e.g., values_changed, type_changes,
        dictionary_item_added, etc.) and extracts relevant information into a uniform format.

        Each change is transformed into a dictionary containing:
        - the change category
        - the normalized path (via path_parser)
        - the old and new values/types depending on the category
        - added or removed items when applicable

        Example:
            Input:
            {
                "values_changed": {
                    "['name']": {
                        "old_value": "Alice",
                        "new_value": "Lora"
                    }
                }
            }

            Output:
            [
                {
                    "field": "[name]",
                    "type": "values_changed",
                    "old": "Alice",
                    "new": "Lora"
                }
            ]

        Args:
            diff (dict): A dictionary representing differences between two JSON-like objects
                        (typically produced by DeepDiff).

        Returns:
            list: A list of structured dictionaries representing each detected change.
    
    """

    # exemple d'un changement à parser :
    #'type_changes': {"root['age']": {'old_type': <class 'int'>, 'new_type': <class 'str'>, 'old_value': 30, 'new_value': '30'}}
    parsed_changes = []
    # Itérer sur changement dans le diff
    for category in diff.keys():
        # Itérer sur chaque chemin dans la catégorie du changement traité 
        for path in diff[category].keys():
            parsed_diff = {}
            parsed_diff["field"] = path_parser(path) # extraire le chemin, ex: "root['age']"
            parsed_diff["type"] = category # extraire la catégorie du changement, ex: 'type_changes'
            changes = diff[category][path] # extraire les changements, 
            # ex: {'old_type': <class 'int'>, 'new_type': <class 'str'>, 'old_value': 30, 'new_value': '30'} 
            if category == "type_changes":
                parsed_diff["old"] = type_parser(changes.get("old_type"))
                parsed_diff["new"] = type_parser(changes.get("new_type"))
            elif category == "values_changed":
                parsed_diff["old"] = changes.get("old_value")
                parsed_diff["new"] = changes.get("new_value")
            elif category == "dictionary_item_added" or category == "iterable_item_added":
                parsed_diff["old"] = None
                parsed_diff["new"] = changes
            elif category == "dictionary_item_removed" or category == "iterable_item_removed":
                parsed_diff["old"] = changes
                parsed_diff["new"] = None
            # ces catégorie sont les plus courantes, mais il en existe d'autres (ex: iterable_item_added, iterable_item_removed, etc.)
            parsed_changes.append(parsed_diff)
        

    return parsed_changes

def path_parser(path):
    """
        Normalizes a path string by removing the 'root' prefix and quotes,
        and formatting it into a bracket-style representation.

        Example:
            "root['age']" → "[age]"

        Args:
            path (str): Raw path string (e.g. from a diff output).

        Returns:
            str: Normalized bracket-style path.
    """
    return path.replace("root", "").replace("'", "")

def type_parser(type_str):
    """
        Converts a type string representation into a more human-readable format.

        Example:
            "<class 'int'>" → "int"

        Args:
            type_str (str): The string representation of a type (e.g. from a diff output).

        Returns:
            str: A simplified type name.
    """
    type_str = str(type_str)
    return type_str.replace("<class '", "").replace("'>", "")