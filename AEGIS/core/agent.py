import json
import os
import re
from tools.cartographer import AegisCartographer
from tools.docker_jail import AegisSandbox
from core.scoring import HealthScorer
import ollama 

class AegisAgent:
    def __init__(self, project_path):
        self.project_path = project_path
        self.carto = AegisCartographer(project_path)
        self.sandbox = AegisSandbox()
        self.scorer = HealthScorer()
        self.model = "deepseek-coder:6.7b" 

    def run_repair_cycle(self, error_report, max_iterations=3):
        print(f"🚀 Début du cycle Aegis pour l'erreur : {error_report['type']}")
        
        target_file = error_report['target_file']
        
        # 1. Lecture du code original
        original_code = self._read_file(target_file)
        
        # 2. Analyse Cartographique
        try:
            self.carto.scan_dependencies()
            dependency_context = self.carto.get_risk_scores()
        except Exception:
            dependency_context = {}
        
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            print(f"🔄 Itération {iteration}/{max_iterations}...")

            # 3. Prompt
            prompt = self._build_prompt(error_report, dependency_context, original_code)
            
            try:
                response = ollama.generate(model=self.model, prompt=prompt, format="json", options={"temperature": 0.2})
                decision = self._clean_json_response(response['response'])
                
                if not decision:
                    print("⚠️ Format JSON invalide.")
                    continue

                # Récupération sécurisée des champs
                # L'IA utilise parfois 'thought' ou 'reasoning' au lieu de 'pensee'
                pensee = decision.get('pensee', decision.get('thought', decision.get('reasoning', 'Aucune')))
                
                # --- CORRECTIF MAJEUR : NETTOYAGE DU CODE ---
                patch_code = decision.get('patch', '')
                
                # On enlève les balises Markdown si l'IA les a mises DANS la chaîne JSON
                if patch_code:
                    patch_code = patch_code.replace("```python", "").replace("```", "").strip()

                print(f"💡 L'IA suggère : {pensee}")

                # Vérification basique
                if not patch_code or "def " not in patch_code:
                    print("⚠️ L'IA n'a pas renvoyé de fonction valide.")
                    continue
                
                # --- Réinjection du bloc __main__ si manquant ---
                code_to_test_in_docker = patch_code
                
                # Si l'original avait un test et que le patch n'en a pas, on le rajoute
                if "if __name__" not in patch_code and "if __name__" in original_code:
                    print("🔧 Réinjection automatique du bloc de test original...")
                    parts = original_code.split('if __name__')
                    if len(parts) > 1:
                        # On rajoute proprement le bloc main
                        code_to_test_in_docker = patch_code + "\n\nif __name__" + parts[1]

                # 4. Test dans la Sandbox
                test_results = self.sandbox.run_test(
                    code_to_test=code_to_test_in_docker,
                    test_script="" 
                )

                # 5. Score
                score_report = self.scorer.calculate_score(
                    patch=patch_code,
                    test_results=test_results,
                    risk_level=dependency_context.get(target_file, 0)
                )

                if score_report['total_score'] >= 80:
                    print(f"✅ Correction validée ! Patch appliqué sur {target_file}")
                    self._apply_patch_to_disk(target_file, patch_code)
                    return True
                else:
                    print("⚠️ Score insuffisant.")
                    clean_output = test_results['output'].strip()
                    # On tronque si c'est trop long pour l'affichage
                    short_output = (clean_output[:200] + '...') if len(clean_output) > 200 else clean_output
                    print(f"🛑 RETOUR DOCKER : {short_output if short_output else 'Aucune sortie'}")
                    error_report['last_fail_logs'] = f"Sortie Docker: {clean_output}"

            except Exception as e:
                print(f"❌ Erreur interne : {e}")
                import traceback
                traceback.print_exc()

        print("❌ Aegis n'a pas pu trouver de solution.")
        return False

    def _read_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _clean_json_response(self, raw_text):
        """Nettoie le JSON (enlève le markdown AUTOUR du json)"""
        try:
            return json.loads(raw_text)
        except:
            if "```" in raw_text:
                try:
                    # On cherche le premier { et le dernier }
                    start = raw_text.find("{")
                    end = raw_text.rfind("}") + 1
                    return json.loads(raw_text[start:end])
                except: pass
            return None

    def _build_prompt(self, error, context, code_content):
        return f"""
        Tu es un expert Python. Répare le bug dans le code ci-dessous.
        
        CODE SOURCE A RÉPARER :
        ```python
        {code_content}
        ```
        
        ERREUR DÉTECTÉE : {error['type']} - {error['message']}
        DERNIER ÉCHEC : {error.get('last_fail_logs', 'Aucun')}
        
        CONSIGNES :
        1. Renvoie le fichier COMPLET corrigé.
        2. NE METS PAS DE MARKDOWN (```python) DANS LE CHAMP "patch", JUSTE LE CODE BRUT.
        3. Réponds UNIQUEMENT au format JSON.

        FORMAT JSON ATTENDU :
        {{
            "pensee": "Explication courte",
            "target_file": "{error['target_file']}",
            "patch": "def ma_fonction()..."
        }}
        """

    def _apply_patch_to_disk(self, file_path, patch_code):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(patch_code)