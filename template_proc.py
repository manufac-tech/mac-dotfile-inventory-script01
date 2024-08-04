def read_template(file_path):
    """Read the template markdown file."""
    with open(file_path, 'r') as file:
        return file.readlines()

def is_blank_or_comment(line):
    """Check if a line is blank or a comment."""
    return not line.strip() or line.strip().startswith('#')

def extract_item_and_folder_status(line):
    """Extract item name, comment, and folder status."""
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

def create_template_dict_master():
    """Read the template and create a dictionary with detailed line information."""
    # Define the template file path internally
    template_path = "/Users/stevenbrown/swd_storage/VCS_local/vcs3_GitHub/GitHub5_mine_private/macOS_util_py_rep_dot_inv01_240723/data/Rep_HOME_dot_inventory_TEMPLATE.md"
    
    template_dict = {}
    
    # Read the template
    lines = read_template(template_path)
    
    # Process each line with its line number
    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        line_type = "data" if not is_blank_or_comment(line) else "formatting"
        
        # Initialize variables for non-comment lines
        item_name = comment = ""
        is_folder = False

        # Process non-comment lines
        if line_type == "data":
            item_name, comment, is_folder = extract_item_and_folder_status(stripped_line)
        
        # Store detailed information in the dictionary
        template_dict[line_number] = {
            "line_content": stripped_line,
            "item_name": item_name,
            "comment": comment,
            "is_folder": is_folder,
            "line_type": line_type,
        }
    
    return template_dict