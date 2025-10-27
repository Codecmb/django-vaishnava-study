# Read the book detail template
with open('study_app/templates/study_app/book_detail.html', 'r') as f:
    content = f.read()

# Check if bulk upload button already exists
if 'bulk_questions' in content:
    print("✅ Bulk upload button already exists in book detail")
else:
    # Add the button after the book title - using proper quotes
    new_content = content.replace(
        '</h1>', 
        '</h1>\\n    <div class="mt-4">\\n        <a href="{% url \\'study_app:bulk_questions\\' book.id %}" class="btn btn-success btn-lg">📥 BULK UPLOAD QUESTIONS</a>\\n    </div>'
    )
    
    # Write back
    with open('study_app/templates/study_app/book_detail.html', 'w') as f:
        f.write(new_content)
    print("✅ Added green bulk upload button to book detail page")
