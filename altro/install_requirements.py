import pip
import os
import subprocess
import sys

def upgrade_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("Aggiornamento di pip completato con successo.")
    except subprocess.CalledProcessError:
        print("Errore durante l'aggiornamento di pip.")

        
upgrade_pip()
if os.path.exists("requirements.txt"):
        try:
            # Utilizza pip.main con il file requirements.txt
            pip.main(["install", "-r", "requirements.txt"])
            print("Tutte le dipendenze sono state installate.")
        except Exception as e:
            print("Errore durante l'installazione delle dipendenze.")
            print(e)
else:
    print("Il file requirements.txt non è stato trovato nella directory.")
