from werkzeug.datastructures import FileStorage
from io import BytesIO
import fitz


def pdf_to_text(file: FileStorage) -> str:
    buffer = BytesIO(file.stream.read())
    with fitz.open(stream=buffer, filetype="pdf") as pdf:
        return "\n".join((page.get_text() for page in pdf.pages()))
