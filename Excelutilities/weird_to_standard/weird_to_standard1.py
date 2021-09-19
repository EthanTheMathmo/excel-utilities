#see the example sheets
#This assumes we have data in rows, but for all data which shares an attribute, that attribute is written in the 
#row above, and in the same colour each time.
#We then process into a standard


def weird_to_standard1_array(rows, write_location):
    #rows should be an iterable from openpyxl obtained when you take a block of cells from a workbook
    #It returns the result as an array, rather than saving it as a new Excel workbook
    return