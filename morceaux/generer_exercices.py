"""Génère des .mid d'apprentissage pour Piano Trainer.
Progression : 5 doigts main droite -> 5 doigts main gauche -> 2 mains -> 2 octaves.

Chaque fichier est écrit en format 1 (multi-pistes) pour que la détection
main gauche/droite du trainer marche automatiquement.
"""
import mido
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
TPQ = 480              # ticks par noire
BPM = 90               # tempo lent pour apprendre
VEL = 80               # vélocité par défaut

# Position 5 doigts main droite Do central : pouce=C4(60) ... auriculaire=G4(67)
C4, D4, E4, F4, G4, A4, B4, C5 = 60, 62, 64, 65, 67, 69, 71, 72
# Position 5 doigts main gauche : auriculaire=C3(48) ... pouce=G3(55)
C3, D3, E3, F3, G3 = 48, 50, 52, 53, 55
# Octave aiguë (C5)
C5, D5, E5, F5, G5, A5, B5, C6 = 72, 74, 76, 77, 79, 81, 83, 84


def ecrire_midi(nom, pistes_droite, pistes_gauche=None):
    """pistes_droite/pistes_gauche : liste de (midi, durée_en_noires). None = silence."""
    mid = mido.MidiFile(type=1, ticks_per_beat=TPQ)
    tempo_track = mido.MidiTrack()
    tempo_track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(BPM), time=0))
    tempo_track.append(mido.MetaMessage("track_name", name="Tempo", time=0))
    mid.tracks.append(tempo_track)

    for pos, notes in [("Main droite", pistes_droite), ("Main gauche", pistes_gauche)]:
        if not notes:
            continue
        tr = mido.MidiTrack()
        tr.append(mido.MetaMessage("track_name", name=pos, time=0))
        for evenement in notes:
            if evenement is None:                                       # silence
                if tr[-1].type == "note_off":
                    tr[-1].time += TPQ                                  # ajoute une noire de silence après la précédente
                continue
            midi, duree = evenement
            duree_tk = int(TPQ * duree)
            tr.append(mido.Message("note_on", note=midi, velocity=VEL, time=0))
            tr.append(mido.Message("note_off", note=midi, velocity=0, time=duree_tk))
        mid.tracks.append(tr)

    chemin = DOSSIER / nom
    mid.save(chemin)
    print(f"{nom:64} {chemin.stat().st_size} octets")


# ===========================================================================
#  NIVEAU 1 — Position 5 doigts main droite, Do central (C4-G4)
# ===========================================================================

# Frère Jacques (uses only C D E F G, PARFAIT pour position 5 doigts)
frere_jacques = [
    (C4,1),(D4,1),(E4,1),(C4,1),  (C4,1),(D4,1),(E4,1),(C4,1),
    (E4,1),(F4,2),                (E4,1),(F4,2),
    (G4,0.5),(A4,0.5),(G4,0.5),(F4,0.5),(E4,1),(C4,1),
    (G4,0.5),(A4,0.5),(G4,0.5),(F4,0.5),(E4,1),(C4,1),
    (C4,1),(E4,1),(C4,2),         (C4,1),(E4,1),(C4,2),
]
ecrire_midi("10-position-5doigts_frere_jacques.mid", frere_jacques)

# Ode à la joie (Beethoven) en Do majeur — position 5 doigts C4-G4
ode_joie = [
    (E4,1),(E4,1),(F4,1),(G4,1),  (G4,1),(F4,1),(E4,1),(D4,1),
    (C4,1),(C4,1),(D4,1),(E4,1),  (E4,1.5),(D4,0.5),(D4,2),
    (E4,1),(E4,1),(F4,1),(G4,1),  (G4,1),(F4,1),(E4,1),(D4,1),
    (C4,1),(C4,1),(D4,1),(E4,1),  (D4,1.5),(C4,0.5),(C4,2),
]
ecrire_midi("11-position-5doigts_ode_a_la_joie.mid", ode_joie)

# Au clair de la lune — position 5 doigts C4-G4
clair_lune = [
    (C4,1),(C4,1),(C4,1),(D4,1),  (E4,2),(D4,2),
    (C4,1),(E4,1),(D4,1),(D4,1),  (C4,4),
    (C4,1),(C4,1),(C4,1),(D4,1),  (E4,2),(D4,2),
    (C4,1),(E4,1),(D4,1),(D4,1),  (C4,4),
]
ecrire_midi("12-position-5doigts_au_clair_de_la_lune.mid", clair_lune)

# ===========================================================================
#  NIVEAU 2 — Position octave complète Do majeur (C4-C5), 8 notes
# ===========================================================================

# Twinkle Twinkle Little Star (utilise le A4, donc 6 notes -> saut de pouce sous ou étirement)
twinkle = [
    (C4,1),(C4,1),(G4,1),(G4,1),  (A4,1),(A4,1),(G4,2),
    (F4,1),(F4,1),(E4,1),(E4,1),  (D4,1),(D4,1),(C4,2),
    (G4,1),(G4,1),(F4,1),(F4,1),  (E4,1),(E4,1),(D4,2),
    (G4,1),(G4,1),(F4,1),(F4,1),  (E4,1),(E4,1),(D4,2),
    (C4,1),(C4,1),(G4,1),(G4,1),  (A4,1),(A4,1),(G4,2),
    (F4,1),(F4,1),(E4,1),(E4,1),  (D4,1),(D4,1),(C4,2),
]
ecrire_midi("13-position-octave_twinkle_twinkle.mid", twinkle)

# Jingle Bells (utilise E4-D5 environ, dans l'octave)
jingle = [
    (E4,1),(E4,1),(E4,2),         (E4,1),(E4,1),(E4,2),
    (E4,1),(G4,1),(C4,1.5),(D4,0.5),(E4,4),
    (F4,1),(F4,1),(F4,1),(F4,1),  (F4,1),(E4,1),(E4,1),(E4,0.5),(E4,0.5),
    (E4,1),(D4,1),(D4,1),(E4,1),  (D4,2),(G4,2),
]
ecrire_midi("14-position-octave_jingle_bells.mid", jingle)

# ===========================================================================
#  NIVEAU 3 — Deux mains, position 5 doigts symétrique
# ===========================================================================

# Ode à la joie avec basse simple (main gauche : do sol do sol...)
ode_droite = ode_joie
ode_gauche = [
    (C3,2),(G3,2),  (C3,2),(G3,2),  (C3,2),(G3,2),  (C3,2),(G3,2),
    (C3,2),(G3,2),  (C3,2),(G3,2),  (C3,2),(G3,2),  (C3,2),(G3,2),
]
ecrire_midi("20-deux-mains_ode_a_la_joie.mid", ode_droite, ode_gauche)

# Frère Jacques avec pulsation main gauche (do sur chaque temps)
fj_droite = frere_jacques
fj_gauche = [(C3,1)] * 32     # 32 noires de C3 tenu
ecrire_midi("21-deux-mains_frere_jacques.mid", fj_droite, fj_gauche)

# Au clair de la lune, main gauche = accord do-mi-sol brisé
clair_droite = clair_lune
clair_gauche = [
    (C3,1),(E3,1),(G3,1),(E3,1),  (C3,2),(G3,2),
    (C3,1),(E3,1),(G3,1),(E3,1),  (C3,4),
    (C3,1),(E3,1),(G3,1),(E3,1),  (C3,2),(G3,2),
    (C3,1),(E3,1),(G3,1),(E3,1),  (C3,4),
]
ecrire_midi("22-deux-mains_au_clair_de_la_lune.mid", clair_droite, clair_gauche)

# ===========================================================================
#  NIVEAU 4 — Deux octaves (couvrir un plus grand espace du clavier)
# ===========================================================================

# Gamme Do majeur montante puis descendante sur 2 octaves (exercice pur)
gamme = []
notes_montee = [C4,D4,E4,F4,G4,A4,B4,C5, D5,E5,F5,G5,A5,B5,C6]
notes_descente = list(reversed(notes_montee[:-1])) + [C4]
for n in notes_montee: gamme.append((n, 0.5))
for n in notes_descente: gamme.append((n, 0.5))
ecrire_midi("30-deux-octaves_gamme_do_majeur.mid", gamme)

# Ode à la joie répété sur 2 octaves (première fois grave, deuxième aiguë)
ode_2oct = ode_joie + [(n+12, d) for (n, d) in ode_joie]
ecrire_midi("31-deux-octaves_ode_joie_grave_puis_aigu.mid", ode_2oct)

# Petit motif à sauts d'octave (imite Prelude Bach) pour habituer aux grands déplacements
arpege = [
    (C4,0.5),(E4,0.5),(G4,0.5),(C5,0.5), (E4,0.5),(G4,0.5),(C5,0.5),(E5,0.5),
    (C4,0.5),(F4,0.5),(A4,0.5),(C5,0.5), (F4,0.5),(A4,0.5),(C5,0.5),(F5,0.5),
    (C4,0.5),(E4,0.5),(G4,0.5),(C5,0.5), (E4,0.5),(G4,0.5),(C5,0.5),(E5,0.5),
    (C4,0.5),(D4,0.5),(F4,0.5),(A4,0.5), (D4,0.5),(F4,0.5),(A4,0.5),(D5,0.5),
    (C4,4),
]
ecrire_midi("32-deux-octaves_arpeges_style_bach.mid", arpege)

print("\nTerminé. 10 fichiers d'exercices générés.")
