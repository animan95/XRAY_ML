#!/bin/bash
PATHTOFILE=/users/PAS0291/aniketmandal95/shift_ML/row1/scan0/631G

sed -i '/$rem/,/$end/d' $PATHTOFILE/*.in 

for file in $(ls *.in)
do 
  cat rem.txt >> ${file}
done
