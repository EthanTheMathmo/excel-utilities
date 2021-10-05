"""
These are helper functions for when we have rows or columns in one spreadsheet we want 
to bring across into another
"""
import xlwings as xw
import PySimpleGUI as sg
import sys
from Excelutilities.index_helpers import is_col_block_bool,  is_row_block_bool
import decimal
import datetime

def add_col_data_from_another_sheet(col_name_1, col_name_2, allowed_data_types=[float, int, decimal.Decimal,datetime.datetime, str]):
    """
    Let col_name_1 be some column with some attribute col_name_2. We then want to add 
    the values of col_name_2 from one sheet to a second sheet

    allowed_data_types is to restrict the types values can take.
    """

    sg.popup_ok(f"Please select the input {col_name_1} and click 'ok' when finished")
    input_col_name_1 = xw.apps.active.books.active.selection.value
    input_col_name_1_address = xw.apps.active.books.active.selection.address
    sg.popup_ok(f"Please select the input {col_name_2} and click 'ok' when finished")
    active_cells = xw.apps.active.books.active.selection
    input_col_name_2 = active_cells.value
    input_col_name_2_address = active_cells.address


    def sanity_check_col_entries(entry1, entry2, addresses_and_names):
        #entry1 is a list of values
        #addresses_and_names is a list of tuples, first entry of tuple
        #is the address, and second is the name
        #implements some sanity checks
        if len(entry1) != len(entry2):
            sg.popup("Oops! Your two input columns of data are of different lengths.\nNow terminating...")
            sys.exit()


        for val1, val2 in zip(entry1, entry2):
            if type(val1) not in allowed_data_types and val1 != None:
                sg.popup(f"Oops you selected some data which we couldn' recognise\nValue: {val1}")
                sys.exit()

            if type(val2) not in allowed_data_types and val2 != None:
                sg.popup(f"Oops you selected some data which we couldn' recognise\n{val2}\n{type(val2)}")
                sys.exit()
        
        for address_and_name in addresses_and_names:
            address = address_and_name[0]
            name = address_and_name[1]
            if not is_col_block_bool(address):
                print(address)
                sg.popup(f"Oops! Your {name} data wasn't from a single column")
                sys.exit()

    #sanity checks
    sanity_check_col_entries(entry1=input_col_name_1, entry2=input_col_name_2, 
                addresses_and_names=[(input_col_name_1_address, "col_name_1"),(input_col_name_2_address, "col_name_2")])





        


    col_name_1_to_col_name_2 = {}
    for val1, val2 in zip(input_col_name_1, input_col_name_2):
        col_name_1_to_col_name_2[val1] = val2
        

    sg.popup_ok("Please select the output col_name_1s and click 'ok' when finished")
    output_col_name_1 = xw.apps.active.books.active.selection.value


    def helper_col_name_1(x):
        if x in col_name_1_to_col_name_2:
            return col_name_1_to_col_name_2[x]
        else:
            return None
    output_array = [[helper_col_name_1(val1)] for val1 in output_col_name_1]

    sg.popup_ok(f"Please select the output location for the {col_name_2} and click ok when finished\nThis should be the same length as your input {col_name_1} data!")
    xw.apps.active.books.active.selection.value = output_array

