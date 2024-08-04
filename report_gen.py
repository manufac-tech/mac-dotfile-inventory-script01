import pandas as pd

def export_dataframe_to_csv(df, filename='output.csv'):
    """
    Export the DataFrame to a CSV file.
    
    Args:
        df (DataFrame): The DataFrame to export.
        filename (str): The filename for the CSV file.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"DataFrame exported to '{filename}'")
    except Exception as e:
        print(f"Failed to export DataFrame to CSV: {e}")