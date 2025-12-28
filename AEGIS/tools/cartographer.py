import os
import ast
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class AegisCartographer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.graph = nx.DiGraph()
        self.project_files = {} # Dict pour stocker {nom_module: chemin_fichier}

    def _count_lines(self, file_path):
        """Compte les lignes de code (poids du fichier)."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return sum(1 for line in f if line.strip() and not line.strip().startswith("#"))
        except:
            return 10 # Valeur par défaut si erreur

    def scan_dependencies(self):
        """Scan complet : Dépendances (Flèches) + Poids (Lignes de code)."""
        ignore_dirs = {"venv", ".git", "__pycache__", ".idea", ".vscode", "build", "dist", "node_modules"}
        
        # 1. Repérage des fichiers et calcul du poids (LOC)
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.root_dir)
                    module_name = rel_path.replace(".py", "").replace(os.sep, ".")
                    
                    self.project_files[module_name] = full_path
                    
                    # On ajoute le nœud avec son attribut de poids (lines of code)
                    loc = self._count_lines(full_path)
                    self.graph.add_node(module_name, size=loc)

        # 2. Analyse des liens (Arêtes)
        for module, path in self.project_files.items():
            self._parse_imports(path, module)

    def _parse_imports(self, file_path, current_mod):
        """Analyse les imports pour créer les flèches."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    target = None
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            target = alias.name
                            if target in self.project_files:
                                self.graph.add_edge(current_mod, target)
                    elif isinstance(node, ast.ImportFrom):
                        target = node.module
                        if node.level > 0: # Imports relatifs
                            parts = current_mod.split('.')
                            if len(parts) >= node.level:
                                base = ".".join(parts[:-(node.level)])
                                target = f"{base}.{target}" if target else base
                        if target and target in self.project_files:
                            self.graph.add_edge(current_mod, target)
        except Exception:
            pass

    def get_risk_scores(self):
        """Retourne le score de risque pour l'IA."""
        if len(self.graph.nodes) == 0: return {}
        # Risque = (Nombre de dépendances entrantes * 2) + (Complexité/Taille / 100)
        scores = {}
        in_degrees = dict(self.graph.in_degree())
        for node in self.graph.nodes:
            loc = self.graph.nodes[node].get('size', 10)
            degree = in_degrees.get(node, 0)
            # Formule de risque pondérée
            scores[node] = (degree * 10) + int(loc / 20)
            
        return dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

    def visualize_graph(self, output_file="aegis_map.png"):
        """Génère la cartographie pondérée (Weighted Tree System)."""
        try:
            plt.figure(figsize=(14, 10)) # Grande image
            ax = plt.gca()
            
            # --- LAYOUT (Disposition) ---
            # 'shell_layout' ou 'kamada_kawai' rend mieux les hiérarchies que spring
            try:
                pos = nx.kamada_kawai_layout(self.graph)
            except:
                pos = nx.spring_layout(self.graph, k=2, iterations=100, seed=42)

            # --- DONNÉES VISUELLES ---
            # 1. TAILLE des nœuds = Nombre de lignes de code (LOC)
            # On normalise pour que ce soit visible (min 300, max 3000)
            raw_sizes = [self.graph.nodes[n].get('size', 10) for n in self.graph.nodes()]
            node_sizes = [min(max(s * 10, 300), 4000) for s in raw_sizes]

            # 2. COULEUR des nœuds = Centralité (Combien de fichiers dépendent de moi ?)
            # Plus c'est foncé/rouge, plus c'est un fichier "Pilier".
            in_degrees = dict(self.graph.in_degree())
            node_colors = [in_degrees.get(n, 0) for n in self.graph.nodes()]
            
            # --- DESSIN ---
            
            # Flèches (Arêtes)
            nx.draw_networkx_edges(
                self.graph, pos,
                edge_color='gray',
                alpha=0.5,
                arrows=True,
                arrowstyle='-|>', # Flèche pointue simple
                arrowsize=25,
                connectionstyle='arc3,rad=0.1' # Légère courbe pour voir les aller-retours
            )

            # Nœuds
            nodes = nx.draw_networkx_nodes(
                self.graph, pos,
                node_size=node_sizes,
                node_color=node_colors,
                cmap=plt.cm.Spectral_r, # Rouge (Chaud/Risque) <-> Bleu (Froid/Calme)
                edgecolors='black',
                linewidths=1.5,
                alpha=0.9
            )

            # Labels (Texte)
            labels = {}
            for n in self.graph.nodes():
                lines = self.graph.nodes[n].get('size', 0)
                # On affiche "nom_fichier \n 50 lignes"
                labels[n] = f"{n.split('.')[-1]}\n({lines} lines)"

            nx.draw_networkx_labels(
                self.graph, pos,
                labels=labels,
                font_size=9,
                font_weight='bold',
                font_color='black'
            )

            # --- LÉGENDE & INFO ---
            plt.title("CARTOGRAPHIE PONDÉRÉE DU SYSTÈME AEGIS", fontsize=15, fontweight='bold', pad=20)
            
            # Création manuelle de la légende pour la clarté
            legend_elements = [
                mpatches.Patch(color='#d7191c', label='Fichier Critique (Pilier Central)'),
                mpatches.Patch(color='#fdae61', label='Fichier Intermédiaire'),
                mpatches.Patch(color='#abdda4', label='Fichier Indépendant (Feuille)'),
                plt.Line2D([0], [0], color='gray', lw=2, label='Sens de la dépendance (A utilise B)'),
            ]
            plt.legend(handles=legend_elements, loc='lower right', title="Légende", frameon=True)
            
            # Note sur la taille
            plt.figtext(0.02, 0.02, "TAILLE DU CERCLE = Volume de code (Lignes)", fontsize=10, style='italic')

            plt.axis('off')
            plt.tight_layout()
            plt.savefig(output_file, dpi=150)
            plt.close()
            print(f"🗺️ Carte Pondérée générée : {output_file}")

        except Exception as e:
            print(f"⚠️ Erreur visuelle : {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("🔬 Analyse et Cartographie...")
    carto = AegisCartographer(root_dir='.') 
    carto.scan_dependencies()
    print("Scores de risque calculés :")
    print(carto.get_risk_scores())
    carto.visualize_graph()