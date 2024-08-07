import os
import pandas as pd
import numpy as np
from dbase.dbase1_load import load_template_csv_with_index, create_dot_items_dataframe
from dbase.dbase3_merge import merge_dataframes  # Import merge function

# Set Pandas display options for console output
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)        # Set console width to prevent line wrapping

def verify_data_types(df, expected_types):
    """
    Verify that the DataFrame columns match the expected data types.

    Args:
        df (DataFrame): The DataFrame to check.
        expected_types (dict): A dictionary mapping column names to expected data types.

    Returns:
        DataFrame: The DataFrame with corrected types.
    """
    for column, expected_type in expected_types.items():
        if df[column].dtype != expected_type:
            try:
                df[column] = df[column].astype(expected_type)
                print(f"Converted {column} to {expected_type}")
            except ValueError as e:
                print(f"Failed to convert {column} to {expected_type}: {e}")
    return df

def setup_database(template_file_path):
    """Master function to set up the database with dot items and template data."""
    # Load the data frames
    dot_items_df = create_dot_items_dataframe()
    template_df = load_template_csv_with_index(template_file_path)

    # Define expected types for dot_items_df
    dot_items_expected_types = {
        "fs_item_name": object,
        "fs_is_folder": bool,
        "unique_id": int
    }

    # Define expected types for template_df
    template_expected_types = {
        "tp_item_name": object,
        "tp_is_folder": bool,
        "tp_cat_1": object,
        "tp_cat_1_name": object,
        "tp_comment": object,
        "tp_cat_2": object,
        "no_show": bool,
        "original_order": int
    }

    # Verify types in dot_items_df
    dot_items_df = verify_data_types(dot_items_df, dot_items_expected_types)

    # Verify types in template_df
    template_df = verify_data_types(template_df, template_expected_types)

    # Merge the DataFrames
    merged_df = merge_dataframes(dot_items_df, template_df)

    # Reorder columns
    reordered_columns = [
        'item_name', 'is_folder', 'fs_item_name', 'fs_is_folder', 'unique_id',
        'tp_item_name', 'tp_is_folder', 'tp_cat_1', 'tp_cat_1_name', 'tp_cat_2', 
        'tp_comment', 'no_show', 'original_order'
    ]

    # Select available columns and reorder
    reordered_columns = [col for col in reordered_columns if col in merged_df.columns]

    # Reorder columns
    merged_df = merged_df[reordered_columns]

    # Sort by original order
    merged_df.sort_values('original_order', inplace=True)

    return merged_df