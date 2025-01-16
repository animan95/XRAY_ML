#!/bin/bash

# Base directory path
base_path="/users/PAS0291/aniketmandal95/shift_ML/row1"  # Replace with your base directory path

# Directories and subdirectories
directories=("scan0" "b3lyp" "cam-b3lyp" "pbe0")
subdirectories=("631G" "aug-cc-pvdz" "aug-cc-pvtz" "def2-tzvpd" "cc-pvtz" "def2-sv_p")
rel_val=("0.03" "0.01" "0.08" "0.53" "0.00" "0.17" "0.84" "0.31")
# Output fite
output_file="testdataset2.csv"

# Clear the output file and add the header
echo "Function,Basis,System,BasFunc,Input,Reference,RelVal" > "$output_file"

# Function to extract the number after '-- Occupied --' section
extract_number() {
    local file=$1
    #grep -A9999 -- ' -- Occupied --' "$file" | grep -B9999 -- ' -- Virtual --' | grep -oE '[0-9]+(\.[0-9]+)?'
     grep -A1 ' -- Occupied --' "$file" | tail -n1 | awk '{print $1}'
}

# Function to extract the number of basis functions
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

# Iterate over directories and subdirectories
for dir in "${directories[@]}"; do
    if [ "$dir" != "src1" ]; then
        for subdir in "${subdirectories[@]}"; do
            subdir_path="$base_path/$dir/$subdir"
            if [ -d "$subdir_path" ]; then
                count=0  # Reset count for each directory
                for file in "$subdir_path"/*_at.out; do
                    if [ -f "$file" ]; then
                        filename=$(basename "$file" "_at.out")
                        number=$(extract_number "$file")
                        basnum=$(extract_bas "$file")
                        src1_number="${src1_values["def2-tzvpd/$filename"]}"
                        src1_def2="${src1_values["def2-tzvpd/$filename"]}"
                        rel="${rel_val[$count]}"
                        if [ -n "$number" ] && [ -n "$src1_number" ]; then
                            echo "$dir,$subdir,$filename,$basnum,$number,$src1_number,$rel" >> "$output_file"
                        elif [ -n "$number" ]; then
                            echo "$dir,$subdir,$filename,$basnum,$number,$src1_def2,$rel" >> "$output_file"
                        fi
                        ((count++))
                    fi
                done
            fi
        done
    fi
done

echo "Data written to $output_file"
