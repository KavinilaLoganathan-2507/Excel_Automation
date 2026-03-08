"""
Data Processing Module - Handles Excel file parsing and analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import io
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import warnings

warnings.filterwarnings('ignore')


class SpreadsheetProcessor:
    """Processes and analyzes spreadsheet data"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.numeric_columns: List[str] = []
        self.categorical_columns: List[str] = []
        self.date_columns: List[str] = []
        self.relationships: Dict[str, Any] = {}
        
    def load_excel(self, file_content: bytes) -> pd.DataFrame:
        """Load Excel file from bytes content"""
        self.df = pd.read_excel(io.BytesIO(file_content))
        self._analyze_columns()
        return self.df
    
    def load_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Load data from an existing DataFrame"""
        self.df = df.copy()
        self._analyze_columns()
        return self.df
    
    def _analyze_columns(self):
        """Categorize columns by data type"""
        self.numeric_columns = []
        self.categorical_columns = []
        self.date_columns = []
        
        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                self.numeric_columns.append(col)
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                self.date_columns.append(col)
            else:
                # Try to parse as date
                try:
                    pd.to_datetime(self.df[col])
                    self.date_columns.append(col)
                except:
                    self.categorical_columns.append(col)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the data"""
        if self.df is None:
            return {}
        
        summary = {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "column_names": list(self.df.columns),
            "numeric_columns": self.numeric_columns,
            "categorical_columns": self.categorical_columns,
            "date_columns": self.date_columns,
            "sample_data": self.df.head(5).to_dict(orient="records"),
            "statistics": {}
        }
        
        # Add statistics for numeric columns
        for col in self.numeric_columns:
            summary["statistics"][col] = {
                "mean": float(self.df[col].mean()),
                "std": float(self.df[col].std()),
                "min": float(self.df[col].min()),
                "max": float(self.df[col].max()),
                "sum": float(self.df[col].sum())
            }
        
        return summary
    
    def detect_relationships(self) -> Dict[str, Any]:
        """Detect relationships between numeric columns using correlation and regression"""
        if self.df is None or len(self.numeric_columns) < 2:
            return {"error": "Not enough numeric columns for relationship detection"}
        
        relationships = {
            "correlations": {},
            "regression_models": {},
            "detected_patterns": []
        }
        
        # Calculate correlation matrix
        numeric_df = self.df[self.numeric_columns].dropna()
        corr_matrix = numeric_df.corr()
        
        # Find strong correlations
        for i, col1 in enumerate(self.numeric_columns):
            for j, col2 in enumerate(self.numeric_columns):
                if i < j:
                    corr = corr_matrix.loc[col1, col2]
                    if abs(corr) > 0.3:  # Threshold for significance
                        relationships["correlations"][f"{col1}_vs_{col2}"] = {
                            "correlation": round(corr, 4),
                            "strength": "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.5 else "weak",
                            "direction": "positive" if corr > 0 else "negative"
                        }
        
        # Build regression models for each potential target variable
        for target_col in self.numeric_columns:
            feature_cols = [c for c in self.numeric_columns if c != target_col]
            if len(feature_cols) > 0:
                model_info = self._build_regression_model(target_col, feature_cols)
                if model_info:
                    relationships["regression_models"][target_col] = model_info
        
        # Detect patterns
        relationships["detected_patterns"] = self._detect_patterns()
        
        self.relationships = relationships
        return relationships
    
    def _build_regression_model(self, target: str, features: List[str]) -> Optional[Dict]:
        """Build a linear regression model"""
        try:
            data = self.df[features + [target]].dropna()
            if len(data) < 5:
                return None
            
            X = data[features].values
            y = data[target].values
            
            # Fit model
            model = LinearRegression()
            model.fit(X, y)
            
            # Calculate R² score
            y_pred = model.predict(X)
            r2 = r2_score(y, y_pred)
            
            # Create coefficient mapping
            coefficients = {}
            for i, feat in enumerate(features):
                coefficients[feat] = round(model.coef_[i], 4)
            
            return {
                "features": features,
                "intercept": round(model.intercept_, 4),
                "coefficients": coefficients,
                "r2_score": round(r2, 4),
                "formula": self._generate_formula(target, model.intercept_, coefficients)
            }
        except Exception as e:
            return None
    
    def _generate_formula(self, target: str, intercept: float, coefficients: Dict[str, float]) -> str:
        """Generate a human-readable formula"""
        parts = [f"{target} = {intercept:.2f}"]
        for feat, coef in coefficients.items():
            sign = "+" if coef >= 0 else "-"
            parts.append(f"{sign} {abs(coef):.2f} × {feat}")
        return " ".join(parts)
    
    def _detect_patterns(self) -> List[Dict]:
        """Detect common patterns in the data"""
        patterns = []
        
        # Check for trends in numeric columns
        for col in self.numeric_columns:
            values = self.df[col].dropna().values
            if len(values) > 3:
                # Check for monotonic trend
                diffs = np.diff(values)
                if np.all(diffs > 0):
                    patterns.append({
                        "type": "increasing_trend",
                        "column": col,
                        "description": f"{col} shows consistent increase"
                    })
                elif np.all(diffs < 0):
                    patterns.append({
                        "type": "decreasing_trend",
                        "column": col,
                        "description": f"{col} shows consistent decrease"
                    })
                
                # Check for high variance
                cv = np.std(values) / np.mean(values) if np.mean(values) != 0 else 0
                if cv > 0.5:
                    patterns.append({
                        "type": "high_variance",
                        "column": col,
                        "description": f"{col} has high variability (CV: {cv:.2f})"
                    })
        
        return patterns
    
    def simulate_what_if(
        self, 
        variable: str, 
        original_value: float, 
        new_value: float,
        row_identifier: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Simulate a what-if scenario"""
        if self.df is None:
            return {"error": "No data loaded"}
        
        if variable not in self.numeric_columns:
            return {"error": f"Variable {variable} not found in numeric columns"}
        
        # Ensure we have relationships detected
        if not self.relationships:
            self.detect_relationships()
        
        results = {
            "variable_changed": variable,
            "original_value": original_value,
            "new_value": new_value,
            "change_percent": round((new_value - original_value) / original_value * 100, 2) if original_value != 0 else 0,
            "impacts": []
        }
        
        # Find dependent variables (where our variable is a feature)
        for target, model_info in self.relationships.get("regression_models", {}).items():
            if variable in model_info.get("features", []):
                # Calculate impact
                coef = model_info["coefficients"].get(variable, 0)
                value_change = new_value - original_value
                estimated_impact = coef * value_change
                
                # Get original target value (mean or specific row)
                original_target = self.df[target].mean()
                new_target = original_target + estimated_impact
                percent_change = (estimated_impact / original_target * 100) if original_target != 0 else 0
                
                results["impacts"].append({
                    "target_variable": target,
                    "coefficient": coef,
                    "original_value": round(original_target, 2),
                    "predicted_value": round(new_target, 2),
                    "change": round(estimated_impact, 2),
                    "percent_change": round(percent_change, 2),
                    "confidence": model_info["r2_score"]
                })
        
        return results
    
    def get_simulation_data(self, variable: str, value_range: Tuple[float, float], steps: int = 10) -> pd.DataFrame:
        """Generate simulation data for a range of values"""
        if not self.relationships:
            self.detect_relationships()
        
        original_value = self.df[variable].mean()
        min_val, max_val = value_range
        
        simulation_rows = []
        
        for val in np.linspace(min_val, max_val, steps):
            row = {"input_value": val}
            
            for target, model_info in self.relationships.get("regression_models", {}).items():
                if variable in model_info.get("features", []):
                    coef = model_info["coefficients"].get(variable, 0)
                    value_change = val - original_value
                    original_target = self.df[target].mean()
                    row[f"predicted_{target}"] = original_target + (coef * value_change)
            
            simulation_rows.append(row)
        
        return pd.DataFrame(simulation_rows)


def process_uploaded_file(file_content: bytes) -> Tuple[SpreadsheetProcessor, Dict]:
    """Process an uploaded Excel file and return processor and summary"""
    processor = SpreadsheetProcessor()
    processor.load_excel(file_content)
    summary = processor.get_summary()
    relationships = processor.detect_relationships()
    
    return processor, {
        "summary": summary,
        "relationships": relationships
    }
