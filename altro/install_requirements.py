import pip
import os

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
