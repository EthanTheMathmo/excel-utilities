"""
Functions for data cleaning utilities, such as removing empty columns and rows


TO-DO. Probably would be better without the numpy dependency at some point,
ideally implement the list iteration using C, although for the time being we haven't 
had a noticeable time lag from python implementation on smallish (<1000 rows) workbooks
"""

import numpy as np

def remove_empty_rows_and_columns_ws(ws):
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
    
    return list(npa)
    
def remove_empty_rows_and_columns_array(data_array):
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
    
    return list(npa)

