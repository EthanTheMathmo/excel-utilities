"""
TO-DO:
-write tests
-error checking, e.g., columns being the same length etc
-sensible way of dealing with user selecting blocks rather than cols
"""


import xlwings as xw
import PySimpleGUI as sg
from Excelutilities.index_helpers import block_to_list, next_down
import os

def folder_address_gui():
        event, values = sg.Window("",[[sg.Text('Folder name')], [sg.Input(),sg.FolderBrowse()],
                [sg.OK(), sg.Cancel()]], no_titlebar=True, keep_on_top=True, grab_anywhere=True).read(close=True)
        return values[0]

def attach_data():
    sht = xw.apps.active.books.active.sheets.active

    range1, range2 = xw.apps.active.books.active.selection.address.split(",")

    layout = [[sg.Text("Folder"), sg.Input(visible=True), sg.FolderBrowse()],
            [sg.Button('Go'), sg.Button('Exit')]  ]

    event, values = sg.Window('Window Title', layout, no_titlebar=True, keep_on_top=True).read(close=True)
    
    file_folder = values[0]

    range2_as_list = block_to_list(range2).split(",")

    index=1
    for row_name, target_address in zip(sht.range(range1).value, range2_as_list):
        target_file = os.path.join(file_folder, row_name + ".pdf")
        if os.path.isfile(target_file): #only adds the link if the file exists
            sht[target_address].api.NoteText(target_file)
        sg.OneLineProgressMeter('Creating worksheet', index, len(range2_as_list), 'single')
        index+=1

def attach_data_method_2():
    """
    Method 2 is a bit more involved as it avoids the .api method and works on mac
    """
    
    macros_workbook_address = r"C:\Users\ethan\Documents\for_SATRO\data\EXCEL_WBs\MACROS_SHFX.xlam" #obviously, this needs to be adjustable
    
    create_comment = xw.Book(macros_workbook_address).macro(r'AddCommentToSpecificCell')
    
    sht = xw.apps.active.books.active.sheets.active

    active_book = xw.apps.active.books.active
    
    range1, range2 = active_book.selection.address.split(",")
    
    active_sheet = active_book.sheets.active
    
    if "," in range1 or "," in range2:
        #TO-DO. ERROR MESSAGE AS WE ONLY WANT THE USER TO ENTER RANGE AS SINGLE BLOCK
        return
    else:
        pass
    
    #names are the names we'll look for in files
    #write_address is the cell address we'll first write to, and then move down
    if ":" in range1 and ":" in range2:
        #TO-DO ERROR MESSAGE. ONE should be a row, one should be a single cell
        return
    elif ":" in range1 and ":" not in range2:
        names = sht.range(range1).value
        write_address = range2
    else:
        names = sht.range(range2).value
        write_address = range1     
    
    openable_file_types = [".pdf", ".txt", ".html", ".docx", ".img", ".jpeg", ".xlsm", ".csv"] #can add to this as needed
   

    names_with_no_file_found = []
    
    names_with_multiple_files_found = {}

    target_directory = folder_address_gui()

    if target_directory == "" or target_directory == None:
        #nothing entered. 
        # CHECK_FOR_MAC because 
        # titlebar is enabled on MAC, I don't know what is returned to target_directory
        #if that cross in the top right hand corner is used
        return
    
    names_to_files = {}

    for dirpath, dirnames, filenames in os.walk(target_directory):
        for filename in filenames:
            name = os.path.splitext(filename)[0]
            if name in names_to_files:
                names_to_files[name] += "\n" + os.path.join(dirpath,filename)
                names_with_multiple_files_found[name] = True
            else:
                names_to_files[name] = os.path.join(dirpath, filename)
                names_with_multiple_files_found[name] = False
    
    index=1
    
    for name in names:
        if name in names_to_files:
            create_comment(names_to_files[name], write_address)
            #sht.range(write_address).api.NoteText(names_to_files[name])
        else:
            names_with_no_file_found.append(name)
            
        write_address = next_down(write_address)
        sg.OneLineProgressMeter('Adding file information', index, len(names))
        index+=1