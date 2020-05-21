import csv

from xml.etree import ElementTree
file_path = '/Users/dolteanu/local_documents/Coding/MSc/Array Express lists/Output/human6.0_arrayexpress_processed_count.xml'
print(file_path)
tree = ElementTree.parse(file_path)
root = tree.getroot()
# empty list to turn into csv, [0] index is a list containing the accesssion number and the dict of exp_factors with values
exp_list=[]
outfile = open('./array express exp factors.tsv','w')
outfile.write('accession'+'\t' +'study sample count total'+ "\t" + 'experiment factor' + "\t" +"factor values" + "\n")
# loop through each experiment
for experiment in tree.findall('experiment'):
    # define empty dictionary for exp factors name:[value, value] pairs where values are a list
    exp_factors={}
    sample_number = experiment.find("./samples").text
    sdrf = experiment.find("./files/sdrf").attrib
    sdrf_file = sdrf.get('name')
    accession = str(sdrf_file.replace('.sdrf.txt',''))
    #exp_list.append(accession )
    factors = experiment.findall('experimentalfactor')
    # loop through each factor to get name & all values for each unique factor
    for f in factors:
        name = f.findtext('name')
        # first item is the name tag which would be a repeat
        val = f[1:]
        for values in val:
            value = values.text
            # append values to existing name key or create new pair
            if name not in exp_factors:
                exp_factors.setdefault(name,[value])
            else:
                exp_factors[name] += [value]
        keys = format(exp_factors.values())
    list = [accession,exp_factors]
    exp_factors.items()
    exp_list.append(list)
exp_list[0]
#     for key,value in exp_factors.items():
#         outfile.write(accession+'\t' +sample_number+"\t" + key + "\t" +str(value) + "\n")
# outfile.close()
    ## example with csv module
    # with open('./cancer.csv', 'w') as csvfile:
    #     docwriter = csv.DictWriter(csvfile, fieldnames=sorted(exp_factors.keys()))
    #     docwriter.writerow(exp_factors)
    #     mainwriter =csv.writer('./cancer.csv',delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL))
    #     mainwriter.writerow(print(exp_list[i][i+1].items()))
    # with open('./cancer.csv', 'w') as csvfile:
    #     mainwriter =csv.writer(csvfile,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     mainwriter.writerow(exp_list[i][1].items())


    ## xpath: any child of the parent . where [.='race'] matches the element (.) text 'race'
    # if experiment.findall(".//*[.='race']") != []:
    #     race_exp = experiment.findall(".//*[.='race']")
    #     sdrf = experiment.find("./files/sdrf").attrib
    #     print(race_exp)
    #     print(sdrf)
    # else:
    #     None
    #for exp in race_exp:
    #        print(exp.find("./files/sdrf").attrib)
