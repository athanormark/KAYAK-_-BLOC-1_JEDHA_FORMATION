import os
import subprocess
import sys
import time

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.theme import Theme

# Configuration du thème Rich
custom_theme = Theme({
    "success": "green",
    "error": "bold red",
    "info": "cyan",
    "warning": "yellow"
})
console = Console(theme=custom_theme)

# Liste ordonnée des notebooks du pipeline
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
        "description": "Extraction des hôtels (long)",
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
        "description": "Génération des cartes interactives",
        "wait_after": 0
    }
]


def run_notebook(notebook_path):
    """Exécute un notebook Jupyter via nbconvert et retourne (succès, erreur)."""
    cmd = [
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        notebook_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def wait_with_bar(seconds):
    """Affiche une barre de progression pendant la pause de sécurité."""
    if seconds <= 0:
        return

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
    """Point d'entrée : exécute les 6 notebooks séquentiellement."""
    # En-tête
    console.print(Align.center(
        Panel.fit(
            "[bold white]KAYAK - Pipeline automatisé[/bold white]",
            style="bold blue",
            subtitle="Projet JEDHA - Bloc 1"
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
            console.print(f"[error]Fichier introuvable : {filename}[/error]")
            sys.exit(1)

        # Séparateur visuel
        console.rule(f"[bold yellow]Etape {i + 1}/6 : {title}[/bold yellow]")

        # Exécution avec chronomètre
        success = False
        error_msg = ""

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold white]{task.description}[/bold white]"),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            progress.add_task(desc, total=None)

            start_step = time.time()
            success, error_msg = run_notebook(filename)
            duration = time.time() - start_step

        # Résultat
        if success:
            console.print(
                f"   [success]Succès[/success] en {round(duration, 2)}s."
            )
            if wait > 0:
                wait_with_bar(wait)
        else:
            console.print(Panel(
                f"[error]ERREUR DANS {filename}[/error]\n\n{error_msg}",
                title="Log d'erreur",
                style="red"
            ))
            console.print("[bold red]Arrêt du pipeline.[/bold red]")
            sys.exit(1)

    total_time = time.time() - start_global
    console.print("")
    console.print(Align.center(
        Panel.fit(
            f"[bold green]Pipeline terminé[/bold green]\n"
            f"Temps total : {round(total_time / 60, 2)} minutes.",
            style="green"
        )
    ))


if __name__ == "__main__":
    main()
