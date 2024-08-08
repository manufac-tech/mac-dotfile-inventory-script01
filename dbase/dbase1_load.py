import logging
import pandas as pd
import numpy as np
import os

# Configure logging to show DEBUG level messages (logging level un-mute - one or the other)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    # level=logging.INFO  # Use INFO for less verbose logging
    level=logging.DEBUG  # Change to DEBUG to capture more detailed output
)

def check_data_types(df, expected_types):
    """
    Check and log data types for DataFrame columns.

    Args:
        df (DataFrame): The DataFrame to check.
        expected_types (dict): A dictionary of expected data types.

    Returns:
        None
    """
    logging.debug("Entering check_data_types function")  # Added DEBUG message
    logging.info("Checking data types...")

    for column, expected_type in expected_types.items():
        if df[column].dtype != expected_type:
            logging.warning(f"Column '{column}' has type {df[column].dtype}, expected {expected_type}.")
            mismatches = df[column].apply(lambda x: type(x).__name__ != expected_type)
            logging.info(f"Mismatches found in column '{column}': {mismatches.sum()} out of {len(df)} entries.")
            logging.debug(f"Detailed mismatches in column '{column}': {df[column][mismatches].tolist()}")  # Detailed DEBUG info

    logging.debug("Data type check complete.")

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
            dot_items.append({"fs_item_name": item, "fs_is_folder": is_folder})

    df = pd.DataFrame(dot_items)

    # Ensure fs_is_folder is boolean
    df['fs_is_folder'] = df['fs_is_folder'].astype(bool)

    # Assign sequential unique ID
    df['fs_unique_id'] = np.arange(1, len(df) + 1)

    # Log data type checks
    check_data_types(df, {
        "fs_item_name": 'object',
        "fs_is_folder": 'bool',
        "fs_unique_id": 'int64'
    })

    return df

def load_template_csv_with_index(template_file_path, start_id=None):
    """
    Load the CSV template into a staging DataFrame with index and prepare it.

    Args:
        template_file_path (str): Path to the template CSV file.
        start_id (int, optional): The starting unique ID for unmatched template items.

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

        # Log data type checks
        check_data_types(template_df, {
            "tp_item_name": 'object',
            "tp_is_folder": 'bool',
            "tp_cat_1": 'object',
            "tp_cat_1_name": 'object',
            "tp_comment": 'object',
            "tp_cat_2": 'object',
            "no_show": 'bool',
            "original_order": 'int64'
        })

        # Assign unique IDs to unmatched template items starting from start_id if provided
        if start_id is not None:
            template_df['tp_unique_id'] = np.arange(start_id, start_id + len(template_df))
        else:
            template_df['tp_unique_id'] = np.nan  # Ensure the column exists

        return template_df
    except Exception as e:
        logging.error(f"Error loading template CSV: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error