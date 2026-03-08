"""
TechXcel - Smart Excel Analytics with AI
"""

import streamlit as st
import pandas as pd
import numpy as np
from data_processor import SpreadsheetProcessor
from ai_engine import ai_engine
from visualization import (
    create_timeline_chart,
    create_correlation_heatmap,
    create_scenario_comparison_chart,
    create_what_if_slider_chart,
    create_impact_gauge_chart,
    create_relationship_network
)

# Page config
st.set_page_config(
    page_title="TechXcel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400&display=swap');
    
    :root {
        --primary: #8b5cf6;
        --primary-glow: rgba(139, 92, 246, 0.4);
        --accent: #06b6d4;
        --success: #10b981;
        --danger: #f43f5e;
        --bg-primary: #09090b;
        --bg-secondary: #18181b;
        --bg-tertiary: #27272a;
        --text-primary: #fafafa;
        --text-secondary: #a1a1aa;
        --border: #3f3f46;
    }
    
    .stApp {
        background: var(--bg-primary);
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Hero */
    .hero {
        text-align: center;
        padding: 3rem 2rem;
        background: radial-gradient(ellipse at top, rgba(139,92,246,0.15) 0%, transparent 50%);
        margin-bottom: 2rem;
    }
    
    .hero h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.03em;
    }
    
    .hero p {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Cards */
    .card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.2s;
    }
    
    .card:hover {
        border-color: var(--primary);
        box-shadow: 0 0 30px var(--primary-glow);
    }
    
    .card-header {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }
    
    /* Metrics */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .metric {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    
    /* Chatbot */
    .chat-container {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 20px;
        overflow: hidden;
        height: 500px;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .chat-header-dot {
        width: 10px;
        height: 10px;
        background: #22c55e;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .chat-header-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: white;
        font-size: 0.9rem;
    }
    
    .chat-messages {
        flex: 1;
        padding: 1.5rem;
        overflow-y: auto;
    }
    
    .chat-message {
        margin-bottom: 1rem;
        display: flex;
        gap: 0.75rem;
    }
    
    .chat-message.user {
        flex-direction: row-reverse;
    }
    
    .chat-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        flex-shrink: 0;
    }
    
    .chat-avatar.ai {
        background: linear-gradient(135deg, var(--primary), var(--accent));
    }
    
    .chat-avatar.user {
        background: var(--bg-tertiary);
    }
    
    .chat-bubble {
        max-width: 80%;
        padding: 0.875rem 1.25rem;
        border-radius: 16px;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .chat-bubble.ai {
        background: var(--bg-tertiary);
        color: var(--text-primary);
        border-bottom-left-radius: 4px;
    }
    
    .chat-bubble.user {
        background: linear-gradient(135deg, var(--primary), #7c3aed);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .chat-input-area {
        padding: 1rem;
        border-top: 1px solid var(--border);
        background: var(--bg-primary);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    
    .sidebar-brand {
        text-align: center;
        padding: 2rem 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    .sidebar-brand-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-brand-text {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .sidebar-section {
        padding: 1.5rem 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    .sidebar-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 0.5rem;
        gap: 0.25rem;
        border: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), #7c3aed);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 4px 20px var(--primary-glow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px var(--primary-glow);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    /* Data display */
    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border);
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    .stat-value {
        color: var(--text-primary);
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stat-positive { color: var(--success); }
    .stat-negative { color: var(--danger); }
    
    /* Section */
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Quick actions */
    .quick-action {
        background: var(--bg-tertiary);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .quick-action:hover {
        border-color: var(--primary);
        color: var(--text-primary);
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 1.5rem 0;
    }
    
    /* Feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-item {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s;
    }
    
    .feature-item:hover {
        border-color: var(--primary);
        transform: translateY(-4px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'processor' not in st.session_state:
    st.session_state.processor = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'relationships' not in st.session_state:
    st.session_state.relationships = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analysis' not in st.session_state:
    st.session_state.analysis = None


def process_chat(user_input: str) -> str:
    """Process user chat input and return AI response"""
    if st.session_state.processor is None:
        return "Please upload data first to start analyzing."
    
    processor = st.session_state.processor
    summary = st.session_state.summary
    relationships = st.session_state.relationships
    
    # Parse the question for what-if scenarios
    user_lower = user_input.lower()
    
    # Check for what-if patterns
    if any(kw in user_lower for kw in ['what if', 'what would', 'if we', 'suppose', 'imagine']):
        # Try to extract variable and values
        for col in summary['numeric_columns']:
            if col.lower().replace('_', ' ') in user_lower or col.lower() in user_lower:
                # Found a variable, run simulation
                import re
                numbers = re.findall(r'[\d,]+\.?\d*', user_input)
                numbers = [float(n.replace(',', '')) for n in numbers if n]
                
                if len(numbers) >= 2:
                    simulation = processor.simulate_what_if(col, numbers[0], numbers[1])
                elif len(numbers) == 1:
                    original = processor.df[col].mean()
                    simulation = processor.simulate_what_if(col, original, numbers[0])
                else:
                    original = processor.df[col].mean()
                    simulation = processor.simulate_what_if(col, original, original * 1.2)
                
                response = ai_engine.process_what_if_question(
                    user_input, summary, relationships, simulation
                )
                return response.get('ai_response', 'Unable to process simulation.')
        
        # No specific variable found
        response = ai_engine.process_what_if_question(
            user_input, summary, relationships, None
        )
        return response.get('ai_response', 'Please specify which variable you want to change.')
    
    # Check for optimization queries
    elif any(kw in user_lower for kw in ['optimize', 'best', 'optimal', 'maximize', 'minimize', 'improve']):
        for col in summary['numeric_columns']:
            if col.lower().replace('_', ' ') in user_lower or col.lower() in user_lower:
                goal = "Maximize" if "maximize" in user_lower or "increase" in user_lower else "Minimize" if "minimize" in user_lower or "reduce" in user_lower else "Maximize"
                result = ai_engine.get_optimal_value_suggestion(col, goal, summary, relationships)
                return result.get('suggestions', 'Unable to generate recommendations.')
        return "Please specify which metric you want to optimize."
    
    # General analysis
    else:
        if st.session_state.analysis is None:
            st.session_state.analysis = ai_engine.analyze_data(summary, relationships)
        return st.session_state.analysis


def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">⚡</div>
            <div class="sidebar-brand-text">TechXcel</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">📁 Upload Your Excel</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Drop Excel file here", type=['xlsx', 'xls'], label_visibility="collapsed", help="Supports .xlsx and .xls files")
        
        if uploaded_file:
            try:
                content = uploaded_file.read()
                processor = SpreadsheetProcessor()
                processor.load_excel(content)
                st.session_state.processor = processor
                st.session_state.summary = processor.get_summary()
                st.session_state.relationships = processor.detect_relationships()
                st.session_state.analysis = None
                st.session_state.chat_history = []
                st.success("✓ Data loaded")
            except Exception as e:
                st.error(f"Error: {e}")
        
        if st.button("🚀 Try Demo Data", use_container_width=True, help="Load sample sales data to explore features"):
            demo_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                'Marketing_Spend': [1000, 1200, 2000, 1800, 2500, 2200, 2800, 3000, 2700, 3200, 3500, 4000],
                'Sales': [5000, 5500, 5800, 6200, 7500, 7000, 8200, 8800, 8000, 9500, 10000, 11500],
                'Employees': [10, 10, 12, 12, 15, 15, 18, 18, 20, 20, 22, 25],
                'Revenue': [50000, 55000, 58000, 62000, 75000, 70000, 82000, 88000, 80000, 95000, 100000, 115000]
            })
            processor = SpreadsheetProcessor()
            processor.load_dataframe(demo_data)
            st.session_state.processor = processor
            st.session_state.summary = processor.get_summary()
            st.session_state.relationships = processor.detect_relationships()
            st.session_state.analysis = None
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stats
        if st.session_state.processor is not None:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-label">Quick Stats</div>', unsafe_allow_html=True)
            s = st.session_state.summary
            st.markdown(f"""
            <div class="stat-row"><span class="stat-label">Rows</span><span class="stat-value">{s['rows']}</span></div>
            <div class="stat-row"><span class="stat-label">Columns</span><span class="stat-value">{s['columns']}</span></div>
            <div class="stat-row"><span class="stat-label">Relationships</span><span class="stat-value">{len(st.session_state.relationships.get('correlations', {}))}</span></div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    if st.session_state.processor is not None:
        # Minimal header
        st.markdown("""
        <div class="hero">
            <h1>TechXcel</h1>
            <p>Your AI-powered Excel analyst — ask anything!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main layout: Chat + Analysis
        chat_col, analysis_col = st.columns([1, 1.5])
        
        with chat_col:
            # Chatbot
            st.markdown("""
            <div class="card">
                <div class="chat-header">
                    <div class="chat-header-dot"></div>
                    <div class="chat-header-title">AI Assistant</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Chat messages container
            chat_container = st.container()
            
            with chat_container:
                # Display chat history
                if not st.session_state.chat_history:
                    st.markdown("""
                    <div style="padding: 2rem; text-align: center; color: #a1a1aa;">
                        <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">👋</div>
                        <div style="font-size: 1rem; font-weight: 500; color: #fafafa;">Hi! I'm your Excel assistant</div>
                        <div style="font-size: 0.85rem; margin-top: 0.5rem; color: #71717a;">Ask questions like:</div>
                        <div style="font-size: 0.8rem; margin-top: 0.25rem; color: #8b5cf6;">"What if we increase marketing by 20%?"</div>
                        <div style="font-size: 0.8rem; margin-top: 0.25rem; color: #8b5cf6;">"Analyze my sales trends"</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    for msg in st.session_state.chat_history[-6:]:
                        if msg['role'] == 'user':
                            st.markdown(f"""
                            <div class="chat-message user">
                                <div class="chat-avatar user">👤</div>
                                <div class="chat-bubble user">{msg['content']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="chat-message">
                                <div class="chat-avatar ai">⚡</div>
                                <div class="chat-bubble ai">{msg['content'][:500]}{'...' if len(msg['content']) > 500 else ''}</div>
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chat input
            user_input = st.chat_input("✨ Type your question here...")
            
            if user_input:
                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                with st.spinner("🧠 Analyzing..."):
                    response = process_chat(user_input)
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                st.rerun()
            
            # Quick actions
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-label">⚡ Quick Questions</div>', unsafe_allow_html=True)
            
            qa_cols = st.columns(2)
            quick_questions = [
                "📊 Analyze trends",
                "💰 Double marketing?",
                "📈 Boost revenue",
                "🔗 Find connections"
            ]
            
            for i, q in enumerate(quick_questions):
                with qa_cols[i % 2]:
                    if st.button(q, use_container_width=True, key=f"qa_{i}"):
                        # Map friendly labels to actual queries
                        query_map = {
                            "📊 Analyze trends": "Analyze my data and show key trends",
                            "💰 Double marketing?": "What if we doubled our marketing spend?",
                            "📈 Boost revenue": "How can we optimize and increase revenue?",
                            "🔗 Find connections": "Show me the relationships between variables"
                        }
                        actual_query = query_map.get(q, q)
                        st.session_state.chat_history.append({'role': 'user', 'content': actual_query})
                        with st.spinner("🧠 Analyzing..."):
                            response = process_chat(actual_query)
                        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                        st.rerun()
        
        with analysis_col:
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Timeline", "🎯 Simulate"])
            
            with tab1:
                # Metrics
                summary = st.session_state.summary
                cols = st.columns(4)
                metrics = [
                    ("📋", summary['rows'], "Rows"),
                    ("📊", summary['columns'], "Cols"),
                    ("🔢", len(summary['numeric_columns']), "Numeric"),
                    ("🔗", len(st.session_state.relationships.get('correlations', {})), "Links")
                ]
                for i, (icon, val, label) in enumerate(metrics):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="metric">
                            <div class="metric-value">{val}</div>
                            <div class="metric-label">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Data preview
                st.markdown('<div class="section-title">📋 Data</div>', unsafe_allow_html=True)
                st.dataframe(st.session_state.processor.df, use_container_width=True, height=200, hide_index=True)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Correlation heatmap
                st.markdown('<div class="section-title">🔥 Correlations</div>', unsafe_allow_html=True)
                fig = create_correlation_heatmap(st.session_state.processor.df)
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#a1a1aa',
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Timeline explorer
                st.markdown('<div class="section-title">📈 Timeline</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    input_var = st.selectbox("Variable", options=summary['numeric_columns'], key="tl_in")
                with col2:
                    steps = st.slider("Points", 5, 30, 15)
                
                current_mean = st.session_state.processor.df[input_var].mean()
                current_std = st.session_state.processor.df[input_var].std()
                
                if st.button("Generate", use_container_width=True, key="gen_timeline"):
                    min_v = max(0, current_mean - 2*current_std)
                    max_v = current_mean + 2*current_std
                    sim_df = st.session_state.processor.get_simulation_data(input_var, (min_v, max_v), steps)
                    
                    if not sim_df.empty and len(sim_df.columns) > 1:
                        output_cols = [c for c in sim_df.columns if c.startswith('predicted_')]
                        if output_cols:
                            fig = create_what_if_slider_chart(sim_df, 'input_value', output_cols, f"Impact of {input_var}")
                            fig.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font_color='#a1a1aa'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Historical chart
                time_cols = summary.get('date_columns', []) + summary.get('categorical_columns', [])
                time_col = time_cols[0] if time_cols else 'index'
                
                value_cols = st.multiselect("Plot", summary['numeric_columns'], default=summary['numeric_columns'][:2], key="hist_cols")
                
                if value_cols:
                    plot_df = st.session_state.processor.df.reset_index() if time_col == 'index' else st.session_state.processor.df
                    fig = create_timeline_chart(plot_df, time_col, value_cols, "Trends")
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color='#a1a1aa',
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Manual simulation
                st.markdown('<div class="section-title">🎯 Simulate</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    var = st.selectbox("Change", summary['numeric_columns'], key="sim_var")
                
                current = st.session_state.processor.df[var].mean()
                
                with col2:
                    orig = st.number_input("From", value=float(current), key="sim_from")
                
                with col3:
                    new = st.number_input("To", value=float(current * 1.3), key="sim_to")
                
                if st.button("Run Simulation", use_container_width=True, type="primary"):
                    simulation = st.session_state.processor.simulate_what_if(var, orig, new)
                    
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    
                    # Results
                    result_cols = st.columns(2)
                    
                    with result_cols[0]:
                        change_pct = simulation.get('change_percent', 0)
                        st.metric(var, f"{new:,.0f}", f"{change_pct:+.1f}%")
                    
                    with result_cols[1]:
                        for impact in simulation.get('impacts', [])[:1]:
                            st.metric(
                                impact['target_variable'],
                                f"{impact['predicted_value']:,.0f}",
                                f"{impact['percent_change']:+.1f}%"
                            )
                    
                    # Visualization
                    if simulation.get('impacts'):
                        fig = create_impact_gauge_chart(simulation['impacts'][0], "Impact")
                        fig.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font_color='#a1a1aa',
                            height=250
                        )
                        st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Landing page
        st.markdown("""
        <div class="hero">
            <h1>TechXcel</h1>
            <p>Turn your Excel data into insights in seconds</p>
        </div>
        
        <div class="feature-grid">
            <div class="feature-item">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Instant Analysis</div>
                <div class="feature-desc">Upload & get insights</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">💬</div>
                <div class="feature-title">Just Ask</div>
                <div class="feature-desc">Chat with your data</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🔮</div>
                <div class="feature-title">What-If</div>
                <div class="feature-desc">Explore possibilities</div>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Smart Tips</div>
                <div class="feature-desc">AI recommendations</div>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <div style="background: linear-gradient(135deg, #27272a, #18181b); border: 1px solid #3f3f46; border-radius: 16px; padding: 2rem; max-width: 500px; margin: 0 auto;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🚀</div>
                <div style="color: #fafafa; font-weight: 500; margin-bottom: 0.5rem;">Get Started in 2 Steps</div>
                <div style="color: #a1a1aa; font-size: 0.9rem;">1. Upload your Excel file (sidebar)</div>
                <div style="color: #a1a1aa; font-size: 0.9rem;">2. Ask any question!</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success("👈 **Start here:** Upload an Excel file or try **Demo Data**")


if __name__ == "__main__":
    main()
