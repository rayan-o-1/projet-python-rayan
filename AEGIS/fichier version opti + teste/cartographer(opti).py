import os
import ast
import networkx as nx

class AegisCartographer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.graph = nx.DiGraph()
        self.project_files = self._get_all_python_files()

    def _get_all_python_files(self):
        """Liste tous les fichiers .py du projet."""
        python_files = []
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.relpath(os.path.join(root, file), self.root_dir)
                    python_files.append(full_path.replace(".py", "").replace(os.sep, "."))
        return python_files

    def scan_dependencies(self):
        """Analyse l'AST de chaque fichier pour trouver les imports."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    current_file = os.path.relpath(os.path.join(root, file), self.root_dir)
                    current_mod = current_file.replace(".py", "").replace(os.sep, ".")
                    
                    self.graph.add_node(current_mod)
                    self._parse_imports(os.path.join(root, file), current_mod)

    def _parse_imports(self, file_path, current_mod):
        """Utilise l'Abstract Syntax Tree pour extraire les imports locaux."""
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    # Cas 'import mon_module'
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name in self.project_files:
                                self.graph.add_edge(current_mod, alias.name)
                    # Cas 'from mon_module import ma_fonction'
                    elif isinstance(node, ast.ImportFrom):
                        if node.module in self.project_files:
                            self.graph.add_edge(current_mod, node.module)
            except SyntaxError:
                print(f"⚠️ Erreur de syntaxe dans {file_path}")

    def get_risk_scores(self):
        """
        Calcule le poids (risque) de chaque fichier.
        Plus un fichier est importé par d'autres, plus son score est élevé.
        """
        # In-degree = nombre de fichiers qui dépendent de ce module
        scores = {node: self.graph.in_degree(node) for node in self.graph.nodes()}
        return dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

# --- Utilisation ---
# carto = AegisCartographer("./ton_projet")
# carto.scan_dependencies()
# print(carto.get_risk_scores())