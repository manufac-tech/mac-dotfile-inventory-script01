import pandas as pd
from dbase.dbase2_setup import setup_database
from report_gen import export_dataframe_to_csv, export_to_markdown

# Set Pandas display options for console output
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)        # Set console width to prevent line wrapping

def main():
    # Setup the database and get the dot items DataFrame
    merged_df = setup_database('data/dot_inv_template.csv')

    # Export the DataFrame to a CSV file
    export_dataframe_to_csv(merged_df, filename='_dotfiles_report.csv')

    # Export the DataFrame to a Markdown report using Jinja2
    export_to_markdown(
        df=merged_df,  # Pass the DataFrame explicitly
        template_path='data',
        template_file='rep_tp.jinja2',
        output_file='_dotfiles_report.md'  # Changed filename here
    )

if __name__ == "__main__":
    main()