from Excelutilities.workbook_debugging.interactive_wb_debugging_tools import compare_rows
import unittest

"""
TEST CURRENTLY FAILS
"""

class TestInteractiveWbDebugging(unittest.TestCase):
    def test_1_compare_rows(self):
        """
        Implements a small number of tests for convert_to_tuple, but the tests 
        are checked to make sure they're all correct
        """
        import pathlib
        import os
        wb_loc = os.path.join(pathlib.Path(__file__).parent.resolve(), "test_1_compare_rows.xlsx")
        correct_output = ["Ethan", "Oranges", "Banana"]
        self.assertEqual(compare_rows(wb_loc=wb_loc), ["Ethan", "Oranges", "Banana"])


if __name__ == "__main__":
    unittest.main()

