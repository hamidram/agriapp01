import sys
from pathlib import Path

# Automatically add 'src' to Python's path for pytest execution
root_path = Path(__file__).parent
src_path = root_path / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))