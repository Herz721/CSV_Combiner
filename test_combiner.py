"""This file is used for unit test, includes:
test of invalid input,
test of empty file,
test of non exist file
test of multiple csv files,
test of large files,
test of files with different columns
"""

import unittest
from unittest import mock
from CSV_Combiner import CSV_Combiner
import generatefixtures
import pandas as pd
import os

class Test(unittest.TestCase): 

    # test file paths
    TEST_FILES = [
        './fixtures/accessories.csv',
        './fixtures/clothing.csv',
        './fixtures/household_cleaners.csv',
        './fixtures/empty_file.csv',
        './fixtures/large_data.csv'
    ]

    OUTPUT_FILES = ['combined.csv', './test.csv']

    CHUNK_SIZE = 50000

    @classmethod
    def setUpClass(cls):
        # generate test data
        generatefixtures.main()

    def tearDown(self):
        if os.path.exists(self.OUTPUT_FILES[1]):
            os.remove(self.OUTPUT_FILES[1])

    def test_invalid_input_case_1(self):
        """test case for len(input) == 2
        """
        args = [self.TEST_FILES[0], self.OUTPUT_FILES[1]]
        with self.assertRaises(SystemExit) as cm:
            cb = CSV_Combiner(args)
            cb.combine()
        with open(self.OUTPUT_FILES[1]) as f:
            testdata = f.read()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("ERROR: invalid input!", testdata)
        self.assertIn("eg. python3 CSV_Combiner.py input_path_1 input_path_2 ... input_path_n output_path", testdata)

    def test_invalid_input_case_2(self):
        """test case for len(input) == 1
        """
        args = [self.OUTPUT_FILES[1]]
        with self.assertRaises(SystemExit) as cm:
            cb = CSV_Combiner(args)
            cb.combine()
        with open(self.OUTPUT_FILES[1]) as f:
            testdata = f.read()    
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("ERROR: invalid input!", testdata)
        self.assertIn("eg. python3 CSV_Combiner.py input_path_1 input_path_2 ... input_path_n output_path", testdata)

    def test_invalid_input_case_3(self):
        """test case for len(input) == 0
        """
        args = []
        with self.assertRaises(SystemExit) as cm:
            cb = CSV_Combiner(args)
            cb.combine()
        self.assertEqual(cm.exception.code, 1)

    def test_file_not_found(self):
        """test case for non exist file
        """
        args = [self.TEST_FILES[0], 'non_exist_file.csv', self.OUTPUT_FILES[1]]
        with self.assertRaises(SystemExit) as cm:
            cb = CSV_Combiner(args)
            cb.combine()
        with open(self.OUTPUT_FILES[1]) as f:
            testdata = f.read()     
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("ERROR: File Not Found!", testdata)

    def test_no_data_and_empty_file(self):
        """test case for empty file and no data situation
        empty file: print warning in terminal
        """
        args = [self.TEST_FILES[3], self.TEST_FILES[3], self.OUTPUT_FILES[1]]
        with self.assertRaises(SystemExit) as cm:
            cb = CSV_Combiner(args)
            cb.combine()
        with open(self.OUTPUT_FILES[1]) as f:
            testdata = f.read()    
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: No Data!", testdata)

    def test_case_1(self):
        """test case for multiple(>2) normal size csv files with same columns
        """
        args = [self.TEST_FILES[0], self.TEST_FILES[1], self.TEST_FILES[2], self.OUTPUT_FILES[1]]
        cb = CSV_Combiner(args)
        cb.combine()
        with open(self.OUTPUT_FILES[1]) as f:
            df = pd.read_csv(f)
        # include column 'filename'
        self.assertIn('filename', df.columns.values)
        filename_set = set(df['filename'].tolist())
        # data of column 'filename' is correct
        self.assertEqual(len(filename_set), len(args) - 1)
        self.assertIn(os.path.basename(self.TEST_FILES[0]), filename_set)
        self.assertIn(os.path.basename(self.TEST_FILES[1]), filename_set)
        self.assertIn(os.path.basename(self.TEST_FILES[2]), filename_set)
        with open(args[0]) as f:
            df2 = pd.read_csv(f)
        with open(args[1]) as f:
            df3 = pd.read_csv(f)
        with open(args[2]) as f:
            df4 = pd.read_csv(f)
        # number of rows before and after merge is the same
        self.assertEqual(len(df), len(df2) + len(df3) + len(df4))

    def test_case_2(self):
        """test case for large size csv files with different columns
        """
        args = [self.TEST_FILES[0], self.TEST_FILES[4], self.OUTPUT_FILES[1]]
        cb = CSV_Combiner(args)
        cb.combine()
        with open(self.OUTPUT_FILES[1]) as f:
            # deal with large size file with chunksize
            df_chunks = pd.read_csv(f, chunksize = self.CHUNK_SIZE)
            df_len = 0
            filename_list = list()
            for chunk in df_chunks:
                column_list = chunk.columns.values
                df_len += len(chunk)
        # include column 'filename'
        self.assertIn('filename', column_list)
        with open(args[0]) as f:
            df2_chunks = pd.read_csv(f, chunksize = self.CHUNK_SIZE)
            df2_len = 0
            for chunk in df2_chunks:
                column2_list = chunk.columns.values
                df2_len += len(chunk)
        with open(args[1]) as f:
            df3_chunks = pd.read_csv(f, chunksize = self.CHUNK_SIZE)
            df3_len = 0
            for chunk in df3_chunks:
                column3_list = chunk.columns.values
                df3_len += len(chunk)
        # deal with different columns correctly
        self.assertEqual(len(column_list.tolist()) - 1, len(set(column2_list.tolist() + column3_list.tolist())))
        # number of rows before and after merge is the same
        self.assertEqual(df_len, df2_len + df3_len)
        
if __name__=='__main__':
    unittest.main()
