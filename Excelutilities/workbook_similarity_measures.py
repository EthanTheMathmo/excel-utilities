"""
This is for measures of similarities of two workbooks, which we use largely for debugging purposes
"""
import openpyxl
import numpy as np
import io

from Excelutilities.worksheet_cleaning_utilities import remove_empty_rows_and_columns_ws
import difflib
"""
TO-DO. 
-test to see which string algorithms have best speed / accuracy trade-off
-Perhaps experiment with graph similarity algorithm approach?
"""


# two helper functions
def replace_row(row):
    """
    replace a row with the string representation we are using
    """
    return ",".join([replace_string(cell_val) for cell_val in row])


def replace_string(x):
    """
    replace values with appropriate string substitutes
    """
    if type(x) == str:
        return x
    elif x == None:
        return " "
    else:
        return str(x)

"""
METHOD 1. Turn the ws into a csv format and use string similarity algorithms
"""

def similarity_values_only(book1, sheet1, book2, sheet2, 
            similarity_function=lambda x,y: difflib.SequenceMatcher(None, x,y).ratio()):
    books = [book1, book2]

    book_strings = []

    for book in books:
        xlsx_filename=book
        import csv
        with open(xlsx_filename, "rb") as f:
            #this needs to be done as well as wb.close to make sure the workbook doesnt get broken by saving and other actions

            in_mem_file = io.BytesIO(f.read())

        wb = openpyxl.load_workbook(in_mem_file, read_only=True)

        ws = wb["Sheet1"]

        no_empties = remove_empty_rows_and_columns_ws(ws)
        book_string = "\n".join([replace_row(row) for row in no_empties])
        book_strings.append(book_string)

    return similarity_function(book_strings[0], book_strings[1])

