# Daniel Olteanu lab book in the Hill lab at the University of Western Ontario
## This lab book is intended to be a complete technical track record of programs run and/or created to generate new results/data. It is meant to be completely reproducible
## 2019/09/23
MSc git repository was created on Daniel's local machine and

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

## 2021/06/16
Downloaded all available GISAID data from website portal https://www.epicov.org/epi3/frontend > "EpiCoV" tab > "Downloads" tab > pop up > "Download packages" header> select "FASTA" and "metadata" download buttons. After unziping the tar.xz we get 2 folders: sequences_fasta_2021_06_16 and metadata_2021_06_16. Also downloaded on the same day all protein sequences https://www.epicov.org/epi3/frontend > "EpiCoV" tab >"Downloads" tab > pop up > "Alignment and proteins" header > allprotXXXX file where on this date XXXX = 0322

NOT USED:
Downloaded Nextstrain website data https://nextstrain.org/ncov/gisaid/global scroll to bottom of page select "DOWNLOAD DATA" button at the very bottom center see ![Nextstrain website download example]('/Users/dolteanu/local_documents/Coding/MSc_github/Lab book/Nextstrain website data download example 2021:06:16.png')

## 2021/08/23
Profiling of MATLAB MLDSP using the BacteriaTest dataset
## 2021/10/06

Redownloaded all available gisaid data from website portal https://www.epicov.org/epi3/frontend > "EpiCoV" tab > "Downloads" tab > pop up > "Download packages" header> select "FASTA" and "metadata" download buttons. After unziping the tar.xz we get 2 folders: sequences_fasta_2021_10_06 and metadata_2021_10_06

## 2022/01/11
Downloaded data used to build tree on Nextstrain's website from the GISAID website portal https://www.epicov.org/epi3/frontend > "EpiCoV" tab > "Downloads" tab > pop up > "Genomic epidemiology" header > 'nextregions' button > pop up "Region-specific Auspice source files" > "Global" download button. This gives "hcov_global_2022-01-09_23-30" containing the fasta of sequences used on the nextstrain website https://nextstrain.org/ncov/gisaid/global as seen on January 9 2022

## 2022/02/27
Will have to redownload the nextstrain website data & raw data used to build it from gisaid on the same day (weekday)

## 2022/03/21
Running Mantel test of Dengue dataset vs covid19 gisaid data, may not be appropriate for different datasets; available packages require symmetric matrix of same size (assumed to come from same dataset), which our use case does not satisfy

## 2022/04/11
MATLAB mldsp was previously profiled on [2021/08/23](#20210823) on my mac at the time running macos 11.5 (MATLAB R2019a). The BacteriaTest dataset was used with the cgr numerical method at k=6; the builtin profiler was run using the `Run & Time` button on the MATLAB desktop, as described in the [MATLAB documentation](https://www.mathworks.com/help/matlab/matlab_prog/profiling-for-improving-performance.html#mw_e3eebe5c-984d-42ad-8b1f-6269890525fc). All other programs were closed during the profiling run. Profiling results can be found in [Profiling/MATLAB/Timing.pdf](../Profiling/MATLAB/Timing.pdf), the approximate run time was **~590 s**.  
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
For preDP refactor of MLDSP python, **the code used was from commit 0f8f3ed** ; only code modifications was changing k value to 6. Results are found in `Profiling/First attempt/Bacteria_preDP_cleanvenv` with [Bacteria_preDP_cleanvenv_profile.prof](../Profiling/First%20attempt/Bacteria_preDP_cleanvenv/Bacteria_preDP_cleanvenv_profile.prof) file being the cProfile output. Profiling was run in a new python 3.9.0 virtual environment, installed modules are listed in [preDP_cleanvenv_requirements.txt](../Profiling/First%20attempt/Bacteria_preDP_cleanvenv/preDP_cleanvenv_requirements.txt). The following code was added/uncommented to the 1st line of main.py 
```
import cProfile
profiler = cProfile.Profile()
profiler.enable()
```
Followed at the end of the main.py script with 
```
profiler.disable()
profiler.dump_stats(f'{Run_name}_profile.prof')
```
Profiling results can be viewed by importing the desired cProfile output file into the [profiling.ipynb](../Scripts/profiling.ipynb) jupyter notebook. The aproximate total run time was **~900 s**.

cProfile could not be run from the command line as a module due to errors in pickling within the parallel code (pool).
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
For postDP refactor profiling, **the code used was from commit 99beda1**. Results are found in `Profiling/BacteriaTest_postDP_cleanvenv` with [postDP_profile.prof](../Profiling/First%20attempt/BacteriaTest_postDP_cleanvenv/postDP_profile.prof) file being the cProfile output. Profiling was run in a new and unique python 3.9.0 virtual environment; installed modules are listed in [postDP_cleanvenv_requirements.txt](../Profiling/First%20attempt/BacteriaTest_postDP_cleanvenv/postDP_cleanvenv_requirements.txt). The following command was used for post DP profiling: `python -m cProfile -o ./postDP_profile.prof -m MLDSP_core.main path/to/BacteriaTest/fastas path/to/metadata.csv -k 6 -r BacteriaTest`. The aproximate total runtime was **~1800 s** or 2X the pre sharcnet DP runtime.

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
Concerns were raised about comparing profiling results between in script vs command-line execution of cProfile and various background programs along with VS Code confounding profiling results. Profiling was re-run for both pre & post sharcnet DP code respectively using the same commits, python virtual environments, dataset and CGR kmer value as decribed in sub-section [2022/05/12](#20220512). The differences being that instead of VS Code terminal used, the default MacOS terminal was used to launch the respective pre or post DP version of the program after all other programs were closed and the local machine restarted. The terminal was the only program opened from the MacOS GUI after restart to launch each profiling run and delete any `__pycache__` present in the virtual environments. This time for both pre and post DP the following code was appended to the start of the respective `main.py` scripts:
```
import cProfile
profiler = cProfile.Profile()
profiler.enable()
```
and the following at the end of the respective `main.py`
```
profiler.disable()
profiler.dump_stats(f'{Run_name}_profile.prof')
```
This was done to control for variances in running profiler inside the script vs. as a command-line module (previously done for post DP profiling). Another possible confounding error was having the post script profiler functions indented under `if __name__ == '__main__':` during the first attempt of pre DP code profiling.
###  Pre DP final results
MLDSP output from the profiling run can be found in `Profiling/preDP/Bacteria_fullscript` with the cProfile output file [Bacteria_fullscript_profile.prof](../Profiling/preDP/Bacteria_fullscript_profile.prof). Run time was **~600 s** and full results can be viewed from the `.prof` using the [profiling.ipynb](../Scripts/profiling.ipynb) jupyter notebook.
### Post DP final results
MLDSP output from the profiling run can be found in `Profiling/postDP/Bacteria_fullscript` with the cProfile output file [Bacteria_post_fullscript_profile.prof](../Profiling/postDP/Bacteria_post_fullscript_profile.prof). Run time was **~1900 s**. 

### 2022/05/19


