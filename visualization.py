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


# ==================== ADVANCED CHART FUNCTIONS ====================

def create_distribution_chart(
    data: pd.DataFrame,
    column: str,
    chart_type: str = "histogram",
    title: str = None,
    color: str = "#8b5cf6"
) -> go.Figure:
    """Create distribution visualization (histogram, box, violin)"""
    
    title = title or f"Distribution of {column}"
    values = data[column].dropna()
    
    if chart_type == "histogram":
        fig = go.Figure(data=[go.Histogram(
            x=values,
            nbinsx=30,
            marker_color=color,
            opacity=0.8,
            hovertemplate='Range: %{x}<br>Count: %{y}<extra></extra>'
        )])
        fig.update_layout(
            xaxis_title=column,
            yaxis_title="Frequency",
            bargap=0.05
        )
    
    elif chart_type == "box":
        fig = go.Figure(data=[go.Box(
            y=values,
            name=column,
            marker_color=color,
            boxpoints='outliers',
            hovertemplate='%{y}<extra></extra>'
        )])
        fig.update_layout(yaxis_title=column)
    
    elif chart_type == "violin":
        fig = go.Figure(data=[go.Violin(
            y=values,
            name=column,
            box_visible=True,
            meanline_visible=True,
            fillcolor=color,
            opacity=0.7,
            line_color=color
        )])
        fig.update_layout(yaxis_title=column)
    
    else:
        fig = go.Figure()
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        showlegend=False
    )
    
    return fig


def create_pie_chart(
    data: pd.DataFrame,
    column: str,
    values_column: str = None,
    title: str = None,
    hole: float = 0.4
) -> go.Figure:
    """Create a pie/donut chart"""
    
    title = title or f"Distribution of {column}"
    
    if values_column and values_column in data.columns:
        # Aggregate values
        agg_data = data.groupby(column)[values_column].sum().reset_index()
        labels = agg_data[column]
        values = agg_data[values_column]
    else:
        # Count occurrences
        value_counts = data[column].value_counts()
        labels = value_counts.index
        values = value_counts.values
    
    colors = px.colors.qualitative.Set3
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        marker=dict(colors=colors),
        textinfo='percent+label',
        textposition='inside',
        hovertemplate='%{label}<br>Value: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    
    return fig


def create_bar_chart(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    color_column: str = None,
    orientation: str = 'v',
    title: str = None,
    aggregation: str = 'sum'
) -> go.Figure:
    """Create a bar chart with optional grouping"""
    
    title = title or f"{y_column} by {x_column}"
    
    if color_column:
        fig = px.bar(
            data,
            x=x_column if orientation == 'v' else y_column,
            y=y_column if orientation == 'v' else x_column,
            color=color_column,
            orientation='v' if orientation == 'v' else 'h',
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
    else:
        # Aggregate data
        if aggregation == 'sum':
            agg_data = data.groupby(x_column)[y_column].sum().reset_index()
        elif aggregation == 'mean':
            agg_data = data.groupby(x_column)[y_column].mean().reset_index()
        elif aggregation == 'count':
            agg_data = data.groupby(x_column)[y_column].count().reset_index()
        else:
            agg_data = data
        
        if orientation == 'v':
            fig = go.Figure(data=[go.Bar(
                x=agg_data[x_column],
                y=agg_data[y_column],
                marker_color='#8b5cf6',
                text=agg_data[y_column].round(1),
                textposition='outside',
                hovertemplate='%{x}<br>%{y:,.2f}<extra></extra>'
            )])
        else:
            fig = go.Figure(data=[go.Bar(
                y=agg_data[x_column],
                x=agg_data[y_column],
                orientation='h',
                marker_color='#8b5cf6',
                text=agg_data[y_column].round(1),
                textposition='outside',
                hovertemplate='%{y}<br>%{x:,.2f}<extra></extra>'
            )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        xaxis_title=x_column if orientation == 'v' else y_column,
        yaxis_title=y_column if orientation == 'v' else x_column
    )
    
    return fig


def create_scatter_plot(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    color_column: str = None,
    size_column: str = None,
    trendline: bool = True,
    title: str = None
) -> go.Figure:
    """Create an interactive scatter plot with optional trendline"""
    
    title = title or f"{y_column} vs {x_column}"
    
    fig = px.scatter(
        data,
        x=x_column,
        y=y_column,
        color=color_column,
        size=size_column,
        trendline="ols" if trendline else None,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_traces(
        marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')),
        hovertemplate=f'{x_column}: %{{x}}<br>{y_column}: %{{y}}<extra></extra>'
    )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        xaxis_title=x_column,
        yaxis_title=y_column
    )
    
    return fig


def create_area_chart(
    data: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    stacked: bool = True,
    title: str = None
) -> go.Figure:
    """Create an area chart for trend visualization"""
    
    title = title or f"{'Stacked ' if stacked else ''}Area Chart"
    
    colors = px.colors.qualitative.Set2
    
    fig = go.Figure()
    
    for i, col in enumerate(y_columns):
        if col in data.columns:
            fig.add_trace(go.Scatter(
                x=data[x_column] if x_column in data.columns else data.index,
                y=data[col],
                name=col,
                mode='lines',
                fill='tonexty' if stacked and i > 0 else 'tozeroy',
                line=dict(color=colors[i % len(colors)], width=2),
                stackgroup='one' if stacked else None,
                hovertemplate='%{x}<br>%{y:,.2f}<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        xaxis_title=x_column,
        yaxis_title="Value",
        hovermode='x unified'
    )
    
    return fig


def create_funnel_chart(
    data: pd.DataFrame,
    stage_column: str,
    value_column: str,
    title: str = "Funnel Analysis"
) -> go.Figure:
    """Create a funnel chart for conversion analysis"""
    
    agg_data = data.groupby(stage_column)[value_column].sum().reset_index()
    agg_data = agg_data.sort_values(value_column, ascending=False)
    
    fig = go.Figure(go.Funnel(
        y=agg_data[stage_column],
        x=agg_data[value_column],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=px.colors.sequential.Purp)
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white"
    )
    
    return fig


def create_treemap(
    data: pd.DataFrame,
    path_columns: List[str],
    values_column: str,
    title: str = "Hierarchical View"
) -> go.Figure:
    """Create a treemap for hierarchical data"""
    
    fig = px.treemap(
        data,
        path=path_columns,
        values=values_column,
        color=values_column,
        color_continuous_scale='Purp'
    )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white"
    )
    
    return fig


def create_sunburst(
    data: pd.DataFrame,
    path_columns: List[str],
    values_column: str,
    title: str = "Sunburst Chart"
) -> go.Figure:
    """Create a sunburst chart for hierarchical data"""
    
    fig = px.sunburst(
        data,
        path=path_columns,
        values=values_column,
        color=values_column,
        color_continuous_scale='Purp'
    )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white"
    )
    
    return fig


def create_waterfall_chart(
    categories: List[str],
    values: List[float],
    title: str = "Waterfall Analysis"
) -> go.Figure:
    """Create a waterfall chart showing incremental changes"""
    
    # Calculate measures (relative or total)
    measures = ['relative'] * (len(values) - 1) + ['total']
    
    fig = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        measure=measures,
        x=categories,
        y=values,
        connector=dict(line=dict(color="#8b5cf6")),
        increasing=dict(marker=dict(color="#22c55e")),
        decreasing=dict(marker=dict(color="#ef4444")),
        totals=dict(marker=dict(color="#8b5cf6")),
        textposition="outside"
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        showlegend=False
    )
    
    return fig


def create_radar_chart(
    categories: List[str],
    values: List[float],
    name: str = "Values",
    title: str = "Radar Chart"
) -> go.Figure:
    """Create a radar/spider chart for multi-dimensional comparison"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=name,
        line_color='#8b5cf6',
        fillcolor='rgba(139, 92, 246, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values) * 1.1])
        ),
        showlegend=True,
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white"
    )
    
    return fig


def create_bullet_chart(
    actual: float,
    target: float,
    ranges: List[float],
    title: str = "Performance",
    subtitle: str = ""
) -> go.Figure:
    """Create a bullet chart for KPI tracking"""
    
    fig = go.Figure()
    
    # Background ranges
    colors = ['#e5e7eb', '#d1d5db', '#9ca3af']
    for i, r in enumerate(sorted(ranges, reverse=True)):
        fig.add_trace(go.Bar(
            y=[subtitle],
            x=[r],
            orientation='h',
            marker_color=colors[i % len(colors)],
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Actual value bar
    fig.add_trace(go.Bar(
        y=[subtitle],
        x=[actual],
        orientation='h',
        marker_color='#8b5cf6',
        width=0.3,
        name='Actual',
        hovertemplate=f'Actual: {actual}<extra></extra>'
    ))
    
    # Target line
    fig.add_vline(x=target, line_dash="dash", line_color="#ef4444", annotation_text=f"Target: {target}")
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        barmode='overlay',
        showlegend=False,
        height=200
    )
    
    return fig


def create_candlestick_chart(
    data: pd.DataFrame,
    date_column: str,
    open_col: str,
    high_col: str,
    low_col: str,
    close_col: str,
    title: str = "Candlestick Chart"
) -> go.Figure:
    """Create a candlestick chart for financial data"""
    
    fig = go.Figure(data=[go.Candlestick(
        x=data[date_column],
        open=data[open_col],
        high=data[high_col],
        low=data[low_col],
        close=data[close_col],
        increasing_line_color='#22c55e',
        decreasing_line_color='#ef4444'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        template="plotly_white",
        xaxis_rangeslider_visible=False
    )
    
    return fig


def create_kpi_card_chart(
    value: float,
    previous_value: float = None,
    title: str = "KPI",
    format_str: str = "{:,.0f}",
    prefix: str = "",
    suffix: str = ""
) -> go.Figure:
    """Create a KPI card with trend indicator"""
    
    display_value = f"{prefix}{format_str.format(value)}{suffix}"
    
    delta = None
    delta_relative = None
    if previous_value is not None and previous_value != 0:
        delta = value - previous_value
        delta_relative = (delta / previous_value) * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=value,
        number={'prefix': prefix, 'suffix': suffix, 'font': {'size': 40, 'color': '#8b5cf6'}},
        delta={'reference': previous_value, 'relative': True, 'valueformat': '.1%'} if previous_value else None,
        title={'text': title, 'font': {'size': 16, 'color': '#64748b'}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        template="plotly_white",
        height=150,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig


def create_sparkline(
    values: List[float],
    color: str = "#8b5cf6",
    height: int = 50
) -> go.Figure:
    """Create a minimal sparkline chart"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=values,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba{tuple(list(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}',
        hoverinfo='y'
    ))
    
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        template="plotly_white"
    )
    
    return fig


def create_dashboard_layout(
    charts: List[Dict[str, Any]],
    title: str = "Dashboard"
) -> go.Figure:
    """Create a dashboard layout with multiple charts"""
    
    n_charts = len(charts)
    cols = min(2, n_charts)
    rows = (n_charts + cols - 1) // cols
    
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[c.get('title', '') for c in charts],
        specs=[[{"type": c.get('type', 'xy')} for c in charts[i*cols:(i+1)*cols]] + 
               [{"type": "xy"}] * (cols - len(charts[i*cols:(i+1)*cols])) 
               for i in range(rows)]
    )
    
    for i, chart in enumerate(charts):
        row = i // cols + 1
        col = i % cols + 1
        
        if 'trace' in chart:
            fig.add_trace(chart['trace'], row=row, col=col)
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=24)),
        template="plotly_white",
        height=400 * rows,
        showlegend=True
    )
    
    return fig


def auto_generate_charts(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """Automatically generate appropriate charts based on data"""
    
    charts = []
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = [col for col in data.columns if pd.api.types.is_datetime64_any_dtype(data[col])]
    
    # Generate distribution chart for first numeric column
    if numeric_cols:
        charts.append({
            "type": "distribution",
            "chart": create_distribution_chart(data, numeric_cols[0], "histogram"),
            "title": f"Distribution of {numeric_cols[0]}",
            "description": "Histogram showing value distribution"
        })
    
    # Generate time series if date column exists
    if date_cols and numeric_cols:
        charts.append({
            "type": "timeline",
            "chart": create_timeline_chart(data, date_cols[0], numeric_cols[:3]),
            "title": "Trend Over Time",
            "description": "Line chart showing trends"
        })
    
    # Generate correlation heatmap if multiple numeric columns
    if len(numeric_cols) >= 2:
        charts.append({
            "type": "heatmap",
            "chart": create_correlation_heatmap(data),
            "title": "Correlation Matrix",
            "description": "Heatmap showing variable correlations"
        })
    
    # Generate pie chart for categorical column
    if categorical_cols:
        charts.append({
            "type": "pie",
            "chart": create_pie_chart(data, categorical_cols[0]),
            "title": f"Distribution of {categorical_cols[0]}",
            "description": "Pie chart showing category distribution"
        })
    
    # Generate scatter plot for two numeric columns
    if len(numeric_cols) >= 2:
        charts.append({
            "type": "scatter",
            "chart": create_scatter_plot(data, numeric_cols[0], numeric_cols[1]),
            "title": f"{numeric_cols[1]} vs {numeric_cols[0]}",
            "description": "Scatter plot with trendline"
        })
    
    # Generate bar chart if categorical and numeric columns exist
    if categorical_cols and numeric_cols:
        charts.append({
            "type": "bar",
            "chart": create_bar_chart(data, categorical_cols[0], numeric_cols[0]),
            "title": f"{numeric_cols[0]} by {categorical_cols[0]}",
            "description": "Bar chart comparison"
        })
    
    return charts
