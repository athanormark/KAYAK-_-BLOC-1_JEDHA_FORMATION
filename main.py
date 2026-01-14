import subprocess
import time
import os
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.theme import Theme
from rich.align import Align # <--- Ajout de l'import nécessaire

# Configuration du design
custom_theme = Theme({
    "success": "green",
    "error": "bold red",
    "info": "cyan",
    "warning": "yellow"
})
console = Console(theme=custom_theme)

# Liste ordonnée des notebooks
pipeline = [
    {
        "filename": "01_Cities_list.ipynb",
        "title": "Partie 1 - Géolocalisation",
        "description": "Récupération des coordonnées GPS",
        "wait_after": 2
    },
    {
        "filename": "02_Meteo_call.ipynb",
        "title": "Partie 2 - Météo",
        "description": "Collecte des prévisions via API",
        "wait_after": 2
    },
    {
        "filename": "03_Booking_Scraping.ipynb",
        "title": "Partie 3 - Scraping Booking",
        "description": "Extraction des hôtels (Long !)",
        "wait_after": 10
    },
    {
        "filename": "04_Upload_S3.ipynb",
        "title": "Partie 4 - Data Lake",
        "description": "Upload vers AWS S3",
        "wait_after": 5
    },
    {
        "filename": "05_SQL_RDS.ipynb",
        "title": "Partie 5 - Data Warehouse",
        "description": "Ingestion SQL dans AWS RDS",
        "wait_after": 2
    },
    {
        "filename": "06_Plotly_Viz.ipynb",
        "title": "Partie 6 - Visualisation",
        "description": "Génération du Dashboard interactif",
        "wait_after": 0
    }
]

def run_notebook(notebook_path):
    """Exécute un notebook et capture les erreurs."""
    cmd = [
        "jupyter", "nbconvert", 
        "--to", "notebook", 
        "--execute", 
        "--inplace", 
        notebook_path
    ]
    try:
        # On capture la sortie pour garder la console propre
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def wait_with_bar(seconds):
    """Affiche une barre de chargement pour la pause de sécurité."""
    if seconds <= 0: return

    with Progress(
        SpinnerColumn(),
        BarColumn(bar_width=40, style="blue", complete_style="green"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Pause de sécurité...", total=seconds)
        for _ in range(seconds):
            time.sleep(1)
            progress.advance(task)

def main():
    # En-tête
    # MODIFICATION ICI : On utilise Align.center AUTOUR du Panel.fit
    # Cela calcule automatiquement le décalage nécessaire.
    console.print(Align.center(
        Panel.fit(
            "[bold white]🚀 KAYAK PROJECT - AUTOMATED PIPELINE[/bold white]",
            style="bold blue",
            subtitle="By Data Engineering Team"
        )
    ))
    console.print("")

    start_global = time.time()

    for i, step in enumerate(pipeline):
        filename = step["filename"]
        title = step["title"]
        desc = step["description"]
        wait = step["wait_after"]

        if not os.path.exists(filename):
            console.print(f"[error]❌ Fichier introuvable : {filename}[/error]")
            sys.exit(1)

        # Séparateur visuel
        console.rule(f"[bold yellow]Étape {i+1}/6 : {title}[/bold yellow]")
        
        # --- EXÉCUTION AVEC CHRONOMÈTRE ---
        success = False
        error_msg = ""
        
        with Progress(
            SpinnerColumn(), # Le petit tourniquet
            TextColumn("[bold white]{task.description}[/bold white]"),
            TimeElapsedColumn(), # <--- LE CHRONOMÈTRE EN TEMPS RÉEL (0:01, 0:02...)
            console=console,
            transient=True # Disparaît quand c'est fini pour laisser place au message de succès
        ) as progress:
            task = progress.add_task(desc, total=None) # total=None fait tourner le spinner indéfiniment
            
            # Lancement du notebook (bloquant, mais Rich continue d'animer le chrono dans un thread)
            start_step = time.time()
            success, error_msg = run_notebook(filename)
            duration = time.time() - start_step

        # --- RÉSULTAT ---
        if success:
            # On réaffiche le temps total fixe une fois fini
            console.print(f"   ✅ [success]Succès[/success] en {round(duration, 2)}s.")
            
            # Pause de sécurité (si demandée)
            if wait > 0:
                wait_with_bar(wait)
        else:
            console.print(Panel(f"[error]ERREUR CRITIQUE DANS {filename}[/error]\n\n{error_msg}", title="Log d'erreur", style="red"))
            console.print("[bold red]⛔ ARRÊT D'URGENCE DU PIPELINE.[/bold red]")
            sys.exit(1)

    total_time = time.time() - start_global
    console.print("")
    # MODIFICATION ICI AUSSI : On centre le panneau de fin
    console.print(Align.center(
        Panel.fit(
            f"[bold green]🎉 PIPELINE TERMINÉ AVEC SUCCÈS ![/bold green]\n⏱️ Temps total : {round(total_time/60, 2)} minutes.",
            style="green"
        )
    ))

if __name__ == "__main__":
    main()