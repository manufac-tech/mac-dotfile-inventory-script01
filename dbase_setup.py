import pandas as pd
import os

def create_dot_items_dataframe():
    dot_items = []
    home_dir_path = os.path.expanduser("~")

    for item in os.listdir(home_dir_path):
        if item.startswith("."):
            item_path = os.path.join(home_dir_path, item)
            is_folder = os.path.isdir(item_path)
            dot_items.append({"item": item, "is_folder": is_folder})

    # Create the DataFrame with correct dtype usage
    df = pd.DataFrame(dot_items, dtype={"item": object, "is_folder": bool})

    # Add new columns with default or empty values
    df['tp_cat1'] = ""  # or a default category
    df['tp_cat2'] = ""  # or a default subcategory
    df['fs_tags'] = ""  # or use pd.NA for missing data
    df['fs_size'] = 0  # or pd.NA if size isn't known yet
    df['fs_date_modified'] = pd.NaT  # Use pd.NaT for datetime
    df['fs_date_created'] = pd.NaT  # Use pd.NaT for datetime
    df['fs_date_added'] = pd.NaT  # Use pd.NaT for datetime

    # Ensure unique ID assignment
    df['unique_id'] = df.groupby(list(df.columns)).ngroup()

    return df

# Commenting out the template DataFrame setup for now
# def create_template_dataframe(template_file_path):
#     template_df = pd.read_csv(template_file_path)
#     return template_df

# Commenting out merge logic for now
# def merge_dataframes(dot_items_df, template_df):
#     merged_df = pd.merge(dot_items_df, template_df, on="item", how="left")
#     return merged_df

def setup_database():
    """
    Master function to set up the database with dot items only.
    
    Returns:
        DataFrame: The DataFrame containing dot items information.
    """
    # Create dot items DataFrame
    dot_items_df = create_dot_items_dataframe()
    
    # Ensure unique ID assignment
    dot_items_df['unique_id'] = dot_items_df.groupby(list(dot_items_df.columns)).ngroup()

    # Return the dot items DataFrame only
    return dot_items_df