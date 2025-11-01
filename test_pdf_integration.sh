#!/bin/bash
echo "Testing PDF Commentary Integration..."

# Test the PDF service
python manage.py shell << EOL
from study_app.pdf_commentary_service import pdf_commentary

# Test with a sample question
question = "What is the importance of chanting Hare Krishna?"
student_answer = "Chanting cleanses the heart and connects us with God"

commentary = pdf_commentary.find_relevant_commentary(question, student_answer)
print("PDF Commentary Test Result:")
print("Question:", question)
print("Student Answer:", student_answer)
print("Commentary:", commentary[:200] + "..." if len(commentary) > 200 else commentary)
print("\nPDF Integration Test Completed!")
EOL

echo "PDF integration test complete!"
