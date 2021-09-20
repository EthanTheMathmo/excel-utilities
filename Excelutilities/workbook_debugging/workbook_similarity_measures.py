"""
This is for measures of similarities of two workbooks, which we use largely for debugging purposes
"""
import openpyxl
import numpy as np
import io

from Excelutilities.cleaning_utilities.worksheet_cleaning_utilities import remove_empty_rows_and_columns_ws
import difflib
"""
TO-DO. 
-test to see which string algorithms have best speed / accuracy trade-off
-Perhaps experiment with graph similarity algorithm approach?
"""


"""
LITERAL EQUIVALENCE
"""
def literally_the_same_empties_deleted(wb1, sheetname1, wb2, sheetname2):
    #checks if two sheets are identical, after removing empty rows and columns
    ws1 = wb1[sheetname1]
    ws2 = wb2[sheetname2]
    data_1 = remove_empty_rows_and_columns_ws(ws1)
    data_2 = remove_empty_rows_and_columns_ws(ws2)
    return data_1==data_2




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

def similarity_values_only(book1, sheetname1, book2, sheetname2, 
            similarity_function=lambda x,y: difflib.SequenceMatcher(None, x,y).ratio()):
    books = [book1, book2]

    book_strings = []

    sheets = [sheetname1, sheetname2]

    for book, sheet in zip(books, sheets):
        xlsx_filename=book
        import csv
        with open(xlsx_filename, "rb") as f:
            #this needs to be done as well as wb.close to make sure the workbook doesnt get broken by saving and other actions

            in_mem_file = io.BytesIO(f.read())

        wb = openpyxl.load_workbook(in_mem_file, read_only=True)

        ws = wb[sheet]

        no_empties = remove_empty_rows_and_columns_ws(ws)
        book_string = "\n".join([replace_row(row) for row in no_empties])
        book_strings.append(book_string)

    return similarity_function(book_strings[0], book_strings[1])

"""METHOD 2:
AVERAGE DISTACE

What this does is take two worksheets, and given the first, iterates through its
values and calculates the distance to that value on the second, sums up and averages
in a sensible way. It then does this in reverse, so returns a tuple, one for comparing
the first sheet to the second, and one for comparing the second to the first
"""

#Helper functions for METHOD 2. Also borrows some helper functions from METHOD 1

###START OF HELPER FUNCTIONS FOR METHOD 2

def calculate_average_val_distance(dict1, dict2, default_val_for_non_matches, max_distance):
    """
    Given two dictionaries, dict1 and dict2, where the dictionarys map values to an array of indices, this iterates through
    values in dict1, and gets the closest distance to a value in 
    """

    total=0
    for val1 in dict1.keys():
        if val1 == None:
            #currently we skip comparing empty entries
            continue
        else:
            if val1 in dict2.keys():
                for index1 in dict1[val1]:
                    total+=min(min(abs(coord[0]-index1[0])+abs(coord[1]-index1[1]) for coord in dict2[val1]),max_distance)
                else:
                    total+= default_val_for_non_matches
    return total

def convert_array_to_values_to_indices(data_array):
    """
    Given an array of values, this converts it to a dictionary which maps from values to a list of indices where 
    the value appears
    """
    return_dict ={}
    for j, row in enumerate(data_array):
        for i, val in enumerate(row):
            if val in return_dict:
                return_dict[val].append((i,j))
            else:
                return_dict[val] = [(i,j)]
                
    return return_dict

###END OF HELPER FUNCTIONS FOR METHOD 2

def avg_val_distance_similarity(book1, sheetname1, book2, sheetname2, default_val_for_non_matches, max_distance=None):
    """
    Given two sheets, calculates the distance_val_similarity method of the first to the second, and the second to the first
    (which are not necessarily the same)
    
    This is calculated by taking the sheets, removing empties, and turning into a dictionary mapping from values to 
    indices. We then calculate the closest distance between a value in the first and the second sheet
    
    The results are summed (with the default val for non matches set by the user), and normalised by the number
    of non-empty entries
    
    Max distance is for the maximum distance between two entries, so large ones don't skew things too much
    """
    if max_distance==None:
        max_distance = default_val_for_non_matches
    
    sheets = [sheetname1, sheetname2]
    
    books = [book1, book2]
    
    as_arrays = []

    size_including_empty_cells_but_after_empty_rows_and_cols_removed = [] #i.e. strip empty rows and cols, and multiply 
                                            #width  by height
    
    size_excluding_all_empties = [] #i.e. take the values above and subtract from it the number of empty cells
    
    for book, sheet in zip(books, sheets):
        xlsx_filename=book
        import csv
        with open(xlsx_filename, "rb") as f:
            #this needs to be done as well as wb.close to make sure the workbook doesnt get broken by saving and other actions

            in_mem_file = io.BytesIO(f.read())

        wb = openpyxl.load_workbook(in_mem_file, read_only=True)

        ws = wb[sheet]

        no_empties = remove_empty_rows_and_columns_ws(ws)

        as_arrays.append(no_empties)
        
    #now calculate the size including empty cells but excluding empty rows and columns
    for data in as_arrays:
        size_including_empty_cells_but_after_empty_rows_and_cols_removed.append(len(data[0])*len(data)) #assums the data is a regular block
        
    #calculate the dictionaries mapping values to indices
    dict1 = convert_array_to_values_to_indices(as_arrays[0])
    dict2 = convert_array_to_values_to_indices(as_arrays[1])
    
    #calculate the size excluding empties
    for size, val_dict in zip(size_including_empty_cells_but_after_empty_rows_and_cols_removed, [dict1, dict2]):
        size_excluding_all_empties.append(size-len(val_dict[None]))
    
    return_vals = []
                                          
    #and calculate the normalised return values
    for size, dicts in zip(size_excluding_all_empties, [(dict1,dict2), (dict2, dict1)]):
        return_vals.append(calculate_average_val_distance(dict1=dicts[0], dict2=dicts[1],
                                                          default_val_for_non_matches=default_val_for_non_matches,
                                                         max_distance=max_distance)/size)
      
    
    return tuple(return_vals)
