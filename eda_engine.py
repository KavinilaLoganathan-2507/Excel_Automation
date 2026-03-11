"""
EDA Engine - Comprehensive Exploratory Data Analysis Module
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from scipy import stats
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')


class EDAEngine:
    """Comprehensive Exploratory Data Analysis Engine"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.date_cols = self._detect_date_columns()
        
    def _detect_date_columns(self) -> List[str]:
        """Detect date columns in the dataframe"""
        date_cols = []
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                date_cols.append(col)
            elif self.df[col].dtype == 'object':
                try:
                    pd.to_datetime(self.df[col].head(10))
                    date_cols.append(col)
                except:
                    pass
        return date_cols
    
    def get_data_overview(self) -> Dict[str, Any]:
        """Get comprehensive data overview"""
        return {
            "shape": {"rows": len(self.df), "columns": len(self.df.columns)},
            "memory_usage": f"{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB",
            "column_types": {
                "numeric": len(self.numeric_cols),
                "categorical": len(self.categorical_cols),
                "datetime": len(self.date_cols)
            },
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.astype(str).to_dict()
        }
    
    def get_missing_values_analysis(self) -> Dict[str, Any]:
        """Analyze missing values in the dataset"""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)
        
        return {
            "total_missing": int(missing.sum()),
            "columns_with_missing": int((missing > 0).sum()),
            "missing_by_column": {
                col: {
                    "count": int(missing[col]),
                    "percentage": float(missing_pct[col])
                }
                for col in self.df.columns if missing[col] > 0
            },
            "completeness_score": round((1 - missing.sum() / (len(self.df) * len(self.df.columns))) * 100, 2)
        }
    
    def get_numeric_summary(self) -> Dict[str, Any]:
        """Get detailed summary for numeric columns"""
        if not self.numeric_cols:
            return {"message": "No numeric columns found"}
        
        summary = {}
        for col in self.numeric_cols:
            data = self.df[col].dropna()
            if len(data) == 0:
                continue
                
            q1, q3 = np.percentile(data, [25, 75])
            iqr = q3 - q1
            
            summary[col] = {
                "count": int(len(data)),
                "mean": round(float(data.mean()), 2),
                "median": round(float(data.median()), 2),
                "mode": round(float(data.mode().iloc[0]) if len(data.mode()) > 0 else data.mean(), 2),
                "std": round(float(data.std()), 2),
                "variance": round(float(data.var()), 2),
                "min": round(float(data.min()), 2),
                "max": round(float(data.max()), 2),
                "range": round(float(data.max() - data.min()), 2),
                "q1": round(float(q1), 2),
                "q3": round(float(q3), 2),
                "iqr": round(float(iqr), 2),
                "skewness": round(float(stats.skew(data)), 4),
                "kurtosis": round(float(stats.kurtosis(data)), 4),
                "sum": round(float(data.sum()), 2),
                "outliers_count": int(((data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)).sum())
            }
        
        return summary
    
    def get_categorical_summary(self) -> Dict[str, Any]:
        """Get detailed summary for categorical columns"""
        if not self.categorical_cols:
            return {"message": "No categorical columns found"}
        
        summary = {}
        for col in self.categorical_cols:
            value_counts = self.df[col].value_counts()
            
            summary[col] = {
                "unique_count": int(self.df[col].nunique()),
                "top_value": str(value_counts.index[0]) if len(value_counts) > 0 else None,
                "top_frequency": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                "value_distribution": {
                    str(k): int(v) for k, v in value_counts.head(10).items()
                }
            }
        
        return summary
    
    def get_correlation_analysis(self) -> Dict[str, Any]:
        """Get correlation analysis between numeric columns"""
        if len(self.numeric_cols) < 2:
            return {"message": "Not enough numeric columns for correlation"}
        
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # Find strong correlations
        strong_correlations = []
        for i in range(len(self.numeric_cols)):
            for j in range(i + 1, len(self.numeric_cols)):
                corr = corr_matrix.iloc[i, j]
                if abs(corr) > 0.5:
                    strong_correlations.append({
                        "var1": self.numeric_cols[i],
                        "var2": self.numeric_cols[j],
                        "correlation": round(float(corr), 4),
                        "strength": "strong" if abs(corr) > 0.7 else "moderate",
                        "direction": "positive" if corr > 0 else "negative"
                    })
        
        return {
            "correlation_matrix": corr_matrix.round(4).to_dict(),
            "strong_correlations": strong_correlations,
            "heatmap_data": {
                "columns": list(corr_matrix.columns),
                "values": corr_matrix.values.tolist()
            }
        }
    
    def get_distribution_analysis(self) -> Dict[str, Any]:
        """Analyze distribution of numeric columns"""
        if not self.numeric_cols:
            return {"message": "No numeric columns found"}
        
        distribution = {}
        for col in self.numeric_cols:
            data = self.df[col].dropna()
            if len(data) < 8:
                continue
            
            # Normality test
            try:
                _, p_value = stats.normaltest(data)
                is_normal = p_value > 0.05
            except:
                is_normal = False
                p_value = 0
            
            # Distribution type inference
            skewness = stats.skew(data)
            if abs(skewness) < 0.5:
                dist_type = "symmetric"
            elif skewness > 0:
                dist_type = "right-skewed"
            else:
                dist_type = "left-skewed"
            
            # Histogram data
            hist, bin_edges = np.histogram(data, bins=20)
            
            distribution[col] = {
                "is_normal": is_normal,
                "normality_p_value": round(float(p_value), 4),
                "distribution_type": dist_type,
                "histogram": {
                    "counts": hist.tolist(),
                    "bin_edges": bin_edges.tolist()
                }
            }
        
        return distribution
    
    def get_outlier_analysis(self) -> Dict[str, Any]:
        """Detect and analyze outliers"""
        if not self.numeric_cols:
            return {"message": "No numeric columns found"}
        
        outliers = {}
        for col in self.numeric_cols:
            data = self.df[col].dropna()
            
            q1, q3 = np.percentile(data, [25, 75])
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outlier_mask = (data < lower_bound) | (data > upper_bound)
            outlier_values = data[outlier_mask]
            
            outliers[col] = {
                "count": int(outlier_mask.sum()),
                "percentage": round(float(outlier_mask.sum() / len(data) * 100), 2),
                "lower_bound": round(float(lower_bound), 2),
                "upper_bound": round(float(upper_bound), 2),
                "outlier_values": outlier_values.tolist()[:10]  # Limit to first 10
            }
        
        return outliers
    
    def get_time_series_analysis(self) -> Dict[str, Any]:
        """Analyze time series patterns if date columns exist"""
        if not self.date_cols:
            return {"message": "No date columns found"}
        
        analysis = {}
        for date_col in self.date_cols:
            try:
                # Convert to datetime if needed
                dates = pd.to_datetime(self.df[date_col])
                
                analysis[date_col] = {
                    "start_date": str(dates.min()),
                    "end_date": str(dates.max()),
                    "date_range_days": int((dates.max() - dates.min()).days),
                    "unique_dates": int(dates.nunique())
                }
                
                # Analyze trends with numeric columns
                for num_col in self.numeric_cols[:3]:  # Limit to first 3
                    temp_df = pd.DataFrame({
                        'date': dates,
                        'value': self.df[num_col]
                    }).dropna().sort_values('date')
                    
                    if len(temp_df) > 2:
                        # Calculate trend
                        x = np.arange(len(temp_df))
                        y = temp_df['value'].values
                        slope, intercept, r_value, _, _ = stats.linregress(x, y)
                        
                        analysis[date_col][f"trend_{num_col}"] = {
                            "slope": round(float(slope), 4),
                            "r_squared": round(float(r_value ** 2), 4),
                            "direction": "increasing" if slope > 0 else "decreasing"
                        }
            except Exception as e:
                analysis[date_col] = {"error": str(e)}
        
        return analysis
    
    def get_duplicate_analysis(self) -> Dict[str, Any]:
        """Analyze duplicate rows"""
        duplicates = self.df.duplicated()
        duplicate_rows = self.df[duplicates]
        
        return {
            "total_duplicates": int(duplicates.sum()),
            "percentage": round(float(duplicates.sum() / len(self.df) * 100), 2),
            "duplicate_columns": [
                col for col in self.df.columns 
                if self.df[col].duplicated().sum() > len(self.df) * 0.5
            ]
        }
    
    def get_data_quality_score(self) -> Dict[str, Any]:
        """Calculate overall data quality score"""
        scores = []
        
        # Completeness score (missing values)
        missing_pct = self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))
        completeness = (1 - missing_pct) * 100
        scores.append(completeness)
        
        # Uniqueness score (duplicates)
        duplicate_pct = self.df.duplicated().sum() / len(self.df)
        uniqueness = (1 - duplicate_pct) * 100
        scores.append(uniqueness)
        
        # Consistency score (outliers in numeric columns)
        if self.numeric_cols:
            outlier_count = 0
            for col in self.numeric_cols:
                data = self.df[col].dropna()
                q1, q3 = np.percentile(data, [25, 75])
                iqr = q3 - q1
                outlier_count += ((data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)).sum()
            
            total_numeric_values = self.df[self.numeric_cols].count().sum()
            consistency = (1 - outlier_count / total_numeric_values) * 100 if total_numeric_values > 0 else 100
            scores.append(consistency)
        
        overall_score = np.mean(scores)
        
        return {
            "overall_score": round(float(overall_score), 1),
            "completeness": round(float(completeness), 1),
            "uniqueness": round(float(uniqueness), 1),
            "consistency": round(float(scores[2]) if len(scores) > 2 else 100, 1),
            "grade": "A" if overall_score >= 90 else "B" if overall_score >= 80 else "C" if overall_score >= 70 else "D" if overall_score >= 60 else "F"
        }
    
    def get_full_eda_report(self) -> Dict[str, Any]:
        """Generate complete EDA report"""
        return {
            "overview": self.get_data_overview(),
            "missing_values": self.get_missing_values_analysis(),
            "numeric_summary": self.get_numeric_summary(),
            "categorical_summary": self.get_categorical_summary(),
            "correlations": self.get_correlation_analysis(),
            "distributions": self.get_distribution_analysis(),
            "outliers": self.get_outlier_analysis(),
            "time_series": self.get_time_series_analysis(),
            "duplicates": self.get_duplicate_analysis(),
            "data_quality": self.get_data_quality_score()
        }
    
    def get_smart_insights(self) -> List[Dict[str, Any]]:
        """Generate AI-like smart insights from the data"""
        insights = []
        
        # Missing data insights
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            worst_col = missing.idxmax()
            insights.append({
                "type": "warning",
                "category": "Data Quality",
                "title": "Missing Data Detected",
                "message": f"{worst_col} has {missing[worst_col]} missing values ({missing[worst_col]/len(self.df)*100:.1f}%)",
                "suggestion": "Consider imputation or data collection improvements"
            })
        
        # Correlation insights
        if len(self.numeric_cols) >= 2:
            corr = self.df[self.numeric_cols].corr()
            for i in range(len(self.numeric_cols)):
                for j in range(i + 1, len(self.numeric_cols)):
                    if abs(corr.iloc[i, j]) > 0.8:
                        insights.append({
                            "type": "info",
                            "category": "Relationships",
                            "title": "Strong Correlation Found",
                            "message": f"{self.numeric_cols[i]} and {self.numeric_cols[j]} are highly correlated ({corr.iloc[i, j]:.2f})",
                            "suggestion": "Consider multicollinearity in modeling"
                        })
        
        # Trend insights
        for col in self.numeric_cols:
            data = self.df[col].dropna().values
            if len(data) > 3:
                diffs = np.diff(data)
                if np.all(diffs > 0):
                    insights.append({
                        "type": "success",
                        "category": "Trends",
                        "title": "Consistent Growth",
                        "message": f"{col} shows consistent upward trend",
                        "suggestion": "This pattern is predictable for forecasting"
                    })
                elif np.all(diffs < 0):
                    insights.append({
                        "type": "danger",
                        "category": "Trends",
                        "title": "Declining Trend",
                        "message": f"{col} shows consistent downward trend",
                        "suggestion": "Investigate root causes for the decline"
                    })
        
        # Outlier insights
        for col in self.numeric_cols:
            data = self.df[col].dropna()
            q1, q3 = np.percentile(data, [25, 75])
            iqr = q3 - q1
            outliers = ((data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)).sum()
            if outliers > len(data) * 0.1:
                insights.append({
                    "type": "warning",
                    "category": "Anomalies",
                    "title": "High Outlier Count",
                    "message": f"{col} contains {outliers} outliers ({outliers/len(data)*100:.1f}%)",
                    "suggestion": "Review data collection process or clean outliers"
                })
        
        # Distribution insights
        for col in self.numeric_cols:
            data = self.df[col].dropna()
            if len(data) > 8:
                skewness = stats.skew(data)
                if abs(skewness) > 2:
                    direction = "right" if skewness > 0 else "left"
                    insights.append({
                        "type": "info",
                        "category": "Distribution",
                        "title": "Highly Skewed Data",
                        "message": f"{col} is heavily {direction}-skewed ({skewness:.2f})",
                        "suggestion": "Consider log transformation for analysis"
                    })
        
        return insights[:10]  # Limit to top 10 insights
    
    def filter_by_date_range(self, date_column: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter data by date range"""
        if date_column not in self.df.columns:
            return self.df
        
        try:
            dates = pd.to_datetime(self.df[date_column])
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            mask = (dates >= start) & (dates <= end)
            return self.df[mask]
        except:
            return self.df
    
    def aggregate_by_period(self, date_column: str, numeric_column: str, period: str = 'M') -> pd.DataFrame:
        """Aggregate data by time period"""
        if date_column not in self.df.columns or numeric_column not in self.df.columns:
            return pd.DataFrame()
        
        try:
            temp_df = self.df.copy()
            temp_df[date_column] = pd.to_datetime(temp_df[date_column])
            temp_df.set_index(date_column, inplace=True)
            
            agg_df = temp_df[numeric_column].resample(period).agg(['sum', 'mean', 'min', 'max', 'count'])
            agg_df = agg_df.reset_index()
            return agg_df
        except:
            return pd.DataFrame()
