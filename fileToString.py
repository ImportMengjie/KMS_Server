import docx
import io
import subprocess
import datetime
import random
import os
import PyPDF2


def handle_doc(Bytes: bytes):
    temp_file_name = str(datetime.datetime.now()) + str(random.randint(10, 1000))
    with open(temp_file_name, 'wb') as f:
        f.write(Bytes)
    output = subprocess.check_output(['antiword', temp_file_name])
    os.remove(temp_file_name)
    return output.encode('utf-8')


def handle_docx(Bytes: bytes):
    doc = docx.Document(io.BytesIO(Bytes))
    res = ''
    for para in doc.paragraphs:
        res += para.text
    return res


def handle_pdf(Bytes):
    pdf = PyPDF2.PdfFileReader(io.BytesIO(Bytes))
    res = b''
    for page in pdf.pages:
        res += bytes(page.extractText(),'utf-8')
    return res.decode('utf-8')


def handle_html(Bytes):
    return 'html'


with open('1.pdf', 'rb') as f:
    print(handle_pdf(f.read()))
