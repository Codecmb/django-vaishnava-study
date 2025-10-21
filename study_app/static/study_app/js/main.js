// Main JavaScript functionality for Vaishnava Study App

document.addEventListener('DOMContentLoaded', function() {
    initializeDropdowns();
    initializeLanguageSwitcher();
    initializeSmoothScrolling();
    initializeFileUploads();
});

// Dropdown functionality
function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.nav-link');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (trigger && menu) {
            // Desktop hover
            dropdown.addEventListener('mouseenter', function() {
                menu.style.display = 'block';
            });
            
            dropdown.addEventListener('mouseleave', function() {
                menu.style.display = 'none';
            });
            
            // Mobile click
            trigger.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const isVisible = menu.style.display === 'block';
                    menu.style.display = isVisible ? 'none' : 'block';
                }
            });
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });
}

// Language switcher enhancements
function initializeLanguageSwitcher() {
    const languageForms = document.querySelectorAll('form[action*="setlang"]');
    
    languageForms.forEach(form => {
        const select = form.querySelector('select[name="language"]');
        if (select) {
            select.addEventListener('change', function() {
                // Add loading state
                this.disabled = true;
                const originalText = this.options[this.selectedIndex].text;
                this.options[this.selectedIndex].text = 'Changing...';
                
                setTimeout(() => {
                    form.submit();
                }, 500);
            });
        }
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// File upload enhancements
function initializeFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            if (fileName) {
                // You can add file preview or validation here
                console.log('File selected:', fileName);
                
                // Add visual feedback
                const parent = this.closest('.file-upload-container') || this.parentElement;
                const feedback = document.createElement('div');
                feedback.className = 'file-feedback text-green';
                feedback.textContent = `Selected: ${fileName}`;
                feedback.style.marginTop = '5px';
                feedback.style.fontSize = '0.9em';
                
                // Remove existing feedback
                const existingFeedback = parent.querySelector('.file-feedback');
                if (existingFeedback) {
                    existingFeedback.remove();
                }
                
                parent.appendChild(feedback);
            }
        });
    });
}

// Utility function to show messages
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        z-index: 10000;
        max-width: 300px;
        animation: slideIn 0.3s ease;
    `;
    
    if (type === 'success') {
        messageDiv.style.background = 'var(--accent-green)';
    } else if (type === 'error') {
        messageDiv.style.background = 'var(--warm-red)';
    } else {
        messageDiv.style.background = 'var(--primary-blue)';
    }
    
    document.body.appendChild(messageDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        messageDiv.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (messageDiv.parentElement) {
                messageDiv.parentElement.removeChild(messageDiv);
            }
        }, 300);
    }, 5000);
}

// Add CSS animations for messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .file-upload-container {
        position: relative;
    }
    
    .file-feedback {
        font-size: 0.9em;
        margin-top: 5px;
    }
`;
document.head.appendChild(style);

// Export functions for global use
window.VaishnavaApp = {
    showMessage,
    initializeDropdowns,
    initializeLanguageSwitcher
};
