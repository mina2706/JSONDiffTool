from app.core.comparator import compare_dicts

old_dict = {"name": "Alice", "age": 30, "address": {"city": "Paris", "zip": "75000"}}
new_dict_value_change = {"name": "Alice", "age": 31, "address": {"city": "Paris", "zip": "75000"}}
new_dict_type_change = {"name": "Alice", "age": "30", "address": {"city": "Paris", "zip": "75000"}}
new_dict_key_added = {"name": "Alice", "age": 30, "address": {"city": "Paris", "zip": "75000"}, "email": "alice@example.com"}
new_dict_key_removed = {"name": "Alice", "address": {"city": "Paris", "zip": "75000"}}
new_dict_nested_change = {"name": "Alice", "age": 30, "address": {"city": "Lyon", "zip": "69000"}}  

def test_value_change():
    changes = compare_dicts(old_dict, new_dict_value_change)
    assert "Changed value: age from 30 to 31" in changes


def test_type_change():
    changes = compare_dicts(old_dict, new_dict_type_change)
    assert "Changed type: age from int to str" in changes


def test_key_added():
    changes = compare_dicts(old_dict, new_dict_key_added)
    assert "Added key: email" in changes


def test_key_removed():
    changes = compare_dicts(old_dict, new_dict_key_removed)
    assert "Removed key: age" in changes


def test_nested_change():
    changes = compare_dicts(old_dict, new_dict_nested_change)
    assert "Changed value: address.city from Paris to Lyon" in changes