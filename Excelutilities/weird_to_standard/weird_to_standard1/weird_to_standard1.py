import xlwings as xw
import openpyxl
from Excelutilities.cleaning_utilities.worksheet_cleaning_utilities import remove_empty_rows_and_columns_input_openpyxl_iterable_output_cell_list
def weird_to_standard1_array(ws_block, color_hex, color_hex_set=False, search_breadth=1, delete_empties=True):
    #ws_block should be an openpyxl iterable
    #color_hex  is the color which marks out the special attribute (this is obvious from looking at
    # the example workbook), but it is also possible to pass in to color_hex_set in which 
    # case several colors can mark out the special category

    #search_breadth is how far along a row we will look for the special character

    #currently deletes empty rows and columns by default
    if delete_empties == True:
        ws_block = remove_empty_rows_and_columns_input_openpyxl_iterable_output_cell_list(ws_block)
    
    return_list = []
    current_special_val = None
    for row in ws_block:
        row_contains_special = False
        return_row = []
        return_row.append(current_special_val)
        for j, cell in enumerate(row):
            if j < search_breadth:
                if cell.font != None:
                    if cell.font.color != None:
                        if color_hex_set == False:

                            #one target value
                            if cell.font.color.rgb == color_hex:
                                #means it is a project title
                                current_special_val = cell.value
                                row_contains_special=True

                        else:
                            if cell.font.color.rgb in color_hex_set:
                                current_special_val = cell.value
                                row_contains_special=True
            if row_contains_special == True:
                break #skips to next row - no need to write anything or read any more cells
            else:
                return_row.append(cell.value)
        if row_contains_special == True:
            continue
        else:
            return_list.append(return_row)
    
    return return_list
        

