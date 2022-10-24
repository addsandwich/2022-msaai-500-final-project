###################################################################################
# The purpose of this script is to have utils for group 1 of MSAAI-500 to use
#   to manipulate data more easily
#
# Contributors:
#   Christopher J. Watson
#   Bin Lu
#   Maimuna Bashir
###################################################################################

import tkinter as tk
from tkinter import filedialog
import json
import numpy as np

def load_py_dict():
    print("Asking for dictionary data file path")
    data = ''
    file_path = open_file_general()
    with open(file_path) as f:
        data = f.read()
    dict_res = json.loads(data)
    return dict_res


def save_py_dict(data_dict):
    root = tk.Tk()
    root.withdraw()
    print("Asking for dictionary save file path")
    json_object = json.dumps(data_dict, indent=4)
    fd = filedialog.asksaveasfile(mode='w', defaultextension=".json")
    if fd is None:
        return
    fd.write(json_object)
    fd.close()
    return fd.name


# General Save Function
def save_file_string(out_string):
    fd = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if fd is None:
        return
    fd.write(out_string)
    fd.close()
    return fd.name


# General file open dialog
def open_file_general():
    # init windows stuff
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def create_enum_dict(unique_list):
    res_dict = {}
    for i in range(len(unique_list)):
        res_dict[str(i)]=unique_list[i]
    return res_dict


# DON'T USE
# Removing the outliers using IRQ
def iqr_outliers(data, col):
    Q3 = np.quantile(data[col], 0.75)
    Q1 = np.quantile(data[col], 0.25)
    IQR = Q3 - Q1

    outlier_free_list = 0
    filtered_data = 0

    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR
    outlier_free_list = [x for x in data[col] if (
            (x > lower_range) & (x < upper_range))]
    filtered_data = data.loc[data[col].isin(outlier_free_list)]
    return filtered_data


# This is our decided outlier removal method
# This is a quantile based capping and flooring method
# This simple method seems to be the best out of all of our other attempts
def remove_outliers2(data, col):
    Q3 = np.quantile(data[col], 0.99985)
    Q1 = np.quantile(data[col], 0.00015)
    
    lower_range = Q1
    upper_range = Q3
    filtered_data = 0
    outlier_free_list = 0
    
    outlier_free_list = [x for x in data[col] if (
        (x > lower_range) & (x < upper_range))]
    filtered_data = data.loc[data[col].isin(outlier_free_list)]
    
    return Q3, Q1, filtered_data


def random_mean_sample(data, group_size):
    n = group_size
    a = len(data)
    b = int(len(data) / n)
    res = []
    for i in range(b):
        x = 0
        temp = n if a >= i * n + n else a - i * n
        for j in range(temp):
            x += data.iloc[n * i + j]
        res.append(int(x / temp))
        res.sort()
    return res
