#!/bin/bash
echo "🔧 FIXING PORT 8000 ISSUE"
echo "========================"

cd ~/django-vaishnava-study

echo "🔍 Checking what's using port 8000..."
# Show what's using the port
sudo lsof -i :8000

echo ""
echo "🔫 Killing processes on port 8000..."
# Kill processes more aggressively
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null || true
pkill -f "runserver" 2>/dev/null || true
pkill -f "python.*8000" 2>/dev/null || true

# Wait for cleanup
sleep 2

echo "✅ Port 8000 should now be free"
echo "💡 Now you can run: python manage.py runserver"
