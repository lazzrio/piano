# Piano Trainer

Petit outil pour apprendre le piano au clavier MIDI, dans le navigateur. Aucun compte, aucune installation côté client.

Ouvre `piano-trainer.html` dans **Brave** ou **Chrome** (double-clic). Ou utilise la version en ligne (voir plus bas).

## Ce que ça fait
- Piano-roll qui défile sur 88 touches. Les notes descendent, tu les joues quand elles atteignent le clavier.
- **Mode une main** : ✋ G / ✋ D / 🖐 2 mains. Quand tu apprends, ne bosse qu'une main à la fois — le PC joue l'autre pour l'accompagnement.
- **Vrai son de piano acoustique** via SoundFont, avec reverb.
- **Vitesse ajustable** 0,25× → 1,5× (0,50× conseillé au début).
- **Score en temps réel** si ton clavier MIDI est branché en USB : notes justes en vert, ratées en rouge, pourcentage et latence moyenne.
- **YouTube → MIDI** (nécessite le serveur Python local, voir plus bas) : donne une URL, récupère un `.mid` transcrit automatiquement.
- **Effets visuels** : particules à l'impact, halo, ligne de frappe dorée — sans se prendre au sérieux.

Guide de méthode : [APPRENDRE.md](APPRENDRE.md).

## Utilisation basique (aucune installation)

1. Double-clic sur `piano-trainer.html` → s'ouvre dans Brave/Chrome.
2. Bouton 📁 .mid → choisis un fichier dans `morceaux/` (6 morceaux fournis, du plus facile au plus dur).
3. Vitesse à 0,50×. Bouton ✋ D pour ne travailler que la main droite.
4. ▶ Lire. Regarde l'écran, pas tes mains.

## Avec un clavier MIDI

Branche-le en USB. Bouton **🎹 Clavier**, autorise l'accès MIDI dans Brave.
- Tes notes justes passent en vert, ratées en rouge.
- Le PC joue automatiquement les notes de l'autre main (quand tu es en mode ✋ G ou ✋ D).

## YouTube → MIDI (option avancée)

Nécessite Python et quelques dépendances. Double-clic sur `pianotrainer.bat` : ça installe ce qu'il faut au premier lancement, lance un petit serveur local et ouvre le navigateur avec un champ URL YouTube en plus. Colle l'URL d'une piano cover, clique **Transcrire**, attends 1-2 min, le `.mid` se charge automatiquement.

Qualité : très bonne sur les piano covers solo (Rousseau, Marioverehrer). Moyenne sur les enregistrements complexes.

## Compatibilité

- **Brave / Chrome / Edge** desktop et Android : ✅ tout marche (Web MIDI + Web Audio + Canvas).
- **Firefox** : ❌ Web MIDI absent, seul le mode « le PC joue pour toi » fonctionne.
- **Safari / iOS / iPad** : Web MIDI absent, sinon OK.
- **Alesis Recital 88** : reconnu comme périphérique MIDI class-compliant, aucun pilote à installer.

## Fichiers

- `piano-trainer.html` — l'app entière, un seul fichier autonome.
- `morceaux/` — 6 `.mid` gratuits (bitmidi.com), rangés du plus facile au plus dur.
- `pianotrainer.bat` — lance le serveur local (pour YouTube → MIDI).
- `serveur.py` — serveur Python, transcription bytedance.
- `yt2mid/` — alternative en deux clics : télécharge l'audio puis ouvre Basic Pitch web.
- `APPRENDRE.md` — méthode pour apprendre le piano avec cet outil.

## Statut

Projet perso, en développement actif. Deviendra à terme la console de pilotage d'un robot pianiste à solénoïdes sur Alesis Recital 88 (voir mon [autre repo](../robot-pianiste)).
