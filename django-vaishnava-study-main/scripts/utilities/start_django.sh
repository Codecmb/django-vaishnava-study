#!/bin/bash
echo "🚀 SMART DJANGO SERVER START"
echo "============================"

cd ~/django-vaishnava-study

# Function to find a free port
find_free_port() {
    for port in {8000..8010}; do
        if ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
            echo $port
            return
        fi
    done
    echo "8000"  # Fallback
}

# Kill any existing Django servers (optional - comment out if you want to keep them)
# echo "🔄 Stopping existing Django servers..."
# pkill -f "python manage.py runserver" 2>/dev/null || true

# Find a free port
FREE_PORT=$(find_free_port)
echo "🎯 Using port: $FREE_PORT"

# Activate virtual environment and start server
source venv/bin/activate
echo "🌟 Starting Django development server..."
python manage.py runserver 127.0.0.1:$FREE_PORT
