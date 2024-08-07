import os
import pandas as pd
import numpy as np
from dbase_load import load_template_csv_with_index, create_dot_items_dataframe

def setup_database(template_file_path):
    """Master function to set up the database with dot items and template data."""
    # Load the data frames
    dot_items_df = create_dot_items_dataframe()
    template_df = load_template_csv_with_index(template_file_path)

    print("Dot Items DataFrame:\n", dot_items_df.head())
    print("Template DataFrame:\n", template_df.head())

    # Rename columns before merging
    dot_items_df = dot_items_df.rename(columns={
        'item_name': 'fs_item_name',
        'is_folder': 'fs_is_folder'
    })

    # Merge the DataFrames
    merged_df = merge_dataframes(dot_items_df, template_df)

    # Ensure fs_item_name and tp_item_name are strings
    merged_df['fs_item_name'] = merged_df['fs_item_name'].astype(str)
    merged_df['tp_item_name'] = merged_df['tp_item_name'].astype(str)

    # Populate item_name, handling potential conflicts
    def resolve_name_conflict(row):
        fs_name = row['fs_item_name'].strip()
        tp_name = row['tp_item_name']
        if fs_name:
            return fs_name  # Prioritize file system name if it exists
        elif tp_name:
            return tp_name
        else:
            return ''  # Or some other default value if both are missing

    merged_df['item_name'] = merged_df.apply(resolve_name_conflict, axis=1)

    # Populate is_folder based on a similar conflict resolution logic
    def resolve_folder_conflict(row):
        if pd.notna(row['fs_is_folder']):
            return row['fs_is_folder']
        elif pd.notna(row['tp_is_folder']):
            return row['tp_is_folder']
        else:
            return np.nan  # Use NaN for unknown states

    merged_df['is_folder'] = merged_df.apply(resolve_folder_conflict, axis=1)

    # Add 'no_show' column to the DataFrame with default False
    merged_df['no_show'] = False

    # Mark common files to exclude from the report
    def mark_no_show(row):
        if row['item_name'] in ['.DS_Store']:  # Add other common files if needed
            return True
        return False

    merged_df['no_show'] = merged_df.apply(mark_no_show, axis=1)

    # Dynamically reorder columns based on available columns
    reordered_columns = [
        'item_name', 'is_folder', 'fs_item_name', 'fs_is_folder', 'unique_id'
    ]
    reordered_columns += [col for col in [
        'tp_item_name', 'tp_is_folder', 'tp_cat_1', 'tp_cat_1_name', 'tp_cat_2', 'tp_comment', 'no_show', 'original_order'
    ] if col in merged_df.columns]
    reordered_columns += [col for col in [
        'fs_size', 'fs_date_created', 'fs_date_modified', 'fs_date_added', 'fs_tags'
    ] if col in merged_df.columns]

    # Reorder columns
    merged_df = merged_df[reordered_columns]

    # Sort by original order
    merged_df.sort_values('original_order', inplace=True)

    print("\nmerged_df (after modifications):\n", merged_df)

    return merged_df

def merge_dataframes(dot_items_df, template_df):
    """Merge the dot items DataFrame with the template DataFrame."""
    
    # Print the Dot Items DataFrame
    print("Dot Items DataFrame:\n", dot_items_df.head())

    # Print the Template DataFrame
    print("Template DataFrame:\n", template_df.head())

    # Merge the DataFrames
    merged_df = pd.merge(
        dot_items_df, template_df,
        left_on=['fs_item_name', 'fs_is_folder'],
        right_on=['tp_item_name', 'tp_is_folder'],
        how='outer',
        suffixes=('_fs', '_tp')
    )

    # Print the Merged DataFrame (Initial)
    print("Merged DataFrame (Initial):\n", merged_df.head())

    # Ensure fs_item_name and tp_item_name are strings
    merged_df['fs_item_name'] = merged_df['fs_item_name'].astype(str)
    merged_df['tp_item_name'] = merged_df['tp_item_name'].astype(str)

    # Populate item_name, handling potential conflicts
    def resolve_name_conflict(row):
        fs_name = row['fs_item_name'].strip()
        tp_name = row['tp_item_name']
        if fs_name:
            return fs_name  # Prioritize file system name if it exists
        elif tp_name:
            return tp_name
        else:
            return ''  # Or some other default value if both are missing

    merged_df['item_name'] = merged_df.apply(resolve_name_conflict, axis=1)

    # Populate is_folder based on a similar conflict resolution logic
    def resolve_folder_conflict(row):
        if pd.notna(row['fs_is_folder']):
            return row['fs_is_folder']
        elif pd.notna(row['tp_is_folder']):
            return row['tp_is_folder']
        else:
            return np.nan  # Use NaN for unknown states

    merged_df['is_folder'] = merged_df.apply(resolve_folder_conflict, axis=1)

    # Add 'no_show' column to the DataFrame with default False
    merged_df['no_show'] = False

    # Mark common files to exclude from the report
    def mark_no_show(row):
        if row['item_name'] in ['.DS_Store']:  # Add other common files if needed
            return True
        return False

    merged_df['no_show'] = merged_df.apply(mark_no_show, axis=1)

    # Dynamically reorder columns based on available columns
    reordered_columns = [
        'item_name', 'is_folder', 'fs_item_name', 'fs_is_folder', 'unique_id'
    ]
    reordered_columns += [col for col in [
        'tp_item_name', 'tp_is_folder', 'tp_cat_1', 'tp_cat_1_name', 'tp_cat_2', 'tp_comment', 'no_show', 'original_order'
    ] if col in merged_df.columns]
    reordered_columns += [col for col in [
        'fs_size', 'fs_date_created', 'fs_date_modified', 'fs_date_added', 'fs_tags'
    ] if col in merged_df.columns]

    # Reorder columns
    merged_df = merged_df[reordered_columns]

    return merged_df