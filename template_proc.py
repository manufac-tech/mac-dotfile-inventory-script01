
def read_template(file_path):
    """Read the template markdown file."""
    with open(file_path, 'r') as file:
        return file.readlines()

def is_blank_or_comment(line):
    """Check if a line is blank or a comment."""
    return not line.strip() or line.strip().startswith('#')

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

# def process_template(template_path, dot_items_dict):
#     formatted_output = []
#     unmatched_in_home = set(dot_items_dict.keys())
#     matched_in_template = set()
#     template_items = set()  # Create a set for template items

#     with open(template_path, "r") as template_file:
#         for line in template_file:
#             stripped_line = line.strip()
#             if is_blank_or_comment(stripped_line):
#                 formatted_output.append(line.rstrip())
#                 continue

#             item_name, comment, is_folder = extract_item_and_folder_status(stripped_line)
#             template_items.add(item_name)  # Add the item to the template_items set

#             # Check if the item exists in the dot items dictionary
#             if item_name in dot_items_dict:
#                 matched_in_template.add(item_name)
#                 unmatched_in_home.discard(item_name)
#                 is_folder = dot_items_dict[item_name]  # Update only is_folder from dot_items_dict
#             formatted_line = compile_line(item_name, comment, is_folder)
#             formatted_output.append(formatted_line)

#     unmatched_in_template = template_items.difference(matched_in_template)  # Use template_items instead of template_dict

#     return formatted_output, unmatched_in_home, unmatched_in_template