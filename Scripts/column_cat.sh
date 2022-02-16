
# Ran the first line for 1 sample to make initial header
for f in *_sample_table.txt; do export f && cat "`pwd`/$f" | tail -n +2 | awk 'BEGIN {print " ,"ENVIRON["f"]","}; {print $1","$2","}'>> calls.csv; done
# Excluded the first sample_table.txt and run this line for all remaining samples (moving to a different directory)
for f in *_sample_table.txt; do export f && cat "`pwd`/$f" | tail -n +2 | awk 'BEGIN {print " ,"ENVIRON["f"]","}; {print $2","}'>> calls2.csv; done
# combine the first file (with row headers) and the second one with all other samples (but no row headers ) together cuz Im too dumb to figure it out
cat calls.csv calls2.csv > calls3.csv
