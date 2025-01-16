#!/bin/bash

# Base directory path
base_path="/users/PAS0291/aniketmandal95/shift_ML/row2"  # Replace with your base directory path

# Directories and subdirectories
directories=("b3lyp" "bhhlyp" "cam-b3lyp" "pbe" "pbe0" "src1" "wB97" "blyp")
subdirectories=("631G" "aug-cc-pvdz" "aug-cc-pvtz" "def2-sv_p" "def2-svpd" "def2-tzvp" "def2-tzvpd")
rel_val=("3.61" "12.98" "10.44" "2.67" "1.89" "6.50" "8.29" "4.97")
# Output file
output_file="dataset.txt"

# Clear the output file and add the header
echo "Function,Basis,System,BasFunc,Input,Reference,RelVal" > "$output_file"

# Function to extract the number after '-- Occupied --' section
extract_number() {
    local file=$1
    grep -A1 ' -- Occupied --' "$file" | tail -n1 | awk '{print $1}'
}

extract_bas() {
    local file=$1
    grep -oP 'There are \d+ shells and \K\d+' "$file"
}

# Read all src1 values into an associative array
declare -A src1_values

for subdir in "${subdirectories[@]}"; do
    subdir_path="$base_path/src1/$subdir"
    if [ -d "$subdir_path" ]; then
        for file in "$subdir_path"/*_at.out; do
            if [ -f "$file" ]; then
                filename=$(basename "$file" "_at.out")
                number=$(extract_number "$file")
                if [ -n "$number" ]; then
                    src1_values["$subdir/$filename"]="$number"
                fi
            fi
        done
    fi
done
count=0
# Iterate over directories and subdirectories
for dir in "${directories[@]}"; do
    if [ "$dir" != "src1" ]; then
        for subdir in "${subdirectories[@]}"; do
            subdir_path="$base_path/$dir/$subdir"
            if [ -d "$subdir_path" ]; then
                for file in "$subdir_path"/*_at.out; do
                    if [ -f "$file" ]; then
                        filename=$(basename "$file" "_at.out")
                        number=$(extract_number "$file")
                        src1_number="${src1_values["def2-tzvpd/$filename"]}"
                        basnum=$(extract_bas "$file")
                        rel="${rel_val[$count]}"
                        if [ -n "$number" ] && [ -n "$src1_number" ]; then
                            echo "$dir,$subdir,$filename,$basnum,$number,$src1_number,$rel" >> "$output_file"
                        elif [ -n "$number" ]; then
                            echo "$dir, $subdir, $filename, $number, NA" >> "$output_file"
                        fi
                       ((count++))
                    fi
                done
            fi
                  count=0
        done
    fi
done

echo "Data written to $output_file"

