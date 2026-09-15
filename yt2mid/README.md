# YouTube → MIDI en deux clics

Tu donnes une URL YouTube, tu récupères un fichier `.mid` prêt à charger dans le Piano Trainer.

## Utilisation

Double-clic sur `yt2mid.bat`. Une console s'ouvre, elle te demande l'URL YouTube (par ex. une « piano cover » d'un morceau que tu aimes). Colle l'URL (clic droit dans la console), Entrée.

Le script fait alors :
1. Télécharge l'audio de la vidéo en `.mp3` dans le sous-dossier `audio/`.
2. Ouvre <https://basicpitch.spotify.com/> dans ton navigateur.
3. Copie le chemin du `.mp3` dans le presse-papiers.

Sur la page Basic Pitch qui vient de s'ouvrir :
1. Glisse-dépose le fichier MP3 depuis l'Explorateur (ou clic « Choose file » + `Ctrl+V`).
2. Attends 20-40 s (le modèle Spotify analyse l'audio).
3. Clique **Download MIDI** — le `.mid` arrive dans ton dossier Téléchargements.
4. Retourne dans Piano Trainer, bouton **📁 Ouvrir .mid**, tu joues.

## Pourquoi ce n'est pas 100 % automatique
Basic Pitch est un modèle de deep learning open-source (TensorFlow) qui ne s'installe pas proprement sur Windows + Python 3.12. La version en ligne fait exactement le même calcul, en 30 secondes, gratuitement, sans compte.

Si un jour tu veux la version 100 % locale (utile pour traiter 20 vidéos d'affilée), il faudra installer un Python 3.11 dédié.

## Qualité
La transcription automatique marche **très bien sur les piano covers solo** (Rousseau, Patrik Pietschmann, Marioverehrer). Elle est moins bonne sur les enregistrements avec voix, batterie, orchestre. Pour ton apprentissage, cible des vidéos « nom du morceau + piano cover ».

## Suggestions de vidéos
- « Merry Go Round of Life piano cover » (Ghibli)
- « River Flows in You Yiruma piano »
- « Nuvole Bianche Ludovico Einaudi piano »
- « Comptine d'un autre été Yann Tiersen piano »
- « Ballade No 1 Chopin piano »
