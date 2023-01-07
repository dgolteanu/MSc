sudo install is required for node server
when updating MLDSP run `git pull`

`sudo pip install -e .` gives `which MLDSP` = `/usr/bin/MLDSP` and CLI does not work.  


`sudo pip install .` gives `which MLDSP` = `/usr/local/bin/MLDSP` and CLI does work (with sudo access).  
Unclear still if `sudo pip install . -U` works.



if you get a `pyfaidx.FastaNotFoundError: Cannot read FASTA file /home/ubuntu/daniel/Results/Ontario_gisaid_2/Train_all_seqs.fasta` error it's probably because you speficied a single fasta file instead of parent dir
