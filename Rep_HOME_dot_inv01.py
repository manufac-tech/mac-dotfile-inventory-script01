#!/usr/bin/env python3

import os
from datetime import datetime

# Define the source file paths
template_path = "/Users/stevenbrown/Desktop/240722_DOT CONTROL GEN 2/Rep_HOME_dot_inventory_TEMPLATE.md"

# Function to check for blank lines or lines starting with a `#`
def is_blank_or_comment(line):
    stripped_line = line.strip()
    return not stripped_line or stripped_line.startswith("#")

# Function to create a dictionary from dot items in the home directory
def create_dot_items_dictionary(home_dir_path):
    dot_items = {}
    for item in os.listdir(home_dir_path):
        if item.startswith("."):
            item_path = os.path.join(home_dir_path, item)
            is_folder = os.path.isdir(item_path)
            dot_items[item] = is_folder
            # print(f"[create_dot_items_dictionary] Item: {item}, Is Folder: {is_folder}")
    return dot_items

# Function to create a dictionary from the template markdown file
def create_template_dict(template_path):
    template_dict = {}
    with open(template_path, "r") as file:
        for line in file:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith("#"):
                continue

            item_name, comment, is_folder = extract_item_and_folder_status(stripped_line)
            template_dict[item_name] = (comment, is_folder)

    # Conditionally print the entry if the item name is '.gem'
    for key, value in template_dict.items():
        if key == ".gem":
            print(f"[create_template_dict] Item: {key}, Comment: {value[0]}, Is Folder: {value[1]}")
    
    return template_dict

# Existing extract_item_and_folder_status function, updated to handle comment extraction correctly
def extract_item_and_folder_status(line):
    # Strip leading '- ' and space
    line = line[2:].strip()
    
    # Check for folder suffix and remove it if present
    is_folder = line.endswith(" (ƒ)**")
    if is_folder:
        line = line[:-6]  # Remove ' (ƒ)**'
    
    # Remove leading bold formatting if present
    if line.startswith("**"):
        line = line[2:]  # Remove starting '**'
    
    # Extract comment if present
    parts = line.split(" | ", 1)
    item_name = parts[0].strip()
    comment = parts[1].strip() if len(parts) > 1 else ""

    return item_name, comment, is_folder

# Function to compile the formatted line
def compile_line(item, comment, is_folder):
    line = item
    if comment:
        line += f" | {comment}"
    if is_folder:
        line += " (ƒ)"
        line = f"**{line}**"
    return f"- {line}"

def process_template(template_path, dot_items_dict):
    formatted_output = []
    unmatched_in_home = set(dot_items_dict.keys())
    matched_in_template = set()
    
    with open(template_path, "r") as template_file:
        for line in template_file:
            stripped_line = line.strip()
            if is_blank_or_comment(stripped_line):
                formatted_output.append(line.rstrip())
                continue

            item_name, comment, is_folder = extract_item_and_folder_status(stripped_line)

            # Check if the item exists in the dot items dictionary
            if item_name in dot_items_dict:
                matched_in_template.add(item_name)
                unmatched_in_home.discard(item_name)
                is_folder = dot_items_dict[item_name]  # dot_items_dict only contains folder status
                formatted_line = compile_line(item_name, comment, is_folder)
            else:
                formatted_line = compile_line(item_name, comment, is_folder)

            formatted_output.append(formatted_line)
    
    unmatched_in_template = set(dot_items_dict.keys()).difference(matched_in_template)
    
    return formatted_output, unmatched_in_home, unmatched_in_template

def post_process_output(formatted_output, unmatched_in_home, unmatched_in_template):
    if unmatched_in_home:
        formatted_output.insert(0, "### Unmatched Items in Home Directory\n")
        for item in sorted(unmatched_in_home):
            formatted_output.insert(1, f"- {item}\n")
    
    if unmatched_in_template:
        formatted_output.append("\n### Template Items Not Found in Home Directory\n")
        for item in sorted(unmatched_in_template):
            formatted_output.append(f"- {item}\n")
    
    return formatted_output

# Function to write the output to a file
def write_output_file(output_path, formatted_output):
    with open(output_path, "w") as dest:
        for line in formatted_output:
            dest.write(line + "\n")
            # print(line)

# Main function to run the script
def main():
    home_dir_path = os.path.expanduser("~")
    dot_items = create_dot_items_dictionary(home_dir_path)
    
    # Template dictionary creation
    template_dict = create_template_dict(template_path)
    
    # Process the template
    formatted_output, unmatched_in_home, unmatched_in_template = process_template(template_path, dot_items)
    
    # Add unmatched items in home to the beginning of the formatted output
    unmatched_home_header = "### $HOME dot items not found in Template"
    formatted_output.insert(0, unmatched_home_header)
    for item in unmatched_in_home:
        is_folder = dot_items.get(item, False)  # Ensure default value if item is missing
        line = compile_line(item, "", is_folder)  # No comment since it's not in the template
        formatted_output.insert(1, line)  # Insert after the header
    
    # Add unmatched items in template to the end of the formatted output
    unmatched_template_header = "### Template Items Not Found in $HOME"
    formatted_output.append(unmatched_template_header)
    for item in unmatched_in_template:
        comment, is_folder = template_dict.get(item, ("", False))  # Ensure default values if item is missing
        line = compile_line(item, comment, is_folder)
        formatted_output.append(line)
    
    # Generate the output file name with current date and time
    output_file_name = datetime.now().strftime("%y%m%d-%H%M%S") + "_Rep_HOME_dot_inventory_TEST.md"
    output_file_path = os.path.join("/Users/stevenbrown/Desktop/240722_DOT CONTROL GEN 2", output_file_name)
    
    write_output_file(output_file_path, formatted_output)

if __name__ == "__main__":
    main()