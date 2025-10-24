#!/bin/bash

echo "📈 SPANISH TRANSLATION PROGRESS TRACKER"
echo "========================================"
echo ""

# Get current status
STATUS=$(msgfmt --statistics "./locale/es/LC_MESSAGES/django.po" 2>&1)
echo "Current: $STATUS"
echo ""

# Parse the numbers
if [[ $STATUS =~ ([0-9]+).*translated.*([0-9]+).*untranslated ]]; then
    TRANSLATED=${BASH_REMATCH[1]}
    UNTRANSLATED=${BASH_REMATCH[2]}
    TOTAL=$((TRANSLATED + UNTRANSLATED))
    PERCENTAGE=$((TRANSLATED * 100 / TOTAL))
    
    echo "📊 Progress: $TRANSLATED/$TOTAL ($PERCENTAGE%)"
    echo ""
    
    # Progress bar
    BAR_LENGTH=50
    FILLED=$((PERCENTAGE * BAR_LENGTH / 100))
    EMPTY=$((BAR_LENGTH - FILLED))
    
    printf "["
    printf "%${FILLED}s" | tr ' ' '█'
    printf "%${EMPTY}s" | tr ' ' '░'
    printf "] $PERCENTAGE%%\n"
    echo ""
    
    # Milestones
    if [ $PERCENTAGE -lt 25 ]; then
        echo "🎯 Next milestone: 25% (translate 15 more strings)"
    elif [ $PERCENTAGE -lt 50 ]; then
        echo "🎯 Next milestone: 50% (translate 18 more strings)" 
    elif [ $PERCENTAGE -lt 75 ]; then
        echo "🎯 Next milestone: 75% (translate 19 more strings)"
    elif [ $PERCENTAGE -lt 90 ]; then
        echo "🎯 Next milestone: 90% (translate 12 more strings)"
    else
        echo "🎯 Almost there! Final stretch to 100%"
    fi
    
else
    echo "Could not parse translation status"
fi

echo ""
echo "🚀 Quick completion plan:"
echo "   • Translate 10 strings per session"
echo "   • 7 sessions to complete all 74 strings"
echo "   • Test after each batch with: python3 manage.py runserver"
echo ""
echo "💪 You can do this! The hard part (setup) is already done."
