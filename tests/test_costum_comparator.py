from app.core.costum_comparator import compare_dicts
from app.core.costum_comparator import compare_lists

old_dict = {"name": "Alice", "age": 30, "address": {"city": "Paris", "zip": "75000"}}
new_dict_value_change = {"name": "Alice", "age": 31, "address": {"city": "Paris", "zip": "75000"}}
new_dict_type_change = {"name": "Alice", "age": "30", "address": {"city": "Paris", "zip": "75000"}}
new_dict_key_added = {"name": "Alice", "age": 30, "address": {"city": "Paris", "zip": "75000"}, "email": "alice@example.com"}
new_dict_key_removed = {"name": "Alice", "address": {"city": "Paris", "zip": "75000"}}
new_dict_nested_change = {"name": "Alice", "age": 30, "address": {"city": "Lyon", "zip": "69000"}}  

# Test cases for compare_dicts function
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

# Test cases for compare_lists function
def test_list_value_change():
    old_list = [1, 2, 3]
    new_list = [1, 4, 3]
    changes = compare_lists(old_list, new_list)
    assert "Changed value: [1] from 2 to 4" in changes

def test_list_type_change():
    old_list = [1, 2, 3]
    new_list = [1, 2, "3"]
    changes = compare_lists(old_list, new_list)
    assert "Changed type: [2] from int to str" in changes

def test_list_element_added():
    old_list = [1, 2, 3]
    new_list = [1, 2, 3, 4]
    changes = compare_lists(old_list, new_list)
    assert "Added element: [3] with value 4" in changes

def test_list_element_removed():
    old_list = [1, 2, 3]
    new_list = [1, 2]
    changes = compare_lists(old_list, new_list)
    assert "Removed element: [2] with value 3" in changes

def test_list_nested_change():
    old_list = [1, [2, 3], 4]
    new_list = [1, [2, 4], 4]
    changes = compare_lists(old_list, new_list)
    assert "Changed value: [1][1] from 3 to 4" in changes

def test_list_nested_dicts_change():
    old_list = [1, {"key": "value"}, 3]
    new_list = [1, {"key": "new_value"}, 3]
    changes = compare_lists(old_list, new_list)
    assert "Changed value: [1].key from value to new_value" in changes