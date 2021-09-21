import unittest
import os
import openpyxl
import io

from worksheet_cleaning_utilities import return_vals_input_openpyxl_ws_output_val_list
class TestTupleConversion(unittest.TestCase):
    #RUAIRIDH: when writing tests, the function name has to begin with test_<rest of name> for unittest.main() to find it
    def test_return_vals_input_openpyxl_ws_output_val_list(self):
        wb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_return_vals_input_openpyxl_ws_output_val_list.xlsx")
        xlsx_filename=wb_path
        with open(xlsx_filename, "rb") as f:
            #this needs to be done as well as wb.close to make sure the workbook doesnt get broken by saving and other actions
            
            in_mem_file = io.BytesIO(f.read())

        wb = openpyxl.load_workbook(in_mem_file, read_only=True)
        ws = wb["Sheet1"]
        vals=return_vals_input_openpyxl_ws_output_val_list(ws)
        comparison_list = [[1,2,3, None], ["Ethan", "Ashley", "Apricot", "Yes"]]
        self.assertEqual(vals, comparison_list)
        

if __name__ == '__main__':
    unittest.main()
