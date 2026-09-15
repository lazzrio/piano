@echo off
rem Piano Trainer — lance le serveur local et ouvre le navigateur.
title Piano Trainer
echo Verification des dependances (silencieux si tout est deja la)...
python -m pip install --quiet yt-dlp audioread librosa piano_transcription_inference
python "%~dp0serveur.py"
pause
