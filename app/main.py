from core.deepdiff_comparator import compareJson

before = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

after = {
    "name": "Lora",
    "age": "30",
    "city": "New York"
}

if __name__ == "__main__":
    differences = compareJson(before, after)
    print(differences)

# Output:
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