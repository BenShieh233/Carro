import os
import pandas as pd
import subprocess
from tabulate import tabulate

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))


def read_args(file_path = None):
    if file_path is None:
        file_path = os.path.join(get_script_directory(), 'args.txt')
    params = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(' = ', 1)
                params[key] = value
    return params 

def delete_files_starting_with(prefix):
    # Get the current working directory or specify a directory path
    directory = get_script_directory() # Change this to your specific directory if needed
    # print(directory)
    try:
        files_to_delete = [filename for filename in os.listdir(directory) if filename.startswith(prefix)]
        
        if files_to_delete:
            for filename in files_to_delete:
                os.remove(os.path.join(directory, filename))
                print(f"已删除文件: {filename}")
        else:
            print(f"并未找到以 '{prefix}'为前缀的文件，删除终止")

    except OSError as e:
        print(f"Error: {e.strerror}")


def read_xls(prefix):
    directory = get_script_directory()

    # Find the file that starts with the given prefix
    file_to_read = next((filename for filename in os.listdir(directory) if filename.startswith(prefix)), None)
    
    if file_to_read:
        file_path = os.path.join(directory, file_to_read)
        # Read the Excel file into a DataFrame, including the header from the first row
        df = pd.read_excel(file_path, header=0)
        return df
    else:
        print(f"未找到以 '{prefix}'为前缀的文件名")
        return None

    
def check_value(df1, df2):
    def is_contained(order_no):
        order_no_lower = order_no.lower() # 统一把"-return"后缀转为小写
        return any(order_no_lower in str(rma).lower() for rma in df2['RMA #'])
    # 找到已经登记在df1但没有登记到df2的订单编号
    mask = df1['Order No'].apply(lambda x: not is_contained(x))
    missing_values_df = df1[mask][['Order No', 'Tracking ID', 'Reference', 'Reference2']]
    return missing_values_df

if __name__ == "__main__":
    script_dir = get_script_directory()
    print(read_args())


# if __name__ == "__main__":

#     ezeeship_prefix = "Shipment_Information(by order)(all)"
#     shipout_prefix = "WMS_Return_Export"
#     delete_files_starting_with(ezeeship_prefix)
#     delete_files_starting_with(shipout_prefix)
#     delete_files_starting_with('未登记订单（In Transit）')

#     script_dir = get_script_directory()
#     ezeeship_script = os.path.join(script_dir, "EzeeShip.py")
#     shipout_script = os.path.join(script_dir, "shipout.py")

#     process1 = subprocess.Popen(["python", ezeeship_script])
#     process2 = subprocess.Popen(["python", shipout_script])

#     process1.wait()
#     process2.wait()

#     ezeeship_df = read_xls(ezeeship_prefix)
#     shipout_df = read_xls(shipout_prefix)

#     file_path =  os.path.join(script_dir, '未登记订单.txt')

#     # Write missing values to a text file
#     with open(file_path, 'w') as file:
#         file.write(tabulate(check_value(ezeeship_df, shipout_df), headers = 'keys', tablefmt='grid'))
#     print('已打印所有未登记订单')

