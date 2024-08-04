# data_proc.py

import pandas as pd  # Importing the pandas package

def create_dataframe(dot_items, template_dict):
    """
    Create a Pandas DataFrame from the dot items and template dictionaries.
    """
    # Prepare the data
    data = {
        'fs_filename': [],
        'fs_type': [],
        'tp_filename': [],
        'tp_type': [],
        'tp_comment': [],
    }

    # Populate the DataFrame with data from the dictionaries
    for item_name, is_folder in dot_items.items():
        # Default template data
        tp_name = ""
        tp_type = ""
        tp_comment = ""

        if item_name in template_dict:
            tp_name, tp_type = item_name, template_dict[item_name][1]
            tp_comment = template_dict[item_name][0]

        # Append the data
        data['fs_filename'].append(item_name)
        data['fs_type'].append('Folder' if is_folder else 'File')
        data['tp_filename'].append(tp_name)
        data['tp_type'].append('Folder' if tp_type else 'File')
        data['tp_comment'].append(tp_comment)

    # Create the DataFrame
    df = pd.DataFrame(data)
    
    return df

def main():
    # Example dictionaries (replace these with actual data)
    dot_items = {
        ".quokka": True,
        ".nuxtrc": False,
        ".vue-cli-ui": True,
        ".config": True,
        ".docker": True
    }
    
    template_dict = {
        "._dotfiles": ('/Users/stevenbrown/.\\_dotfiles/.\\_dotfiles_srb_repo', True),
        ".zshrc": ('', False),
        ".zshrc_aliases": ('', False),
        ".zshrc_scripts": ('', False),
        ".zshrc_themes_omp": ('', False),
        ".zshrc_autocomplete1": ('', False),
        ".zprofile": ('zsh profile file', False)
    }

    # Create the DataFrame
    df = create_dataframe(dot_items, template_dict)

    # Display the DataFrame
    print(df)

if __name__ == "__main__":
    main()