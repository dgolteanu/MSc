# Author Daniel Stueckmann dstueckm@uwo.ca
import os
import csv
from itertools import *
import matplotlib.pyplot as plt
from Bio.Seq import Seq
from Bio import SeqIO
from sklearn import cluster
import numpy as np

#helper function to return folder path (outside class)
#works for a filepath or folderpath
def getFolder(filepath):
    filename_list = os.path.splitext(filepath)[0].split('\\')
    folder_path = ''
    if '.' in filepath:
        for x in range(len(filename_list)-1):
            folder_path = folder_path + filename_list[x] + '\\'
        folder_path = folder_path[:-1]
    else:
        for x in range(len(filename_list)):
            folder_path = folder_path + filename_list[x] + '\\'
        folder_path = folder_path[:-1]
    return folder_path

class FastaSeq:
    #initializer: takes a fasta file and converts it to a FastaSeq object (string)
    #default format is 'dsDNA': analyzes both the input sequence and reverse complement
    #can specify format to be 'ssDNA' (only looks at input sequence), no other valid formats
    def __init__(self, seqfile, format = 'dsDNA'):
        try:
            s1 = SeqIO.read(seqfile, 'fasta')
            filename_list = os.path.splitext(seqfile)[0].split('\\')
            self.seq_name = filename_list[len(filename_list)-1]
            self.folder_path = ''
            #check if command window has been set with os.chdir or if the whole filepath is specified, create folder_path attribute accordingly
            if 'Users' in seqfile:
                self.folder_path = getFolder(seqfile)
            else:
                self.folder_path = getFolder(os.getcwd() + '\\' + seqfile)
            #origin is required for FASTA file I/O, as we need our header information when writing files
            self.origin = s1
            self.sequence = s1.seq
            #if len(self.sequence) > 500000:
                #self.sequence = self.sequence[:500000]
            if format == 'dsDNA':
                self.format = 'dsDNA'
                self.sequence = self.sequence + 'N' + self.sequence.reverse_complement()
            elif format == 'ssDNA':
                self.format = 'ssDNA'
            else:
                print('Not a valid format - please choose from 1 (dsDNA - default) or 2 (ssDNA)')
        except:
            print(seqfile)

    #getKmers: for a kmer length of your choosing, return the frequency of each kmer found in the sequence as a dictionary
    #must install BioPython (via pip) to run this
    def getKmers(self, kmer):
        self.kmer_dict = {}
        kmer_tuples = list(product(['A', 'C', 'G', 'T'], repeat = kmer))
        kmer_list = []
        for x in range(len(kmer_tuples)):
            new_kmer = ''
            for y in range(kmer):
                new_kmer += kmer_tuples[x][y]
            kmer_list.append(new_kmer)
        for x in range(len(kmer_list)):
            self.kmer_dict[kmer_list[x]] = 0
        for substr in kmer_list:
            self.kmer_dict[substr] = self.sequence.count_overlap(substr)
        return self.kmer_dict

    #exportKmers: uses getKmers to export kmer frequencies to a .csv or .xlsx named after the seq file and kmer size, located in the folder specified
    #default parameter results in export to current directory folder, can specift output folder
    def exportKmers(self, kmer, exportfolder = None):
        if exportfolder == None:
            exportfolder = self.folder_path
        export_dict = self.getKmers(kmer)
        with open(exportfolder + '\\' + self.seq_name + str(kmer) + 'mers.csv', mode = 'w+') as csvfile:
            writer = csv.writer(csvfile, lineterminator = '\n')
            for key,item in export_dict.items():
                writer.writerow([key, item])

    #drawCGRPlot: draws a CGR plot, saves as a PNG in a specified folder
    #uncomment plt.show and comment plt.close if you prefer to view the images as they are created (will save upon closing the window)
    #default parameter results in export to current directory folder, can specift output folder
    #default point size is 0.1 (ideal for larger sequeces), if images are too sparse this can be increased to ~0.3
    def drawCGRPlot(self, exportfolder = None, pointsize = 0.1):
        if exportfolder == None:
            exportfolder = self.folder_path
        seq = self.sequence
        x = 0
        y = 0
        pointlist = [(x,y)]
        cnum = 0
        gnum = 0
        anum = 0
        tnum = 0
        totnum = 0
        cper = 0
        gper = 0
        aper = 0
        tper = 0
        for c in range(len(seq)):
            if seq[c] == 'A':
                anum += 1
                x = (x-1)/2
                y = (y-1)/2
            elif seq[c] == 'C':
                cnum += 1
                x = (x-1)/2
                y = (y+1)/2
            elif seq[c] == 'G':
                gnum += 1
                x = (x+ 1)/2
                y = (y+1)/2
            elif seq[c] == 'T':
                tnum += 1
                x = (x+1)/2
                y = (y-1)/2
            pointlist.append((x,y))
        xs, ys = zip(*pointlist)
        plt.figure(figsize=(7,7))
        plt.plot(xs, ys, marker = 'o', color = 'black', markersize = pointsize, linewidth = 0)
        plt.title(self.seq_name.capitalize())
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        plt.text(-1.1, -1.1, "A", fontsize = 16)
        plt.text(-1.1, 1.05, "C", fontsize = 16)
        plt.text(1.05, 1.05, "G", fontsize = 16)
        plt.text(1.05, -1.1, "T", fontsize = 16)

        totnum = anum + cnum + gnum + tnum
        aper = anum/totnum
        cper = cnum/totnum
        gper = gnum/totnum
        tper = tnum/totnum

        plt.text(1.02, 0.15, 'A: ' + str(aper*100)[:5] + r'%', fontsize = 8)
        plt.text(1.02, 0.05, 'C: ' + str(cper*100)[:5] + r'%', fontsize = 8)
        plt.text(1.02, -0.05, 'G: ' + str(gper*100)[:5] + r'%', fontsize = 8)
        plt.text(1.02, -0.15, 'T: ' + str(tper*100)[:5] + r'%', fontsize = 8)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.savefig(exportfolder + '\\' + self.seq_name + 'CGRPlot.png')
        #uncomment .show() and comment .close() if you do not prefer autosaving without viewing the image
        #comment .savefig() if you do not want to save a file and simply want to view the plot
        #plt.show()
        plt.close()

    #drawFCGRPlot: draws an FCGR plot, saves as a .PNG in a specified folder
    #can change to view the image before saving as in CGR plot
    #can take a kmer input of 1-4, larger sizes not supported
    def drawFCGRPlot(self, kmer, exportfolder = None):
        import seaborn as sns
        if exportfolder == None:
            exportfolder = self.folder_path
        kmer_dict = self.getKmers(kmer)
        kmer_list = []
        label_list = []
        font_size = 0
        if kmer == 1:
            font_size = 15
            label_list = ['C', 'G', 'A', 'T']
        elif kmer == 2:
            font_size = 12
            label_list = ['CC', 'GC', 'CG', 'GG', 'AC', 'TC', 'AG', 'TG', 'CA', 'GA', 'CT', 'GT', 'AA', 'TA', 'AT', 'TT']
        elif kmer == 3:
            font_size = 9
            label_list = ['CCC', 'GCC', 'CGC', 'GGC', 'CCG', 'GCG', 'CGG', 'GGG', \
                          'ACC', 'TCC', 'AGC', 'TGC', 'ACG', 'TCG', 'AGG', 'TGG', \
                          'CAC', 'GAC', 'ATC', 'CTC', 'CAG', 'GAG', 'CTG', 'GTG', \
                          'AAC', 'TAC', 'GTC', 'TTC', 'AAG', 'TAG', 'ATG', 'TTG', \
                          'CCA', 'GCA', 'CGA', 'GGA', 'CCT', 'GCT', 'CGT', 'GGT', \
                          'ACA', 'TCA', 'AGA', 'TGA', 'ACT', 'TCT', 'AGT', 'TGT', \
                          'CAA', 'GAA', 'CTA', 'GTA', 'CAT', 'GAT', 'CTT', 'GTT', \
                          'AAA', 'TAA', 'ATA', 'TTA', 'AAT', 'TAT', 'ATT', 'TTT']
        elif kmer == 4:
            label_list = ['CCCC', 'GCCC', 'CGCC', 'GGCC', 'CCGC', 'GCGC', 'CGGC', 'GGGC', 'CCCG', 'GCCG', 'CGCG', 'GGCG', 'CCGG', 'GCGG', 'CGGG', 'GGGG']
            label_list += ['ACCC', 'TCCC', 'AGCC', 'TGCC', 'ACGC', 'TCGC', 'AGGC', 'TGGC', 'ACCG', 'TCCG', 'AGCG', 'TGCG', 'ACGG', 'TCGG', 'AGGG', 'TGGG']
            label_list += ['CACC', 'GACC', 'CTCC', 'GTCC', 'CAGC', 'GAGC', 'CTGC', 'GTGC', 'CACG', 'GACG', 'CTCG', 'GTCG', 'CAGG', 'GAGG', 'CTGG', 'GTGG']
            label_list += ['AACC', 'TACC', 'ATCC', 'TTCC', 'AAGC', 'TAGC', 'ATGC', 'TTGC', 'AACG', 'TACG', 'ATCG', 'TTCG', 'AAGG', 'TAGG', 'ATGG', 'TTGG']
            label_list += ['CCAC', 'GCAC', 'CGAC', 'GGAC', 'CATC', 'GATC', 'CCTC', 'GCTC', 'CCAG', 'GCAG', 'CGAG', 'GGAG', 'CCTG', 'GCTG', 'CGTG', 'GGTG']
            label_list += ['ACAC', 'TCAC', 'AGAC', 'TGAC', 'AATC', 'TATC', 'ACTC', 'TCTC', 'ACAG', 'TCAG', 'AGAG', 'TGAG', 'ACTG', 'TCTG', 'AGTG', 'TGTG']
            label_list += ['CAAC', 'GAAC', 'CTAC', 'GTAC', 'CGTC', 'GGTC', 'CTTC', 'GTTC', 'CAAG', 'GAAG', 'CTAG', 'GTAG', 'CATG', 'GATG', 'CTTG', 'GTTG']
            label_list += ['AAAC', 'TAAC', 'ATAC', 'TTAC', 'AGTC', 'TGTC', 'ATTC', 'TTTC', 'AAAG', 'TAAG', 'ATAG', 'TTAG', 'AATG', 'TATG', 'ATTG', 'TTTG']
            label_list += ['CCCA', 'GCCA', 'CGCA', 'GGCA', 'CCGA', 'GCGA', 'CGGA', 'GGGA', 'CCCT', 'GCCT', 'CGCT', 'GGCT', 'CCGT', 'GCGT', 'CGGT', 'GGGT']
            label_list += ['ACCA', 'TCCA', 'AGCA', 'TGCA', 'ACGA', 'TCGA', 'AGGA', 'TGGA', 'ACCT', 'TCCT', 'AGCT', 'TGCT', 'ACGT', 'TCGT', 'AGGT', 'TGGT']
            label_list += ['CACA', 'GACA', 'CTCA', 'GTCA', 'CAGA', 'GAGA', 'CTGA', 'GTGA', 'CACT', 'GACT', 'CTCT', 'GTCT', 'CAGT', 'GAGT', 'CTGT', 'GTGT']
            label_list += ['AACA', 'TACA', 'ATCA', 'TTCA', 'AAGA', 'TAGA', 'ATGA', 'TTGA', 'AACT', 'TACT', 'ATCT', 'TTCT', 'AAGT', 'TAGT', 'ATGT', 'TTGT']
            label_list += ['CCAA', 'GCAA', 'CGAA', 'GGAA', 'CCTA', 'GCTA', 'CGTA', 'GGTA', 'CCAT', 'GCAT', 'CGAT', 'GGAT', 'CCTT', 'GCTT', 'CGTT', 'GGTT']
            label_list += ['ACAA', 'TCAA', 'AGAA', 'TGAA', 'ACTA', 'TCTA', 'AGTA', 'TGTA', 'ACAT', 'TCAT', 'AGAT', 'TGAT', 'ACTT', 'TCTT', 'AGTT', 'TGTT']
            label_list += ['CAAA', 'GAAA', 'CTAA', 'GTAA', 'CATA', 'GATA', 'CTTA', 'GTTA', 'CAAT', 'GAAT', 'CTAT', 'GTAT', 'CATT', 'GATT', 'CTTT', 'GTTT']
            label_list += ['AAAA', 'TAAA', 'ATAA', 'TTAA', 'AATA', 'TATA', 'ATTA', 'TTTA', 'AAAT', 'TAAT', 'ATAT', 'TTAT', 'AATT', 'TATT', 'ATTT', 'TTTT']
            font_size = 5
        for x in range(len(label_list)):
            for key, item in kmer_dict.items():
                if key == label_list[x]:
                    kmer_list.append(item)
        r_and_c = 2 ** kmer
        kmer_values = np.array(kmer_list).reshape(r_and_c,r_and_c)
        labels = np.array(label_list).reshape(r_and_c,r_and_c)
        if kmer < 5:
            ax = sns.heatmap(kmer_values, square = True, cbar = True, yticklabels = False, xticklabels = False, annot = labels, fmt = '', annot_kws={"size": font_size}, cmap = ['#FFFFFF', '#F5F5F5', '#DCDCDC', '#D3D3D3', '#C0C0C0', '#A9A9A9', '#808080', '#696969', '#000000'], linewidths = 0.2, linecolor = 'black')
            ax.set_title(self.seq_name)
            plt.savefig(exportfolder + '\\' + self.seq_name + str(kmer) + 'merFCGRPlot.png')
            plt.close()
        else:
             print('This program does not support FCGR generation with kmers greater than 4')

class FastaGroup:
    #initializer: takes a folder path for a folder of fasta files and converts it to a FastaGroup object (string)
    #similar functionality to FastaSeq, but now can take a folder with multiple sequence files
    #default format is 'dsDNA': analyzes both the input sequence and reverse complement
    #can specify format to be 'ssDNA' (only looks at input sequence), no other valid formats
    def __init__(self, seqfolder, format = 'dsDNA'):

        #only looks at fasta files, will ignore any other files in the source folder
        files = sorted([os.path.join(seqfolder, f) for f in os.listdir(seqfolder) if f.endswith('fasta') or f.endswith('fa') or f.endswith('fna')])
        self.file_list = []
        for file in files:
            self.file_list.append(FastaSeq(file, format))
        self._curItem = 0
        #check if command window has been set with os.chdir or if the whole filepath is specified, create folder_path attribute accordingly
        if 'Users' in seqfolder:
            self.folder_path = getFolder(seqfolder)
        else:
            self.folder_path = getFolder(os.getcwd() + '\\' + seqfolder)

        filename_list = os.path.splitext(seqfolder)[0].split('\\')
        self.group_name = filename_list[len(filename_list)-1]


    #create an iterator for the FastaGroup object
    def __iter__(self):

        return self

    #returns the next item in the FastaGroup object when a for loop is called
    def __next__(self):

        if self._curItem < len(self.file_list):
            #set the item to return
            item = self.file_list[self._curItem]
        else:
            #return current item to 0 after the iteration ends, necessary to utilize the iterator multiple times in one execution
            self._curItem = 0
            raise StopIteration
        #increment current item to loop through the FastaGroup object
        self._curItem += 1
        return item

    #getKmers: returns the frequency of each kmer for a specified length as an array, used to draw FCGRs or to export kmers
    #probably won't need to use this function directly
    #output is a 2D numpy array, containing the kmer freqeuncies for each sequence in the FastaGroup object
    def getKmers(self, kmer):

        kmer_list = []
        for fasta_file in self:
            templist = []
            labelList = []
            temp = self.file_list[self._curItem -1].getKmers(kmer).items()
            for key, item in temp:
                templist.append(item/(len(self.file_list[self._curItem -1].sequence) - (kmer-1)))
                labelList.append(key)
            kmer_list.append(templist)
        kmer_array = np.array(kmer_list)
        return labelList, kmer_array

    #getSeqNames: returns a list of sequence names for all fasta files in the FastaGroup object
    def getSeqNames(self):

        seq_name_list = []
        for fasta_file in self:
            seq_name_list.append(self.file_list[self._curItem -1].seq_name)
        return seq_name_list

    #exportKmers: exports a .csv file into the specified folder for all fasta files in the FastaGroup object based on the specified kmer length
    #if exportfolder is not specified, will use source folder
    #.csv file contains the kmers themselves, the corresponding frequencies, and the sequence names
    #.csv file name is "groupname_k=#.csv", # corresponding to the kmer value chosen
    def exportKmers(self, kmer, groupname, exportfolder = None):
        if exportfolder == None:
            exportfolder = self.folder_path
        kmerLabels, kmerFrequencies = self.getKmers(kmer)
        sequenceNames = self.getSeqNames()
        sequenceNames.insert(0, '')
        with open(exportfolder + '\\' + str(groupname) + '_k=' + str(kmer) + '.csv', mode = 'w+') as csvfile:
            writer = csv.writer(csvfile, lineterminator = '\n')
            writer.writerow(sequenceNames)
            for x in range(len(kmerLabels)):
                tmpRow = []
                tmpRow.append(kmerLabels[x])
                for y in range(len(kmerFrequencies)):
                    tmpRow.append(kmerFrequencies[y][x])
                writer.writerow(tmpRow)

    #converts a folder of .csv files to .xlsx files for use in R codes which require .xlsx files
    def convertToExcel(self, folderpath):
        from xlsxwriter.workbook import Workbook
        import glob
        csvfiles = sorted([os.path.join(folderpath, f) for f in os.listdir(folderpath) if f.endswith('csv')])
        for csvfile in csvfiles:
            workbook = Workbook(csvfile[:-4] + '.xlsx')
            worksheet = workbook.add_worksheet()
            with open(csvfile, 'rt', encoding='utf8') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
            workbook.close()

    #generates the files required to run a spearman rank correlation test in RStudio
    #note that if the default '.xlsx' format is chosen, it will generate both '.csv' and '.xlsx' files for each kmer, whereas changing format to '.csv' will generate only .csv files
    def spearmanPrep(self, groupname, exportfolder = None, format = '.xlsx'):
        if exportfolder == None:
            exportfolder = self.folder_path
        assert format in ['.xlsx', '.csv'], 'Not a valid format: please choose from .csv, or .xlsx (default)'
        for k in range(1,8):
            self.exportKmers(k, groupname, exportfolder)
        if format == '.xlsx':
            self.convertToExcel(exportfolder)

    #export under/over-represented kmers for each sequence in a faster group into a .csv file
    def exportRep(self, kmer, exportfolder = None):
        if exportfolder == None:
            exportfolder = self.folder_path
        kmerLabels, kmerFrequencies = self.getKmers(kmer)
        sequenceNames = self.getSeqNames()
        with open(exportfolder + '\\' + 'OverandUnderRep_k=' + str(kmer) + '.csv', mode = 'w+') as csvfile:
            writer = csv.writer(csvfile, lineterminator = '\n')
            for x in range(len(sequenceNames)):
                tmpLow = np.percentile(kmerFrequencies[x], 2.5)
                tmpHigh = np.percentile(kmerFrequencies[x], 97.5)

                tmpRow = []
                tmpRow.append(sequenceNames[x])
                tmpRow.append('Below 2.5th percentile:')
                for y in range(len(kmerFrequencies[0])):
                    if float(kmerFrequencies[x][y]) < tmpLow:
                        tmpRow.append(kmerLabels[y])
                writer.writerow(tmpRow)

                tmpRow = []
                tmpRow.append(sequenceNames[x])
                tmpRow.append('Above 97.5th percentile:')
                for y in range(len(kmerFrequencies[0])):
                    if float(kmerFrequencies[x][y]) > tmpHigh:
                        tmpRow.append(kmerLabels[y])
                writer.writerow(tmpRow)

    #drawCGRs: draws a CGR plot for each fasta file in the FastaGroup object
    #saves as a .PNG in a specified folder
    #if exportfolder is not specified, will use source folder
    #can change to viewing each image before saving, but requires modification of drawCGRPlot in the FastaSeq group
    def drawCGRs(self, exportfolder = None):
        if exportfolder == None:
            for fasta_file in self:
                self.file_list[self._curItem -1].drawCGRPlot()
        else:
            for fasta_file in self:
                self.file_list[self._curItem -1].drawCGRPlot(exportfolder)

    #drawFCGRs: draws a FCGR plot for each fasta file in the FastaGroup object based on a kmer length of 1-4
    #saves as a .PNG in a specified folder
    #if exportfolder is not specified, will use source folder
    #can change to viewing each image before saving, but requires modification of drawFCGRPlot in the FastaSeq group
    def drawFCGRs(self, kmer, exportfolder = None):
        if exportfolder == None:
            for fasta_file in self:
                self.file_list[self._curItem -1].drawFCGRPlot(kmer)
        else:
            for fasta_file in self:
                self.file_list[self._curItem -1].drawFCGRPlot(kmer, exportfolder)

    #unsupervisedLearn: performs k-means clustering to cluster the fasta sequences into 2 or 3 groups (specified by kmeans parameter)
    #creates a .txt file in the specified folder under the specified filename which contains the grouped sequence names
    #kmer parameter allows you to control the complexity of the feature arrays used for clustering (larger kmer == more accurate, longer analysis time)
    #exportfilename must contain the whole filepath unless os.chdir has been used to change directory to the specified folder
    def unsupervisedLearn(self, exportfilename, kmer = 4, kmeans = 2):
        from sklearn import cluster
        data = self.getKmers(kmer)[1]
        k_means = cluster.KMeans(kmeans)
        k_means.fit(data)
        labels = k_means.labels_
        if kmeans == 2:
            group1 = []
            group2 = []
            for x in range(len(labels)):
                if labels[x] == 0:
                    group1.append(self.file_list[x].seq_name)
                else:
                    group2.append(self.file_list[x].seq_name)
            f = open(exportfilename, 'a+')
            str_to_app = 'Group 1:' + '\n' + '\n'
            for x in range(len(group1)):
                str_to_app = str_to_app + group1[x] + '\n'
            str_to_app += '\n' + 'Group 2:' + '\n' + '\n'
            for x in range(len(group2)):
                str_to_app = str_to_app + group2[x] + '\n'
            f.write(str_to_app)
            f.close()
        elif kmeans == 3:
            group1 = []
            group2 = []
            group3 = []
            for x in range(len(labels)):
                if labels[x] == 0:
                    group1.append(self.file_list[x].seq_name)
                elif labels[x] == 1:
                    group2.append(self.file_list[x].seq_name)
                else:
                    group3.append(self.file_list[x].seq_name)
            f = open(exportfilename, 'a+')
            str_to_app = 'Group 1:' + '\n' + '\n'
            for x in range(len(group1)):
                str_to_app = str_to_app + group1[x] + '\n'
            str_to_app += '\n' + 'Group 2:' + '\n' + '\n'
            for x in range(len(group2)):
                str_to_app = str_to_app + group2[x] + '\n'
            str_to_app += '\n' + 'Group 3:' + '\n' + '\n'
            for x in range(len(group3)):
                str_to_app = str_to_app + group3[x] + '\n'
            f.write(str_to_app)
            f.close()
        elif kmeans == 4:
            group1 = []
            group2 = []
            group3 = []
            group4 = []
            for x in range(len(labels)):
                if labels[x] == 0:
                    group1.append(self.file_list[x].seq_name)
                elif labels[x] == 1:
                    group2.append(self.file_list[x].seq_name)
                elif labels[x] == 2:
                    group3.append(self.file_list[x].seq_name)
                else:
                    group4.append(self.file_list[x].seq_name)
            f = open(exportfilename, 'a+')
            str_to_app = 'Group 1:' + '\n' + '\n'
            for x in range(len(group1)):
                str_to_app = str_to_app + group1[x] + '\n'
            str_to_app += '\n' + 'Group 2:' + '\n' + '\n'
            for x in range(len(group2)):
                str_to_app = str_to_app + group2[x] + '\n'
            str_to_app += '\n' + 'Group 3:' + '\n' + '\n'
            for x in range(len(group3)):
                str_to_app = str_to_app + group3[x] + '\n'
            str_to_app += '\n' + 'Group 4:' + '\n' + '\n'
            for x in range(len(group4)):
                str_to_app = str_to_app + group4[x] + '\n'
            f.write(str_to_app)
            f.close()
        else:
            print( 'This function currently does not support grouping sequences into more than 4 or less than 2 groups')

        #output is copying source files into new groups instead of creating a .txt file representing groups
        #requires specific creation of named subfolders in the desired exportfolder
        #for kmeans = 2, subfolders are 'group1' and 'group2'
        #for kmeans = 3, subfolders are 'group1', 'group2', and 'group3'
    def unsupervisedLearn2(self, exportfolder, kmer = 4, kmeans = 2):
        from sklearn import cluster
        from shutil import copyfile
        data = self.getKmers(kmer)[1]
        k_means = cluster.KMeans(kmeans)
        k_means.fit(data)
        labels = k_means.labels_
        if kmeans == 2:
            group1 = []
            group2 = []
            for x in range(len(labels)):
                if labels[x] == 0:
                    group1.append(self.file_list[x].seq_name)
                else:
                    group2.append(self.file_list[x].seq_name)
            for x in range(len(group1)):
                copyfile(self.folder_path + '\\' + str(group1[x]) + '.fasta', exportfolder + '\\' + 'group1' + '\\' + str(group1[x]) + '.fasta')
            for x in range(len(group2)):
                copyfile(self.folder_path + '\\' + str(group2[x]) + '.fasta', exportfolder + '\\' + 'group2' + '\\' + str(group2[x]) + '.fasta')
        elif kmeans == 3:
            group1 = []
            group2 = []
            group3 = []
            for x in range(len(labels)):
                if labels[x] == 0:
                    group1.append(self.file_list[x].seq_name)
                elif labels[x] == 1:
                    group2.append(self.file_list[x].seq_name)
                else:
                    group3.append(self.file_list[x].seq_name)
            for x in range(len(group1)):
                copyfile(self.folder_path + '\\' + str(group1[x]) + '.fasta', exportfolder + '\\' + 'group1' + '\\' + str(group1[x]) + '.fasta')
            for x in range(len(group2)):
                copyfile(self.folder_path + '\\' + str(group2[x]) + '.fasta', exportfolder + '\\' + 'group2' + '\\' + str(group2[x]) + '.fasta')
            for x in range(len(group3)):
                copyfile(self.folder_path + '\\' + str(group3[x]) + '.fasta', exportfolder + '\\' + 'group3' + '\\' + str(group3[x]) + '.fasta')
        else:
            print( 'This function currently does not support grouping sequences into more than 3 or less than 2 groups')

    #eucDisMatrix: calculates N-dimensional euclidian distance between multiple sequences based on the kmer chosen (N = 4^kmer)
    #stores this information as a distance matrix in a pandas dataframe, and uses the matrix to generate a seaborn heatmap
    #must specify kmer, exportfolder is set to the current folder by default
    def eucDisMatrix(self, kmer, exportfolder = None):
        import pandas as pd
        from scipy.spatial import distance_matrix
        import seaborn as sns
        if exportfolder == None:
            exportfolder = self.folder_path
        labels = np.array(self.getSeqNames())
        data = self.getKmers(kmer)[1]
        df = pd.DataFrame(data, index = labels)
        distanceMatrix = pd.DataFrame(distance_matrix(df.values, df.values), index = df.index, columns = df.index)
        sns.heatmap(distanceMatrix, annot = False, cbar_kws={'label': 'Genomic Distance'})
        plt.savefig(exportfolder + '\\' + 'GenomicDistanceHeatmap.png')
        plt.show()

    #chopSequencesdsDNA: chops each fasta sequence in a folder into smaller fasta files of length 10 kb (20 kb dsDNA)
    #will only create full-length subfiles, so all subfiles will be the same length
    #discards any files with over 500 'N's in the 10 kb section as this indicates poor read quality for this section
    #IMPORTANT: must create one subfolder in the source folder for EACH file to be split, and the names of the new folders must match the names of the sequences EXACTLY
    #e.g. if you have a sequence HumanGenome.fasta, create a folder called HumanGenome, this will be the output for the smaller fasta files
    #IMPORTANT: this program works ONLY for FastaGroups created with 'ssDNA' specified for their format as it reverse transcribes the 10 kb fragments
    def chopSequencesdsDNA(self, exportfolder, size = 10000):
        for file in self:
            assert file.format == 'ssDNA', 'Must use ssDNA as the format type for the FastaGroup when attempting to chop sequences'
            numGroups = len(file.sequence) // size
            for x in range(numGroups):
                curSeq = file.origin[x*size : x*size + size]
                curSeq = curSeq + 'N' + curSeq.seq.reverse_complement()
                if curSeq.seq.count('N') < 1000:
                    SeqIO.write(curSeq, exportfolder + '\\' + file.seq_name + str(x + 1) + '.fasta', "fasta")

    #same idea as chopSequencesdsDNA, but now creates ssDNA outputs of 20kb rather than dsDNA outputs
    #used for ML-DSP
    def chopSequences(self, exportfolder, size = 20000):
        for file in self:
            assert file.format == 'ssDNA', 'Must use ssDNA as the format type for the FastaGroup when attempting to chop sequences'
            numGroups = len(file.sequence) // size
            for x in range(numGroups):
                curSeq = file.origin[x*size : x*size + size]
                if curSeq.seq.count('N') < 1000:
                    SeqIO.write(curSeq, exportfolder +  '\\' + file.seq_name + str(x + 1) + '.fasta', "fasta")

    #take a folder of fasta files and create smaller versions of these files in a new folder
    def shrink(self, exportfolder, size = 25000):
        for file in self:
            assert file.format == 'ssDNA', 'Must use ssDNA as the format type for the FastaGroup when attempting to shrink sequences'
            curSeq = file.origin[:size]
            curSeq = curSeq + 'N' + curSeq.seq.reverse_complement()
            SeqIO.write(curSeq, exportfolder + '\\' + file.seq_name + '.fasta', "fasta")

    def spearmanRank(self, other, exportfolder = None, kmer = 'all'):
        import scipy.stats
        if exportfolder == None:
            exportfolder = self.folder_path
        if kmer != 'all':
            try:
                a = int(kmer)
            except:
                print("kmer must be an integer between 2 and 7, or choose 'all' to display all kmers from 2 to 7")
            if a < 2 or a > 7:
                print('Kmers larger than 7 or smaller than 2 are currently not supported')
            else:
                labelSelf = self.getKmers(kmer)[0]
                dataSelf = self.getKmers(kmer)[1]
                dataOther = other.getKmers(kmer)[1]
                newSelf = np.zeros(len(dataSelf[0]))
                newOther = np.zeros(len(dataOther[0]))
                for x in range(len(dataSelf[0])):
                    tmp = 0.0
                    tmp2 = 0.0
                    for y in range(len(dataSelf)):
                        tmp += dataSelf[y][x]
                    for z in range(len(dataOther)):
                        tmp2 += dataOther[z][x]
                    newSelf[x] = tmp/len(dataSelf)
                    newOther[x] = tmp2/len(dataOther)
                output = scipy.stats.spearmanr(newSelf, newOther)
                printstr = 'For k = ' + str(kmer) + ',' + '\n' + 'rho = ' + str(output[0]) + '\n' + 'p = ' + str(output[1])
                fig,ax = plt.subplots()
                plt.plot(newSelf, newOther, 'ko', markersize = 10 - kmer) #'ko' is string format for black circles
                ax.set_title('Spearman rank correlation of ' + str(self.group_name) + ' vs. ' + str(other.group_name))

                #set axes min/max
                minX, maxX = plt.xlim()
                minY, maxY = plt.ylim()

                if kmer > 4:
                    plt.xscale('log')
                    plt.yscale('log')
                    plt.xlabel(str(self.group_name) + '(log)')
                    plt.ylabel(str(other.group_name) + '(log)')

                else:
                    plt.xscale('linear')
                    plt.yscale('linear')
                    plt.xlabel(str(self.group_name))
                    plt.ylabel(str(other.group_name))

                #representing 2.5th and 97.5th percentiles via red dotted lines
                selfLow = np.percentile(newSelf, 2.5)
                selfHigh = np.percentile(newSelf, 97.5)

                otherLow = np.percentile(newOther, 2.5)
                otherHigh = np.percentile(newOther, 97.5)

                plt.vlines([selfLow, selfHigh], minY, maxY, color = 'r', linestyle = 'dashed')
                plt.hlines([otherLow, otherHigh], minX, maxX, color = 'r', linestyle = 'dashed')

                #getting output summary and formatting
                printstr = 'For k = ' + str(kmer) + ',' + '\n' + 'rho = ' + str(output[0]) + '\n' + 'p = ' + str(output[1])
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                ax.text(0.025,0.975, printstr, transform = ax.transAxes, fontsize = 10, verticalalignment = 'top', bbox = props)
                plt.show()

        else:
            for k in range(2,8):
                labelSelf = self.getKmers(k)[0]
                dataSelf = self.getKmers(k)[1]
                dataOther = other.getKmers(k)[1]
                newSelf = np.zeros(len(dataSelf[0]))
                newOther = np.zeros(len(dataOther[0]))
                for x in range(len(dataSelf[0])):
                    tmp = 0.0
                    tmp2 = 0.0
                    for y in range(len(dataSelf)):
                        tmp += dataSelf[y][x]
                    for z in range(len(dataOther)):
                        tmp2 += dataOther[z][x]
                    newSelf[x] = tmp/len(dataSelf)
                    newOther[x] = tmp2/len(dataOther)
                output = scipy.stats.spearmanr(newSelf, newOther)
                fig,ax = plt.subplots()
                plt.plot(newSelf, newOther, 'ko', markersize = 10 - k)
                ax.set_title('Spearman rank correlation of ' + str(self.group_name) + ' vs. ' + str(other.group_name))

                #get axes min/max
                minX, maxX = plt.xlim()
                minY, maxY = plt.ylim()

                if k > 4:
                    plt.xscale('log')
                    plt.yscale('log')
                    plt.xlabel(str(self.group_name) + '(log)')
                    plt.ylabel(str(other.group_name) + '(log)')

                else:
                    plt.xscale('linear')
                    plt.yscale('linear')
                    plt.xlabel(str(self.group_name))
                    plt.ylabel(str(other.group_name))


                #representing 2.5th and 97.5th percentiles via red dotted lines
                selfLow = np.percentile(newSelf, 2.5)
                selfHigh = np.percentile(newSelf, 97.5)

                otherLow = np.percentile(newOther, 2.5)
                otherHigh = np.percentile(newOther, 97.5)

                plt.vlines([selfLow, selfHigh], minY, maxY, color = 'r', linestyle = 'dashed')
                plt.hlines([otherLow, otherHigh], minX, maxX, color = 'r', linestyle = 'dashed')

                #getting output summary and formatting
                printstr = 'For k = ' + str(k) + ',' + '\n' + 'rho = ' + str(output[0]) + '\n' + 'p = ' + str(output[1])
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                ax.text(0.025,0.975, printstr, transform = ax.transAxes, fontsize = 10, verticalalignment = 'top', bbox = props)
                plt.savefig(exportfolder + '\\' + str(self.group_name) + '_vs._' + str(other.group_name) + '_k_' + str(k) + '.png')
                plt.close()
