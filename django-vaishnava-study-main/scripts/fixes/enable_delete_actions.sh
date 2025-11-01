#!/bin/bash
echo "🗑️  ENABLING DELETE ACTIONS"
echo "==========================="

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os

admin_file = 'study_app/admin.py'

# Read current admin content
with open(admin_file, 'r') as f:
    content = f.read()

# Ensure all admin classes have delete_selected action
models_to_fix = ['QuizModule', 'QuizQuestion', 'Book', 'QAUpload']

for model_name in models_to_fix:
    pattern = rf'@admin\.register\({model_name}\)\s*class (\w+)\(.*?\):'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        admin_class_name = match.group(1)
        print(f"✅ Found {model_name}Admin: {admin_class_name}")
        
        # Check if actions include delete_selected
        actions_pattern = rf'class {admin_class_name}\(.*?actions = \[(.*?)\]'
        actions_match = re.search(actions_pattern, content, re.DOTALL)
        
        if actions_match:
            current_actions = actions_match.group(1)
            if 'delete_selected' not in current_actions:
                print(f"🔧 Adding delete_selected to {model_name}Admin")
                new_actions = current_actions.replace(']', ', 'delete_selected']')
                content = content.replace(f'actions = [{current_actions}]', f'actions = [{new_actions}]')
        else:
            print(f"🔧 Adding actions with delete_selected to {model_name}Admin")
            # Find the class and add actions
            class_pattern = rf'(class {admin_class_name}\(.*?\):\s*\n)'
            replacement = rf'\1    actions = ['delete_selected']\n'
            content = re.sub(class_pattern, replacement, content)

# Write updated content
with open(admin_file, 'w') as f:
    f.write(content)

print("🎉 Delete actions enabled for all models!")
PYEOF

echo ""
echo "🔄 Restarting Django server to apply changes..."
# Kill any running server and restart
pkill -f "python manage.py runserver"
python manage.py runserver --skip-checks &
echo "✅ Server restarted. Check the admin interface now."
