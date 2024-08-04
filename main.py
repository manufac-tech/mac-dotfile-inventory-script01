import os
from datetime import datetime
from template_proc import read_template, is_blank_or_comment, extract_item_and_folder_status, create_template_dict
from report_gen import process_template, compile_line, post_process_output, write_output_file  

# Define the source file paths
template_path = "/Users/stevenbrown/swd_storage/VCS_local/vcs3_GitHub/GitHub5_mine_private/macOS_util_py_rep_dot_inv01_240723/data/Rep_HOME_dot_inventory_TEMPLATE.md"

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
    
def main():
    # Read the template
    template = read_template(template_path)

    # Define the home directory path
    home_dir_path = os.path.expanduser("~")
    
    # Create the dictionary of dot items in the home directory
    dot_items = create_dot_items_dictionary(home_dir_path)
    
    # Create the template dictionary
    template_dict = create_template_dict(template_path)

    # # Print the contents of dot_items
    # print("\nDot Items Dictionary:")
    # for key, value in dot_items.items():
    #     print(f"{key}: {value}")

    # # Print the contents of template_dict
    # print("\nTemplate Dictionary:")
    # for key, value in template_dict.items():
    #     print(f"{key}: {value}")
    
    # Process each line in the template
    for line in template:
        if is_blank_or_comment(line):
            continue

        item_name, comment, is_folder = extract_item_and_folder_status(line)
        # if item_name:
        #     # Logic to process each item (e.g., checking if it exists in dot_items)
        #     print(f"Processing item: {item_name}, Comment: {comment}, Is Folder: {is_folder}")

    # Process the template
    formatted_output, unmatched_in_home, unmatched_in_template = process_template(template_path, dot_items)
    
    # Post-process the output to handle unmatched items
    formatted_output = post_process_output(formatted_output, unmatched_in_home, unmatched_in_template, dot_items, template_dict)
    
    # Generate the output file name with current date and time
    output_file_name = datetime.now().strftime("%y%m%d-%H%M%S") + "_Rep_HOME_dot_inventory.md"
    output_file_path = os.path.join("/Users/stevenbrown/Library/Mobile Documents/com~apple~CloudDocs/Documents_SRB iCloud/Filespace control/FS Ctrl - LOGS/Info Reports + Logs IN", output_file_name)
    
    # Write the formatted output to the output file
    write_output_file(output_file_path, formatted_output)

if __name__ == "__main__":
    main()