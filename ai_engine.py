"""
AI Engine - Handles OpenAI integration for insights and what-if analysis
"""

import json
import re
from typing import Dict, Any, Optional, List
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


class AIEngine:
    """AI Engine for spreadsheet analysis and what-if simulations"""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.model = OPENAI_MODEL
        self.conversation_history: List[Dict] = []
    
    def _create_system_prompt(self, data_summary: Dict) -> str:
        """Create a system prompt with data context"""
        return f"""You are an AI Spreadsheet Analyst specializing in counterfactual analysis and business simulations.

You are analyzing a spreadsheet with the following structure:
- Rows: {data_summary.get('rows', 'Unknown')}
- Columns: {', '.join(data_summary.get('column_names', []))}
- Numeric columns: {', '.join(data_summary.get('numeric_columns', []))}

Sample data:
{json.dumps(data_summary.get('sample_data', [])[:3], indent=2)}

Statistics:
{json.dumps(data_summary.get('statistics', {}), indent=2)}

Your role:
1. Understand the business context of this data
2. Answer "What if?" questions by simulating alternate scenarios
3. Provide confidence levels for predictions
4. Suggest optimal values for business decisions
5. Explain the relationships between variables

Always respond with:
- Clear numerical predictions when asked what-if questions
- Confidence percentages for predictions
- Business impact explanations
- Recommendations for optimal values

Format numbers appropriately (currency with ₹ or $, percentages with %, etc.)
"""

    def analyze_data(self, data_summary: Dict, relationships: Dict) -> str:
        """Generate AI insights about the data"""
        if not self.client:
            return self._fallback_analysis(data_summary, relationships)
        
        system_prompt = self._create_system_prompt(data_summary)
        
        user_prompt = f"""Analyze this spreadsheet data and provide:

1. **Data Overview**: What kind of business data is this?
2. **Key Relationships**: What variables are related?
3. **Detected Patterns**: Any trends or anomalies?
4. **Suggested What-If Questions**: What scenarios would be valuable to explore?

Detected Relationships:
{json.dumps(relationships, indent=2)}

Provide a concise but insightful analysis."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return self._fallback_analysis(data_summary, relationships)
    
    def process_what_if_question(
        self, 
        question: str, 
        data_summary: Dict, 
        relationships: Dict,
        simulation_results: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process a what-if question and generate AI response"""
        
        # First, parse the question to extract variables and values
        parsed = self._parse_what_if_question(question, data_summary)
        
        if not self.client:
            return self._fallback_what_if(parsed, simulation_results, relationships)
        
        system_prompt = self._create_system_prompt(data_summary)
        
        user_prompt = f"""User Question: {question}

Based on our analysis:
- Detected relationships: {json.dumps(relationships.get('regression_models', {}), indent=2)}

{f"Simulation Results: {json.dumps(simulation_results, indent=2)}" if simulation_results else ""}

Please provide:
1. **Simulated Outcome**: What would happen in this scenario?
2. **Specific Predictions**: Numerical estimates for affected variables
3. **Confidence Level**: How confident is this prediction (percentage)?
4. **Business Impact**: What does this mean for the business?
5. **Recommendations**: Should this change be made?

Be specific with numbers and percentages."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "question": question,
                "parsed_variables": parsed,
                "simulation_data": simulation_results,
                "ai_response": ai_response,
                "confidence": self._extract_confidence(ai_response)
            }
        except Exception as e:
            return self._fallback_what_if(parsed, simulation_results, relationships)
    
    def _parse_what_if_question(self, question: str, data_summary: Dict) -> Dict:
        """Parse what-if question to extract variable and value changes"""
        result = {
            "variable": None,
            "original_value": None,
            "new_value": None,
            "change_type": None
        }
        
        question_lower = question.lower()
        
        # Find mentioned column
        for col in data_summary.get('column_names', []):
            if col.lower() in question_lower:
                result["variable"] = col
                break
        
        # Extract numbers from question
        numbers = re.findall(r'[\d,]+\.?\d*', question)
        numbers = [float(n.replace(',', '')) for n in numbers if n]
        
        if len(numbers) >= 2:
            result["original_value"] = numbers[0]
            result["new_value"] = numbers[1]
        elif len(numbers) == 1:
            result["new_value"] = numbers[0]
        
        # Detect change type
        if "increase" in question_lower:
            result["change_type"] = "increase"
        elif "decrease" in question_lower or "reduce" in question_lower:
            result["change_type"] = "decrease"
        elif "double" in question_lower:
            result["change_type"] = "double"
        elif "half" in question_lower:
            result["change_type"] = "half"
        
        return result
    
    def _extract_confidence(self, response: str) -> float:
        """Extract confidence percentage from AI response"""
        # Look for confidence patterns
        patterns = [
            r'confidence[:\s]+(\d+)%',
            r'(\d+)%\s*confidence',
            r'(\d+)%\s*certain',
            r'accuracy[:\s]+(\d+)%'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response.lower())
            if match:
                return float(match.group(1)) / 100
        
        return 0.75  # Default confidence
    
    def get_optimal_value_suggestion(
        self, 
        target_variable: str,
        optimization_goal: str,
        data_summary: Dict,
        relationships: Dict
    ) -> Dict[str, Any]:
        """Get AI suggestion for optimal values"""
        if not self.client:
            return self._fallback_optimization(target_variable, optimization_goal, relationships)
        
        system_prompt = self._create_system_prompt(data_summary)
        
        user_prompt = f"""Based on the data and relationships:

Relationships: {json.dumps(relationships.get('regression_models', {}), indent=2)}

User wants to optimize: {target_variable}
Goal: {optimization_goal}

Provide:
1. **Optimal Values**: Suggested values for input variables
2. **Expected Outcome**: Predicted result
3. **ROI Estimate**: Expected return
4. **Implementation Steps**: How to achieve this"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            return {
                "target": target_variable,
                "goal": optimization_goal,
                "suggestions": response.choices[0].message.content
            }
        except Exception as e:
            return self._fallback_optimization(target_variable, optimization_goal, relationships)
    
    def _fallback_analysis(self, data_summary: Dict, relationships: Dict) -> str:
        """Fallback analysis when OpenAI is not available"""
        analysis = []
        analysis.append("## 📊 Data Analysis Report\n")
        
        # Overview
        analysis.append(f"**Dataset Overview:**")
        analysis.append(f"- Total Rows: {data_summary.get('rows', 0)}")
        analysis.append(f"- Columns: {', '.join(data_summary.get('column_names', []))}")
        analysis.append("")
        
        # Statistics
        analysis.append("**Key Statistics:**")
        for col, stats in data_summary.get('statistics', {}).items():
            analysis.append(f"- {col}: Mean = {stats['mean']:.2f}, Range = [{stats['min']:.2f} - {stats['max']:.2f}]")
        analysis.append("")
        
        # Relationships
        analysis.append("**Detected Relationships:**")
        for key, corr in relationships.get('correlations', {}).items():
            analysis.append(f"- {key}: {corr['strength']} {corr['direction']} correlation ({corr['correlation']:.2f})")
        analysis.append("")
        
        # Regression formulas
        analysis.append("**Predictive Models:**")
        for target, model in relationships.get('regression_models', {}).items():
            if model.get('r2_score', 0) > 0.5:
                analysis.append(f"- {model['formula']} (R² = {model['r2_score']:.2f})")
        
        return "\n".join(analysis)
    
    def _fallback_what_if(self, parsed: Dict, simulation: Optional[Dict], relationships: Dict) -> Dict:
        """Fallback what-if response when OpenAI is not available"""
        response_parts = []
        
        if simulation and simulation.get('impacts'):
            response_parts.append("## 🔮 Simulated Outcome\n")
            
            for impact in simulation['impacts']:
                change_direction = "increase" if impact['change'] > 0 else "decrease"
                response_parts.append(f"**{impact['target_variable']}**:")
                response_parts.append(f"- Original: {impact['original_value']:.2f}")
                response_parts.append(f"- Predicted: {impact['predicted_value']:.2f}")
                response_parts.append(f"- Change: {abs(impact['percent_change']):.1f}% {change_direction}")
                response_parts.append(f"- Confidence: {impact['confidence']*100:.0f}%")
                response_parts.append("")
        
        return {
            "question": parsed.get('variable', 'Unknown'),
            "parsed_variables": parsed,
            "simulation_data": simulation,
            "ai_response": "\n".join(response_parts) if response_parts else "Unable to process question",
            "confidence": 0.7
        }
    
    def _fallback_optimization(self, target: str, goal: str, relationships: Dict) -> Dict:
        """Fallback optimization when OpenAI is not available"""
        suggestions = []
        suggestions.append(f"## 🎯 Optimization Suggestions for {target}\n")
        suggestions.append(f"**Goal:** {goal}\n")
        
        # Find relevant model
        model = relationships.get('regression_models', {}).get(target)
        if model:
            suggestions.append("**Key Drivers:**")
            for feat, coef in model['coefficients'].items():
                impact = "positive" if coef > 0 else "negative"
                suggestions.append(f"- {feat}: {impact} impact (coefficient: {coef:.2f})")
        
        return {
            "target": target,
            "goal": goal,
            "suggestions": "\n".join(suggestions)
        }


# Singleton instance
ai_engine = AIEngine()
