"""
Parsing Array Express experiment query results in xml format
"""

import sys
# defining function to parse the xml output from the Array Express API
from xml.etree import ElementTree


def main():
    input = sys.argv[1]
    output = sys.argv[2]
    tree = ElementTree.parse(input)
    # empty list to turn into csv, [0] index is a list containing the accesssion
    # number and the dict of exp_factors with values
    exp_list = []
    outfile = open('./Output/'+output+'.csv', 'w')
    outfile.write('accession'+',' + 'study sample count total'
                  + "," + 'Experimental Factor Name' + "," + "FactorValue" + "\n")
    # loop through each experiment (top level of xml tree)
    for experiment in tree.findall('experiment'):
        # define empty dictionary for exp factors name:[value, value] pairs where
        # values are a list
        exp_factors = {}
        sample_number = experiment.find("./samples").text
        accession = experiment.find('./accession').text
        factors = experiment.findall('experimentalfactor')
        # loop through each factor to get name & all values for each unique factor (2nd level of xml tree)
        for f in factors:
            name = f.findtext('name')
            # first item is the name tag which would be a repeat
            val = f[1:]
            for values in val:
                value = values.text
                # append values to existing name key or create new pair
                if name not in exp_factors:
                    exp_factors.setdefault(name, [value])
                else:
                    exp_factors[name] += [value]
            # insert a for loop here for a 3rd level xml branch
            # add the desired variables to the next line as a list item
        list = [accession, exp_factors]
        exp_factors.items()
        exp_list.append(list)
        for key, value in exp_factors.items():
            factor_var = ','.join(value)
            outfile.write(accession+',' + sample_number
                          + "," + key + "," + factor_var + "\n")
    outfile.close()


if __name__ == '__main__':
    main()
