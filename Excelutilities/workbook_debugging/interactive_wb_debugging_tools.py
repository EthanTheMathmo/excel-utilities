"""
For interactive workbook debugging tools, where you actively select values from
workbooks
"""
import PySimpleGUI as sg
import xlwings as xw
import jellyfish
from Excelutilities.cleaning_utilities.worksheet_cleaning_utilities import remove_empty_rows_and_columns_input_val_list_output_val_list


def compare_rows(wb_loc = None):
    """
    Given two groups of rows this compares values from the first to the second, and returns a list of all values in the 
    first group of rows but not the second
    """
    if wb_loc != None:
        xw.Book(wb_loc)

    user_input_1 = sg.popup_ok_cancel('Please open the first workbook or sheet, and select the rows.\nPress ok when finished.')
    if user_input_1 == "OK":
        values1 = xw.apps.active.books.active.selection.value
    else:
        sg.popup("You have now terminated the application")
    user_input_2 = sg.popup_ok_cancel('Please open the second workbook or sheet, and select the rows.\nPress ok when finished.',
                                    keep_on_top=True)
    if user_input_2 == "OK":
        values2 = xw.apps.active.books.active.selection.value
    else:
        sg.popup("You have now terminated the application")
    user_input_3 = sg.popup_yes_no("Do you blank columns and rows to be removed?")
    if user_input_3 == "Yes":
        values1 = remove_empty_rows_and_columns_input_val_list_output_val_list(values1)
        values2 = remove_empty_rows_and_columns_input_val_list_output_val_list(values2)
    else:
        pass


    values1_as_set = set([tuple(row) for row in values1])
    values2_as_set = set([tuple(row) for row in values2])

    in_values1_but_not_values2 = []
    for row in values1:
        if tuple(row) not in values2_as_set:
            vals_ordered = sorted(values2, key=lambda x: jellyfish.damerau_levenshtein_distance(str(x), str(row)))
            response = sg.popup_yes_no(f"For row: {','.join([str(x) for x in row])}, is this the same as: {','.join([str(x) for x in vals_ordered[0]])}?",
                                        keep_on_top=True, grab_anywhere=True)
            if response == "Yes":
                pass
            else:
                in_values1_but_not_values2.append(row)
    return in_values1_but_not_values2

if __name__ == "__main__":
    compare_rows()