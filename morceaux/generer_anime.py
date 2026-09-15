"""Génère des .mid de mélodies d'anime pour Piano Trainer.
Deux versions par morceau :
  - 5 doigts : main droite seule, position fixe (généralement C4-G4)
  - 10 doigts : deux mains avec accompagnement basique
Toutes les mélodies sont transposées si nécessaire pour rester en position 5 doigts.
"""
import mido
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
TPQ = 480
BPM = 80             # tempo lent pour apprendre confortablement

# Position main droite 5 doigts Do central
C4, D4, E4, F4, G4, A4, B4, C5 = 60, 62, 64, 65, 67, 69, 71, 72
# Main gauche
C3, D3, E3, F3, G3, A3, B3 = 48, 50, 52, 53, 55, 57, 59


def ecrire(nom, droite, gauche=None, bpm=BPM):
    """droite/gauche : liste de (midi, duree_en_noires). midi=None pour un silence."""
    mid = mido.MidiFile(type=1, ticks_per_beat=TPQ)
    tempo_tr = mido.MidiTrack()
    tempo_tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    mid.tracks.append(tempo_tr)

    for label, notes in [("Main droite", droite), ("Main gauche", gauche)]:
        if not notes:
            continue
        tr = mido.MidiTrack()
        tr.append(mido.MetaMessage("track_name", name=label, time=0))
        silence_accumule = 0
        for ev in notes:
            m, d = ev
            dur = int(TPQ * d)
            if m is None:
                silence_accumule += dur
                continue
            tr.append(mido.Message("note_on", note=m, velocity=80, time=silence_accumule))
            tr.append(mido.Message("note_off", note=m, velocity=0, time=dur))
            silence_accumule = 0
        mid.tracks.append(tr)
    mid.save(DOSSIER / nom)


# ============================================================================
#  TOTORO — Sanpo (thème d'ouverture, « Aru-ko aru-ko »)
# ============================================================================

totoro_droite_5d = [
    (G4,1),(G4,1),(E4,1),(C4,1),  (D4,1),(E4,1),(D4,1),(C4,2),
    (G4,1),(G4,1),(E4,1),(C4,1),  (D4,1),(C4,1),(D4,1),(E4,2),
    (E4,1),(F4,1),(G4,1),(E4,1),  (D4,1),(E4,1),(D4,1),(C4,2),
    (C4,1),(D4,1),(E4,1),(F4,1),  (G4,2),(C4,2),
]
ecrire("40-anime_5doigts_totoro_sanpo.mid", totoro_droite_5d, bpm=100)

totoro_gauche_10d = [
    (C3,2),(G3,2),  (F3,2),(G3,2),  (C3,2),(G3,2),  (C3,2),(G3,2),
    (C3,2),(G3,2),  (F3,2),(G3,2),  (C3,2),(G3,2),  (C3,4),
]
ecrire("50-anime_10doigts_totoro_sanpo.mid", totoro_droite_5d, totoro_gauche_10d, bpm=100)

# ============================================================================
#  LE CHÂTEAU AMBULANT — Merry-Go-Round of Life (Hisaishi)
#  Original Fa mineur en 3/4. Version simplifiée en Do majeur.
# ============================================================================

# Motif waltz en 3/4 (3 temps par mesure)
merry_droite_5d = [
    (E4,1),(G4,1),(F4,1),  (E4,1),(D4,1),(C4,1),  (D4,1),(E4,1),(F4,1),  (G4,3),
    (E4,1),(G4,1),(F4,1),  (E4,1),(D4,1),(C4,1),  (D4,1),(C4,1),(D4,1),  (E4,3),
    (C4,1),(D4,1),(E4,1),  (F4,1),(G4,1),(F4,1),  (E4,1),(D4,1),(C4,1),  (D4,3),
    (E4,1),(G4,1),(F4,1),  (E4,1),(D4,1),(C4,1),  (D4,1),(E4,1),(F4,1),  (G4,3),
]
ecrire("41-anime_5doigts_merry_go_round.mid", merry_droite_5d, bpm=90)

# Version 10 doigts : main gauche fait une basse waltz "bass-chord-chord"
merry_gauche_10d = [
    (C3,1),(G3,1),(G3,1),  (F3,1),(G3,1),(G3,1),  (C3,1),(G3,1),(G3,1),  (C3,1),(G3,1),(G3,1),
    (C3,1),(G3,1),(G3,1),  (F3,1),(G3,1),(G3,1),  (C3,1),(G3,1),(G3,1),  (C3,3),
    (C3,1),(G3,1),(G3,1),  (F3,1),(G3,1),(G3,1),  (C3,1),(G3,1),(G3,1),  (C3,3),
    (C3,1),(G3,1),(G3,1),  (F3,1),(G3,1),(G3,1),  (C3,1),(G3,1),(G3,1),  (C3,3),
]
ecrire("51-anime_10doigts_merry_go_round.mid", merry_droite_5d, merry_gauche_10d, bpm=90)

# ============================================================================
#  NARUTO — Sadness and Sorrow (thème triste de l'anime original)
#  Simplifié en position 5 doigts C4-G4.
# ============================================================================

naruto_droite_5d = [
    (E4,1.5),(F4,0.5),(E4,1),(D4,1),  (C4,2),(D4,1),(E4,1),
    (F4,2),(E4,1),(D4,1),             (E4,4),
    (E4,1.5),(F4,0.5),(E4,1),(D4,1),  (C4,2),(D4,1),(C4,1),
    (D4,2),(E4,1),(C4,1),             (C4,4),
]
ecrire("42-anime_5doigts_naruto_sadness.mid", naruto_droite_5d, bpm=70)

naruto_gauche_10d = [
    (C3,4),  (F3,4),
    (C3,4),  (G3,4),
    (C3,4),  (F3,4),
    (G3,4),  (C3,4),
]
ecrire("52-anime_10doigts_naruto_sadness.mid", naruto_droite_5d, naruto_gauche_10d, bpm=70)

# ============================================================================
#  TOKYO GHOUL — Unravel (riff d'introduction, simplifié)
# ============================================================================

unravel_droite_5d = [
    (E4,0.5),(F4,0.5),(G4,1),(F4,0.5),(E4,0.5),  (D4,1),(E4,1),
    (E4,0.5),(F4,0.5),(G4,1),(F4,0.5),(E4,0.5),  (D4,2),
    (C4,0.5),(D4,0.5),(E4,1),(D4,0.5),(C4,0.5),  (D4,1),(E4,1),
    (G4,0.5),(F4,0.5),(E4,1),(D4,0.5),(C4,0.5),  (C4,2),
]
ecrire("43-anime_5doigts_tokyo_ghoul_unravel.mid", unravel_droite_5d, bpm=85)

unravel_gauche_10d = [
    (C3,2),(G3,2),  (A3,2),(F3,2),
    (C3,2),(G3,2),  (F3,4),
    (C3,2),(G3,2),  (A3,2),(F3,2),
    (C3,2),(G3,2),  (C3,4),
]
ecrire("53-anime_10doigts_tokyo_ghoul_unravel.mid", unravel_droite_5d, unravel_gauche_10d, bpm=85)

print("8 morceaux d'anime générés (4 titres x 2 versions).")
