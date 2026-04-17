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
    diff = DeepDiff(json1, json2)
    return diff
