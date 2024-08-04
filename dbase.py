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
    
    # Create the DataFrame and specify the data types correctly
    df = pd.DataFrame(dot_items)
    df = df.astype({"item": "string", "is_folder": "bool"})

    return df