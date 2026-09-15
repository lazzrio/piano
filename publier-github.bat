@echo off
rem Pousse Piano Trainer sur ton repo GitHub. Necessite d'avoir cree le repo sur github.com d'abord.
title Publier Piano Trainer sur GitHub
cd /d "%~dp0"
echo.
echo === Publier Piano Trainer sur GitHub ===
echo.
echo Avant de continuer :
echo   1. Va sur https://github.com/new
echo   2. Nom du repo : piano-trainer  (ou autre, note le)
echo   3. Public. Ne coche NI README, NI gitignore, NI license.
echo   4. Clique "Create repository".
echo   5. Copie l'URL que GitHub affiche (ex: https://github.com/toncompte/piano-trainer.git)
echo.
set /p URL=Colle l'URL du repo ici puis Entree :
if "%URL%"=="" (echo URL vide, abandon. & pause & exit /b)
git remote remove origin 2>nul
git remote add origin %URL%
git branch -M main
git push -u origin main
echo.
echo === Push termine ===
echo.
echo Etape finale (une seule fois) : activer GitHub Pages
echo   1. Sur github.com dans ton repo, onglet "Settings"
echo   2. Menu de gauche : "Pages"
echo   3. Source : "Deploy from a branch", Branch : "main", dossier : "/ (root)", Save
echo   4. Attends 1-2 minutes, GitHub affiche l'URL publique en haut.
echo   5. L'app sera a : https://TONCOMPTE.github.io/NOMDUREPO/piano-trainer.html
echo.
pause
