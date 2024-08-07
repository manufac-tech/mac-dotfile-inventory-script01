import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader
import os
import re

def load_csv_with_index(file_path):
    """Load CSV data with an explicit index to preserve original order."""
    df = pd.read_csv(file_path)
    df['original_order'] = np.arange(len(df)) 
    return df

def main():
    # Define file paths
    csv_file_path = 'data/dotfiles_inventory_template_mast1_EXP.csv'
    jinja_template_path = 'data'
    jinja_template_file = 'rep_tp.jinja2'
    output_file_path = 'dotfiles_report.md' 

    # Load CSV data
    csv_data = load_csv_with_index(csv_file_path)

    # Jinja2 setup
    env = Environment(
        loader=FileSystemLoader(jinja_template_path),
        trim_blocks=False,  
        lstrip_blocks=False  
    )
    env.globals['pd'] = pd  

    # Convert to list of dictionaries
    data_list = csv_data.to_dict(orient='records')

    # Render template
    template = env.get_template(jinja_template_file)
    rendered_markdown = template.render(csv_data=data_list)  # Moved up

    # Apply regex after template rendering
    rendered_markdown = re.sub(r'\n{2,}', '\n', rendered_markdown)
    rendered_markdown = re.sub(r'(?<=\n)(?=###)', r'\n', rendered_markdown)  

    # Output to file
    with open(output_file_path, 'w') as file:
        file.write(rendered_markdown)

    print(f"Markdown report generated at: {os.path.abspath(output_file_path)}")

if __name__ == "__main__":
    main()
