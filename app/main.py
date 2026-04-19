from core.deepdiff_comparator import compareJson , diff_parser
from utils.json_utils import jprint

before = {
    "name": "Alice",
    "age": "30",
    "adresse": {"street": "123 Main St", "zip": "20001"},
    "city": "New York",
    "job": "Engineer",
    "projects": ["Project A", "Project B"]
}

after = {
    "name": "Alice",
    "age": 30,
    "adresse": {"street": "123 Main St", "zip": "10001"},
    "city": "New York",
    "nationality": "American",
    "projects": ["Project D"]
}

if __name__ == "__main__":
    differences = compareJson(before, after)
    jprint(differences)
    parsed_differences = diff_parser(differences)
    jprint(parsed_differences)

# Output:
# diff brut
"""
    {
        "type_changes": {
            "root['age']": {
                "old_type": "<class 'str'>",
                "new_type": "<class 'int'>",
                "old_value": "30",
                "new_value": 30
            }
        },
        "dictionary_item_added": {
            "root['nationality']": "American"
        },
        "dictionary_item_removed": {
            "root['job']": "Engineer"
        },
        "values_changed": {
            "root['adresse']['zip']": {
                "new_value": "10001",
                "old_value": "20001"
            },
            "root['projects'][0]": {
                "new_value": "Project D",
                "old_value": "Project A"
            }
        },
        "iterable_item_removed": {
            "root['projects'][1]": "Project B"
        }
    }
"""
# diff parsé
"""
    [
        {
            "field": "[age]",
            "type": "type_changes",
            "old": "str",
            "new": "int"
        },
        {
            "field": "[nationality]",
            "type": "dictionary_item_added",
            "old": null,
            "new": "American"
        },
        {
            "field": "[job]",
            "type": "dictionary_item_removed",
            "old": "Engineer",
            "new": null
        },
        {
            "field": "[adresse][zip]",
            "type": "values_changed",
            "old": "20001",
            "new": "10001"
        },
        {
            "field": "[projects][0]",
            "type": "values_changed",
            "old": "Project A",
            "new": "Project D"
        },
        {
            "field": "[projects][1]",
            "type": "iterable_item_removed",
            "old": "Project B",
            "new": null
        }
    ]
"""