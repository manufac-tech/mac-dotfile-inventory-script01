import pandas as pd
import numpy as np

def resolve_name_conflict(row):
    """
    Resolve conflicts between filesystem and template item names.
    
    In edge cases where both filesystem and template names are present,
    the filesystem name is prioritized. This decision likely doesn't affect
    the outcome, as this conflict resolution only occurs when the names 
    are identical in the first place.

    Args:
        row (Series): A row from the merged DataFrame.

    Returns:
        str: The resolved item name.
    """
    tp_name = row['tp_item_name'] if pd.notna(row['tp_item_name']) else ''
    fs_name = row['fs_item_name'] if pd.notna(row['fs_item_name']) else ''
    if row['_merge'] == 'right_only':  # Only in template
        return tp_name
    elif row['_merge'] == 'left_only':  # Only in filesystem
        return fs_name
    elif fs_name:  # Prioritize filesystem name
        return fs_name
    elif tp_name:
        return tp_name
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

def replace_nan_values(df):
    """
    Replace NaN values with descriptive placeholders based on the field prefix.

    Args:
        df (DataFrame): The DataFrame to process.

    Returns:
        DataFrame: The DataFrame with NaN values replaced.
    """
    # Identify columns that start with 'fs_' and 'tp_'
    fs_columns = [col for col in df.columns if col.startswith('fs_')]
    tp_columns = [col for col in df.columns if col.startswith('tp_')]

    # Print identified columns for debugging
    print("Filesystem columns:", fs_columns)
    print("Template columns:", tp_columns)

    # Print the DataFrame before replacing NaN values
    print("DataFrame before replacing NaN values in replace_nan_values:\n", df.head())

    # Replace NaN values with descriptive placeholders
    for col in fs_columns:
        df[col] = df[col].replace(np.nan, '[NO FS ITEM]')
    for col in tp_columns:
        df[col] = df[col].replace(np.nan, '[NO TP ITEM]')

    # Print the DataFrame after replacing NaN values
    print("DataFrame after replacing NaN values in replace_nan_values:\n", df.head())

    return df

def reorder_columns(df, columns):
    """Reorder columns based on a predefined order."""
    reordered_columns = [col for col in columns if col in df.columns]
    return df[reordered_columns]

def print_data_checks(df, stage):
    """Print data types and missing values for the DataFrame."""
    print(f"\n{stage} DataFrame Info:\n")
    print(df.info())
    print(f"\nData types after {stage}:\n", df.dtypes)
    print(f"\nMissing values after {stage}:\n", df.isnull().sum())