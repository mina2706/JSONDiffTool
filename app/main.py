from core.deepdiff_comparator import compareJson , diff_parser
from app.utils.json_utils import jprint

before = {
    "name": "Alice",
    "age": 30,
    "adresse": {"street": "123 Main St", "zip": "20001"},
    "city": "New York"
}

after = {
    "name": "Alice",
    "age": 30,
    "adresse": {"street": "123 Main St", "zip": "10001"},
    "city": "New York"
}

if __name__ == "__main__":
    parsed_differences = diff_parser(compareJson(before, after))
    jprint(parsed_differences)

# Output:
# diff brut
"""
    {
        'type_changes': 
            {
                "root['age']": 
                {
                    'old_type': <class 'int'>, 
                    'new_type': <class 'str'>, 
                    'old_value': 30, 
                    'new_value': '30'
                }
            }, 
        'values_changed': 
        {
            "root['name']": 
            {
                'new_value': 'Lora', 
                'old_value': 'Alice'
            }
        }
    }

"""
# diff parsé
"""
    [
        {
            "category": "type_changes",
            "path": "root['age']",
            "old_type": "<class 'int'>",
            "new_type": "<class 'str'>"
        },
        {
            "category": "dictionary_item_added",
            "path": "root['adresse']",
            "added": {
                "street": "123 Main St",
                "zip": "10001"
            }
        },
        {
            "category": "values_changed",
            "path": "root['name']",
            "old_value": "Alice",
            "new_value": "Lora"
        },
        {
            "category": "values_changed",
            "path": "root['city']",
            "old_value": "New York",
            "new_value": "los angeles"
        }
    ]

"""