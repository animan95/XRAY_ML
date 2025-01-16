#!/bin/bash
for item in *.slurm; do
    sbatch $item
done
