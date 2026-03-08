# ⚡ TechXcel - Smart Excel Analytics

> **Transform your spreadsheets into decision simulators. Ask "What If?" questions and see alternate business timelines.**

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-purple)

## 🚀 Features

### 📊 Smart Data Analysis
- Automatic relationship detection between variables
- Correlation analysis and regression modeling
- Pattern recognition (trends, anomalies, seasonality)

### 🔮 What-If Simulator
- Ask natural language questions: *"What if marketing spend doubled?"*
- Get AI-powered predictions with confidence levels
- See impact analysis for all related variables

### 📈 Timeline Explorer
- Interactive timeline visualization
- Slide through different scenarios
- Compare actual vs. simulated outcomes

### 🎯 Optimization Engine
- AI recommendations for optimal values
- ROI predictions
- Strategy suggestions

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Engine | OpenAI GPT-4 |
| Data Processing | Pandas, NumPy, Scikit-learn |
| Visualization | Plotly |

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd excel-automation
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key

```bash
# Copy example config
copy .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Running the Application

### Option 1: Streamlit App (Recommended for Demo)

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

### Option 2: FastAPI Backend

```bash
python backend.py
# or
uvicorn backend:app --reload
```

API available at `http://localhost:8000`

## 📊 Sample Data

Generate sample Excel files for testing:

```bash
python generate_samples.py
```

This creates:
- `samples/sales_data.xlsx` - Marketing & Sales data
- `samples/inventory_data.xlsx` - Inventory management data
- `samples/hr_data.xlsx` - HR workforce data

## 🎮 Demo Usage

1. **Upload Data**: Click "Upload Excel File" or use "Load Sample Data"
2. **View Analysis**: See AI-detected relationships and patterns
3. **Ask Questions**: Try "What if marketing spend was 3000 instead of 2000?"
4. **Explore Timeline**: Slide through scenarios to see predictions
5. **Get Recommendations**: Ask for optimization suggestions

### Example Questions

- *"What if we increased marketing spend by 50%?"*
- *"What would sales be if we hired 5 more employees?"*
- *"How would revenue change if customer satisfaction improved by 0.5?"*

## 📁 Project Structure

```
excel-automation/
├── app.py                 # Streamlit frontend
├── backend.py             # FastAPI backend
├── ai_engine.py           # OpenAI integration
├── data_processor.py      # Data analysis & simulation
├── visualization.py       # Plotly charts
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── generate_samples.py    # Sample data generator
├── samples/               # Sample Excel files
│   ├── sales_data.xlsx
│   ├── inventory_data.xlsx
│   └── hr_data.xlsx
└── README.md
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload Excel file |
| `/analyze` | GET | Get AI analysis |
| `/whatif` | POST | Process what-if question |
| `/simulate` | POST | Run value simulation |
| `/optimize` | POST | Get optimization suggestions |
| `/data` | GET | Get current data |
| `/relationships` | GET | Get detected relationships |

## 🧠 How It Works

### 1. Data Understanding
```
AI analyzes spreadsheet structure
↓
Identifies numeric, categorical, date columns
↓
Calculates statistics (mean, std, etc.)
```

### 2. Relationship Detection
```
Correlation Matrix → Find related variables
↓
Linear Regression → Build predictive models
↓
Formula: Sales = 2.5 × Marketing + 1000
```

### 3. Counterfactual Simulation
```
User changes: Marketing 1200 → 2000
↓
AI applies model coefficients
↓
Predicts: Sales increases by 18%
```

## 🏆 Hackathon Value

✅ **Unique Concept** - Few tools do counterfactual spreadsheet analysis  
✅ **High Impact** - Useful for finance, marketing, operations  
✅ **Great Demo** - Visual, interactive, impressive  
✅ **Real AI** - Uses GPT-4 for intelligent responses  

## 📝 License

MIT License - Feel free to use for your hackathon!

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

Built with ❤️ for hackathon success!
