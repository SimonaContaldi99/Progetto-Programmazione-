import os
import subprocess
import sys

# Funzione per verificare se Git è installato
def is_git_installed():
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Nome del progetto e percorso
project_name = "progetto programmazione"
project_path = os.path.expanduser("~/Desktop/progetto programmazione")  # Percorso su macOS/Linux
# project_path = os.path.expanduser("C:\\Users\\tuo-username\\Desktop\\progetto-programmazione")  # Percorso su Windows, decommentare e modificare questo se usi Windows

# URL del repository GitHub
github_username = "Anomis1999"
github_repo_url = f"https://github.com/Anomis1999/Progetto-Programmazione-.git"

# Comandi Git
commands = [
    "git init",
    "git add .",
    'git commit -m "Initial commit"',
    f"git remote add origin {github_repo_url}",
    "git push -u origin master"
]

# Funzione per eseguire i comandi nel terminale
def run_command(command, cwd):
    result = subprocess.run(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Errore eseguendo il comando: {command}")
        print(result.stderr)
    else:
        print(result.stdout)

# Verifica se Git è installato
if not is_git_installed():
    print("Errore: Git non è installato o non è configurato nel PATH di sistema.")
    sys.exit(1)

# Naviga nella directory del progetto
if os.path.isdir(project_path):
    os.chdir(project_path)
    for command in commands:
        run_command(command, project_path)
else:
    print(f"La directory {project_path} non esiste.")

# Aggiunta file .gitignore (esempio per progetto Python)
gitignore_content = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyderworkspace

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# PyBuilder
target/

# VS Code
.vscode/
"""

gitignore_path = os.path.join(project_path, ".gitignore")
with open(gitignore_path, "w") as file:
    file.write(gitignore_content)

# Aggiungi .gitignore al repository
run_command("git add .gitignore", project_path)
run_command('git commit -m "Add .gitignore"', project_path)
run_command("git push", project_path)
