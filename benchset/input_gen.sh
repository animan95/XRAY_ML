#!/bin/bash
PATHTOFILE=/users/PAS0291/aniketmandal95/shift_ML/benchset

sed -i '/$rem/,/$end/d' $PATHTOFILE/*.in 
sed -i '/$alist/,/$end/d' $PATHTOFILE/*.in
for file in $(ls *.in)
do 
  cat rem.txt >> ${file}
done
