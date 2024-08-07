import os
import pandas as pd
import numpy as np

# Set Pandas display options for console output
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)        # Set console width to prevent line wrapping

def resolve_name_conflict(row):
  tp_name = row['tp_item_name'] if pd.notna(row['tp_item_name']) else ''
  fs_name = row['fs_item_name'] if pd.notna(row['fs_item_name']) else ''
  if row['_merge'] == 'right_only':  # Only in template
      return tp_name
  elif row['_merge'] == 'left_only':  # Only in filesystem
      return fs_name
  elif tp_name:
      return tp_name
  elif fs_name:
      return fs_name
  else:
      return ''  # Default value if both are missing

def resolve_folder_conflict(row):
    if row['_merge'] == 'right_only':  # Only in template
        return row['tp_is_folder']
    elif row['_merge'] == 'left_only':  # Only in filesystem
        return row['fs_is_folder']
    elif pd.notna(row['tp_is_folder']):
        return row['tp_is_folder']  # Prioritize template folder status
    elif pd.notna(row['fs_is_folder']):
        return row['fs_is_folder']  # Otherwise, use file system folder status
    else:
        return np.nan  # Use NaN for unknown states

def merge_dataframes(dot_items_df, template_df):
    """Merge the dot items DataFrame with the template DataFrame."""
    
    # Print the dot_items_df DataFrame
    print("Dot Items DataFrame (Pre-Merge):\n", dot_items_df.head())
    print("\nDot Items DataFrame Info (Pre-Merge):\n")
    print(dot_items_df.info())

    # Print the template_df DataFrame
    print("Template DataFrame (Pre-Merge):\n", template_df.head())
    print("\nTemplate DataFrame Info (Pre-Merge):\n")
    print(template_df.info())

    # Merge the DataFrames with an indicator
    merged_df = pd.merge(
        dot_items_df, template_df,
        left_on=['fs_item_name', 'fs_is_folder'],
        right_on=['tp_item_name', 'tp_is_folder'],
        how='outer',
        suffixes=('_fs', '_tp'),
        indicator=True  # Add indicator to identify source of each row
    )

    # Print the Merged DataFrame (Initial)
    print("Merged DataFrame (Initial):\n", merged_df.head())

    # Testing: Check for initial data types and missing values
    print("\nData types after initial merge:\n", merged_df.dtypes)
    print("\nMissing values after initial merge:\n", merged_df.isnull().sum())

    # Ensure fs_item_name and tp_item_name are strings
    merged_df['fs_item_name'] = merged_df['fs_item_name'].astype(str)
    merged_df['tp_item_name'] = merged_df['tp_item_name'].astype(str)

    # Apply name conflict resolution
    merged_df['item_name'] = merged_df.apply(resolve_name_conflict, axis=1)

    # Ensure item_name is properly populated
    print("\nFinal item_name values:\n", merged_df['item_name'].head())

    # Apply folder conflict resolution
    merged_df['is_folder'] = merged_df.apply(resolve_folder_conflict, axis=1)

    # Testing: Check for data types and missing values after folder conflict resolution
    # print("\nData types after folder conflict resolution:\n", merged_df.dtypes)
    # print("\nMissing values after folder conflict resolution:\n", merged_df.isnull().sum())

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

    # Print the Merged DataFrame (Processed)
    # print("\nMerged DataFrame (Processed):\n", merged_df.head())

    # Final testing: Confirm final data types and missing values
    # print("\nFinal data types:\n", merged_df.dtypes)
    # print("\nFinal missing values:\n", merged_df.isnull().sum())

    return merged_df