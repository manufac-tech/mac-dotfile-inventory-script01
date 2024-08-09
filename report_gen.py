import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import regex as re
from dbase.dbase4_merge_sup import process_blanks

def export_dataframe_to_csv(df, filename='output.csv', columns=None):
    """
    Export the DataFrame to a CSV file.

    Args:
        df (DataFrame): The DataFrame to export.
        filename (str): The filename for the CSV file.
        columns (list): List of column names specifying the desired order.
    """
    try:
        # Process blanks and edge cases
        df = process_blanks(df)

        # Print the DataFrame to inspect before exporting
        print("DataFrame before exporting to CSV:\n", df.head())

        # Export the DataFrame with specified column order
        df.to_csv(filename, index=False, columns=columns)
        print(f"DataFrame exported to '{filename}'")
    except Exception as e:
        print(f"Failed to export DataFrame to CSV: {e}")

def export_to_markdown(df, template_path, template_file, output_file):
    """
    Export the DataFrame to a Markdown file using Jinja2 templates.
    
    Args:
        df (DataFrame): The DataFrame to export.
        template_path (str): The path to the Jinja2 template directory.
        template_file (str): The Jinja2 template file name.
        output_file (str): The output Markdown file name.
    """
    try:
        # Filter out items marked as no_show
        filtered_df = df[df['no_show'] == False]

        # Identify mismatches
        fs_not_in_tp = filtered_df[(filtered_df['item_name'].notnull()) & (filtered_df['tp_item_name'].isnull())]
        tp_not_in_fs = filtered_df[(filtered_df['item_name'].isnull()) & (filtered_df['tp_item_name'].notnull())]

        # Jinja2 setup
        env = Environment(
            loader=FileSystemLoader(template_path),
            trim_blocks=True,  
            lstrip_blocks=True  
        )
        env.globals['pd'] = pd

        # Render template - pass the filtered DataFrame and mismatched DataFrames directly
        template = env.get_template(template_file)
        rendered_markdown = template.render(
            csv_data=filtered_df.to_dict(orient='records'),
            fs_not_in_tp=fs_not_in_tp.to_dict(orient='records'),
            tp_not_in_fs=tp_not_in_fs.to_dict(orient='records')
        )

        # Output the rendered Markdown to a file
        with open(output_file, 'w') as file:
            file.write(rendered_markdown)

        print(f"Markdown report generated at: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Failed to export DataFrame to Markdown: {e}")