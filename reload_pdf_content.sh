#!/bin/bash
echo "Reloading PDF content for quiz commentaries..."

python manage.py shell << EOL
from study_app.pdf_commentary_service import pdf_commentary
pdf_commentary.load_pdf_content()
print("PDF content reloaded!")
print("Available books:", list(pdf_commentary.pdf_content.keys()))
EOL

echo "PDF content reload complete!"
