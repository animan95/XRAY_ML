import os
import re

def extract_number(file_path):
    """Extract the first number after the '-- Occupied --' section in the file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    match = re.search(r'-- Occupied --\s+([\d.-]+)', content)
    if match:
        return match.group(1)
    else:
        print(f"The '-- Occupied --' section or number not found in the file: {file_path}")
        return None

def process_files_in_subdirectory(subdirectory_path):
    """Process all *_at.out files in a subdirectory and extract numbers."""
    numbers = []
    for file_name in os.listdir(subdirectory_path):
        if file_name.endswith('_at.out'):
            file_path = os.path.join(subdirectory_path, file_name)
            number = extract_number(file_path)
            if number:
                numbers.append((file_name[:-7], number))  # Remove '_at.out' from filename
    return numbers

def main():
    base_path = '/users/PAS0291/aniketmandal95/shift_ML/row2'  # Replace with your base directory path
    directories = ['/b3lyp', '/bhhlyp', '/cam-b3lyp', '/pbe', '/pbe0', '/src1', '/wB97']
    subdirectories = ['/631G', '/aug-cc-pvdz', '/aug-cc-pvtz', '/def2-sv_p', '/def2-svpd', '/def2-tzvp', '/def2-tzvpd']
    output_file = 'dataset.txt'  # Output file name
    
    print(f"Base path: {base_path}")
    
    # Open output file for writing
    with open(output_file, 'w') as f:
        # Iterate over each directory
        for directory in directories:
            directory_path = os.path.join(base_path, directory)
            print(f"Processing directory: {base_path}")
            if os.path.isdir(directory_path):
                print(f"Processing directory: {directory_path}")
                # Iterate over each subdirectory
                for subdirectory in subdirectories:
                    subdirectory_path = os.path.join(directory_path, subdirectory)
                    if os.path.isdir(subdirectory_path):
                        print(f"Processing subdirectory: {subdirectory_path}")
                        # Process files in each subdirectory
                        subdirectory_numbers = process_files_in_subdirectory(subdirectory_path)
                        
                        # Write combined results to output file
                        for filename, number in subdirectory_numbers:
                            f.write(f"{directory}, {subdirectory}, {filename}, {number}\n")
                            print(f"Writing to file: {directory}, {subdirectory}, {filename}, {number}")
    
    print(f"Data written to {output_file}")

if __name__ == "__main__":
    main()

