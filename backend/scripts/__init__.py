import os
import sys

def setup_paths():
    """Add the project root and backend directory to Python path."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    backend_dir = os.path.join(project_root, 'backend')
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
