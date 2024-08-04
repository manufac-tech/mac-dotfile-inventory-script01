from dbase_setup import setup_database
from report_gen import export_dataframe_to_csv

def main():
    # Setup the database and get the dot items DataFrame
    df = setup_database()

    # Export the DataFrame to a CSV file using the new function
    export_dataframe_to_csv(df, filename='_dotfiles_report.csv')

if __name__ == "__main__":
    main()