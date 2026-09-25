@echo off
echo =====================================================================
echo  POLARIS: NCPOR Polar Science Outreach & Knowledge Repository Portal
echo  Ministry of Earth Sciences (MoES) - SIH Problem Statement 26063
echo =====================================================================
echo.
echo Initializing database and starting server...
python sample_data.py
echo.
echo Starting web portal at http://127.0.0.1:5000 ...
start http://127.0.0.1:5000
python app.py
pause
