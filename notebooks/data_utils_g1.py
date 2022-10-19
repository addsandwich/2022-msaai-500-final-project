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