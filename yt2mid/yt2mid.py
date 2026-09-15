"""YouTube -> fichier MIDI, en deux clics.

Utilisation :
  python yt2mid.py <URL YouTube>
  ou : double-clic sur yt2mid.bat et coller l'URL quand demandé.

Ce que ça fait :
  1. Télécharge l'audio de la vidéo YouTube en MP3 (yt-dlp + ffmpeg déjà installés).
  2. Ouvre https://basicpitch.spotify.com/ dans le navigateur ET copie le chemin du MP3
     dans le presse-papier.
  3. Toi, sur la page ouverte : glisse-dépose le fichier (ou clique "Choose file"
     et colle le chemin), attends 30 s, télécharge le .mid.
  4. Charge ce .mid dans Piano Trainer.

Pourquoi pas 100 % automatique : le modèle Basic Pitch de Spotify fait tourner un
réseau de neurones qui ne s'installe pas proprement sur Windows/Python 3.12 (TensorFlow).
La version en ligne (gratuite, sans compte) fait exactement le même travail, en une glissade.
"""
import argparse
import subprocess
import sys
import webbrowser
from pathlib import Path

BASIC_PITCH_URL = "https://basicpitch.spotify.com/"
SORTIE = Path(__file__).resolve().parent / "audio"
SORTIE.mkdir(exist_ok=True)


def telecharger(url: str) -> Path:
    print(f"[1/3] Téléchargement de l'audio de {url} ...")
    modele = str(SORTIE / "%(title).100s.%(ext)s")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-x", "--audio-format", "mp3", "--audio-quality", "0",
        "-o", modele, "--no-playlist", "--force-overwrites",
        "--print", "after_move:filepath",
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        raise SystemExit("Échec du téléchargement (vidéo indisponible, restreinte, ou pas de connexion).")
    chemin = Path(r.stdout.strip().splitlines()[-1])
    print(f"      -> {chemin.name}  ({chemin.stat().st_size // 1024} Ko)")
    return chemin


def copier_dans_presse_papiers(texte: str) -> bool:
    """PowerShell Set-Clipboard, natif Windows, aucune installation."""
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", "Set-Clipboard", "-Value", texte],
                       check=True, capture_output=True)
        return True
    except Exception:
        return False


def ouvrir_basic_pitch(chemin_audio: Path):
    print(f"[2/3] Ouverture de Basic Pitch dans ton navigateur : {BASIC_PITCH_URL}")
    webbrowser.open(BASIC_PITCH_URL)
    ok = copier_dans_presse_papiers(str(chemin_audio))
    print(f"[3/3] Chemin du fichier {'copié dans le presse-papiers ✓' if ok else '(copie presse-papiers non disponible)'}")
    print()
    print("=" * 74)
    print("  À TOI DE JOUER (sur la page Basic Pitch qui vient de s'ouvrir) :")
    print("  1. Glisse-dépose le fichier MP3 depuis l'Explorateur")
    print(f"     ou clique « Choose file » puis colle le chemin :")
    print(f"     {chemin_audio}")
    print("  2. Attends ~30 s (le modèle analyse l'audio).")
    print("  3. Clique « Download MIDI » -> le fichier .mid arrive dans Téléchargements.")
    print("  4. Charge-le dans Piano Trainer (bouton 📁 Ouvrir .mid).")
    print("=" * 74)


def main():
    ap = argparse.ArgumentParser(description="YouTube -> MIDI via yt-dlp + Basic Pitch")
    ap.add_argument("url", nargs="?", help="URL YouTube (si omis, sera demandé)")
    args = ap.parse_args()
    url = args.url or input("URL YouTube : ").strip()
    if not url:
        raise SystemExit("Pas d'URL fournie.")
    audio = telecharger(url)
    ouvrir_basic_pitch(audio)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAnnulé.")
