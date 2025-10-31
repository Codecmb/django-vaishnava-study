#!/bin/bash
echo "Quick System Test - should complete in < 2 seconds"
time python manage.py health_check
echo "---"
echo "✅ System is running fast!"
