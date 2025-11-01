import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import BookPDF

pdf = BookPDF.objects.first()
if pdf and pdf.pdf_file:
    print(f"PDF path: {pdf.pdf_file.path}")
    print(f"File exists: {os.path.exists(pdf.pdf_file.path)}")
    
    # Try direct extraction
    try:
        import PyPDF2
        with open(pdf.pdf_file.path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            pdf.extracted_text = text
            pdf.text_extracted = True
            pdf.save()
            print(f"Success! Extracted {len(text)} characters")
    except Exception as e:
        print(f"Error: {e}")
