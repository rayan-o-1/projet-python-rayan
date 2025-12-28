import ast

class HealthScorer:
    def calculate_score(self, patch, test_results, risk_level):
        score = 100
        nb_nodes = 0 # <-- CORRECTIF : On initialise la variable ici par sécurité
        
        # 1. Sanction si les tests échouent dans Docker
        if test_results.get("exit_code") != 0:
            score -= 60  # Échec critique
            
        # 2. Analyse de complexité
        try:
            # On tente de lire le code généré par l'IA
            tree = ast.parse(patch)
            nb_nodes = len(list(ast.walk(tree)))
            
            if nb_nodes > 100: # Si le patch est trop complexe
                score -= 15
        except:
            # Si le code de l'IA n'est même pas du Python valide
            score -= 50 
            nb_nodes = 0

        # 3. Malus de risque (venant du Cartographe)
        if risk_level > 5:
            score -= 10

        return {
            "total_score": max(0, score),
            "details": f"Nodes: {nb_nodes}, Risk: {risk_level}"
        }