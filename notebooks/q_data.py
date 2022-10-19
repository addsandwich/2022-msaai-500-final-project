###################################################################################
# The purpose of this script is to quanitize the sanitized data
#
# Contributors:
#   Christopher J. Watson
#   Bin Lu
#   Maimuna Bashir
###################################################################################
import re
import csv
import pandas as pd
import data_utils_g1 as du

# This dictionary stores the sanitize functions
sanitize_dict = {}

def do_nothing(value):
    # print("not implemented")
    return value






# Initialization Measures
def init():
    global sanitize_dict
    # add all definitions
    sanitize_dict = {'ID': do_nothing, 'Price': do_nothing, 'Levy': do_nothing,
                     'Manufacturer': do_nothing, 'Model': do_nothing,
                     'Prod_year': do_nothing,
                     'Category': do_nothing, 'Leather_interior': do_nothing,
                     'Fuel_type': do_nothing,
                     'Engine_volume': do_nothing, 'Mileage': do_nothing,
                     'Cylinders': do_nothing,
                     'Gear_box_type': do_nothing, 'Drive_wheels': do_nothing, 'Wheel': do_nothing, 'Doors': do_nothing,
                     'Color': do_nothing, 'Airbags': do_nothing}





def main():
    # sets up the variables needed for run
    print("Setting Up Variables")
    init()
    print("Entering Scrubbing Methods")
    # scrub the output


if __name__ == "__main__":
    main()