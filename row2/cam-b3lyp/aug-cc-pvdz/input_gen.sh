#!/bin/bash
PATHTOFILE=/users/PAS0291/aniketmandal95/shift_ML/row2/cam-b3lyp/aug-cc-pvdz

sed -i '/$rem/,/$end/d' $PATHTOFILE/*.in 

for file in $(ls *.in)
do 
  cat rem.txt >> ${file}
done
