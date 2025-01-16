#!/bin/bash
#SBATCH --job-name=TiO2_camb3lyp
#SBATCH --time=02:59:00
#SBATCH --nodes=1 --ntasks=20
#SBATCH --account=PAS0291
#SBATCH --output=%x.%j
#SBATCH --mem=100gb

cd $SLURM_SUBMIT_DIR
module unload mvapich
module load boost
module load qchem/6.1.0
export QC=/users/PAS0291/aniketmandal95/qctrunk2
#export QCSCRATCH=/users/PAS0291/aniketmandal95
export QCAUX=/users/PAS0291/aniketmandal95/qcaux
export QCSCRATCH=$TMPDIR
echo 'This job is running on ' `hostname`
echo 'Temporary directory is ' $TMPDIR
echo 'Q-Chem scratch directory is ' $QCSCRATCH
$QC/bin/qchem -nt 20 Be_at.in > Be_at.out
#$QC/bin/qchem -save $FileName.in $FileName.out "$FileName"dat


