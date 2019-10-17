# ArrayExpress personal notes
MAGE-TAB(MicroArray Gene Expression Tabular)
  SDRF `.sdrf` "(Sample and Data Relationship Format) describes the sample characteristics and the relationship between samples, arrays, data files"

## Retrieving detailed metadata
**Experiment** metadata XML for the accession E-xxxx-nnnnn:
`https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments/E-xxxx-nnnnn`

**Files** metadata XML for the experiment with accession E-xxxx-nnnnn:
`https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments/E-xxxx-nnnnn/files`

**Samples** metadata XML for the experiment with accession E-xxxx-nnnnn:
`https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments/E-xxxx-nnnnn/samples`

**Protocols** metadata XML for the experiment with accession E-xxxx-nnnnn:
`https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments/E-xxxx-nnnnn/protocols`
## Finding individual Files (incl ftp location)
`https://www.ebi.ac.uk/arrayexpress/xml/v3/files`

# FTP
In ftp server archive there are 2 directories: experiments and array

## Experiment
.idf.txt 	Top level information about the experiment including title, description, submitter contact details and protocols.

.sdrf.txt 	Information about the samples, the relationships between the samples, extracts, labeled extracts, hybridizations, factor values and data files.

## Array

.idf.txt
