# JSONDiffTool

JSONDiffTool is a Python application designed to compare two JSON states, detect updated fields, and help analyze how data changes after a user action.

## Context

This project comes from a real need observed during an internship.  
The goal was to compare JSON API responses before and after a user input in order to identify which fields were impacted, then track how these fields evolve during testing scenarios.

At first, this need was partially covered with Bash scripts:
- one script to compare a **before** state and an **after** state,
- one script to follow the evolution of the fields detected as changed.

JSONDiffTool is the Python version of this idea, with a cleaner structure and a user interface.

## Main goal

The main objective of this project is to provide a simple tool that can:

- compare two JSON contents,
- detect changed, added, removed, or type-changed fields,
- display differences clearly,
- export results if needed.

## V1 scope

The first version focuses on:

- a simple interface,
- two input areas for pasting JSON content,
- comparison of a **before** JSON and an **after** JSON,
- direct display of differences in the interface,
- optional CSV export of comparison results.

## Recent changes
- Kept the learning comparator in `app/core/costum_comparator.py`
- Project is moving toward the main `app/core/deepdiff_comparator.py` implementation

## Planned improvements

Future versions may include:

- loading JSON files from the interface,
- tracking changed fields across multiple GET/PUT pairs,
- search for a specific field,
- comparison history,
- ignoring technical fields,
- stronger DeepDiff-based comparison support.

## Expected difference format

Each detected difference should contain at least:

- `path`
- `change_type`
- `old_value`
- `new_value`

Handled change types in V1:

- `modified`
- `added`
- `removed`
- `type_changed`

## Project structure

```text
JSONDiffTool/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── costum_comparator.py
│   │   └── deepdiff_comparator.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── interface.py
│   └── utils/
│       ├── __init__.py
│       └── json_loader.py
├── tests/
│   ├── __init__.py
│   ├── test_contum_comparator.py
│   └── test_deepdiff_comparator.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Tech stack

- Python
- Streamlit for the interface
- DeepDiff for JSON comparison
- Pytest for testing

## Project status

V1 in progress.

## Notes

All example JSON files used in this repository must be anonymized.