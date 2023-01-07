# Daniel Olteanu lab book in the Hill lab at the University of Western Ontario
## This lab book is intended to be a complete technical track record in chronological order of programs run and/or created to generate new results/data. It is meant to be completely reproducible. "Comments"-are added after the fact (Post-hoc) to give the reader context on errors, re-runs or cautions when (re)reading.  

# None of this stuff was used, genotyping databases have lots of different formats, need an AI ontology cleanup before revisiting, 5 years??
## 2019/09/23
MSc git repository was created on Daniel's local machine (lenovo thinkpad x1 yoga) and

I have a modified genotyping call file ` NMRI_calls.csv, CD1_calls.csv` for CD-1 and NMRI mice strains provided by Hailie Pavanel. Nick Boehler & Hailie Pavanel provided genome position annotation files ` MDGA_Annotation.csv,MDGA_functional_anno.csv ` respectively, created by the Hill lab for the Affymetrix MDGA microarray probes used in our lab. Kathleen Hill provided a file `MLDSP_labels.csv` containing clustering information for 800 mice within the Jackson laboratory database `url` for use as feature labels in training the Machine learning (ML) alogorithm of MLDSP.

I am importing the data files into R data frames as they're too large to open in excel. The data frame will be a matrix of SNP calls with  probes as rownames and samples as colnames.

I am looking at merging an SNP genotyping call file with the probe annotations (Chromosome number `Affy.chr..build.38.` & Chromosome nucleotide position `Affy.position..build.38.`) inserted as 2nd & 3rd columns respectively, next I am looking at inserting the ML labels as the 2nd row, finally all the run information lines above the sample names will be removed to make the sample names row \# 1.

This is a proof of principle as we wait for the 800 mice to be genotyped, and will be combined into an R script to automate genotyping data formatting for input into MLDSP.

Imported `MDGA_Annotation.csv` as `annotated_probes` variable in R
#### These steps are for Affymetrix power tools `apt-1.16.0`
## 2019/09/24
Removed all rows except genomic position from the  `probe_position` dataframe using `probe_position <- annotated_probes[-4:-17,]`, `probe_position <- probe_position[rowSums(is.na(probe_position)) != ncol(probe_position),]` and `probes_position <- probe_position[rowSums(is.na(probe_position)) == 0,]`
## 2019/10/01
Re-focus on looking for Human 6.0 SNP array data and creating a pipeline for data cleanup.

Looked into European Bioinformatics Institute (EBI) ArrayExpress database(db) which encompases NCBI's GEO database.

Searched the ArrayExpress db using the following: **Filtered by organism Homo sapiens, experiment type "dna assay", experiment type "array assay"**

The tab-delimited file from the search page`ArrayExpress-Experiments-191001-153147.txt` was imported into R `ebi_human_array<-read.table('./ArrayExpress-Experiments-191001-153147.txt', header=T, sep= '\t', row.names="Accession")`

The dataframe was subset by "Type" column for any sample containing the word "genotyping" or "SNP" to capture all possible genotyping microarray datasets within the db
`geno<- (grepl('genotyping', Type, ignore.case = T)|grepl('SNP', Type, ignore.case = T))`. 295 projects were identified`ebi_SNParray_human`, of these 6 had no raw or processed data associated and were removed `ebi_SNParray_human<-subset(ebi_geno, Processed.Data!='Data is not available'|Raw.Data!='Data is not available',)`.

The final list was exported as csv `ArrayExpress_human_arrays_list.csv`
# End of unused stuff, below begins a chronological history of software version tracking & history of programs run. 
## 2019/11/18
Local machine was changed to Macbook Pro (16-inch 2019) model A2141 Part Number: MVVJ2LL/A running MacOS catalina 10.15.1
## 2021/02/19
MacOS updated to Big Sur 11.2.1
## 2021/04/27
MacOS updated to 11.3
## 2021/05/26 
MacOS updated to 11.4
## 2021/06/16
Downloaded all available GISAID data from website portal https://www.epicov.org/epi3/frontend > "EpiCoV" tab > "Downloads" tab > pop up > "Download packages" header> select "FASTA" and "metadata" download buttons. After unziping the tar.xz we get 2 folders: sequences_fasta_2021_06_16 and metadata_2021_06_16. Also downloaded on the same day all protein sequences https://www.epicov.org/epi3/frontend > "EpiCoV" tab >"Downloads" tab > pop up > "Alignment and proteins" header > allprotXXXX file where on this date XXXX = 0322

## NOT USED:
Downloaded Nextstrain website data https://nextstrain.org/ncov/gisaid/global scroll to bottom of page select "DOWNLOAD DATA" button at the very bottom center see ![Nextstrain website download example]('Lab book/Nextstrain website data download example 2021:06:16.png'). This dataset does not have a nextstrain clade metadata csv, only gisaid & pangolin; would need to be extracted from the newick tree.
## 2021/07/25
MacOS updated to 11.5
## 2021/08/23
Profiling of MATLAB MLDSP using the BacteriaTest dataset
## 2021/08/29
MacOS updated to 11.5.2
## 2021/10/06
## NOT USED, TOO BIG
Redownloaded all available gisaid data from website portal https://www.epicov.org/epi3/frontend > "EpiCoV" tab > "Downloads" tab > pop up > "Download packages" header> select "FASTA" and "metadata" download buttons. After unziping the tar.xz we get 2 folders: sequences_fasta_2021_10_06 and metadata_2021_10_06
## 2021/10/12
MacOS updated to 11.6
## 2022/01/11
## Nextstrain dataset download
Downloaded data used to build tree on Nextstrain's website from the GISAID website portal https://www.epicov.org/epi3/frontend > "EpiCoV" tab > "Downloads" tab > pop up > "Genomic epidemiology" header > 'nextregions' button > pop up "Region-specific Auspice source files" > "Global" download button. This gives "hcov_global_2022-01-09_23-30" containing the fasta of sequences used on the nextstrain website https://nextstrain.org/ncov/gisaid/global as seen on January 9 2022

## 2022/02/27
Will have to redownload the nextstrain website data & raw data used to build it from gisaid on the same day (weekday)

## 2022/03/21
Running Mantel test of Dengue dataset vs covid19 gisaid data, may not be appropriate for different datasets; available packages require symmetric matrix of same size (assumed to come from same dataset), which our use case does not satisfy

## 2022/04/11
### MATLAB profiling
MATLAB mldsp was previously profiled on [2021/08/23](#2021/08/23) on my mac at the time running macos 11.5 (MATLAB R2019a). The BacteriaTest dataset was used with the cgr numerical method at k=6; the builtin profiler was run using the `Run & Time` button on the MATLAB desktop, as described in the [MATLAB documentation](https://www.mathworks.com/help/matlab/matlab_prog/profiling-for-improving-performance.html#mw_e3eebe5c-984d-42ad-8b1f-6269890525fc). All other programs were closed during the profiling run. Profiling results can be found in [Profiling/MATLAB/Timing.pdf](../Profiling/MATLAB/Timing.pdf), the approximate run time was **~590 s**.  
Attempting to reproduce profiling with python version (pre & post DP)
## 2022/04/13
Mac os auto updated following an overnight crash from 11.6 to `11.6.5 (20G527)`. 
VS Code updates were turned off, going forward: `Version: 1.66.2
Commit: dfd34e8260c270da74b5c2d86d61aee4b6d56977
Date: 2022-04-11T07:49:20.994Z
Electron: 17.2.0
Chromium: 98.0.4758.109
Node.js: 16.13.0
V8: 9.8.177.11-electron.0
OS: Darwin x64 20.6.0`

## 2022/05/12
Profiling of run time for MLDSP pre and post sharcnet dedicated programming (DP) refactoring. The bulk of refactoring was done by Sergio Hleap in collaboration with myself. For both versions profiling was performed by myself on my local mac computer using VS code and it's integrated terminal; the code profiled is from https://github.com/HillLab/MLDSP repository.  

### Pre sharcnet DP profiling
## Comment: better (more controled) profiling method see 2022/05/16
For preDP refactor of MLDSP python, **the code used was from commit 0f8f3ed**. Results are found in `Profiling/Initial attempts/Bacteria_preDP_cleanvenv` with `Bacteria_preDP_cleanvenv_profile.prof` file being the cProfile output. Profiling was run in a new python 3.9.0 virtual environment using the command `python main.py`, installed modules are listed in `preDP_cleanvenv_requirements.txt`. The following code was added to line 1 of main.py:

### cProfile code blocks
```python 
import cProfile
profiler = cProfile.Profile()
profiler.enable()
```
Followed at the end of the main.py script (line 282 as seen in commit, N.B lines numbers shifted after addition of .enable codeblock): 
```python
profiler.disable()
profiler.dump_stats(f'{Run_name}_profile.prof')
```
All other mentions of cProfile/Pstats code were removed/commented from main.py as seen in the commit, `data_set` (line 110), `metadata` (line 111), `Run_name` (line 112) and `k_val` (line 127) variables were changed to the "BacteriaTest" dataset and k value of 6 respectively. No other code modifications from what is seen in the commit were made, all line numbers are quoted as seen in the commit (as modifications susequently change line numbering). **Exact profiling code existed only on local machine as profiling occured after commit 0f8f3ed where the branch had significant commits; to reporduce profiling download the given commit and perform above mentioned modifications before running**   

**Any 'Profiling' results/files seen in this or subsequent MLDSP code commits on github should not be interpreted as they may be incorrect or test runs, only results in this MSC_github repository**  
Profiling results can be viewed by importing the desired cProfile output file into the [profiling.ipynb](../Scripts/profiling.ipynb) jupyter notebook. The aproximate total run time was **930.171 s**.

N.B cProfile could not be run from the command line as a module due to errors in pickling within the parallel code (pool).
```
Traceback (most recent call last):
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/cProfile.py", line 180, in <module>
    main()
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/cProfile.py", line 173, in main
    runctx(code, globs, None, options.outfile, options.sort)
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/cProfile.py", line 19, in runctx
    return _pyprofile._Utils(Profile).runctx(statement, globals, locals,
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/profile.py", line 62, in runctx
    prof.runctx(statement, globals, locals)
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/cProfile.py", line 100, in runctx
    exec(cmd, globals, locals)
  File "MLDSP/main.py", line 177, in <module>
    for abs_fft_output, fft_output, cgr_output in pool.map(partial(compute_cgr, seq_dict=seq_dict, keys=keys, method_num=method_num, k_val=k_val,Result_path=Result_path), range(total_seq)):
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/multiprocessing/pool.py", line 364, in map
    return self._map_async(func, iterable, mapstar, chunksize).get()
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/multiprocessing/pool.py", line 771, in get
    raise self._value
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/multiprocessing/pool.py", line 537, in _handle_tasks
    put(task)
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/multiprocessing/connection.py", line 211, in send
    self._send_bytes(_ForkingPickler.dumps(obj))
  File "/Users/dolteanu/.pyenv/versions/3.9.0/lib/python3.9/multiprocessing/reduction.py", line 51, in dumps
    cls(buf, protocol).dump(obj)
_pickle.PicklingError: Can't pickle <function compute_cgr at 0x108392820>: attribute lookup compute_cgr on __main__ failed
```
### PostDP profiling
## Comment: better (more controled) profiling method see 2022/05/16
For postDP refactor profiling, **the code used was from commit 99beda1**. Results are found in `Profiling/Initial attempts/BacteriaTest_postDP_cleanvenv` with `postDP_profile.prof` file being the cProfile output. Profiling was run from the command line in a new and unique python 3.9.0 virtual environment; installed modules are listed in `postDP_cleanvenv_requirements.txt`. The following command was used for post DP profiling: `python -m cProfile -o ./postDP_profile.prof -m MLDSP_core.main path/to/BacteriaTest/fastas path/to/metadata.csv -k 6 -r BacteriaTest`. The aproximate total runtime was **~1800 s** or 2X the pre sharcnet DP runtime.

## 2022/05/13
VS Code extensions were found to be auto updating and turned off, going forward unless otherwise stated versions will be: 
```
alefragnani.rtf@2.5.0
codezombiech.gitignore@0.7.0
donjayamanne.python-environment-manager@1.0.4
donjayamanne.python-extension-pack@1.7.0
eamodio.gitlens@12.0.6
emmanuelbeziat.vscode-great-icons@2.1.86
Gimly81.matlab@2.3.1
GitHub.vscode-pull-request-github@0.40.0
GrapeCity.gc-excelviewer@4.2.54
KevinRose.vsc-python-indent@1.15.0
magicstack.MagicPython@1.1.0
ms-python.python@2022.4.1
ms-python.vscode-pylance@2022.5.1
ms-toolsai.jupyter@2022.3.1000901801
ms-toolsai.jupyter-keymap@1.0.0
ms-toolsai.jupyter-renderers@1.0.6
ms-vscode-remote.remote-containers@0.234.0
ms-vscode-remote.remote-ssh@0.80.0
ms-vscode-remote.remote-ssh-edit@0.80.0
ms-vscode-remote.remote-wsl@0.66.2
ms-vscode-remote.vscode-remote-extensionpack@0.21.0
ms-vsliveshare.vsliveshare@1.0.5561
njpwerner.autodocstring@0.6.1
samuelcolvin.jinjahtml@0.17.0
VisualStudioExptTeam.vscodeintellicode@1.2.21
wholroyd.jinja@0.0.8
yzhang.markdown-all-in-one@3.4.3
```

## 2022/05/16
Concerns were raised about comparing profiling results between in script vs command-line execution of cProfile and various background programs along with VS Code confounding profiling results. Profiling was re-run for both pre & post sharcnet DP code respectively using the aforementioned commits, python virtual environments, dataset and CGR kmer value as decribed in sub-section [2022/05/12](#20220512). MAIN difference here is only using cProfile in-script; the other differences being that instead of VS Code terminal used, the default MacOS terminal was used to launch the respective pre or post DP version of the MLDSP after all other programs were closed and the local machine restarted. The terminal was the only program opened from the MacOS GUI after restart to launch each profiling run and delete any `__pycache__` present in the virtual environments. This time for postDP profiling the following code was added to the start of  `main.py` script (line 9):
```
import cProfile
profiler = cProfile.Profile()
profiler.enable()
```
and the following at the end of the `main.py` script (line 278 as seen in commit 99beda1, N.B lines numbers shifted after addition of .enable codeblock)
```
profiler.disable()
profiler.dump_stats(f'{args.run_name}_profile.prof')
```
This was done to control for variances in running profiler inside the script(previously done for pre DP profiling) vs. as a command-line module (previously done only for post DP profiling). Another possible confounding error is to have the profiler disable function NOT indented under `if __name__ == '__main__':` versus indented as it is in these runs; more experimentation here may be required. **in script execution of cProfile for Post DP was not used until much later (2022/11/14) due to incorrect calling of cProfile CLI despite codeblock being added**
###  Pre DP profiling final results
MLDSP output from this profiling run can be found in `Profiling/preDP/Bacteria_fullscript` with the cProfile output file [Bacteria_fullscript_profile.prof](../Profiling/preDP/Bacteria_fullscript_profile.prof). Run time was **829.277 s** and full results can be viewed from the `.prof` using the [profiling.ipynb](../Scripts/profiling.ipynb) jupyter notebook.
### Post DP profiling
## Comment: re-run several times below, iterave modifications to narrow down runtime gap with Pre DP results, all results under `Profiling/postDP`
(cProfile in CLI mode here; comparison to preDP incorrect)
MLDSP output from this profiling run can be found in `Profiling/Initial attempts/Bacteria_fullscript` with the cProfile output file `Bacteria_post_fullscript_profile.prof`. Run time was **~1900 s**. 

## 2022/05/25
### Ontario covid (gisaid classes) MLDSP run
### Comment: Dataset renamed to 'Ontario_gisaid_1' but subsequently deleted as accuracy percentage was misformatted
MLDSP CLI was run on the cloud machine Ubuntu 20.04 virtual machine with 40 cores, 160 Gb RAM using the Ontario covid data provided by David Chen using the gisaid clade class labels. Clade L with 7 samples was removed from both metadata `gisaid_filtered<10.csv` and fasta file `ontario_filtered<10.fasta`. Default numerical method (CGR) and k value (7) were used: (note CLI arguments not specified as these are the defaults for this version of MLDSP CLI ). Samples "Canada/Hu-1/2019" and "Microbiologist-in-Chief" were removed from the metadata as they weren't present in the fasta. Command used to run MLDSP CLI: `MLDSP ./daniel_data/Ontario_covid/OneDrive_1_2022-02-06/ ./daniel_data/Ontario_covid/gisaid_filtered\<10.csv -r Ontario_covid`  

## 2022/05/30
### Ontario covid (epochs classes) MLDSP run **Ontario_epochs**
MLDSP CLI was run on the cloud using the same Ontrio covid dataset with identical parameters except different metadata of epochs as class labels: `MLDSP ./daniel_data/Ontario_covid/OneDrive_1_2022-02-06/ ./daniel_data/Ontario_covid/epoch_metadata.csv -r Ontario_epochs`. Not deduplicated data, may want to re-run with deduplicated in the future.
### Comment: INCORRECT DEDUPLICATION, rerun on 06/25
Performed sequence deduplication of Ontario covid dataset using Seqkit 2.2.0 with the following command: `seqkit rmdup -P -i -s -D duplicates.txt concatenated.fasta ` on my local computer, duplicates saved in `duplicates.txt`. **Deduplicated datasets only used if explicitly mentioned, otherwise non-deduplicated**  

### 2022/06/07
Re-ran MLDSP CLI on the cloud, same Ontario covid dataset, identical parameters (cgr, k=7) with gisaid class data after updating MLDSP to commit `2a483b3` (fixed results format & speedup, no functional change), Run name: **Ontario_gisaid_2**,. Not deduplicated data

### 2022/06/15
### Post DP profiling
On local machine Post DP profiling was run as previously described on 2022/05/12 (cProfile in CLI mode here; comparison to preDP incorrect) except MLDSP code from commit **59c47bf** is used going forward, and command modified as follows: `python -m cProfile -o ./postDP_2.prof -m MLDSP_core.main /Users/dolteanu/local_documents/Coding/MLDSP_dev_git/data/BacteriaTest/fastas /Users/dolteanu/local_documents/Coding/MLDSP_dev_git/data/BacteriaTest/metadata.csv -k 6 -r BacteriaTest_postDP_2`  
Run **BacteriaTest_postDP_2** time was reduced to ~1500 s by restricting computation of full model only to last fold.

### MLDSP codebase going forward is branched; will be specified as either daniel or dev branch until merged, dev branch is being kept separate (stale) for post DP profiling. daniel branch is run in a separate python virtual environment on the server
daniel branch (commit 43120a7) includes classification report (precision, recall & F1), Area Under the Receiver Operator Characteristic 'score' and **BALANCED ACCURACY SCORE**. daniel branch updated to commit 695dd9c modified so that CGR figure shows 1st (arbitrary) CGR from each class in a MLDSP run.

# Comment: Multiple hardware failures occured on this cloud over the next 3 weeks
Re-ran MLDSP CLI on cloud again, same Ontario covid dataset (Not deduplicated data), identical parameters (cgr, k=7) with gisaid class data but using MLDSP repo **daniel branch (commit 695dd9c)** in a new virtualenv on the cloud; run failed due to server hardware failure, temp. files deleted.  

### 2022/06/25
Realized the deduplication command that was ran on 05/30 was incorrect, output file was not deduplicated because I ran it incorrectly, below is the correct command that was re-run: `cat 'ontario_filtered<10.fasta' | seqkit rmdup -P -i -s -o './OneDrive_1_2022-02-06/deduplicated<10.fasta' -D duplicates.txt`, old duplicate outputs from 05/30 were removed. The duplicates.txt was used as input into `deduplication.ipynb` to build the `removed_duplicates_ont_covid.csv` with accession Id, gisaid class label pairs in row. 
output: `4299 duplicated records removed`  

## Metadata fix
MLDSP update which changes logic so that all samples in fasta must be in metadata but not inverse (metadata file can have extra sample ids & act as a "database", previously had to be remade everytime).  This is required to run MLDSP with deduplicated datasets without regenerating metadata file.

Deduplicated fasta file `deduplicated<10.fasta` was used in the following run **Ontario_gisaid_3**:
`MLDSP daniel_data/Ontario_covid/OneDrive_1_2022-02-06/ daniel_data/Ontario_covid/gisaid_filtered\<10.csv -r Ontario_gisaid_3`. MLDSP version here is a local version of future commit 3172c7d

### 2022/06/28
### Post DP profiling
Re-ran post DP profiling using the same procedure as stated on 2022/05/12 (cProfile in CLI mode here; comparison to preDP incorrect) and commit **59c47bf (dev branch)** , except the following command was used:
`python -m cProfile -o ./postDP_no_testing.prof -m MLDSP_core.main /Users/dolteanu/local_documents/Coding/MLDSP_dev_git/data/BacteriaTest/fastas /Users/dolteanu/local_documents/Coding/MLDSP_dev_git/data/BacteriaTest/metadata.csv -k 6 -r BacteriaTest_no_testing`  
Run **BacteriaTest_no_testing** time was reduced to ~1200 s by removing execution of full model training (used for testing prediction) altogether; roughly 2X the pre DP run time, down from 3X initially.

### 2022/07/15
MLDSP repo updated to **commit 3172c7d** encompassing metadata changes from 06/25.

### 2022/07/27
Re-run MLDSP CLI **daniel_branch 3172c7d** on the cloud using `ontario_filtered<10.fasta` data file, this is essentially a rerun of `Ontario_gisaid_2` but using balanced accuracy score to make appropriate comaprison between deduplicated (Ontario_gisaid_3) and unduplicated runs of MLDSP (here named **Ontario_gisaid_4**): `MLDSP daniel_data/Ontario_covid/OneDrive_1_2022-02-06/ daniel_data/Ontario_covid/gisaid_filtered\<10.csv -r Ontario_gisaid_4`.

Ran MLDSP CLI **daniel_branch 3172c7d** on local with Nextstrain dataset using both Gisaid clades **Nextstrain_gisaid<20** and Nextstrain clades **Nextstrain<20**. In both cases datasets were cleaned to remove classes with fewer than 20 samples (so each fold in 10X cross validation has at least 2 samples in worst case). Re-run below with imporved output formatting but results remain the same, Class size 'incorrect' showing removed classes present in metadata but not run
```
10X cross validation classifier accuracies:
	LinearDiscriminant: 0.8360432725435075
	LinearSVM: 0.8974799496620509
	QuadSVM: 0.36659675338743114
	KNN: 0.6679658896956
```

### 2022/11/14
### Post DP profiling
Re-ran post DP profiling on local machine with cProfile in-line as shown in the [cProfile code blocks](#cprofile-code-blocks) using the following command: `python -m MLDSP_core.main /Users/dolteanu/local_documents/Coding/MLDSP_dev_git/data/BacteriaTest/fastas /Users/dolteanu/local_documents/Coding/MLDSP_dev_git/data/BacteriaTest/metadata.csv -k 6 -r BacteriaTest_no_testing_2`. **BacteriaTest_no_testing_2**

Realized the reason for 2X discrepancy between pre and post Sharcnet Dedicated Programming (DP) is that the preDP profiling was done with MLDSP MoDMap computed using principle componenet analysis (PCA) method but the post DP profiling was done with MLDSP MoDMap computed using multi-dimensional scaling (MDS). This can be seen when comparing the outputs of the `profiling.ipynb` respectively. This hypothesis will be tested by running the postDP profiling one more time using the PCA method. 

### 2022/11/15
## Actual final post sharcnet DP profiling results
Ran post DP profiling again from same commit **59c47bf (dev branch)** but with MoDMap method set to PCA (full model still commented out)
`python -m MLDSP_core.main /Users/dolteanu/local_documents/Coding/MLDSP_dev_git/data/BacteriaTest/fastas /Users/dolteanu/local_documents/Coding/MLDSP_dev_git/data/BacteriaTest/metadata.csv -k 6 -i 'pca' -r BacteriaTest_no_testing_3`. **BacteriaTest_no_testing_3** Total run time was ~770s which is faster than the preDP profiling ~830s. For an accurate comparison to MATLAB, we must wait for scikit learn pull request #

Run **Ontario_epochs_2** on the cloud with deduplicated Ontario covid dataset and epochs metadata `nohup MLDSP /home/ubuntu/daniel/daniel_data/Ontario_covid/OneDrive_1_2022-02-06/ /home/ubuntu/daniel/daniel_data/Ontario_covid/epoch_metadata.csv -k 7 -r Ontario_epochs_2 > ./Ontario_epochs_2.log &`

### 2023/01/03
## ALL MLDSP runs up to now will have inaccurate Class sizes showing what is available in the metadata.csv not how many samples per class from the fasta were actually run. Class sizes will not sum up to total dataset size
Cleaned MLDSP confusion matrix output to show whole numbers an intercluster distance csv to show scientific notation.  
MLDSP CLI now ouputs MoDMap.json (same as what is passed to web server) which can be viewed with plotly in python or in jupyter notebook.

### 2023/01/04
MLDSP github: 'daniel' branch merged into 'dev' branch and 'daniel' branch deleted but all commit numbers remain available in dev branch.


