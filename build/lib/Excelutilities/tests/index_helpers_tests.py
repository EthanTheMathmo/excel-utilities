import unittest
import Excelutilities
import random
from Excelutilities import index_helpers
from numpy import random

class TestTupleConversion(unittest.TestCase):
    def test_convert_to_tuple_small(self, convert_to_tuple=index_helpers.convert_to_tuple):
        """
        Implements a small number of tests for convert_to_tuple, but the tests 
        are checked to make sure they're all correct
        """
        self.assertEqual(convert_to_tuple("A1"), (1,1))
        self.assertEqual(convert_to_tuple("A100"), (1,100))
        self.assertEqual(convert_to_tuple("AZ36"), (52,36))
        self.assertEqual(convert_to_tuple("ZBG19"), (26**2*26+26**1*2+26**0*7,19))


    def test_convert_from_tuple_small(self, convert_from_tuple = index_helpers.convert_from_tuple):
        """
        Implements a small number of tests for the convert_from_tuple function, but the 
        tests are checked to make sure they're all correct
        """

        self.assertEqual(convert_from_tuple((26,1)), "Z1")

    def test_convert_from_and_to_tuple_large(self, convert_from_tuple = index_helpers.convert_from_tuple,
                    convert_to_tuple=Excelutilities.index_helpers.convert_to_tuple,
                    randint = random.randint):
        """
        Implements a large test of a probabilistic nature - checks that the output
        of convert_from_tuple followed by convert_to_tuple gives the same result
        """
        iterations = 1000
        max_num_1 = randint(50,8000)
        max_num_2 = randint(10,1000)
        random_numbers = [(randint(1,max_num_1), randint(1,max_num_2)) for i in range(iterations)]

        for x,y in zip([convert_to_tuple(convert_from_tuple(x)) for x in random_numbers], random_numbers):
            self.assertEqual(x,y)
            
    def test_int2base_small(self, int2base = index_helpers.int2base):
        iterations = 100
        maximum = 1000
        x = random.randint(27, maximum, size=(iterations))
        
        for element in x:
            self.assertEqual(int2base(26, element), 'Z')
            
    def test_convert_base_26_to_base_26_no_zero_small(self, convert_base_26_to_base_26_no_zero = index_helpers.convert_base_26_to_base_26_no_zero):
        self.assertEqual(convert_base_26_to_base_26_no_zero('C0D'), 'BZD')
        self.assertEqual(convert_base_26_to_base_26_no_zero('BA0'), 'AZZ')
        
        
    def test_convert_from_tuple_small(self, convert_from_tuple = index_helpers.convert_from_tuple):
        self.assertEqual(convert_from_tuple((1, 1)), 'A1')
        self.assertEqual(convert_from_tuple((26**2*1+26*2+3, 123)), 'ABC123')
    
    def test_block_to_list(self, block_to_list = index_helpers.block_to_list):
        self.assertEqual(block_to_list('$A$1:$B$2'), 'A1,A2,B1,B2')
        self.assertEqual(block_to_list('A1:B2'), 'A1,A2,B1,B2')

    def test_next_down(self, next_down=index_helpers.next_down):
        self.assertEqual(next_down("AZ1"), "AZ2")
        self.assertEqual(next_down("B6"), "B7")
        self.assertEqual(next_down("ZZ54"), "ZZ55")

       
    def test_next_down(self, next_along=index_helpers.next_along):
        self.assertEqual(next_along("AB6"), "AC6")
        self.assertEqual(next_along("D2"), "E2")
        self.assertEqual(next_along("ZZ36"), "AAA36")
        self.assertEqual(next_along("ZZA234"), "ZZB234")

    def test_is_row_block_bool(self, is_row_block_bool=index_helpers.is_row_block_bool):
        self.assertEqual(is_row_block_bool("A3,A4"),False)
        self.assertEqual(is_row_block_bool("A3,B3"),True)
        self.assertEqual(is_row_block_bool("A1,C1,B1"),True)
        self.assertEqual(is_row_block_bool("AA1,C1:Z1,AB1:AZ1"),True)
        self.assertEqual(is_row_block_bool("A3,B4"),False)
    
    def test_is_col_block_bool(self, is_col_block_bool=index_helpers.is_col_block_bool):
        self.assertEqual(is_col_block_bool('A1:A5,A6'), True)
        self.assertEqual(is_col_block_bool('B1:B12'), True)
        self.assertEqual(is_col_block_bool('A1:A5,A7'), False)
        self.assertEqual(is_col_block_bool("Z1:AA22"), False)
        self.assertEqual(is_col_block_bool('A7,A1:A5,A6'), True)



if __name__ == '__main__':
    unittest.main()
