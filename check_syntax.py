"""
Skrypt do sprawdzania składni wszystkich plików Python w projekcie
Uzycie: python check_syntax.py
"""
import py_compile
import os

def check_python_files(directory="."):
    """Sprawdza składnię wszystkich plików .py w katalogu"""
    errors = []
    checked = 0
    
    # Wyklucz te katalogi
    exclude_dirs = {'__pycache__', '.git', 'venv', 'env', '.venv', 'node_modules'}
    
    for root, dirs, files in os.walk(directory):
        # Usuń wykluczone katalogi z listy
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                checked += 1
                try:
                    py_compile.compile(file_path, doraise=True)
                    print(f"OK  {file_path}")
                except py_compile.PyCompileError as e:
                    print(f"ERROR {file_path}: {e}")
                    errors.append((file_path, str(e)))
    
    print(f"\n{'='*60}")
    print(f"Sprawdzono: {checked} plikow")
    if errors:
        print(f"BLEDY SKLADNIOWE: {len(errors)}")
        for file_path, error in errors:
            print(f"  - {file_path}")
        return False
    else:
        print(f"WSZYSTKIE PLIKI MAJA POPRAWNA SKLADNIE!")
        return True

if __name__ == "__main__":
    print("Sprawdzanie skladni plikow Python...\n")
    success = check_python_files()
    exit(0 if success else 1)
