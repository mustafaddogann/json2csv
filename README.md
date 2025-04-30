# JSON to CSV Converter

## Description

This Python script converts JSON files into CSV format, handling nested structures gracefully. It flattens JSON data, ensuring that all nested keys are represented as flattened columns in the output CSV file.

## Features

- Supports nested JSON objects and arrays.
- Customizable separator for flattened key names.
- Comprehensive error handling for invalid JSON and other edge cases.
- Command-line interface for easy usage.

## Requirements

- Python 3.6 or later

## How to Use

1. Save your JSON file (e.g., `input.json`).
2. Run the script from the command line:
   ```
   python json_to_csv.py input.json output.csv
   ```
3. Optionally, specify a custom separator for nested keys:
   ```
   python json_to_csv.py input.json output.csv -s "_"
   ```

## Example

### Input JSON (`input.json`):
```json
[
    {
        "name": "John",
        "address": {
            "city": "New York",
            "zipcode": "10001"
        },
        "hobbies": ["reading", "traveling"]
    },
    {
        "name": "Jane",
        "address": {
            "city": "San Francisco",
            "zipcode": "94105"
        },
        "hobbies": ["cooking"]
    }
]
```

### Output CSV (`output.csv`):
```
address.city,address.zipcode,hobbies,name
New York,10001,["reading", "traveling"],John
San Francisco,94105,["cooking"],Jane
```

## Notes

- Empty or invalid JSON files will result in an empty CSV file.
- Nested lists are converted to their string representation in the CSV.

## License

This project is licensed under the MIT License - see the LICENSE file for details.