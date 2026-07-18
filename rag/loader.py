import fitz

from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf(file_path):
    """
    Extract text from PDF.
    """

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def split_text(text):
    """
    Split text into chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    return chunks