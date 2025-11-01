#!/bin/bash
echo "🔄 RESTARTING DJANGO SERVER"
echo "==========================="

cd ~/django-vaishnava-study
source venv/bin/activate

# Kill any running Django servers
echo "Stopping any running servers..."
pkill -f "python manage.py runserver"
sleep 2

# Check if port 8000 is still in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "Port 8000 still in use, forcing kill..."
    sudo kill -9 $(lsof -t -i:8000)
    sleep 2
fi

# Start fresh server
echo "Starting Django server..."
python manage.py runserver --skip-checks &

echo "✅ Server started on http://127.0.0.1:8000/"
echo "💡 Now check the admin interface at: http://127.0.0.1:8000/admin/"
