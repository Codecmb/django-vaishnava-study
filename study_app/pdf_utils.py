try:
    import PyPDF2
    PDF_ENGINE = "PyPDF2"
except ImportError:
    try:
        import pypdf as PyPDF2
        PDF_ENGINE = "pypdf"
    except ImportError:
        try:
            import pdfplumber
            PDF_ENGINE = "pdfplumber"
        except ImportError:
            PDF_ENGINE = None

def extract_pdf_text(book_pdf):
    """
    Extract text from uploaded PDF using available PDF library
    """
    try:
        pdf_path = book_pdf.pdf_file.path
        text_content = ""
        
        if PDF_ENGINE in ["PyPDF2", "pypdf"]:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text_content += page.extract_text() + "\n"
        
        elif PDF_ENGINE == "pdfplumber":
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text_content += page.extract_text() + "\n"
        
        else:
            print("No PDF library available")
            return False
        
        book_pdf.extracted_text = text_content
        book_pdf.text_extracted = True
        book_pdf.save()
        
        print(f"Extracted text from {book_pdf.book.title} PDF using {PDF_ENGINE}")
        return True
        
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return False
