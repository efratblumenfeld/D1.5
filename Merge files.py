import os
import pandas as pd


def compile_csv_to_excel(folder_path):
    # Initialize an Excel writer object using pandas
    output_excel_path = os.path.join(folder_path, 'compiled_data.xlsx')
    writer = pd.ExcelWriter(output_excel_path, engine='openpyxl')

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a CSV file and follows the naming convention
        if filename.endswith('.csv') :
            # Read the CSV file
            file_path = os.path.join(folder_path, filename)
            data = pd.read_csv(file_path)

            # Use the filename (without extension) as the sheet name
            sheet_name = filename.replace('.csv', '')

            # Write the dataframe to a specific sheet
            data.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Added {filename} to the Excel file.")

    # Close the Excel writer to save the file
    writer.close()
    print(f"All data compiled into {output_excel_path}")


# Input the folder path from the user
user_input_folder_path = input("Enter the path to the folder containing the CSV files: ")

# Call the function with user provided path
compile_csv_to_excel(user_input_folder_path)
