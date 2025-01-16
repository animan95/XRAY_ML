template_file="$(pwd)/templ_custm.slurm"

files="$(ls -p *.in | cut -d "." -f1 | grep -v / | tr '\n' ',')"

file_array=($(echo $files | tr "," "\n"))

echo ${file_array}

for file in ${file_array[@]}; do
        sed "s/TODO_NAME/${file}/g" ${template_file} > ${file}.slurm
    done
