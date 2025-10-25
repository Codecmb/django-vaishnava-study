#!/bin/bash
echo "🎯 QUIZ SYSTEM MANAGEMENT"
echo "========================"

cd ~/django-vaishnava-study

case "$1" in
    "status")
        ./scripts/utilities/system_status_report.sh
        ;;
    "start")
        source venv/bin/activate
        python manage.py runserver
        ;;
    "test")
        ./scripts/tests/test_quiz_system.py
        ;;
    "fix-admin")
        ./scripts/fixes/fix_admin_display.sh
        ;;
    "clean-duplicates")
        ./scripts/fixes/clean_existing_duplicates.sh
        ;;
    "organize")
        ./scripts/utilities/organize_all_files.sh
        ;;
    "help"|"")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  status       - Show system status report"
        echo "  start        - Start Django development server"
        echo "  test         - Run system tests"
        echo "  fix-admin    - Fix admin interface issues"
        echo "  clean-duplicates - Remove duplicate questions"
        echo "  organize     - Organize project files"
        echo "  help         - Show this help message"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use '$0 help' for available commands"
        ;;
esac
