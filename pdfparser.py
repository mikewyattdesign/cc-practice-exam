"""
PDF DATA Extractor
"""

import PyPDF2 as p2

PDFfile = open("./source.pdf","rb")
pdfread = p2.PdfFileReader(PDFfile)

x = pdfread.getPage(0)
print(x.extractText())
text = x.extractText()
print(text)
contents = x.getContents()

print(pdfread.getNumPages())