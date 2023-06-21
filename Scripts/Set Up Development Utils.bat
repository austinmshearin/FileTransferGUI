@ECHO OFF
cd /d %~dp0
cd ..
for %%I in (.) do set CurrDirName=%%~nxI
set VirEnvName=%CurrDirName%_VirEnv
Call ./%VirEnvName%/Scripts/activate.bat
python -m pip install -e .
pause
