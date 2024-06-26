import os
import pandas as pd
import subprocess

def delete_files_starting_with(prefix):
    # Get the current working directory or specify a directory path
    directory = '.' # Change this to your specific directory if needed
    print(directory)
    try:
        files_to_delete = [filename for filename in os.listdir(directory) if filename.startswith(prefix)]
        
        if files_to_delete:
            for filename in files_to_delete:
                os.remove(os.path.join(directory, filename))
                print(f"Deleted: {filename}")
        else:
            print(f"No files found starting with '{prefix}', nothing deleted.")

    except OSError as e:
        print(f"Error: {e.strerror}")


def read_xls(prefix):
    directory =  '.'

    # Find the file that starts with the given prefix
    file_to_read = next((filename for filename in os.listdir(directory) if filename.startswith(prefix)), None)
    
    if file_to_read:
        file_path = os.path.join(directory, file_to_read)
        # Read the Excel file into a DataFrame, including the header from the first row
        df = pd.read_excel(file_path, header=0)
        return df
    else:
        print(f"No Excel file found starting with '{prefix}'.")
        return None
    
def compare(df1, df2):
    missing_RMA = df1[~df1['Order No'].isin(df2['RMA #'])]['Order No']

    file_path =  './未登记订单.txt'

    # Write missing values to a text file
    with open(file_path, 'w') as file:
        for value in missing_RMA:
            file.write(value + '\n')


if __name__ == "__main__":

    ezeeship_prefix = "Shipment_Information(by order)(all)"
    shipout_prefix = "WMS_Return_Export"
    delete_files_starting_with(ezeeship_prefix)
    delete_files_starting_with(shipout_prefix)
    delete_files_starting_with('未登记订单（In Transit）')

    process1 = subprocess.Popen(["python", "EzeeShip.py"])
    process2 = subprocess.Popen(["python", "shipout-test.py"])

    process1.wait()
    process2.wait()

    ezeeship_df = read_xls(ezeeship_prefix)
    shipout_df = read_xls(shipout_prefix)

    compare(ezeeship_df, shipout_df)


