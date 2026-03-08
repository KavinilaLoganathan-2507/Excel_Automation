#!/bin/bash
echo "========================================"
echo " TechXcel - Smart Excel Analytics"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! pip show streamlit > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Generate sample data if not exists
if [ ! -d "samples" ]; then
    echo "Generating sample data..."
    python generate_samples.py
fi

echo ""
echo "Starting Streamlit application..."
echo "Open http://localhost:8501 in your browser"
echo ""
streamlit run app.py
