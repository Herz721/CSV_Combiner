#!/usr/bin/env python3

import pandas as pd
import os
import sys

class CSV_Combiner:

    file_list = []
    output_file = str()
    CHUNK_SIZE = 50000

    def _read_csv(self):
        csv_list = []
        for file in self.file_list:
            csv_chunks = pd.read_csv(file, chunksize = self.CHUNK_SIZE)
            for chunk in csv_chunks:
                csv_list.append(chunk.assign(filename = os.path.basename(file)))
        return csv_list

    def _combine_csv(self, csv_list):
        return pd.concat(csv_list, ignore_index = True)

    def _output_csv(self, combined_csv):
        combined_csv.to_csv(self.output_file, index = False, chunksize = self.CHUNK_SIZE)

    def combine(self):
        csv_list = self._read_csv()
        combined_csv = self._combine_csv(csv_list)
        self._output_csv(combined_csv)
        return
        
    def __init__(self, file_list, output_file):
        self.file_list = file_list
        self.output_file = output_file

def main():
    args = sys.argv
    cb = CSV_Combiner(args[1:-1], args[-1])
    cb.combine()
    
if __name__ == '__main__':
    main()
    