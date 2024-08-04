import pandas as pd  # Importing the pandas package

def create_dataframe(dot_items, template_dict):
    """
    Create a Pandas DataFrame from the dot items and template dictionaries.
    """
    # Prepare the data
    data = {
        'unique_id': [],  # Adding a unique identifier for each entry
        'line_number': [],
        'line_content': [],
        'fs_filename': [],
        'fs_type': [],
        'tp_filename': [],
        'tp_type': [],
        'tp_comment': [],
        'line_type': [],  # Add line type to track formatting vs. data
    }

    # Populate the DataFrame with data from the template dictionary
    for line_number, line_info in template_dict.items():
        item_name = line_info['item_name']
        comment = line_info['comment']
        is_folder = line_info['is_folder']
        line_type = line_info['line_type']
        line_content = line_info['line_content']

        # Default file system data
        fs_type = ""
        fs_name = ""

        # Check if item exists in the dot_items
        if item_name in dot_items:
            fs_name = item_name
            fs_type = 'Folder' if dot_items[item_name] else 'File'

        # Append the data
        data['unique_id'].append(line_number)  # Using line_number as a unique ID for simplicity
        data['line_number'].append(line_number)
        data['line_content'].append(line_content)
        data['fs_filename'].append(fs_name)
        data['fs_type'].append(fs_type)
        data['tp_filename'].append(item_name)
        data['tp_type'].append('Folder' if is_folder else 'File')
        data['tp_comment'].append(comment)
        data['line_type'].append(line_type)

    # Create the DataFrame
    df = pd.DataFrame(data)

    # Ensuring the index is unique by creating a new unique ID
    df.reset_index(drop=True, inplace=True)

    # Optionally, you can set the unique_id column as the index
    df.set_index('unique_id', inplace=True)

    return df