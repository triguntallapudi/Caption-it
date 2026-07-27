@echo off
echo ===================================
echo Starting AI Image Generator App
echo ===================================
echo.
echo Activating Conda Environment...
call C:\Users\raghu\anaconda3\Scripts\activate.bat image-app
echo.
echo Starting Flask application...
python app.py
pause
