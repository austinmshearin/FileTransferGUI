@ECHO OFF
ECHO "Setting up Python virtual environment"
cd /d %~dp0
cd ..
for %%I in (.) do set CurrDirName=%%~nxI
set VirEnvName=%CurrDirName%_VirEnv
python -m venv %VirEnvName%
