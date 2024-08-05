import pandas as pd
import os

def create_dot_items_dataframe():
    dot_items = []
    home_dir_path = os.path.expanduser("~")

    for item in os.listdir(home_dir_path):
        if item.startswith("."):
            item_path = os.path.join(home_dir_path, item)
            is_folder = os.path.isdir(item_path)
            dot_items.append({"item": str(item), "is_folder": is_folder})  # Convert item to string here

    # Print the list of dot items to verify the content
    print("Dot Items List:", dot_items)

    # Create the DataFrame without specifying dtype initially
    df = pd.DataFrame(dot_items)

    # Set the dtype for each column using astype
    df["item"] = df["item"].astype(str)
    df["is_folder"] = df["is_folder"].astype(bool)

    return df