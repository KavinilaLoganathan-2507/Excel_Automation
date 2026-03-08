"""
FastAPI Backend - API endpoints for TechXcel
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json

from data_processor import SpreadsheetProcessor, process_uploaded_file
from ai_engine import ai_engine
from config import HOST, PORT, MAX_FILE_SIZE_MB

app = FastAPI(
    title="TechXcel API",
    description="Smart Excel Analytics - What-if simulations and AI insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for current session
session_data: Dict[str, Any] = {
    "processor": None,
    "summary": None,
    "relationships": None
}


class WhatIfRequest(BaseModel):
    question: str
    variable: Optional[str] = None
    original_value: Optional[float] = None
    new_value: Optional[float] = None


class SimulationRequest(BaseModel):
    variable: str
    min_value: float
    max_value: float
    steps: int = 10


class OptimizationRequest(BaseModel):
    target_variable: str
    optimization_goal: str


@app.get("/")
async def root():
    return {
        "message": "TechXcel API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload - Upload Excel file",
            "analyze": "/analyze - Get AI analysis",
            "whatif": "/whatif - Ask what-if questions",
            "simulate": "/simulate - Run simulations",
            "optimize": "/optimize - Get optimization suggestions"
        }
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process an Excel file"""
    
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Maximum size: {MAX_FILE_SIZE_MB}MB")
    
    try:
        # Process the file
        processor, analysis = process_uploaded_file(content)
        
        # Store in session
        session_data["processor"] = processor
        session_data["summary"] = analysis["summary"]
        session_data["relationships"] = analysis["relationships"]
        
        return {
            "status": "success",
            "filename": file.filename,
            "summary": analysis["summary"],
            "relationships": analysis["relationships"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/analyze")
async def analyze_data():
    """Get AI-powered analysis of the uploaded data"""
    
    if session_data["processor"] is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a file first.")
    
    try:
        analysis = ai_engine.analyze_data(
            session_data["summary"],
            session_data["relationships"]
        )
        
        return {
            "status": "success",
            "analysis": analysis,
            "summary": session_data["summary"],
            "relationships": session_data["relationships"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")


@app.post("/whatif")
async def what_if_analysis(request: WhatIfRequest):
    """Process a what-if question"""
    
    if session_data["processor"] is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a file first.")
    
    processor = session_data["processor"]
    
    try:
        # Run simulation if we have variable details
        simulation_results = None
        if request.variable and request.original_value is not None and request.new_value is not None:
            simulation_results = processor.simulate_what_if(
                request.variable,
                request.original_value,
                request.new_value
            )
        
        # Get AI response
        response = ai_engine.process_what_if_question(
            request.question,
            session_data["summary"],
            session_data["relationships"],
            simulation_results
        )
        
        return {
            "status": "success",
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.post("/simulate")
async def run_simulation(request: SimulationRequest):
    """Run a simulation for a range of values"""
    
    if session_data["processor"] is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a file first.")
    
    processor = session_data["processor"]
    
    try:
        simulation_df = processor.get_simulation_data(
            request.variable,
            (request.min_value, request.max_value),
            request.steps
        )
        
        return {
            "status": "success",
            "simulation_data": simulation_df.to_dict(orient="records"),
            "variable": request.variable,
            "range": [request.min_value, request.max_value]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running simulation: {str(e)}")


@app.post("/optimize")
async def get_optimization(request: OptimizationRequest):
    """Get AI suggestions for optimal values"""
    
    if session_data["processor"] is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a file first.")
    
    try:
        suggestions = ai_engine.get_optimal_value_suggestion(
            request.target_variable,
            request.optimization_goal,
            session_data["summary"],
            session_data["relationships"]
        )
        
        return {
            "status": "success",
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting optimization: {str(e)}")


@app.get("/data")
async def get_current_data():
    """Get the currently loaded data"""
    
    if session_data["processor"] is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a file first.")
    
    processor = session_data["processor"]
    
    return {
        "status": "success",
        "data": processor.df.to_dict(orient="records"),
        "columns": list(processor.df.columns)
    }


@app.get("/relationships")
async def get_relationships():
    """Get detected relationships between variables"""
    
    if session_data["relationships"] is None:
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a file first.")
    
    return {
        "status": "success",
        "relationships": session_data["relationships"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
