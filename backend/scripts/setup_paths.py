import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Add the app directory to the Python path
app_dir = os.path.join(backend_dir, 'app')
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
