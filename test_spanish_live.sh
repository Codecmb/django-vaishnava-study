#!/bin/bash

echo "=== LIVE SPANISH TRANSLATION TEST ==="
echo ""

echo "🚀 Starting Django server in background..."
python3 manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 5

echo ""
echo "🌐 Testing English version..."
EN_RESPONSE=$(curl -s http://localhost:8000/)
echo "Page title:"
echo "$EN_RESPONSE" | grep -o '<title>.*</title>'
echo "Key content:"
echo "$EN_RESPONSE" | grep -E "(Vaishnava Study App|Home|Courses|Explore Course)" | head -5

echo ""
echo "🌐 Testing Spanish version..."
ES_RESPONSE=$(curl -s http://localhost:8000/es/)
echo "Page title:"
echo "$ES_RESPONSE" | grep -o '<title>.*</title>'
echo "Key content:"
echo "$ES_RESPONSE" | grep -E "(Aplicación de Estudio|Inicio|Cursos|Explorar Curso)" | head -5

echo ""
echo "🔍 Checking for Spanish translations..."
if echo "$ES_RESPONSE" | grep -q "Inicio" && echo "$ES_RESPONSE" | grep -q "Cursos"; then
    echo "✅ Spanish translations are working!"
    echo "   Found 'Inicio' and 'Cursos' in Spanish page"
else
    echo "⚠️  Spanish translations may not be fully working yet"
    echo "   Check if templates have proper {% trans %} tags"
fi

echo ""
echo "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo ""
echo "📝 For manual testing:"
echo "   English: http://localhost:8000/"
echo "   Spanish: http://localhost:8000/es/"
