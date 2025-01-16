#!/bin/bash

# Set the keyword you want to search for
keyword="-- Occupied --"

# Specify the directory where your files are located
directory_path= "/users/PAS0291/aniketmandal95/dftcis_param/row2_camb3lyp"
rm /users/PAS0291/aniketmandal95/dftcis_param/row2_camb3lyp/camb3lyp_en.txt
# Use the find command to locate text files in the directory
find $directory_path -type f -name "*.out" -print0 |
while IFS= read -r -d $'\0' file; do
    # Use grep to find lines containing the keyword, and awk to extract the first word from the next line
    if grep -q -e "$keyword" "$file"; then
        # Use awk to print the first word from the next line
        next_line=$(sed -n "/$keyword/{n;p}" "$file")
        # Use awk to extract the first word from the next line
        first_word=$(awk '{print $1}' <<< "$next_line")
        echo "$first_word" >> "camb3lyp_en.txt"
    fi
done

