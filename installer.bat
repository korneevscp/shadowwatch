@echo off
:: ╔══════════════════════════════════════════╗
:: ║  ShadowWatch — Installer tache auto      ║
:: ║  Lance ce fichier en tant qu'Admin       ║
:: ╚══════════════════════════════════════════╝

echo.
echo === ShadowWatch — Installation de la tache automatique ===
echo.

:: Cherche py.exe (lanceur Python Windows)
where py >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON=py
    goto :found
)

:: Fallback sur python
where python >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON=python
    goto :found
)

echo ERREUR : Python introuvable. Installe Python depuis python.org
pause
exit /b 1

:found
echo Python trouve : %PYTHON%

:: Supprime l'ancienne tache si elle existe
schtasks /delete /tn "ShadowWatch" /f >nul 2>&1

:: Cree la tache : tous les jours a 09:00
schtasks /create ^
  /tn "ShadowWatch" ^
  /tr "%PYTHON% C:\ShadowWatch\monitor.py" ^
  /sc DAILY ^
  /st 09:00 ^
  /ru "%USERNAME%" ^
  /rl HIGHEST ^
  /f

if %errorlevel% == 0 (
    echo.
    echo [OK] Tache installee avec succes !
    echo      Le scan se lancera chaque jour a 09h00 automatiquement.
    echo      Tu peux changer l'heure dans le Planificateur de taches Windows.
    echo.
) else (
    echo.
    echo [ERREUR] Impossible de creer la tache.
    echo          Fais un clic droit sur ce fichier et choisis "Executer en tant qu'administrateur"
    echo.
)

:: Lance un premier scan maintenant
echo Lancement du premier scan...
%PYTHON% C:\ShadowWatch\monitor.py

echo.
echo Termine ! Ferme cette fenetre.
pause
