# import os
import pandas as pd
import numpy as np
from dbase.dbase4_merge_sup import resolve_name_conflict, resolve_folder_conflict, replace_nan_values, print_data_checks, reorder_columns

def merge_dataframes(dot_items_df, template_df):
    """Merge the dot items DataFrame with the template DataFrame."""
    
    # Initial data type and missing value checks
    print_data_checks(dot_items_df, "dot_items_df (Pre-Merge)")
    print_data_checks(template_df, "template_df (Pre-Merge)")

    # Merge the DataFrames with an indicator
    merged_df = pd.merge(
        dot_items_df, template_df,
        left_on=['fs_item_name', 'fs_is_folder'],
        right_on=['tp_item_name', 'tp_is_folder'],
        how='outer',
        indicator=True  # Add indicator to identify source of each row
    )

    # Print the Merged DataFrame (Initial)
    print("Merged DataFrame (Initial):\n", merged_df.head())

    # Ensure fs_item_name and tp_item_name are strings
    merged_df['fs_item_name'] = merged_df['fs_item_name'].astype(str)
    merged_df['tp_item_name'] = merged_df['tp_item_name'].astype(str)

    # Apply name conflict resolution
    merged_df['item_name'] = merged_df.apply(resolve_name_conflict, axis=1)

    # Ensure item_name is properly populated
    print("\nFinal item_name values:\n", merged_df['item_name'].head())

    # Apply folder conflict resolution
    merged_df['is_folder'] = merged_df.apply(resolve_folder_conflict, axis=1)

    # Combine 'unique_id' fields
    merged_df['unique_id'] = merged_df['fs_unique_id'].combine_first(merged_df['tp_unique_id'])

    # Drop unnecessary columns
    merged_df.drop(['fs_unique_id', 'tp_unique_id'], axis=1, inplace=True)

    # Handle NaN values for fs_ and tp_ fields
    merged_df = replace_nan_values(merged_df)

    # Reorder columns based on the updated table
    columns_order = [
        'item_name', 'is_folder', 
        'fs_item_name', 'fs_is_folder', 'unique_id', 
        'tp_item_name', 'tp_is_folder', 'tp_cat_1', 
        'tp_cat_1_name', 'tp_comment', 'tp_cat_2', 
        'no_show', 'original_order'
    ]
    merged_df = reorder_columns(merged_df, columns_order)

    # Final data type and missing value checks
    print_data_checks(merged_df, "Merged DataFrame (Processed)")

    return merged_df