import os
import csv
from tqdm import tqdm


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


directory = '/Users/dolteanu/local_documents/Coding/MSc/Data/letter calls'
files = list(listdir_nohidden(directory))
outfile = open(
    "/Users/dolteanu/local_documents/Coding/MSc/Output/calls.csv", 'w')

writer = csv.writer(outfile, delimiter=',')

writer.writerow([''] + files)
line_data = []
for filename in tqdm(files):
    print(filename)
    file = open(directory+'/'+filename, 'r')
    lines = tqdm(file.readlines())
    for x, line in enumerate(lines):
        if x != 0:
            line_strip = line.strip('\n').split(' ')
            line_elements = line_strip[0].split('\t')
            first_calls = line_elements[1]
            if filename == os.listdir(directory)[0]:
                line_data.append([line_elements[0]])

            line_data[x-1].append(first_calls)

writer.writerows(line_data)
outfile.close()
