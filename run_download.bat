@echo off
:: Ask the user for a YouTube URL
set /p URL=Enter YouTube URL:

:: Run the Python script
python youtube_to_audio.py %URL% -f mp3 -o downloads

echo.
echo Download finished. Press ESC to close.

:: Wait for ESC key
:WAIT
choice /c E /n /m "Press E to exit"
if errorlevel 1 goto END
goto WAIT

:END