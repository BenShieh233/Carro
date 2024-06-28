from EzeeShip import ezeeship_driver
from shipout import shipout_driver
from search import delete_files_starting_with, read_xls, check_value, get_script_directory
import threading
from tabulate import tabulate
import os

ezeeship_prefix = "Shipment_Information(by order)(all)"
shipout_prefix = "WMS_Return_Export"

if __name__ == "__main__":

    delete_files_starting_with(ezeeship_prefix)
    delete_files_starting_with(shipout_prefix)
    delete_files_starting_with('未登记订单')

    # Create threads for each function
    thread1 = threading.Thread(target=ezeeship_driver)
    thread2 = threading.Thread(target=shipout_driver)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    ezeeship_df = read_xls(ezeeship_prefix)
    shipout_df = read_xls(shipout_prefix)

    script_dir = get_script_directory()
    file_path =  os.path.join(script_dir, '未登记订单.txt')

    # Write missing values to a text file
    with open(file_path, 'w') as file:
        file.write(tabulate(check_value(ezeeship_df, shipout_df), headers = 'keys', tablefmt='grid'))
    print('已打印所有未登记订单')
