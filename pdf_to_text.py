import sys
from pathlib import Path
from PyPDF2 import PdfReader

def pdf_to_text(pdf_path, output_path=None):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"File {pdf_path} does not exist.")
        return

    reader = PdfReader(str(pdf_path))
    all_text = ""

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            all_text += text + "\n"
        else:
            print(f"⚠️ No text extracted from page {i+1}")
        print(f"Extracted page {i+1}/{len(reader.pages)}")

    if not output_path:
        output_path = pdf_path.with_suffix('.txt')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(all_text)

    print(f"Saved extracted text to {output_path}")
    print(f"Total extracted text length: {len(all_text)} characters")
    if len(all_text.strip()) == 0:
        print("The PDF file is corrupted or unreadable.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_text.py kanun.pdf")
    else:
        pdf_to_text(sys.argv[1])

