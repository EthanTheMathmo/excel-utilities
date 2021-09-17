"""
Functions for removing empty columns and rows

"""

import numpy as np

def remove_empty_rows_and_columns_ws(ws):
    """
    Given a worksheet, returns a numpy array with all empty rows and columns removed
    
    NOTE: Empty means no value, so ignores all formatting etc
    
    """
    npa=np.array([row for row in ws.values])
    boolean_nones = npa != None
    indices2=np.where(np.all(boolean_nones==False, axis=0))
    indices1=np.where(np.all(boolean_nones==False, axis=1))
    npa = np.delete(npa, indices1, axis=0)
    npa = np.delete(npa, indices2, axis=1)
    
    return npa
    
def remove_empty_rows_and_columns_array(data_array):
    """
    Given a data_array, returns a numpy array with all empty rows and columns removed, (empty: the value is None)
    
    NOTE: Empty means no value, so ignores all formatting etc
    
    """
    npa=np.array([row for row in data_array])
    boolean_nones = npa != None
    indices2=np.where(np.all(boolean_nones==False, axis=0))
    indices1=np.where(np.all(boolean_nones==False, axis=1))
    npa = np.delete(npa, indices1, axis=0)
    npa = np.delete(npa, indices2, axis=1)
    
    return npa

def replace_row(row):
    return ",".join([replace_string(cell_val) for cell_val in row])


def replace_string(x):
    if type(x) == str:
        return x
    elif x == None:
        return " "
    else:
        return str(x)