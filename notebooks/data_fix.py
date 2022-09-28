###################################################################################
# The purpose of this script is to preprocess the given car data
#   It does so by using an initial sanitization sweep
#   Then it uses individual sanitize processors for the different columns
#
# Contributors:
#   Christopher J. Watson
#   Bin Lu
#   Maimuna Bashir
###################################################################################

import re
import tkinter as tk
from tkinter import filedialog
import csv
import pandas as pd
from IPython.display import display

# This dictionary stores the sanitize functions
sanitize_dict = {}


# Column Sanitize Functions
def id_col_preprocess(value):
    regex = "[^0-9]"
    clean_str = re.sub(regex, '', value)
    return clean_str


def price_levy_col_preprocess(value):
    regex = "[^0-9]"
    clean_str = re.sub(regex, '', value)
    if not clean_str and not clean_str.strip():
        clean_str = "0"
    return clean_str


def manuf_preprocess(value):
    clean_str = str(value).upper()
    clean_str = clean_str.strip()
    return clean_str


def model_preprocess(value):
    clean_str = str(value).upper()
    clean_str = clean_str.strip()
    clean_str = clean_str.replace(',', '.')
    clean_str = clean_str.replace('9-MAR', '9-3')
    return clean_str


def engine_col_preprocess(value):
    clean_str = [value, '']
    return clean_str


def do_nothing(value):
    # print("not implemented")
    return value


# Initialization Measures
def init():
    global sanitize_dict
    # add all definitions
    sanitize_dict = {'ID': id_col_preprocess, 'Price': price_levy_col_preprocess, 'Levy': price_levy_col_preprocess,
                     'Manufacturer': manuf_preprocess, 'Model': model_preprocess, 'Prod_year': do_nothing,
                     'Category': do_nothing, 'Leather_interior': do_nothing, 'Fuel_type': do_nothing,
                     'Engine_volume': engine_col_preprocess, 'Mileage': do_nothing, 'Cylinders': do_nothing,
                     'Gear_box_type': do_nothing, 'Drive_wheels': do_nothing, 'Doors': do_nothing, 'Wheel': do_nothing,
                     'Color': do_nothing, 'Airbags': do_nothing}


# File Scrubbing Function
def scrub_txt_file():
    # THIS SECTION SCRUBS SPECIAL CHARACTERS FROM THE ENTIRE FILE
    # get the file path
    # init windows stuff
    root = tk.Tk()
    root.withdraw()
    print("Asking for original data file path")
    file_path = filedialog.askopenfilename()
    print("Replacing all special characters for clean read")
    bad_string = open(file_path, encoding="utf8").read()
    # create regex that only gets basic characters
    regex = "[^a-zA-Z0-9\n\.\,\-\"]"
    clean_str = re.sub(regex, ' ', bad_string)
    # write out sanitized file
    print("Asking for cleaned data file save location")
    clean_file = save_file_string(clean_str)
    print("Printing save location:")
    print(clean_file)

    # THIS SECTION CALLS THE SANITIZE METHODS
    # create working variables
    first_row = True
    df_1 = []
    tmp_a_1 = []
    # open the cleaner file for processing
    with open(clean_file, 'rt', encoding="utf8") as f:
        # list to store the names of columns
        list_of_column_names = []
        reader = csv.reader(f, skipinitialspace=True, quotechar='"')
        # loop to iterate through the rows of csv
        for xrow in reader:
            if first_row:
                # adding the first row header
                for col in xrow:
                    col = col.replace(' ', '_')
                    col = col.replace('.', '')
                    list_of_column_names.append(col)
                list_of_column_names.append("Turbo")
                # set the flag to continue
                first_row = False
            else:
                # create a storing dictionary
                temp_values = {}
                row_temp = xrow
                # sort the columns through the various preprocessors
                for xcol in range(len(list_of_column_names)-1):
                    if list_of_column_names[xcol] == 'Engine_volume':
                        # account for turbo expansion
                        t1 = sanitize_dict[list_of_column_names[xcol]](row_temp[xcol])
                        temp_values[list_of_column_names[xcol]] = t1[0]
                        temp_values[list_of_column_names[len(list_of_column_names)-1]] = t1[1]
                    else:
                        temp_values[list_of_column_names[xcol]] = \
                            sanitize_dict[list_of_column_names[xcol]](row_temp[xcol])
                # add dictionary to dictionary list
                # Account for empty manufacturing slots by using the model
                if not temp_values["Manufacturer"] and not temp_values["Manufacturer"].strip():
                    temp_values["Manufacturer"] = sanitize_dict["Manufacturer"](temp_values["Model"])
                tmp_a_1.append(temp_values)
        # move it all to a panda dataframe
        df_1 = pd.json_normalize(tmp_a_1)
        # make final outfile
        final_out = clean_file[:-4] + "_final.csv"
        # create final CSV
        df_1.to_csv(final_out)
        print(final_out)
        # return data for usage in other applications
        return df_1


# General Save Function
def save_file_string(out_string):
    fd = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if fd is None:
        return
    fd.write(out_string)
    fd.close()
    return fd.name


def main():
    # sets up the variables needed for run
    print("Setting Up Variables")
    init()
    print("Entering Scrubbing Methods")
    # scrub the output
    display(scrub_txt_file())


if __name__ == "__main__":
    main()
