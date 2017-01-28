import numpy as np
import pandas as pd
import os
from Bio import SeqIO

import sys

#filter FASTA file sequences by name index, we want B-15 and B-44
def filter_seq(filename):
    targeted_sequences = []
    input_handle=open(sys.argv[1],'rU')
    output_handle = open(sys.argv[2], "w")
    
    #find and filter sequences in B-44 and B-15 allele group
    for record in SeqIO.parse(input_handle, "fasta") :
        if record.name.startswith("B-15") or record.name.startswith("B-44"):
            targeted_sequences.append(record)

    #rewrite filtered sequnces to new file, 77 total
    for item in targeted_sequences:

        id_old=item.description
        id_new='>'+id_old[2:4]
        #for now we deal with two groups, so we label sequences as either "15" or "44" for the purpose of classification later on

        print>>output_handle, id_new
        sequence=item.seq
        print>>output_handle, sequence

    
    input_handle.close()
    output_handle.close()

if __name__=="__main__":
    filter_seq(sys.argv[1])
    
