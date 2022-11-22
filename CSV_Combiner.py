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
    # deal with large csv file
    CHUNK_SIZE = 50000

    def _check_inputs(self, args):
        """check if there are at least one input path and one output path

        Args:
            args (list): command line args
        """
        if len(args) <= 2:
            with open(args[-1], 'w') as f:
                print("ERROR: invalid input!", file = f)
                print("eg. python3 CSV_Combiner.py input_path_1 input_path_2 ... input_path_n output_path", file = f)
                sys.exit(1)
        return args[:-1], args[-1]

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
                with open(self.output_file, 'w') as f:
                    print("ERROR: File Not Found!", file = f)
                    sys.exit(1)
            except pd.errors.EmptyDataError:
                print("ERROR: Empty File!")
            else:
                for chunk in csv_chunks:
                    # append additional columns
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
            with open(self.output_file, 'w') as f:
                print("Error: No Data!", file = f)
                sys.exit(1)
        else:
            return combined_data

    def _output_csv(self, combined_csv):
        """Output combined data

        Args:
            combined_csv (pd.dataFrame): combined data
        """
        with open(self.output_file, 'w') as f:
            print(combined_csv.to_csv(index = False, chunksize = self.CHUNK_SIZE), file = f)
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
        if len(args) < 1:
            sys.exit(1)
        file_list, output_file = self._check_inputs(args)
        self.output_file = output_file
        self.file_list = file_list

def main():
    args = sys.argv
    cb = CSV_Combiner(args[1:])
    cb.combine()
    
if __name__ == '__main__':
    main()
    