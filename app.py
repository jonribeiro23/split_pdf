from PyPDF2 import PdfFileWriter, PdfFileReader
from tqdm import tqdm

# https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052
# https://www.thepythoncode.com/article/extract-text-from-images-or-scanned-pdf-python

inputpdf = PdfFileReader(open("bb0121_edital.pdf", "rb"))

for i in tqdm(range(inputpdf.numPages)):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)
