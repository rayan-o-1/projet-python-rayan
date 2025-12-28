import docker
import base64

class AegisSandbox:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception:
            self.client = None
            print("⚠️ Docker n'est pas détecté. La sandbox sera désactivée.")

    def run_test(self, code_to_test, test_script):
        if not self.client:
            return {"exit_code": -1, "output": "Docker non disponible."}
            
        container = None
        try:
            # 1. Fusion du patch et du script de test (si présent)
            full_script = code_to_test
            if test_script:
                full_script += "\n\n" + test_script

            # 2. ENCODAGE BASE64 (La solution magique)
            # On transforme tout le code en une chaîne sûre sans guillemets conflictuels
            b64_script = base64.b64encode(full_script.encode('utf-8')).decode('utf-8')

            # 3. La commande devient une instruction de décodage
            # On dit à Docker : "Prends ce paquet codé, décode-le et exécute-le"
            cmd = f"python3 -c \"import base64; exec(base64.b64decode('{b64_script}').decode('utf-8'))\""
            
            # 4. Lancement sécurisé
            container = self.client.containers.run(
                image="python:3.10-slim",
                command=cmd,
                detach=True,
                network_disabled=True,
                mem_limit="128m",
                remove=False 
            )
            
            result = container.wait(timeout=15)
            logs = container.logs().decode('utf-8')
            
            return {"exit_code": result["StatusCode"], "output": logs}

        except Exception as e:
            return {"exit_code": 1, "output": f"Erreur Sandbox: {str(e)}"}
            
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:
                    pass