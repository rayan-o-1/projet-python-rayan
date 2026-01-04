import subprocess
import sys
from core.agent import AegisAgent

def auto_repair_system():
    target_file = "buggy_app.py"
    
    print(f"SCANNER: Analyse de '{target_file}' en cours...")

    # 1. On tente d'exécuter le fichier pour voir s'il plante
    try:
        process = subprocess.run(
            [sys.executable, target_file], 
            capture_output=True, 
            text=True
        )
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{target_file}' n'existe pas, ou est intoruvable.")
        return

    # 2. Analyse du résultat
    if process.returncode == 0:
        print("Le fichier s'est exécuté sans erreur. Aucune réparation nécessaire.")
        print(f"Sortie : {process.stdout}")
        return
    else:
        print("CRASH DÉTECTÉ ")
        
        # 3. Extraction automatique de l'erreur + récupère les logs d'erreur
        full_error_log = process.stderr.strip()
        lines = full_error_log.split('\n')
        
        # La dernière ligne contient généralement "ZeroDivisionError: division by zero"
        last_line = lines[-1]
        
        if ":" in last_line:
            error_type, error_msg = last_line.split(':', 1)
        else:
            error_type = "Erreur Inconnue"
            error_msg = last_line

        print('\033[31m' + "Type: {error_type.strip()}" + '\33[0m')
        print('\033[31m' + "Message: {error_msg.strip()}"+ '\33[0m')
        
        # On dit à l'agent : "Le script de reproduction, c'est le fichier lui-même" et on laisse le champ vide car le code contient déjà le 'if __main__' qui plante
        reproduction_script = "" 

        error_info = {
            "type": error_type.strip(),
            "message": error_msg.strip(),
            "target_file": target_file,
            "reproduction_script": reproduction_script,
            "last_fail_logs": full_error_log
        }

        # 5. Lancement d'Aegis
        print("\n ACTIVATION DU PROTOCOLE AEGIS...")
        agent = AegisAgent(project_path=".")
        success = agent.run_repair_cycle(error_info)
        
        if success:
            print("BUG CORRIGÉ AVEC SUCCÈS !")
        else:
            print('\033[31m' + "Échec de la réparation automatique."+'\33[0m')

if __name__ == "__main__":
    auto_repair_system()
