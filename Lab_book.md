# Daniel Olteanu lab book in the Hill lab at the University of Western Ontario
## This lab book is intended to be a complete technical track record of programs run and/or created to generate new results/data. It is meant to be completely reproducible
### 2019/09/23
MSc git repository was created on Daniel's local machine and

I have a modified genotyping call file ` NMRI_calls.csv, CD1_calls.csv` for CD-1 and NMRI mice strains provided by Hailie Pavanel. Nick Boehler & Hailie Pavanel provided genome position annotation files ` MDGA_Annotation.csv,MDGA_functional_anno.csv ` respectively, created by the Hill lab for the Affymetrix MDGA microarray probes used in our lab. Kathleen Hill provided a file `MLDSP_labels.csv` containing clustering information for 800 mice within the Jackson laboratory database `url` for use as feature labels in training the Machine learning (ML) alogorithm of MLDSP.

I am importing the data files into R data frames as they're too large to open in excel. The data frame will be a matrix of SNP calls with  probes as rownames and samples as colnames.

I am looking at merging an SNP genotyping call file with the probe annotations (Chromosome number `Affy.chr..build.38.` & Chromosome nucleotide position `Affy.position..build.38.`) inserted as 2nd & 3rd columns respectively, next I am looking at inserting the ML labels as the 2nd row, finally all the run information lines above the sample names will be removed to make the sample names row \# 1.

This is a proof of principle as we wait for the 800 mice to be genotyped, and will be combined into an R script to automate genotyping data formatting for input into MLDSP.

Imported `MDGA_Annotation.csv` as `annotated_probes` variable in R
#### These steps are for Affymetrix power tools `apt-1.16.0`
### 2019/09/24
Removed all rows except genomic position from the  `probe_position` dataframe using `probe_position <- annotated_probes[-4:-17,]`, `probe_position <- probe_position[rowSums(is.na(probe_position)) != ncol(probe_position),]` and `probes_position <- probe_position[rowSums(is.na(probe_position)) == 0,]`
### 2019/10/01
Re-focus on looking for Human 6.0 SNP array data and creating a pipeline for data cleanup.

Looked into European Bioinformatics Institute (EBI) ArrayExpress database(db) which encompases NCBI's GEO database.

Searched the ArrayExpress db using the following: **Filtered by organism Homo sapiens, experiment type "dna assay", experiment type "array assay"**

The tab-delimited file from the search page`ArrayExpress-Experiments-191001-153147.txt` was imported into R `ebi_human_array<-read.table('./ArrayExpress-Experiments-191001-153147.txt', header=T, sep= '\t', row.names="Accession")`

The dataframe was subset by "Type" column for any sample containing the word "genotyping" or "SNP" to capture all possible genotyping microarray datasets within the db
`geno<- (grepl('genotyping', Type, ignore.case = T)|grepl('SNP', Type, ignore.case = T))`. 295 projects were identified`ebi_SNParray_human`, of these 6 had no raw or processed data associated and were removed `ebi_SNParray_human<-subset(ebi_geno, Processed.Data!='Data is not available'|Raw.Data!='Data is not available',)`.

The final list was exported as csv `ArrayExpress_human_arrays_list.csv`
