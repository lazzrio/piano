@echo off
rem MuseScore -> MIDI gratuit. Colle l'URL de la partition quand demande.
rem Utilise dl-librescore (outil open source npm, telechargement direct sans compte).
title MuseScore vers MIDI
echo.
echo Prets a telecharger un MIDI depuis MuseScore.
echo Va sur la page de la partition, copie son URL, colle ici quand demande.
echo Choisis "midi" avec les fleches puis Entree.
echo.
cd /d "%~dp0"
npx dl-librescore@latest
echo.
echo Termine. Ferme cette fenetre.
pause
