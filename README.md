## Introduction
Genotyping data is an abundant data type that is used to characterize Single Nucleotide Polymorphisms (SNPs) within a genome across populations at a fraction of the cost of DNA sequencind data. With large amounts of data available in public repositories, it lends itself well to meta-analyses, particularly using machine learning. The challenge is that with much of the focus shifting to sequencing, there are not many packages available to collect and streamline the meta-analysis of large datasets with various metadata formats. Here these programs attempt to automate the download and agregation of data from the [Array Express](https://www.ebi.ac.uk/arrayexpress/) database into the input format suitable for use with [MLDSP](https://sourceforge.net/projects/mldsp-gui/) a (Machine Learning with Digital Signal Processing) program, note: MLDSP is currently only published for sequencing data at the provided link, and MLDSP for genotyping will be available soon.

Here this project aims to take the xml file output from Array Express' search API and parse it to determine the experimental variables that were analysed within each study found for a given database search criteria. The user can then curate the list based on their variables of interest, the associated genotype call files will be automatically downloaded from Array Express, and a file containing sample labels for training the machine learning algorithm will be created. The goal of this program is to make it easy for researchers to parse search results of large size and automate the data download.

## Methodology
#### NOTE: data files in `/Data` and `MLDSP_labels.csv` file should be removed before a subsequent run as they will not be overwritten but appended.
The program consists of 2 python scripts, both of which are in the top level directory: `xml_parser.py` and `file_downloader.py`, there are 2 sub folders: `/Data` and `/Output`. The input for the program is the xml file which itself is output when doing a search of the Array Express database. The Experiment search API <https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments> is the only type acceptable as input for this program. The python scripts need to be run using the `python3` command from a bash command-line within the top level directory. The script takes 2 arguments: first the path of the input xml file and second the name of the output file without any extension. The output will be a comma delimited csv file in the Output directory. Example code: ``` python3 xml_parser.py input.xml samples_output```.

Once you have your `samples_output.csv` the 1st column data are all the study accessions from your search, the 2nd column data are the total number of samples for that study, note: studies with multiple experimental factors will come up with multiple rows each with the same sample number that represents the study total, the second column can therefore not be summed to get the total sample number. The 3rd column is the experimental factor of that study, and the 4th+ column(s) are all the experimental factor variables for that study. The user can subset the csv by rows using their text editor of choice to select experimental factors of interest, but column structure must be maintained. This subset can be saved as a new csv or overwrite the output of `xml_parser.py`.

The new or overwritten csv is then used as input for the `file_downloader.py` script to download and extract the processed genotype files for all studies of interest. This script is run in the same manner as the previous using one input argument: the subset csv, note: the full output of `xml_parser.py` can also be used as input. E.g. ``` python3 file_downloader.py subset_samples.csv```. The output will be a file `MLDSP_labels.csv` in the `/Output` directory alongside the downloaded genotyping files in the `/Data` directory.

The downloaded data can now be used in MLDSP along with the `MLDSP_labels.csv` file by calling the `Sample` column and `experimental factor variable` column in MLDSP.

## Dependencies
The python scripts require several modules to be downloaded: `wget` and `arrayexpress` using the following commands:
```
pip3 install wget
pip3 install Orange-Bioinformatics
```

## Example dataset analysis
In this example an xml file from a search of: all processed, Human 6.0 SNP genotyping array format files, from Homo Sapiens in the Array Express database is provided in the top level directory: `human6.0_arrayexpress_processed_count.xml` it contains 232 studies with  18191 samples.  This file was used with the xml_parser.py script:

```
python3 xml_parser.py human6.0_arrayexpress_processed_count.xml samples
```

where `samples` was the name given to the output file that is found in: `/Output/samples.csv`.
We can see in the this output several major clusters of experimental factors such as: Age, Cancer (and several subtypes), Disease state, Sex, Cell type and Race.

The `samples.csv` file was then sorted by "Experimental Factor Name" column and all studies with the `RACE` factor was selected as this is a strong known genetic signal that will make a good control case for MLDSP as we would like to control for it in future studie. As such all rows not containing the race factor were removed and a new file `query_factors.csv` was saved in the top level directory. This file was then used as input for the `file_downloader.py` script as follows:

```
python3 file_downloader.py query_factors.csv
```
The final output is the `MLDSP_labels.csv` that contains two colunms, 1st the list of all sample genotyping file names downloaded to the `/Output` directory and 2nd all the experimental factor variables for MLDSP labeling.
