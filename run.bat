@echo off
echo ========================================
echo  TechXcel - Smart Excel Analytics
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if dependencies are installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Generate sample data if not exists
if not exist "samples" (
    echo Generating sample data...
    python generate_samples.py
)

echo.
echo Starting Streamlit application...
echo Open http://localhost:8501 in your browser
echo.
streamlit run app.py
