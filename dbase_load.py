import os
import pandas as pd
import numpy as np

def create_dot_items_dataframe():
    """
    Create a DataFrame from the dot items in the home directory.

    Returns:
        DataFrame: A DataFrame containing item names, folder status, and unique IDs.
    """
    dot_items = []
    home_dir_path = os.path.expanduser("~")

    for item in os.listdir(home_dir_path):
        if item.startswith("."):
            item_path = os.path.join(home_dir_path, item)
            is_folder = os.path.isdir(item_path)
            dot_items.append({"item_name": item, "is_folder": is_folder})

    df = pd.DataFrame(dot_items)

    # Rename columns to avoid conflicts during merging
    df = df.rename(columns={
        'item_name': 'fs_item_name',
        'is_folder': 'fs_is_folder'
    })

    # Ensure fs_is_folder is boolean
    df['fs_is_folder'] = df['fs_is_folder'].astype(bool)

    # Assign sequential unique ID
    df['unique_id'] = np.arange(len(df))  

    # Add 'no_show' column with default False
    df['no_show'] = False

    # Mark common files to exclude from the report
    def mark_no_show(row):
        if row['fs_item_name'] in ['.DS_Store']:  # Add other common files if needed
            return True
        return False

    df['no_show'] = df.apply(mark_no_show, axis=1)

    return df

def load_template_csv_with_index(template_file_path):
    """
    Load the CSV template into a staging DataFrame with index and prepare it.

    Args:
        template_file_path (str): Path to the template CSV file.

    Returns:
        DataFrame: A DataFrame containing the template data with an original order index.
    """
    try:
        template_df = pd.read_csv(template_file_path, dtype={
            "tp_item_name": object,
            "tp_is_folder": bool,
            "tp_cat_1": object, 
            "tp_cat_1_name": object, 
            "tp_comment": object, 
            "tp_cat_2": object,
            "no_show": bool  # Ensure no_show is read as boolean
        })

        # Ensure tp_is_folder is boolean
        template_df['tp_is_folder'] = template_df['tp_is_folder'].astype(bool)

        # Ensure no_show is boolean
        template_df['no_show'] = template_df['no_show'].astype(bool)

        # Assign original order for consistency
        template_df['original_order'] = np.arange(len(template_df))

        # Fill NaN values in comments
        template_df['tp_comment'] = template_df['tp_comment'].fillna('')

        return template_df
    except Exception as e:
        print(f"Error loading template CSV: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error