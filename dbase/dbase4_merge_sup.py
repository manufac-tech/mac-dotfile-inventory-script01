import pandas as pd
import numpy as np

def reorder_columns(df, columns):
    """Reorder columns based on a predefined order."""
    reordered_columns = [col for col in columns if col in df.columns]
    return df[reordered_columns]

def process_dupe_names(row):
    """
    Process and resolve conflicts between filesystem and template item names.

    Args:
        row (Series): A row from the merged DataFrame.

    Returns:
        str: The resolved item name.
    """
    fs_name = row['fs_item_name'] if pd.notna(row['fs_item_name']) else ''
    tp_name = row['tp_item_name'] if pd.notna(row['tp_item_name']) else ''
    
    if row['_merge'] == 'left_only':  # Only in filesystem
        return fs_name
    elif row['_merge'] == 'right_only':  # Only in template
        return tp_name
    elif fs_name:  # Prioritize filesystem name if both exist
        return fs_name
    elif tp_name:
        return tp_name
    else:
        return ''  # Default to empty string if both are missing

def process_dupe_folders(row):
    """
    Process and resolve conflicts between filesystem and template folder status.

    Args:
        row (Series): A row from the merged DataFrame.

    Returns:
        bool or NaN: The resolved folder status.
    """
    if row['_merge'] == 'left_only':  # Only in filesystem
        return row['fs_is_folder']
    elif row['_merge'] == 'right_only':  # Only in template
        return row['tp_is_folder']
    elif pd.notna(row['fs_is_folder']):
        return row['fs_is_folder']  # Prioritize filesystem folder status
    elif pd.notna(row['tp_is_folder']):
        return row['tp_is_folder']
    else:
        return np.nan  # Use NaN for unknown states

def process_blanks_fs(df):
    """Replace NaN values with '[NO FS ITEM]' for 'fs_' prefixed columns."""
    fs_columns = [col for col in df.columns if col.startswith('fs_')]
    for col in fs_columns:
        df[col] = df[col].replace(np.nan, '[NO FS ITEM]')
    return df

def process_blanks_tp(df):
    """Replace NaN values with '[NO TP ITEM]' for 'tp_' prefixed columns."""
    tp_columns = [col for col in df.columns if col.startswith('tp_')]
    for col in tp_columns:
        df[col] = df[col].replace(np.nan, '[NO TP ITEM]')
    return df

def process_blanks_edge(df):
    """
    Handle edge cases where both fs_item_name and fs_is_folder are NaN,
    and tp_item_name is valid but tp_is_folder is NaN.
    """
    # Identify Scenario 3 conditions
    scenario_3_mask = df['fs_item_name'].isna() & df['fs_is_folder'].isna() & df['tp_item_name'].notna() & df['tp_is_folder'].isna()
    
    # Apply the specific replacements for Scenario 3
    df.loc[scenario_3_mask, 'tp_item_name'] = df.loc[scenario_3_mask, 'tp_item_name'] + ' [NO TYPE]'
    df.loc[scenario_3_mask, 'fs_is_folder'] = '[NO ITEM DATA]'
    df.loc[scenario_3_mask, 'tp_is_folder'] = '[NO ITEM DATA]'
    
    return df

def process_blanks(df):
    """
    Replace NaN values with descriptive placeholders based on the field prefix.
    This includes handling standard blanks and edge cases.
    """
    # Process standard blanks
    df = process_blanks_fs(df)
    df = process_blanks_tp(df)
    
    # Handle edge cases
    df = process_blanks_edge(df)
    
    return df

def print_data_checks(df, stage):
    """Print data types and missing values for the DataFrame."""
    print(f"\n{stage} DataFrame Info:\n")
    print(df.info())
    print(f"\nData types after {stage}:\n", df.dtypes)
    print(f"\nMissing values after {stage}:\n", df.isnull().sum())