from PyPDF2 import PdfFileWriter, PdfFileReader
from tqdm import tqdm

# https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052
# https://www.thepythoncode.com/article/extract-text-from-images-or-scanned-pdf-python


def split_pdf(path_to_file, path_to_save):
    inputpdf = PdfFileReader(open(path_to_file, "rb"))

    for i in tqdm(range(inputpdf.numPages)):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("./"+path_to_save+"/%s.pdf" % i, "wb") as outputStream:
            output.write(outputStream)