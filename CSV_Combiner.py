#!/usr/bin/env python3
"""a command line program that takes several CSV files as arguments.
Each CSV file (found in the fixtures directory) will have same or different columns. 
Script will output a new CSV file that contains the rows from each of the inputs 
    along with an additional column that has the file's basename using 'filename' as the header.

Output: output combined data to a single file(.csv)
"""

import pandas as pd
import os
import sys

class CSV_Combiner:

    file_list = []
    output_file = str()
    CHUNK_SIZE = 50000

    def _check_inputs(self, args):
        """check if there are at least one input path and one output path

        Args:
            args (list): command line args
        """
        if len(args) <= 2:
            print("ERROR: invalid input!")
            print("eg. python3 CSV_Combiner.py input_path_1 input_path_2 ... input_path_n output_path")
            sys.exit()
        return

    def _read_csv(self):
        """read csv files in CHUNK_SIZE

        Returns:
            list: [description]
        """
        csv_list = []
        for file in self.file_list:
            try:
                csv_chunks = pd.read_csv(file, chunksize = self.CHUNK_SIZE)
            except FileNotFoundError:
                print("ERROR: File Not Found!")
            except pd.errors.EmptyDataError:
                print("WARNING: Empty File!")
            else:
                for chunk in csv_chunks:
                    csv_list.append(chunk.assign(filename = os.path.basename(file)))
        return csv_list

    def _combine_csv(self, csv_list):
        """concat data with same/different columns

        Args:
            csv_list (list): data in CHUNK_SIZE with same/differemt columns

        Returns:
            pd.DataFrame: concat data
        """
        try:
            combined_data = pd.concat(csv_list, ignore_index = True)
        except ValueError:
            print("Error: No Data!")
            sys.exit()
        else:
            return combined_data

    def _output_csv(self, combined_csv):
        """Output combined data

        Args:
            combined_csv (pd.dataFrame): combined data
        """
        combined_csv.to_csv(self.output_file, index = False, chunksize = self.CHUNK_SIZE)
        return

    def combine(self):
        """function used for combine multiple csv files
        """
        csv_list = self._read_csv()
        combined_csv = self._combine_csv(csv_list)
        self._output_csv(combined_csv)
        return
        
    def __init__(self, args):
        """init class
        """
        file_list, output_file = self._check_inputs(args)
        self.file_list = file_list
        self.output_file = output_file

def main():
    args = sys.argv
    cb = CSV_Combiner(args[1:])
    cb.combine()
    
if __name__ == '__main__':
    main()
    