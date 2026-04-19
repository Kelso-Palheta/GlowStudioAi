import os
import sys

def verify_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Base dir (simulating /app): {base_dir}")
    
    paths = [
        "src/views/home.py",
        "src/views/01_configuracao.py",
        "src/views/login.py"
    ]
    
    for p in paths:
        full_path = os.path.join(base_dir, p)
        exists = os.path.exists(full_path)
        print(f"Path: {p} -> Exists: {exists}")
        
if __name__ == "__main__":
    verify_paths()
