#!/bin/bash
echo "🚀 STARTING DJANGO SERVER RELIABLY"
echo "================================="

cd ~/django-vaishnava-study

# Kill any existing processes on port 8000
echo "🔫 Stopping any existing servers..."
sudo lsof -t -i:8000 | xargs kill -9 2>/dev/null || true
pkill -f "python manage.py runserver" 2>/dev/null || true
pkill -f "runserver" 2>/dev/null || true

# Wait a moment for processes to die
sleep 2

# Check if port is still in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "❌ Port 8000 still in use. Trying alternative port..."
    # Use port 8001 instead
    source venv/bin/activate
    python manage.py runserver 127.0.0.1:8001
else
    echo "✅ Port 8000 is free. Starting server..."
    source venv/bin/activate
    python manage.py runserver
fi
