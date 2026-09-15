"""Vague 2 d'anime : Bunny Girl Senpai, Steins;Gate, Fairy Tail, Code Geass.
Deux versions par titre (5 doigts main droite / 10 doigts avec main gauche).
Toutes transposées en Do majeur position C4-G4 pour rester en position 5 doigts.
"""
import mido
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
TPQ = 480
BPM_DEFAUT = 80

C4, D4, E4, F4, G4, A4 = 60, 62, 64, 65, 67, 69
C3, D3, E3, F3, G3, A3, B3 = 48, 50, 52, 53, 55, 57, 59


def ecrire(nom, droite, gauche=None, bpm=BPM_DEFAUT):
    mid = mido.MidiFile(type=1, ticks_per_beat=TPQ)
    tempo_tr = mido.MidiTrack()
    tempo_tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    mid.tracks.append(tempo_tr)
    for label, notes in [("Main droite", droite), ("Main gauche", gauche)]:
        if not notes:
            continue
        tr = mido.MidiTrack()
        tr.append(mido.MetaMessage("track_name", name=label, time=0))
        silence = 0
        for m, d in notes:
            dur = int(TPQ * d)
            if m is None:
                silence += dur
                continue
            tr.append(mido.Message("note_on", note=m, velocity=80, time=silence))
            tr.append(mido.Message("note_off", note=m, velocity=0, time=dur))
            silence = 0
        mid.tracks.append(tr)
    mid.save(DOSSIER / nom)


# ============================================================================
#  BUNNY GIRL SENPAI — Fukashigi no Carte (ED, piano mélancolique)
# ============================================================================
# Original en Fa# mineur. Motif du refrain simplifié en Do majeur position C-G.

bg_droite = [
    (E4,1),(E4,1),(D4,1),(C4,1),  (D4,2),(E4,2),
    (E4,1),(D4,1),(C4,1),(D4,1),  (E4,2),(G4,2),
    (F4,1),(E4,1),(D4,1),(C4,1),  (D4,2),(E4,2),
    (D4,1),(C4,1),(D4,1),(E4,1),  (C4,4),
]
ecrire("44-anime_5doigts_bunny_girl_fukashigi.mid", bg_droite, bpm=70)

# Main gauche : accords tenus (do-mi-sol arpégés lents)
bg_gauche = [
    (C3,2),(E3,2),  (F3,2),(G3,2),
    (C3,2),(E3,2),  (C3,2),(G3,2),
    (F3,2),(A3,2),  (C3,2),(G3,2),
    (F3,2),(G3,2),  (C3,4),
]
ecrire("54-anime_10doigts_bunny_girl_fukashigi.mid", bg_droite, bg_gauche, bpm=70)

# ============================================================================
#  STEINS;GATE — Hacking to the Gate (OP)
# ============================================================================
# Motif synthé principal en La mineur original, transposé en Do position 5 doigts.

sg_droite = [
    (E4,0.5),(F4,0.5),(G4,1),(E4,1),  (G4,0.5),(F4,0.5),(E4,1),(D4,1),
    (C4,0.5),(D4,0.5),(E4,1),(F4,1),  (G4,0.5),(F4,0.5),(E4,1),(C4,1),
    (E4,0.5),(F4,0.5),(G4,1),(E4,1),  (G4,0.5),(F4,0.5),(E4,1),(D4,1),
    (C4,0.5),(D4,0.5),(E4,1),(D4,1),  (C4,4),
]
ecrire("45-anime_5doigts_steins_gate_hacking.mid", sg_droite, bpm=105)

# Main gauche : basse rythmique électro (pulse sur les temps)
sg_gauche = [
    (C3,1),(C3,1),(G3,1),(G3,1),  (F3,1),(F3,1),(G3,1),(G3,1),
    (C3,1),(C3,1),(G3,1),(G3,1),  (F3,1),(F3,1),(C3,1),(C3,1),
    (C3,1),(C3,1),(G3,1),(G3,1),  (F3,1),(F3,1),(G3,1),(G3,1),
    (C3,1),(C3,1),(G3,1),(G3,1),  (C3,4),
]
ecrire("55-anime_10doigts_steins_gate_hacking.mid", sg_droite, sg_gauche, bpm=105)

# ============================================================================
#  FAIRY TAIL — Main Theme (thème principal de Yasuharu Takanashi)
# ============================================================================
# Original en La mineur, épique. Transposé en Do position 5 doigts.

ft_droite = [
    (C4,1),(D4,1),(E4,2),         (F4,1),(G4,1),(F4,2),
    (E4,1),(D4,1),(C4,1),(D4,1),  (E4,2),(D4,2),
    (C4,1),(D4,1),(E4,2),         (F4,1),(G4,1),(A4,2),
    (G4,1),(F4,1),(E4,1),(D4,1),  (C4,4),
    (E4,1),(F4,1),(G4,2),         (F4,1),(E4,1),(D4,2),
    (E4,1),(F4,1),(G4,1),(F4,1),  (E4,2),(D4,2),
    (C4,1),(D4,1),(E4,1),(F4,1),  (G4,2),(E4,2),
    (F4,1),(E4,1),(D4,1),(C4,1),  (C4,4),
]
ecrire("46-anime_5doigts_fairy_tail_main.mid", ft_droite, bpm=95)

# Main gauche : basse épique (fondamentale + quinte, très marquée)
ft_gauche = [
    (C3,4),  (F3,4),
    (C3,2),(G3,2),  (C3,4),
    (C3,4),  (F3,4),
    (G3,2),(C3,2),  (C3,4),
    (C3,4),  (F3,4),
    (C3,2),(G3,2),  (C3,4),
    (C3,4),  (F3,4),
    (G3,4),  (C3,4),
]
ecrire("56-anime_10doigts_fairy_tail_main.mid", ft_droite, ft_gauche, bpm=95)

# ============================================================================
#  CODE GEASS — Continued Story (ED, très pianistique)
# ============================================================================
# Mélodie du refrain, simplifiée en Do majeur position 5 doigts.

cg_droite = [
    (E4,1),(D4,1),(C4,1),(D4,1),  (E4,2),(D4,2),
    (C4,1),(D4,1),(E4,1),(D4,1),  (C4,2),(E4,2),
    (F4,1),(E4,1),(D4,1),(E4,1),  (F4,2),(G4,2),
    (F4,1),(E4,1),(D4,1),(C4,1),  (D4,2),(C4,2),
]
ecrire("47-anime_5doigts_code_geass_continued.mid", cg_droite, bpm=75)

# Main gauche : arpège doux do-mi-sol-mi qui roule
cg_gauche = [
    (C3,1),(E3,1),(G3,1),(E3,1),  (C3,1),(E3,1),(G3,1),(E3,1),
    (F3,1),(A3,1),(C4-12,1),(A3,1),  (C3,1),(E3,1),(G3,1),(E3,1),
    (F3,1),(A3,1),(C4-12,1),(A3,1),  (G3,1),(B3,1),(D3+12,1),(B3,1),
    (F3,1),(A3,1),(C4-12,1),(A3,1),  (C3,1),(E3,1),(G3,1),(C3,1),
]
ecrire("57-anime_10doigts_code_geass_continued.mid", cg_droite, cg_gauche, bpm=75)

print("8 morceaux d'anime (vague 2) générés.")
