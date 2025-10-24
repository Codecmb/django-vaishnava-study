#!/bin/bash

# Vaishnava Study Platform - Button Modification Script
# This script removes the blue button and moves the red button to navbar

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_debug() { echo -e "${BLUE}[DEBUG]${NC} $1"; }

# Backup original file
backup_file() {
    local file="$1"
    local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
    
    if [[ -f "$file" ]]; then
        cp "$file" "$backup"
        log_info "Backup created: $backup"
        return 0
    else
        log_error "File not found: $file"
        return 1
    fi
}

# Create modified HTML with separate navbar CSS
create_modified_html() {
    local output_file="$1"
    
    cat > "$output_file" << 'HTML_EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aplicación de Estudio Vaishnava</title>
    
    <!-- Main CSS Styles -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #f8f9fa;
            color: #333;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Header Styles */
        .header {
            background: linear-gradient(135deg, #8e44ad, #3498db);
            color: white;
            padding: 4rem 0;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        .header p {
            font-size: 1.2rem;
            max-width: 700px;
            margin: 0 auto;
        }

        /* Course Section */
        .courses {
            padding: 4rem 0;
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: #2c3e50;
            font-size: 2rem;
        }

        .course-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 2rem;
            max-width: 800px;
            margin: 0 auto;
        }

        .course-card h3 {
            color: #8e44ad;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }

        .course-card p {
            margin-bottom: 1.5rem;
            color: #555;
        }

        /* Footer */
        .footer {
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: 2rem;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .course-card {
                padding: 1.5rem;
            }
        }
    </style>
    
    <!-- Separate Navbar CSS -->
    <style>
        /* Navbar Styles */
        .navbar {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 3px solid #e74c3c;
        }

        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #e74c3c;
            padding: 1rem 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .nav-links a {
            color: #ecf0f1;
            text-decoration: none;
            font-weight: 500;
            padding: 1rem 0.5rem;
            transition: all 0.3s ease;
            position: relative;
            border-radius: 4px;
        }

        .nav-links a:hover {
            color: #e74c3c;
            background-color: rgba(255,255,255,0.1);
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 2px;
            background: #e74c3c;
            transition: all 0.3s ease;
            transform: translateX(-50%);
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        .explore-btn {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            border: none;
            padding: 0.7rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
            margin-left: 1rem;
        }

        .explore-btn:hover {
            background: linear-gradient(135deg, #c0392b, #a93226);
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(231, 76, 60, 0.4);
        }

        .explore-btn:active {
            transform: translateY(0);
        }

        /* Mobile Navbar Styles */
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                padding: 1rem 20px;
            }

            .nav-links {
                flex-direction: column;
                gap: 1rem;
                width: 100%;
                margin-top: 1rem;
            }

            .nav-links a {
                padding: 0.8rem;
                width: 100%;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.1);
            }

            .explore-btn {
                margin-left: 0;
                margin-top: 0.5rem;
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">Vaishnava Study</div>
            <div class="nav-links">
                <a href="#">Inicio</a>
                <a href="#">Cursos</a>
                <a href="#">Recursos</a>
                <a href="#">Contacto</a>
                <!-- Red button moved to navbar -->
                <button class="explore-btn">Explorar Curso</button>
            </div>
        </div>
    </nav>

    <!-- Header -->
    <header class="header">
        <div class="container">
            <h1>Aplicación de Estudio Vaishnava</h1>
            <p>Comprehensive study platform for ISICON's Bhakti Shastri and advanced courses with multilingual support</p>
        </div>
    </header>

    <!-- Courses Section -->
    <section class="courses">
        <div class="container">
            <h2 class="section-title">Cursos Disponibles</h2>
            
            <div class="course-card">
                <h3>Bhakti Shastri</h3>
                <p>Estudio completo de los textos fundamentales del Gaudiya Vaishnavismo incluyendo el Bhagavad-gita y las escrituras esenciales.</p>
                <!-- Blue button has been removed -->
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2023 Aplicación de Estudio Vaishnava. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>
HTML_EOF
}

# Main function
main() {
    local output_file="${1:-vaishnava_study_modified.html}"
    
    log_info "Starting Vaishnava Study Platform modification..."
    log_info "This script will:"
    log_info "1. Remove the blue button from course card"
    log_info "2. Move the red button to the navbar"
    log_info "3. Create separate CSS for navbar styling"
    
    # If modifying existing file, create backup
    if [[ -f "$output_file" ]]; then
        log_warn "Output file $output_file already exists"
        backup_file "$output_file"
    fi
    
    # Create the modified HTML file
    log_info "Creating modified HTML file: $output_file"
    create_modified_html "$output_file"
    
    # Verify the file was created
    if [[ -f "$output_file" ]]; then
        log_info "✅ Successfully created modified HTML file: $output_file"
        log_info "✅ Blue button removed from course card"
        log_info "✅ Red button moved to navbar"
        log_info "✅ Separate navbar CSS implemented"
        
        # Show file info
        local file_size=$(du -h "$output_file" | cut -f1)
        local line_count=$(wc -l < "$output_file")
        log_info "File details: Size: $file_size, Lines: $line_count"
    else
        log_error "Failed to create output file: $output_file"
        return 1
    fi
}

# Function to serve the file locally for testing
serve_file() {
    local file="$1"
    local port="${2:-8000}"
    
    if command -v python3 &> /dev/null; then
        log_info "Starting local server on http://localhost:$port"
        cd "$(dirname "$file")"
        python3 -m http.server "$port"
    elif command -v python &> /dev/null; then
        log_info "Starting local server on http://localhost:$port"
        cd "$(dirname "$file")"
        python -m SimpleHTTPServer "$port"
    else
        log_warn "Python not found. Cannot start local server."
        log_info "Open the file directly in your browser: file://$(pwd)/$file"
    fi
}

# Show usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "OPTIONS:"
    echo "  -o, --output FILE    Output file name (default: vaishnava_study_modified.html)"
    echo "  -s, --serve [PORT]   Serve the file locally after creation (default port: 8000)"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -o my_app.html          # Create modified HTML file"
    echo "  $0 --serve                 # Create and serve the file"
    echo "  $0 -o app.html --serve 8080 # Create and serve on port 8080"
}

# Parse command line arguments
parse_args() {
    local output_file="vaishnava_study_modified.html"
    local serve=false
    local port=8000
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            -s|--serve)
                serve=true
                if [[ $2 =~ ^[0-9]+$ ]]; then
                    port="$2"
                    shift 2
                else
                    shift
                fi
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    main "$output_file"
    
    if [[ "$serve" == true ]]; then
        serve_file "$output_file" "$port"
    fi
}

# Run the script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    parse_args "$@"
fi
