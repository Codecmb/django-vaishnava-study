#!/bin/bash

# Create Django Admin Interface HTML
echo "Creating Django admin interface..."

# Define the models
models=("Books" "Courses" "Qa uploads" "Question answers" "Quiz attempts" "Quiz modules" "Quiz questions" "Study materials")

# Generate the HTML file
{
cat << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STUDY_APP - Django Site Admin</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: "Roboto", "Lucida Grande", sans-serif; }
        body { background-color: #f8f8f8; color: #333; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background-color: #417690; color: white; padding: 15px 20px; margin-bottom: 20px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        h1 { font-size: 24px; font-weight: 300; }
        .admin-table { width: 100%; background-color: white; border-collapse: collapse; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 4px; overflow: hidden; }
        .admin-table th { background-color: #79aec8; color: white; text-align: left; padding: 12px 15px; font-weight: 400; }
        .admin-table td { padding: 12px 15px; border-bottom: 1px solid #e1e1e1; }
        .admin-table tr:last-child td { border-bottom: none; }
        .admin-table tr:hover { background-color: #f9f9f9; }
        .btn { display: inline-block; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px; font-weight: 400; cursor: pointer; transition: background-color 0.15s; }
        .btn-add { background-color: #417690; color: white; border: 1px solid #417690; }
        .btn-add:hover { background-color: #2c5a6e; }
        .btn-change { background-color: #70bf2b; color: white; border: 1px solid #70bf2b; }
        .btn-change:hover { background-color: #5a9c22; }
        .action-cell { white-space: nowrap; }
        .action-cell .btn { margin-right: 5px; }
        .breadcrumb { margin-bottom: 20px; font-size: 14px; color: #666; }
        .breadcrumb a { color: #447e9b; text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <header><h1>STUDY_APP</h1></header>
        <div class="breadcrumb"><a href="#">Home</a> › STUDY_APP</div>
        <table class="admin-table">
            <thead><tr><th>Model</th><th>Actions</th></tr></thead>
            <tbody>
EOF

for model in "${models[@]}"; do
    echo "                <tr>"
    echo "                    <td>$model</td>"
    echo '                    <td class="action-cell">'
    echo '                        <a href="#" class="btn btn-add">+ Add</a>'
    echo '                        <a href="#" class="btn btn-change">Change</a>'
    echo '                    </td>'
    echo "                </tr>"
done

cat << 'EOF'
            </tbody>
        </table>
    </div>
</body>
</html>
EOF
} > django_admin_interface.html

echo "✅ Django admin interface created: django_admin_interface.html"
echo "📁 File location: $(pwd)/django_admin_interface.html"

# Try to open in browser based on OS
if command -v xdg-open > /dev/null; then
    echo "🌐 Opening in default browser..."
    xdg-open django_admin_interface.html 2>/dev/null
elif command -v open > /dev/null; then
    echo "🌐 Opening in default browser..."
    open django_admin_interface.html 2>/dev/null
else
    echo "📋 To view the file, open 'django_admin_interface.html' in your web browser"
fi
