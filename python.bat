@echo off
setlocal

echo Checking if Python is installed...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python before running this script.
    echo You can download Python from https://www.python.org/
    pause
    exit /b 1
)

echo Checking if pip is installed...
where pip >nul 2>&1
if %errorlevel% neq 0 (
  echo pip is not installed. Trying to install pip...
  python -m ensurepip --upgrade
  if %errorlevel% neq 0 (
    echo Error installing pip. Make sure the Python installation includes pip.
    pause
    exit /b 1
  )
)

echo Installing required Python packages...
pip install Flask
pip install Pillow
pip install Werkzeug
pip install python-dotenv
pip install flask-wtf
pip install wtforms
pip install heapdict

echo All required Python packages have been installed.
echo Please make sure to install ffmpeg using the other scripts, or manually

pause
endlocal