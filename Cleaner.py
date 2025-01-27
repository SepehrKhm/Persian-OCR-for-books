import os

def find_txt_files(directory):
    txt_files = [file for file in os.listdir(directory) if file.endswith('.txt')]
    return txt_files

def clean_file_content(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    cleaned_lines = [line for line in lines if not line.startswith(("Filename:", "Left column:", "Right column:"))]
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)

directory_path = "C:/Users/Asus/Desktop/code/python/PdfExtractor/جزایی"     ##################################################################
output_directory = os.path.join(directory_path, "cleaned_files")
os.makedirs(output_directory, exist_ok=True)

txt_files = find_txt_files(directory_path)

print("Processing text files:")
for txt_file in txt_files:
    file_path = os.path.join(directory_path, txt_file)
    output_path = os.path.join(output_directory, txt_file)
    print(f"Creating cleaned file: {output_path}")
    clean_file_content(file_path, output_path)

print(f"All files have been cleaned. Cleaned files are saved in: {output_directory}")
