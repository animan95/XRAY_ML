#!/bin/bash
PATHTOFILE=/users/PAS0291/aniketmandal95/shift_ML/row2/pbe/def2-tzvpd

sed -i '/$rem/,/$end/d' $PATHTOFILE/*.in 

for file in $(ls *.in)
do 
  cat rem.txt >> ${file}
done
