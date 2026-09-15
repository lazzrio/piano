"""Piano Trainer — serveur local (stdlib pur + yt-dlp + piano_transcription_inference).

Sert `piano-trainer.html` sur http://localhost:5173 et expose deux endpoints :

  POST /api/youtube  { "url": "https://youtube.com/..." }
       -> renvoie le fichier .mid transcrit depuis l'audio de la vidéo.

  GET  /api/etat
       -> {ready:bool, message:str} — sait si le modèle est chargé.

Lancement : `pianotrainer.bat`, ou `python serveur.py`.
"""
import http.server
import json
import os
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path

BASE = Path(__file__).resolve().parent
PORT = 5173
HTML = "piano-trainer.html"

_transcripteur = None
_lock = threading.Lock()
_etat_modele = "non chargé"


CHECKPOINT_URL = "https://zenodo.org/record/4034264/files/CRNN_note_F1%3D0.9677_pedal_F1%3D0.9186.pth?download=1"
CHECKPOINT_PATH = Path.home() / "piano_transcription_inference_data" / "note_F1=0.9677_pedal_F1=0.9186.pth"


def telecharger_checkpoint():
    """La lib bytedance utilise `wget` (absent sur Windows). On télécharge nous-mêmes."""
    global _etat_modele
    if CHECKPOINT_PATH.exists() and CHECKPOINT_PATH.stat().st_size > 100_000_000:
        return
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    import urllib.request
    _etat_modele = "téléchargement du modèle (~170 Mo, une seule fois)…"
    print(f"[serveur] {_etat_modele}")
    t0 = time.time()
    dernier_pct = -1
    def progres(bloc, taille, total):
        nonlocal dernier_pct
        if total <= 0: return
        pct = min(100, bloc * taille * 100 // total)
        if pct != dernier_pct and pct % 5 == 0:
            print(f"[serveur]   {pct}% ({bloc*taille//(1024*1024)} / {total//(1024*1024)} Mo)")
            dernier_pct = pct
    urllib.request.urlretrieve(CHECKPOINT_URL, CHECKPOINT_PATH, reporthook=progres)
    print(f"[serveur] checkpoint téléchargé en {time.time()-t0:.1f} s")


def charger_modele():
    """Charge le modèle piano bytedance (télécharge le checkpoint la 1ère fois)."""
    global _transcripteur, _etat_modele
    with _lock:
        if _transcripteur is not None:
            return _transcripteur
        telecharger_checkpoint()
        _etat_modele = "chargement du modèle en mémoire…"
        print(f"[serveur] {_etat_modele}")
        from piano_transcription_inference import PianoTranscription
        _transcripteur = PianoTranscription(device="cpu", checkpoint_path=str(CHECKPOINT_PATH))
        _etat_modele = "prêt"
        print("[serveur] modèle prêt.")
        return _transcripteur


def telecharger_audio(url: str, dossier: Path) -> Path:
    """yt-dlp -> WAV mono 16 kHz dans `dossier`. Retourne le chemin."""
    modele_nom = str(dossier / "audio.%(ext)s")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-x", "--audio-format", "wav", "--audio-quality", "0",
        "-o", modele_nom, "--no-playlist", "--force-overwrites",
        "--print", "after_move:filepath",
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).splitlines()[-1] if r.stderr or r.stdout else "yt-dlp a échoué")
    return Path(r.stdout.strip().splitlines()[-1])


def transcrire(url: str) -> tuple[bytes, str]:
    """URL YouTube -> (contenu du fichier .mid, nom du morceau)."""
    with tempfile.TemporaryDirectory(prefix="pianotrainer_") as tmp:
        d = Path(tmp)
        print(f"[serveur] téléchargement audio : {url}")
        t0 = time.time()
        audio = telecharger_audio(url, d)
        print(f"[serveur] audio prêt ({audio.stat().st_size // 1024} Ko) en {time.time()-t0:.1f} s")

        modele = charger_modele()
        import librosa
        from piano_transcription_inference import sample_rate as SR
        print("[serveur] lecture audio + transcription…")
        t0 = time.time()
        y, _ = librosa.core.load(str(audio), sr=SR, mono=True)
        midi = d / "sortie.mid"
        modele.transcribe(y, str(midi))
        print(f"[serveur] transcription terminée en {time.time()-t0:.1f} s")
        propre = d / "propre.mid"
        avant, apres = nettoyer_midi(midi, propre)
        print(f"[serveur] nettoyage : {avant} -> {apres} notes")
        return propre.read_bytes(), audio.stem


def nettoyer_midi(entree: Path, sortie: Path,
                  duree_min: float = 0.06, velocite_min: int = 15,
                  fusion_delta: float = 0.03) -> tuple[int, int]:
    """Supprime les notes trop courtes / trop faibles et fusionne les doublons proches.
    Filtre typique des transcriptions bytedance qui sur-détectent des notes fantômes."""
    import mido
    mid = mido.MidiFile(entree)
    if not mid.tracks:
        sortie.write_bytes(entree.read_bytes()); return 0, 0

    # Extraire les notes en temps absolu (secondes)
    events = []
    for tr in mid.tracks:
        t = 0
        for msg in tr:
            t += msg.time
            events.append((t, msg))
    events.sort(key=lambda x: x[0])

    tempo = 500000
    for _, m in events:
        if m.type == "set_tempo": tempo = m.tempo; break
    tick = mid.ticks_per_beat
    def sec(tk): return mido.tick2second(tk, tick, tempo)

    en_attente = {}
    notes = []
    for tk, m in events:
        if m.type == "note_on" and m.velocity > 0:
            en_attente[m.note] = (tk, m.velocity)
        elif m.type in ("note_off",) or (m.type == "note_on" and m.velocity == 0):
            if m.note in en_attente:
                tk0, v = en_attente.pop(m.note)
                notes.append({"midi": m.note, "tk_on": tk0, "tk_off": tk, "vel": v})

    avant = len(notes)
    # Filtres de qualité
    filtrees = [n for n in notes if sec(n["tk_off"] - n["tk_on"]) >= duree_min and n["vel"] >= velocite_min]

    # Fusion doublons : mêmes notes qui se recouvrent presque totalement
    filtrees.sort(key=lambda n: (n["midi"], n["tk_on"]))
    fusion = []
    for n in filtrees:
        if fusion and fusion[-1]["midi"] == n["midi"] and sec(n["tk_on"] - fusion[-1]["tk_off"]) < fusion_delta:
            fusion[-1]["tk_off"] = max(fusion[-1]["tk_off"], n["tk_off"])
            fusion[-1]["vel"] = max(fusion[-1]["vel"], n["vel"])
        else:
            fusion.append(dict(n))
    fusion.sort(key=lambda n: n["tk_on"])

    # Réécriture propre
    out = mido.MidiFile(ticks_per_beat=tick)
    tr = mido.MidiTrack(); out.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=tempo, time=0))
    evs = []
    for n in fusion:
        evs.append((n["tk_on"], mido.Message("note_on",  note=n["midi"], velocity=n["vel"])))
        evs.append((n["tk_off"], mido.Message("note_off", note=n["midi"], velocity=0)))
    evs.sort(key=lambda x: x[0])
    prev = 0
    for tk, msg in evs:
        msg.time = tk - prev; prev = tk
        tr.append(msg)
    out.save(sortie)
    return avant, len(fusion)


class Gestionnaire(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[HTTP] {self.address_string()} - {fmt % args}")

    def do_GET(self):
        if self.path == "/api/etat":
            self._json({"pret": _transcripteur is not None, "message": _etat_modele})
            return
        if self.path == "/" or self.path == "":
            self.send_response(302)
            self.send_header("Location", "/" + HTML)
            self.end_headers()
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/youtube":
            self.send_error(404, "endpoint inconnu")
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n).decode("utf-8"))
            url = payload.get("url", "").strip()
            if not url:
                return self._json({"erreur": "URL vide"}, 400)
            mid, nom = transcrire(url)
        except Exception as e:
            print(f"[serveur] ERREUR : {e}")
            return self._json({"erreur": str(e)}, 500)
        self.send_response(200)
        self.send_header("Content-Type", "audio/midi")
        self.send_header("Content-Disposition", f'attachment; filename="{nom}.mid"')
        self.send_header("X-Nom-Morceau", nom.encode("ascii", "replace").decode("ascii"))
        self.send_header("Content-Length", str(len(mid)))
        self.send_header("Access-Control-Expose-Headers", "X-Nom-Morceau")
        self.end_headers()
        self.wfile.write(mid)

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class ServeurThread(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    os.chdir(BASE)
    url_app = f"http://localhost:{PORT}/{HTML}"
    print("=" * 66)
    print(f"  Piano Trainer — serveur local sur {url_app}")
    print(f"  Le navigateur va s'ouvrir. Laisse cette fenêtre ouverte.")
    print(f"  Ctrl+C pour arrêter.")
    print("=" * 66)
    # Précharge le modèle en arrière-plan (le premier appel sera instantané).
    threading.Thread(target=charger_modele, daemon=True).start()
    threading.Timer(0.8, lambda: webbrowser.open(url_app)).start()
    try:
        with ServeurThread(("", PORT), Gestionnaire) as srv:
            srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[serveur] arrêté.")


if __name__ == "__main__":
    main()
