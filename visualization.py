"""
Visualization Module - Creates charts and graphs for simulations
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


def create_actual_vs_simulated_chart(
    actual_data: pd.DataFrame,
    simulation_results: Dict,
    x_column: str,
    y_column: str,
    title: str = "Actual vs Simulated"
) -> go.Figure:
    """Create a comparison chart showing actual vs simulated values"""
    
    fig = go.Figure()
    
    # Actual data
    fig.add_trace(go.Scatter(
        x=actual_data[x_column] if x_column in actual_data.columns else list(range(len(actual_data))),
        y=actual_data[y_column],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=10)
    ))
    
    # Simulated data
    impacts = simulation_results.get('impacts', [])
    for impact in impacts:
        if impact['target_variable'] == y_column:
            # Add a horizontal line for simulated value
            fig.add_trace(go.Scatter(
                x=[actual_data[x_column].iloc[-1]] if x_column in actual_data.columns else [len(actual_data) - 1],
                y=[impact['predicted_value']],
                mode='markers',
                name='Simulated',
                marker=dict(size=15, color='#E94F37', symbol='star')
            ))
            
            # Add annotation
            fig.add_annotation(
                x=actual_data[x_column].iloc[-1] if x_column in actual_data.columns else len(actual_data) - 1,
                y=impact['predicted_value'],
                text=f"Simulated: {impact['predicted_value']:.0f} ({impact['percent_change']:+.1f}%)",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                ax=50,
                ay=-40
            )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        xaxis_title=x_column,
        yaxis_title=y_column,
        template="plotly_white",
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig


def create_timeline_chart(
    data: pd.DataFrame,
    time_column: str,
    value_columns: List[str],
    title: str = "Timeline Analysis"
) -> go.Figure:
    """Create a timeline chart for multiple variables"""
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    
    for i, col in enumerate(value_columns):
        if col in data.columns:
            fig.add_trace(go.Scatter(
                x=data[time_column] if time_column in data.columns else list(range(len(data))),
                y=data[col],
                mode='lines+markers',
                name=col,
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=8)
            ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        xaxis_title=time_column if time_column in data.columns else "Period",
        yaxis_title="Value",
        template="plotly_white",
        hovermode='x unified',
        showlegend=True
    )
    
    return fig


def create_correlation_heatmap(
    data: pd.DataFrame,
    title: str = "Variable Correlations"
) -> go.Figure:
    """Create a correlation heatmap"""
    
    numeric_data = data.select_dtypes(include=[np.number])
    corr_matrix = numeric_data.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu_r',
        zmin=-1,
        zmax=1,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 12},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        template="plotly_white",
        height=500,
        width=600
    )
    
    return fig


def create_scenario_comparison_chart(
    scenarios: List[Dict],
    target_variable: str,
    title: str = "Scenario Comparison"
) -> go.Figure:
    """Create a bar chart comparing different scenarios"""
    
    scenario_names = []
    values = []
    colors = []
    
    for i, scenario in enumerate(scenarios):
        scenario_names.append(scenario.get('name', f'Scenario {i+1}'))
        values.append(scenario.get('value', 0))
        colors.append('#2E86AB' if i == 0 else '#E94F37')
    
    fig = go.Figure(data=[
        go.Bar(
            x=scenario_names,
            y=values,
            marker_color=colors,
            text=[f'{v:,.0f}' for v in values],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        xaxis_title="Scenario",
        yaxis_title=target_variable,
        template="plotly_white",
        showlegend=False
    )
    
    return fig


def create_what_if_slider_chart(
    simulation_data: pd.DataFrame,
    input_column: str,
    output_columns: List[str],
    title: str = "What-If Analysis"
) -> go.Figure:
    """Create an interactive chart for what-if analysis"""
    
    fig = make_subplots(
        rows=len(output_columns), 
        cols=1,
        shared_xaxes=True,
        subplot_titles=output_columns,
        vertical_spacing=0.1
    )
    
    colors = px.colors.qualitative.Set2
    
    for i, col in enumerate(output_columns):
        if col in simulation_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=simulation_data[input_column],
                    y=simulation_data[col],
                    mode='lines+markers',
                    name=col,
                    line=dict(color=colors[i % len(colors)], width=3),
                    fill='tozeroy',
                    fillcolor=f'rgba({int(colors[i][1:3], 16)},{int(colors[i][3:5], 16)},{int(colors[i][5:7], 16)},0.2)'
                ),
                row=i+1,
                col=1
            )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        template="plotly_white",
        height=300 * len(output_columns),
        showlegend=True,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text=input_column, row=len(output_columns), col=1)
    
    return fig


def create_impact_gauge_chart(
    impact: Dict,
    title: str = "Impact Gauge"
) -> go.Figure:
    """Create a gauge chart showing impact percentage"""
    
    percent_change = impact.get('percent_change', 0)
    confidence = impact.get('confidence', 0.7) * 100
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=['Change', 'Confidence']
    )
    
    # Impact gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=percent_change,
            number={'suffix': '%'},
            delta={'reference': 0, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            gauge={
                'axis': {'range': [-50, 50]},
                'bar': {'color': "#2E86AB"},
                'steps': [
                    {'range': [-50, -10], 'color': '#ffcccb'},
                    {'range': [-10, 10], 'color': '#fffacd'},
                    {'range': [10, 50], 'color': '#90EE90'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': percent_change
                }
            }
        ),
        row=1, col=1
    )
    
    # Confidence gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={'suffix': '%'},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#E94F37"},
                'steps': [
                    {'range': [0, 50], 'color': '#ffcccb'},
                    {'range': [50, 75], 'color': '#fffacd'},
                    {'range': [75, 100], 'color': '#90EE90'}
                ]
            }
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        template="plotly_white",
        height=300
    )
    
    return fig


def create_relationship_network(
    relationships: Dict,
    title: str = "Variable Relationships"
) -> go.Figure:
    """Create a network diagram showing variable relationships"""
    
    correlations = relationships.get('correlations', {})
    
    if not correlations:
        return go.Figure().add_annotation(text="No relationships detected", showarrow=False)
    
    # Extract unique variables
    variables = set()
    edges = []
    
    for key, value in correlations.items():
        vars_pair = key.split('_vs_')
        if len(vars_pair) == 2:
            variables.add(vars_pair[0])
            variables.add(vars_pair[1])
            edges.append({
                'source': vars_pair[0],
                'target': vars_pair[1],
                'weight': abs(value['correlation']),
                'direction': value['direction']
            })
    
    variables = list(variables)
    n = len(variables)
    
    # Create circular layout
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    x_pos = np.cos(angles) * 2
    y_pos = np.sin(angles) * 2
    
    pos = {var: (x_pos[i], y_pos[i]) for i, var in enumerate(variables)}
    
    fig = go.Figure()
    
    # Add edges
    for edge in edges:
        x0, y0 = pos[edge['source']]
        x1, y1 = pos[edge['target']]
        color = '#2E86AB' if edge['direction'] == 'positive' else '#E94F37'
        
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(width=edge['weight']*5, color=color),
            hoverinfo='text',
            text=f"{edge['source']} ↔ {edge['target']}: {edge['weight']:.2f}",
            showlegend=False
        ))
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=[pos[v][0] for v in variables],
        y=[pos[v][1] for v in variables],
        mode='markers+text',
        marker=dict(size=30, color='#F4A261'),
        text=variables,
        textposition='middle center',
        textfont=dict(size=10, color='white'),
        hoverinfo='text',
        showlegend=False
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        template="plotly_white",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=500,
        width=600
    )
    
    return fig
