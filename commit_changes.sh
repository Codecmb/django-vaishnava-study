#!/bin/bash
echo "🚀 Starting commit process..."

echo "1. Checking git status..."
git status

echo ""
echo "2. Adding files to staging..."
git add .

echo ""
echo "3. Creating commit..."
git commit -m "feat: Complete Bhakti Shastri quiz system

- Added all Bhakti Shastri quiz modules (22 total)
- Implemented AI auto-population of correct answers  
- Made prabhupada_commentary optional
- Added 'Take Test' buttons for all modules
- Created student-driven answer evaluation
- Built certificate system foundation
- Fixed admin interface for easy question management"

echo ""
echo "4. Verifying commit..."
git log --oneline -2

echo ""
echo "✅ Commit completed successfully!"
echo "📱 Now open GitHub Desktop to see your changes"
