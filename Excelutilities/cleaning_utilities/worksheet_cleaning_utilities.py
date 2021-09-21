"""
Functions for data cleaning utilities, such as removing empty columns and rows

TO-READ: The cleaning is different depending on the desired input and output. The input can be 
a list of values, an openpyxl worksheet, or an openpyxl iterable of cells. 

TO-DO. Probably would be better without the numpy dependency at some point,
ideally implement the list iteration using C, although for the time being we haven't 
had a noticeable time lag from python implementation on smallish (<1000 rows) workbooks
"""

import numpy as np
import openpyxl
def return_vals_input_openpyxl_ws_output_val_list(ws):
    """
    Input: an openpyxl worksheet
    Output: a list of values for that worksheet
    """
    return [list(row) for row in ws.values]


def remove_empty_rows_and_columns_input_openpyxl_iterable_output_cell_list(ws_block):
    """
    Input: an iterable of openpyxl cells (NOT an openpyxl worksheet)
    Output: a list of the values of the iterable, with empty rows and columns removed
    """
    npa_val=np.array([[cell.value for cell in row] for row in ws_block])
    npa = np.array([[cell for cell in row] for row in ws_block])
    boolean_nones = npa_val != None
    indices2=np.where(np.all(boolean_nones==False, axis=0))
    indices1=np.where(np.all(boolean_nones==False, axis=1))
    npa = np.delete(npa, indices1, axis=0)
    npa = np.delete(npa, indices2, axis=1)
    
    return list(npa)

def remove_empty_rows_and_columns_input_ws_output_val_list(ws):
    """
    Given a worksheet, returns a list with all empty rows and columns removed
    
    NOTE: Empty means no value, so ignores all formatting etc
    """

    npa=np.array([row for row in ws.values])
    boolean_nones = npa != None
    indices2=np.where(np.all(boolean_nones==False, axis=0))
    indices1=np.where(np.all(boolean_nones==False, axis=1))
    npa = np.delete(npa, indices1, axis=0)
    npa = np.delete(npa, indices2, axis=1)
    
    return [list(row) for row in npa]
    
def remove_empty_rows_and_columns_input_val_list_output_val_list(data_array):
    """
    Given a data_array, returns a list with all empty rows and columns removed, (empty: the value is None)
    
    NOTE: Empty means no value, so ignores all formatting etc
    
    """
    npa=np.array([row for row in data_array])
    boolean_nones = npa != None
    indices2=np.where(np.all(boolean_nones==False, axis=0))
    indices1=np.where(np.all(boolean_nones==False, axis=1))
    npa = np.delete(npa, indices1, axis=0)
    npa = np.delete(npa, indices2, axis=1)
    
    return [list(row) for row in npa]