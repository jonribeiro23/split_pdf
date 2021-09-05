from split import split_pdf
from get_files import get_files_name
from pdf import ocr_file
from tqdm import tqdm
import subprocess

# https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052
# https://www.thepythoncode.com/article/extract-text-from-images-or-scanned-pdf-python

menu = 0

while menu != 9:
    print("1 - Dividir pdf")
    print("2 - Renomear pdf")
    print("9 - Sair")
    menu = int(input("Escolher: "))

    if menu == 1:
        path_to_file = str(input("Caminho/nome do arquivo: "))
        path_to_save = str(input("Pasta para salvar: "))
        split_pdf(path_to_file, path_to_save)
    
    if menu == 2:
        path_to_file = str(input("Caminho para os arquivos: "))
        files = get_files_name(path_to_file)
        for file in tqdm(files):
            print(f"{path_to_file}/{file}")
            subprocess.run(["python", "pdf.py", "-s", "ANY", "-i", f"{path_to_file}/{file}", "-o", "output.pdf"])

    if menu == 3:
        break
