"""
For interactive workbook debugging tools, where you actively select values from
workbooks
"""
import PySimpleGUI as sg
import xlwings as xw
import jellyfish
from Excelutilities.workbook_debugging.worksheet_cleaning_utilities import remove_empty_rows_and_columns_array


def compare_rows():
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
        values1 = remove_empty_rows_and_columns_array(values1)
        values2 = remove_empty_rows_and_columns_array(values2)
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
    print(in_values1_but_not_values2)
    return in_values1_but_not_values2

compare_rows()