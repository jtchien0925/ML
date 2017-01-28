import numpy as np
import pandas as pd
import os
from Bio import SeqIO

from collections import Counter
from itertools import chain


#create list of sequences from FASTA
data = list(SeqIO.parse("Sequence_HLA_B_gDNA", "fasta"))
mylist = []
for i in range(0,len(data)):
	mylist.append(data[i].id)

#truncate sequence names to just allele group
mylist2 = [item[:4] for item in mylist]

#generate frequency table:
series_1 = pd.Series(mylist2)
counts_1 = series_1.value_counts()
print "Frequency Table:"
print counts_1