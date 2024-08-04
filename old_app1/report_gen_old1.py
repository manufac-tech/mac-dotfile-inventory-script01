import os
import pandas as pd  # Import pandas for DataFrame operations
from datetime import datetime
from template_proc_old1 import extract_item_and_folder_status

# Function to compile the formatted line
def compile_line(item, comment, is_folder):
    """Compile a formatted line from item details."""
    line = item
    if comment:
        line += f" | {comment}"
    if is_folder:
        line += " (ƒ)"
        line = f"**{line}**"
    return f"- {line}"


def report_builder(template_dict, dot_items_dict):
    """Process the template dictionary and return formatted output for the report."""
    
    formatted_output = []
    fs_items_no_match_template = set(dot_items_dict.keys())  # Start with all home items as unmatched
    template_items_matched_fs = set()  # Start empty, will track matched items in the template

    # Iterate through the template dictionary
    for line_number, line_info in template_dict.items():
        # Extract necessary data
        item_name = line_info["item_name"]
        comment = line_info["comment"]
        is_folder = line_info["is_folder"]
        line_type = line_info["line_type"]

        # If it's a formatting line, add it directly to the output
        if line_type == "formatting":
            formatted_output.append(line_info["line_content"])
            continue

        # Check if the item exists in the dot items dictionary for data lines
        if line_type == "data" and item_name in dot_items_dict:
            template_items_matched_fs.add(item_name)  # Track successful matches
            fs_items_no_match_template.discard(item_name)  # Remove matched items from fs_items_no_match_template
            is_folder = dot_items_dict[item_name]  # Update is_folder from dot_items_dict

        formatted_line = compile_line(item_name, comment, is_folder)
        formatted_output.append(formatted_line)

    # Calculate unmatched items in the template
    template_items_no_match_fs = set(item_info['item_name'] for item_info in template_dict.values() if item_info['line_type'] == 'data').difference(template_items_matched_fs)

    return formatted_output, fs_items_no_match_template, template_items_no_match_fs

def report_builder_db(df):
    """Generate the markdown report using the DataFrame as the data source."""
    formatted_output = []
    
    # Start with all home items as unmatched
    fs_items_no_match_template = set(df['fs_filename'].dropna())  
    
    # Start empty, will track matched items in the template
    template_items_matched_fs = set()
    
    # Set of template items
    template_items = set(df['tp_filename'].dropna())

    for index, row in df.iterrows():
        item_name = row['tp_filename']  # Use the template filename from the DataFrame
        comment = row['tp_comment']
        is_folder = row['tp_type'] == 'Folder'
        line_type = row['line_type']
        line_content = row['line_content']

        # If it's a formatting line, add it directly to the output
        if line_type == "formatting":
            formatted_output.append(line_content)
            continue

        # Check if the item exists in the file system
        if line_type == "data" and pd.notna(row['fs_filename']):
            template_items_matched_fs.add(item_name)  # Track successful matches
            fs_items_no_match_template.discard(item_name)  # Remove matched items from fs_items_no_match_template

        formatted_line = compile_line(item_name, comment, is_folder)
        formatted_output.append(formatted_line)

    # Calculate unmatched items in the template
    template_items_no_match_fs = template_items.difference(template_items_matched_fs)

    return formatted_output, fs_items_no_match_template, template_items_no_match_fs

def post_process_output(formatted_output, unmatched_in_home, unmatched_in_template, dot_items_dict, template_dict):
    """Post-process the output to handle unmatched items."""
    # Add unmatched items in home to the beginning of the formatted output
    if unmatched_in_home:
        formatted_output.insert(0, "### _$HOME dot items not found in Template_")
        for item in sorted(unmatched_in_home):
            is_folder = dot_items_dict.get(item, False)
            line = compile_line(item, "", is_folder)
            formatted_output.insert(1, line)
    
    # Add unmatched items in template to the end of the formatted output
    if unmatched_in_template:
        formatted_output.append("### _Template Items Not Found in $HOME_")
        for item in sorted(unmatched_in_template):
            comment, is_folder = template_dict.get(item, ("", False))
            line = compile_line(item, comment, is_folder)
            formatted_output.append(line)
    
    return formatted_output

def generate_output_filename(suffix=""):
    """
    Generate a unique output filename with an optional suffix.
    """
    # Base directory path for saving reports
    base_dir_path = "/Users/stevenbrown/Library/Mobile Documents/com~apple~CloudDocs/Documents_SRB iCloud/Filespace control/FS Ctrl - LOGS/Info Reports + Logs IN"

    # Generate the filename
    filename = datetime.now().strftime("%y%m%d-%H%M%S") + "_Rep_HOME_dot_inventory" + suffix + ".md"

    # Create the full output file path
    output_file_path = os.path.join(base_dir_path, filename)

    return output_file_path

def write_output_file(output_path, formatted_output):
    """Write the formatted output to a file."""
    with open(output_path, "w") as dest:
        for line in formatted_output:
            dest.write(line + "\n")

import pandas as pd

def create_report_master(template_dict, dot_items_dict, df):
    """
    Master function to generate reports from the template and database.

    Args:
        template_dict (dict): The template dictionary containing template information.
        dot_items_dict (dict): The dot items dictionary containing file system information.
        df (DataFrame): The DataFrame containing the merged information.

    Returns:
        None
    """

    # Set the unique_id column as the index
    df.set_index('unique_id', inplace=True)

    # Generate Report A
    formatted_output_a, fs_items_no_match_template_a, template_items_no_match_fs_a = report_builder(template_dict, dot_items_dict)
    formatted_output_a = post_process_output(formatted_output_a, fs_items_no_match_template_a, template_items_no_match_fs_a, dot_items_dict, template_dict)
    output_file_path_a = generate_output_filename()  # Generate output file path
    write_output_file(output_file_path_a, formatted_output_a)  # Write Report A

    # Generate Report B
    formatted_output_b, fs_items_no_match_template_b, template_items_no_match_fs_b = report_builder_db(df)
    formatted_output_b = post_process_output(formatted_output_b, fs_items_no_match_template_b, template_items_no_match_fs_b, df.to_dict(orient='index'), df.to_dict(orient='index'))
    output_file_path_b = generate_output_filename("_db")  # Generate output file path for Report B
    write_output_file(output_file_path_b, formatted_output_b)  # Write Report B