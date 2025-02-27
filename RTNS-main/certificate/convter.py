import json
import platform
import requests
from pptx import Presentation
import tempfile
from docx2pdf import convert

def ppt2pdf(f_path,filename, token):

    headers = {"Authorization": token}
    para = {
        "name": filename,
        "parents": ["13GzxN9pBRmFPP960zK0xfDbZbCll0w_Q"]
        }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open(f_path, "rb")
        }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
        )
    fi = r.text.split()
    st = fi[4]
    st = st[1:-2]
    return st


def convert_pptx_to_pdf(pptx_file_path):
    pdf_file_path = pptx_file_path.replace('.pptx', '.pdf')

    subprocess.call(['libreoffice', '--convert-to', 'pdf', '--outdir', pdf_file_path, pptx_file_path])

    return pdf_file_path