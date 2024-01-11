import os
import PyPDF2
import docx

def read_book(book_path):
    text_content = ""
    
    if book_path.endswith(".pdf"):
        with open(book_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text_content += page.extract_text()
    elif book_path.endswith(".docx"):
        doc = docx.Document(book_path)
        for paragraph in doc.paragraphs:
            text_content += paragraph.text
    else:
        print("Unsupported file format.")

    return text_content

# Example usage:
book_path = "C:/Users/mrhack1/Desktop/test2.pdf"  # Replace with the actual path to your PDF or DOCX file
book_text = read_book(book_path)

print(book_text)

