import os
import csv
from tqdm import tqdm
import re

directory = '/Users/dolteanu/local_documents/Coding/MSc/FinalProject/Data/letter calls'
files = sorted(os.listdir(directory))
outfile = open("/Users/dolteanu/local_documents/Coding/MSc/FinalProject/Output/calls.csv", 'w')
writer = csv.writer(outfile, delimiter=',')

writer.writerow([''] + files)
line_data = []
for filename in tqdm(os.listdir(directory)):
    if filename != '.*':
        file = open(directory+'/'+filename,'r')
        lines = tqdm(file.readlines())
        print(filename)
        for x,line in enumerate(lines):
            if x != 0:
                line_strip = line.strip('\n').split(' ')
                line_elements = line_strip[0].split('\t')
                first_calls = line_elements[1]
                if filename == os.listdir(directory)[0]:
                    line_data.append([line_elements[0]])

                line_data[x-1].append(first_calls)

writer.writerows(line_data)
    # else:
    #     lines = lines[1:]
    #     for line in lines:
    #         line_elements = line.strip('\n').split('\t')
    #         calls = line_elements[1]
    #         rows = zip(calls)
    #         writer.writerows(rows)
outfile.close()





# for filename in os.listdir[1:]:
#     if filename.endswith(".txt"):
#         file = open(filename, 'r')
#         lines = file.readlines()
#         outfile = open("/Users/dolteanu/local_documents/Coding/MSc/FinalProject/Output", 'w')
#         for line in lines[1:]:
#             line_elements = line.strip('\n').split('\t')
#             calls = line_elements[1]
#             outfile.write(calls)
