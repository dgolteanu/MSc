"""
Parsing Array Express experiment query results in xml format
"""
from orangecontrib.bio import arrayexpress as AE
import sys
import wget
import zipfile
import os
import csv


def main():
    study_list_array = open(sys.argv[1], 'r')
    # store remaining lines
    lines = study_list_array.readlines()
    # exmpty list for accession numbers used. May be used in future to track usage
    acc = []
    outfile = open('./Output/MLDSP_labels.csv', 'w')
    outfile.write('Sample'+',' + 'experimental factor variable' "\n")
    for line in lines[1:]:
        # split the tsv file line to get accession
        line_elements = line.strip('\n').split(',')
        accession = line_elements[0]
        # sanity check to make sure there are no duplicate accessions in tsv
        if accession not in acc:
            acc.append(accession)
            exp_factors = line_elements[2]
            # uncomment for selecting specific experimental factor variables
            # factor_vars = line_elements[3:]
            experiment = AE.ArrayExpressExperiment('E-GEOD-27105')
            # directly downloads the sdrf (genotyping data matrix) file from array express ftp server
            sdrf = experiment.sample_data_relationship()
            idf = experiment.investigation_design()
            sample_name = sdrf.derived_array_data_file()
            experiment.parse_data_matrix(sample_name)
            factors = sdrf._column("FactorValue "+"["+exp_factors+"]")
            table = experiment.fgem_to_table()
            rows = zip(sample_name, factors)
            writer = csv.writer(outfile, delimiter=',', quotechar='"')
            for row in rows:
                writer.writerow(row)
            for file in experiment.files:
                if file["kind"] == "fgem":
                    file = wget.download(file['url'])
                    compressed = zipfile.ZipFile(file, 'r')
                    compressed.extractall('./Data')
                    os.remove(file)
                else:
                    None
        else:
            None
    outfile.close()

if __name__ == '__main__':
    main()
