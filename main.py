import os
from report_gen import create_report_master
from data_proc import create_dataframe
from template_proc import create_template_dict_master

# Function to create a dictionary from dot items in the home directory
def create_dot_items_dictionary():
    dot_items = {}
    home_dir_path = os.path.expanduser("~")  # Define the home directory path internally
    for item in os.listdir(home_dir_path):
        if item.startswith("."):
            item_path = os.path.join(home_dir_path, item)
            is_folder = os.path.isdir(item_path)
            dot_items[item] = is_folder
            # print(f"[create_dot_items_dictionary] Item: {item}, Is Folder: {is_folder}")
    return dot_items

def find_duplicate_indices(df):
    # Check for duplicate indices in the DataFrame
    duplicates = df.index[df.index.duplicated()].unique()
    
    if len(duplicates) > 0:
        print("Duplicate indices found:")
        print(duplicates)
        # Print the rows with duplicate indices
        print("Rows with duplicate indices:")
        print(df.loc[duplicates])
    else:
        print("All indices are unique.")

def main():
    # Create the dictionary of dot items in the home directory
    dot_items = create_dot_items_dictionary()

    # Create the template dictionary using the master function
    template_dict = create_template_dict_master()

    # Create the DataFrame using the new function
    df = create_dataframe(dot_items, template_dict)

    # Set the DataFrame index to line_number for unique indexing
    df.set_index('line_number', inplace=True)

    # Check for duplicate indices
    find_duplicate_indices(df)

    # Debug: Print DataFrame information
    print("\nGenerated DataFrame Info:")
    print(df.info())
    print("\nDataFrame Head:")
    print(df.head())

    # Call the master report generation function
    create_report_master(template_dict, dot_items, df)

if __name__ == "__main__":
    main()
