import json

def jprint(obj):
    """
        readable prints a JSON object.

    """
    print(json.dumps(obj, indent=4, ensure_ascii=False, default=str))

