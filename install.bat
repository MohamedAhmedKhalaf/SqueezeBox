@echo off

:: Check if Scoop is installed
where scoop >nul 2>nul
if %errorlevel% neq 0 (
    echo Scoop is not installed. Installing Scoop...
    powershell -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser; iwr -useb get.scoop.sh | iex"
) else (
    echo Scoop is already installed.
)

:: Check if ffmpeg is installed via Scoop
scoop list ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo ffmpeg is not installed. Installing ffmpeg...
    scoop install ffmpeg
) else (
    echo ffmpeg is already installed.
)

echo Process completed.
pause
