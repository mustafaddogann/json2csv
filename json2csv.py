import json
import csv
import argparse
from collections.abc import MutableMapping, Sequence # More robust type checking

def flatten_json(json_obj, parent_key='', sep='.'):
    """
    Flattens a nested dictionary or list.

    Args:
        json_obj: The dictionary or list to flatten.
        parent_key (str): The prefix to prepend to keys (used in recursion).
        sep (str): The separator to use between parent and child keys.

    Returns:
        dict: A flattened dictionary.
    """
    items = {}
    if isinstance(json_obj, MutableMapping): # Check if it's dict-like
        for k, v in json_obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.update(flatten_json(v, new_key, sep=sep))
    elif isinstance(json_obj, Sequence) and not isinstance(json_obj, (str, bytes)):
        # Handle lists/tuples but not strings/bytes
        # Option 1: Represent list as a string in the cell (simplest)
        items[parent_key] = str(json_obj)

        # --- Alternative Options for Lists (more complex, choose one if needed) ---
        # Option 2: Flatten list items into numbered keys (e.g., list.0, list.1)
        # Note: This works well for lists of simple types but can get complex with lists of objects
        # if not parent_key: # Avoid creating keys like ".0", ".1" if the list is top-level
        #     parent_key = 'list'
        # for i, v in enumerate(json_obj):
        #     new_key = f"{parent_key}{sep}{i}"
        #     items.update(flatten_json(v, new_key, sep=sep))

        # Option 3: Handle lists of objects by trying to flatten them (can lead to complex keys)
        # is_list_of_objects = all(isinstance(item, MutableMapping) for item in json_obj)
        # if is_list_of_objects:
        #      # Decide how to represent - maybe JSON stringify is still best? Or complex keying?
        #      items[parent_key] = json.dumps(json_obj) # Stringify complex lists
        # else: # List of simple items or mixed
        #      items[parent_key] = str(json_obj) # Default to string representation
        # ----------------------------------------------------------------------

    else:
        # It's a simple value (string, number, boolean, null)
        # Handle empty parent_key case (e.g., if the input JSON is just a single value)
        key_to_use = parent_key if parent_key else 'value'
        items[key_to_use] = json_obj

    return items

def json_to_csv(input_file, output_file, separator='.'):
    """
    Converts a JSON file (object or array of objects) to a CSV file.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output CSV file.
        separator (str): Separator for flattening nested keys.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            try:
                data = json.load(infile)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON file '{input_file}': {e}")
                return
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading input file '{input_file}': {e}")
        return

    # Ensure data is a list of objects for consistent processing
    if isinstance(data, dict):
        data = [data]
    elif not isinstance(data, list):
        print(f"Error: JSON root must be an object or an array of objects. Found type: {type(data)}")
        return

    if not data:
        print("Warning: JSON data is empty. Creating an empty CSV.")
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
             pass # Creates an empty file
        return

    # Flatten each JSON object in the list
    flattened_data = [flatten_json(item, sep=separator) for item in data if isinstance(item, (dict, list))]

    if not flattened_data:
         print("Warning: No valid objects found to flatten in the JSON data. Creating an empty CSV.")
         with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            pass
         return

    # Collect all unique headers from all flattened objects
    headers = set()
    for item in flattened_data:
        headers.update(item.keys())

    # Sort headers for consistent column order (optional but recommended)
    sorted_headers = sorted(list(headers))

    # Write to CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=sorted_headers, restval='', extrasaction='ignore') # ignore extra fields, write empty string for missing fields
            writer.writeheader()
            writer.writerows(flattened_data)
        print(f"Successfully converted '{input_file}' to '{output_file}'")
    except IOError as e:
        print(f"Error writing to output file '{output_file}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred during CSV writing: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a JSON file (including nested structures) to CSV.")
    parser.add_argument("input_file", help="Path to the input JSON file.")
    parser.add_argument("output_file", help="Path for the output CSV file.")
    parser.add_argument("-s", "--separator", default=".", help="Separator character for flattening nested keys (default: '.')")

    args = parser.parse_args()

    json_to_csv(args.input_file, args.output_file, args.separator)