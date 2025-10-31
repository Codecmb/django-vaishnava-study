import logging
import warnings

# Completely silence PyPDF2 warnings
logging.getLogger('PyPDF2').setLevel(logging.CRITICAL)
logging.getLogger('pypdf').setLevel(logging.CRITICAL)

# Also suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module='PyPDF2')
warnings.filterwarnings("ignore", category=UserWarning, module='pypdf')

print("✅ PyPDF2 warnings silenced!")
