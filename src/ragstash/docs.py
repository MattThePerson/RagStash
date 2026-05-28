from pathlib import Path
from pypdf import PdfReader

def getFilesByExtension(path, ext) -> list[Path]:
    return sorted(Path(path).rglob(f'*.{ext}'))

def getFileContent_pdf(fn: str|Path) -> str:
    reader = PdfReader(str(fn))
    return '\n'.join([ p.extract_text() for p in reader.pages ])

def getFileContent_txt(fn: str|Path) -> str:
    with open(str(fn), 'r') as f:
        return f.read()

def readFiles(path: str):
    texts, filenames = [], []

    # txt
    for _file in getFilesByExtension(path, "txt"):
        content = getFileContent_txt(_file)
        texts.append(content)
        filenames.append(str(_file))

    # md
    for _file in getFilesByExtension(path, "md"):
        content = getFileContent_txt(_file)
        texts.append(content)
        filenames.append(str(_file))

    # pdf
    for _file in getFilesByExtension(path, "pdf"):
        content = getFileContent_pdf(_file)
        texts.append(content)
        filenames.append(str(_file))

    return texts, filenames
