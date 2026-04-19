from app.core.deepdiff_comparator import diff_parser, compareJson, type_parser, path_parser

def test_diff_parser_values_changed():
    before = {
        "name": "Alice",
    }
    after = {
        "name": "Lora",
    }
    diff = compareJson(before, after)
    expected_output = [
        {
            "field": "[name]",
            "type": "values_changed",  
            "old": "Alice",
            "new": "Lora"
        }
    ]
    assert diff_parser(diff) == expected_output

def test_diff_parser_type_changes():
    before = {
        "age": 30,
    }
    after = {
        "age": "30",
    }
    diff = compareJson(before, after)
    
    expected_output = [
        {
            "field": "[age]",
            "type": "type_changes",  
            "old": "int",
            "new": "str"
        }
    ]
    assert diff_parser(diff) == expected_output

def test_diff_parser_dictionary_item_added():
    before = {
        "name": "Alice",
    }
    after = {
        "name": "Alice",
        "age": 30
    }
    diff = compareJson(before, after)
    
    expected_output = [
        {
            "field": "[age]",
            "type": "dictionary_item_added",  
            "old": None,
            "new": 30
        }
    ]
    assert diff_parser(diff) == expected_output

def test_diff_parser_dictionary_item_removed():
    before = {
        "name": "Alice",
        "age": 30
    }
    after = {
        "name": "Alice",
    }
    diff = compareJson(before, after)
    
    expected_output = [
        {
            
            "field": "[age]",
            "type": "dictionary_item_removed",  
            "old" : 30,
            "new": None
        }
    ]
    assert diff_parser(diff) == expected_output

def test_diff_parser_lists_changes():
    before = {
        "projects": ["project1", "project2"]
    }
    after = {
        "projects": ["project11", "project2", "project3"]
    }
    diff = compareJson(before, after)
    
    expected_output = [
        {
            "field": "[projects][0]",
            "type": "values_changed",
            "old": "project1",
            "new": "project11"
        },
        {
            "field": "[projects][2]",
            "type": "iterable_item_added",
            "old": None,
            "new": "project3"
        }
    ]
    assert diff_parser(diff) == expected_output
       
def test_path_parser(): 
    assert path_parser("root['name']") == "[name]"
    assert path_parser("root['adresse']['street']") == "[adresse][street]"
    assert path_parser("root['age']") == "[age]"
    assert path_parser("root['items'][0]") == "[items][0]"

def test_type_parser():
    assert type_parser(int) == "int"
    assert type_parser(str) == "str"
    assert type_parser(list) == "list"
    assert type_parser(dict) == "dict"