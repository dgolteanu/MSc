# Deduplication of datasets was tested
Jupyter notebooks allow generation of csv file where every pair of columns is the removed fasta's header & associated classes, last cell shows duplicates with multiple classes **if present** and their counts.

Raw seqkit & notebook outputs cannot be uplaoded here as this would be publishing restricted data from the GISAID database and go against their terms of use (according to our interpretation). This may change in the future if/when clarification is requested from GISAID.  
For details see jupyter notebooks within this folder for details & reproduction
## Summary
Nextstrain dataset with gisaid clades: 0 duplicates with multiple class labels (all duplicates from same clade).  

Nextstrain dataset with nextstrain clades: 0 duplicates with multiple class labels (all duplicates from same clade).  

Ontario covid dataset (gisaid clades): 7 duplicates with multiples class labels (all between GY & GRY clades).  

Ontario covid dataset (epochs): 46 duplicates among multiple classes (epochs).