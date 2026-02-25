import subprocess
import os

def compile_latex(cv_file_path: str = "../cv.xtx") -> str:
    \"\"\"
    Compiles the LaTeX file into a PDF using XeLaTeX.
    Requires XeLaTeX to be installed on the system.
    \"\"\"
    
    original_dir = os.getcwd()
    target_dir = os.path.dirname(cv_file_path)
    file_name = os.path.basename(cv_file_path)
    
    try:
        # Change directory to where the file is so LaTeX finds the .cls and fonts
        os.chdir(target_dir)
        
        # Run xelatex
        result = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', file_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        os.chdir(original_dir)
        return f"Successfully compiled {file_name} to PDF."
        
    except subprocess.CalledProcessError as e:
        os.chdir(original_dir)
        error_msg = f"LaTeX Compilation Failed.\\nSTDOUT:\\n{e.stdout}\\nSTDERR:\\n{e.stderr}"
        print(error_msg)
        raise Exception("Failed to compile LaTeX PDF.")
    except FileNotFoundError:
        os.chdir(original_dir)
        raise Exception("xelatex command not found. Please install TeX Live or MiKTeX.")
