import unittest
import Excelutilities
import random
from Excelutilities import index_helpers
from numpy import random

class TestTupleConversion(unittest.TestCase):
    #RUAIRIDH: when writing tests, the function name has to begin with test_<rest of name> for unittest.main() to find it
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
        
    
        

if __name__ == '__main__':
    unittest.main()
