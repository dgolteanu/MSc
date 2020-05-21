# Compute canada tutorial
Documentation: docs.computecanada.ca
clusters: cedar.computecanada.ca x.computecanada.ca
cloud (running database, portals): graham.cloud.computecanada.ca, arbutus.cloud.computecanada.ca, east.cloud.computecanada.ca


Look into MPI (which one is best?)
OpenMP: parallelise legacy code
CUDA: gpu multithreding

How would we leverege multithreading in non supported language (python)

Batch computing via slurm
## login nodes
/home: 50G (source code)

/project: 1T upto 10T per group (run programs here)

/scratch: 20T upto 100T per user, not backed up & 2 month limit (intermediate files)

nearline: store less used files (not available on compute nodes

moving files: SSHFS (mounted drive) or scp/sftp

# Running a job (slurm)
` #!/bin/bash #SBATCH-time=01:00 #DD-HH:MM #SBATCH-account=def-bge (billing account) R -no-save --args input 23 output < sample.R`

## Running a series of jobs
`#!/bin/bash #SBATCH-time=01:00 #DD-HH:MM #SBATCH-account=def-bge (billing account)#SBATCH--array=1-200 R-no-save--args input $SLURM_ARRAY_TASK_ID \ output < sample.R` where inputN.csv and outputN.csv N will be replaced by slurm id

## Submitting a threaded job
`-cpus-per-task=32` # One single cpu with 32 cores
set thread option ` export\ (-t, OMP_NUM_THREADS)=$SLURM_CPUS_PER_TASK `

# Submitting a parallel job
#SBATCH --ntasks
srun ./myMPIproj.exe

Tip: use node reservation instead of by core

`quota`
`module spider julia` is the spyder program available for julia
`module list` currently loaded modules
`module load`

# Submitting serial job

`#SBATCH --output=%x-%j sbatch job.sh scancel # cancel a job # %x replaced by jobname %j` 
