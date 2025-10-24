#!/bin/bash

echo "=== TESTING SPANISH BOOK PAGES ==="
echo ""

echo "🚀 Starting server to test Spanish book pages..."
python3 manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo "🌐 Testing Spanish course pages for Bhakti Shastri books..."
echo ""

# Test if we can access Spanish course pages
if curl -s http://localhost:8000/es/courses/ | grep -q "Estudie este Libro"; then
    echo "✅ 'Estudie este Libro' found on Spanish courses page"
else
    echo "❌ 'Estudie este Libro' not found - may need to check template"
fi

echo ""
echo "📝 Manual testing steps:"
echo "   1. Visit: http://localhost:8000/es/"
echo "   2. Click on 'Cursos Disponibles'"
echo "   3. Click on 'Bhakti Shastri' course"
echo "   4. Check that each book shows 'Estudie este Libro'"
echo "   5. Verify the translation looks correct"

echo ""
echo "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null

echo ""
echo "🔧 If the translation doesn't show up:"
echo "   - The text might be hardcoded in templates instead of using {% trans %}"
echo "   - We may need to add translation tags to the templates"
