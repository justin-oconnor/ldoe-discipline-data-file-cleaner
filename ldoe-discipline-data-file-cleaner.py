# Import necessary libraries
import os
import pandas as pd
import glob

# Defines a dictionary to map sheet names to their corresponding variable column names in the raw discipline data files.
SHEETS_AND_VARIABLES = {
        'Gender': 'Gender',
        'Ethnicity': 'Ethnicity',
        'SWD': 'Special Education Status',
        'ED': 'Economically Disadvantaged',
        'EL': 'English Learner Status',
        '504': '504 Status',
        'Homeless': 'Homeless Status',
        'Grade': 'Grade'
    }

# Defines function to strip header rows and rename columns for LDOE
# discipline files. The function takes in the number of header rows to skip,
# a folder path of files to clean, a destination path for the cleaned files,
# the desired sheet name to clean, and a suffix for the output filenames.
# The function will detect the number of columns in the file (13, in line with
# older LDOE data releases, or 14 for the newer ones) and rename them accordingly.
# It assumes the 13-column files are missing the 'Level' column. Sheets with column
# numbers other than 13 or 14 will be skipped with a console message.

def clean_file(header_rows, file_list, destination_path, sheet, suffix):
    for file in file_list:
        df = pd.read_excel(file, sheet_name=sheet, skiprows=header_rows)
        if len(df.columns) == 14:
            df.columns = [
                'Level',
                'LEA Code',
                'LEA Name',
                'Site Code',
                'Site Name',
                SHEETS_AND_VARIABLES[sheet],
                'In-School Suspension - Count',
                'In-School Suspension - Percent',
                'Out of School Suspension - Count', 
                'Out of School Suspension - Percent', 
                'In-School Expulsion - Count',
                'In-School Expulsion - Percent', 
                'Out of School Expulsion - Count', 
                'Out of School Expulsion - Percent'
                ]

            raw_filename = os.path.basename(file)
            input_years = '-'.join(raw_filename.split('-', 2)[:2])
            output_filename = f'{input_years}-{suffix}.csv' 

            df.to_csv(os.path.join(destination_path, output_filename), index=False)
            print(f'Cleaned file: {output_filename}')

        elif len(df.columns) == 13:
            df.columns = [
                'LEA Code',
                'LEA Name',
                'Site Code',
                'Site Name',
                SHEETS_AND_VARIABLES[sheet],
                'In-School Suspension - Count',
                'In-School Suspension - Percent',
                'Out of School Suspension - Count', 
                'Out of School Suspension - Percent', 
                'In-School Expulsion - Count',
                'In-School Expulsion - Percent', 
                'Out of School Expulsion - Count',
                'Out of School Expulsion - Percent'
                ]

            raw_filename = os.path.basename(file)
            input_years = '-'.join(raw_filename.split('-', 2)[:2])
            output_filename = f'{input_years}-{suffix}.csv'

            df.to_csv(os.path.join(destination_path, output_filename), index=False)
            print(f'Cleaned file: {output_filename}')

        else:
            print(f"Unexpected number of columns in file {file} (not 13 or 14). Skipping this file.")

# Defines function to get a list of all .xlsx files in the specified path for cleaning.
# Only works with .xlsx files.
def path_to_clean(path):
    file_list = glob.glob(f'{path}/*.xlsx')
    return file_list

# Main function to prompt user for input and call the cleaning functions.
def main():
    path = input("Enter the path to the directory containing the files: ")
    header_rows = int(input("Enter the number of header rows to skip: "))
    destination_path = input("Enter the destination path for cleaned files: ")
    sheet = input("Enter the exact sheet name (Gender, Ethnicity, SWD, ED, EL, 504, Homeless, Grade): ")
    suffix = input("Enter the suffix for the output filenames (YYYY-YYYY-suffix.csv): ")

    file_list = path_to_clean(path)

    clean_file(header_rows, file_list, destination_path, sheet, suffix)

# Run the main function if this script is executed directly.
if __name__ == "__main__":
    main()