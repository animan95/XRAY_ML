#!/bin/bash
PATHTOFILE=/users/PAS0291/aniketmandal95/shift_ML/row1/b3lyp/def2-tzvp

sed -i '/$rem/,/$end/d' $PATHTOFILE/*.in 

for file in $(ls *.in)
do 
  cat rem.txt >> ${file}
done
