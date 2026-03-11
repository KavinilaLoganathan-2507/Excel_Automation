"""
TechXcel - Smart Excel Analytics with AI
Enhanced with EDA, Dashboard, Reports, Email & Auto Charts
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_processor import SpreadsheetProcessor
from ai_engine import ai_engine
from eda_engine import EDAEngine
from report_generator import ReportGenerator, DashboardBuilder
from email_service import EmailService
from visualization import (
    create_timeline_chart,
    create_correlation_heatmap,
    create_scenario_comparison_chart,
    create_what_if_slider_chart,
    create_impact_gauge_chart,
    create_relationship_network,
    create_distribution_chart,
    create_pie_chart,
    create_bar_chart,
    create_scatter_plot,
    create_area_chart,
    create_radar_chart,
    create_kpi_card_chart,
    auto_generate_charts
)

# Page config
st.set_page_config(
    page_title="TechXcel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def get_theme_css(theme):
    """Generate CSS based on selected theme"""
    if theme == 'dark':
        colors = {
            'primary': '#8b5cf6',
            'primary_light': '#a78bfa',
            'primary_glow': 'rgba(139, 92, 246, 0.2)',
            'accent': '#06b6d4',
            'accent_light': '#22d3ee',
            'success': '#22c55e',
            'success_light': 'rgba(34, 197, 94, 0.15)',
            'warning': '#f59e0b',
            'warning_light': 'rgba(245, 158, 11, 0.15)',
            'danger': '#ef4444',
            'danger_light': 'rgba(239, 68, 68, 0.15)',
            'bg_primary': '#0a0a0b',
            'bg_secondary': '#141416',
            'bg_tertiary': '#1e1e22',
            'bg_app': 'linear-gradient(180deg, #0a0a0b 0%, #141416 100%)',
            'text_primary': '#fafafa',
            'text_secondary': '#a1a1aa',
            'text_muted': '#71717a',
            'border': '#27272a',
            'border_light': '#1f1f23',
            'shadow_sm': '0 1px 2px rgba(0, 0, 0, 0.3)',
            'shadow_md': '0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3)',
            'shadow_lg': '0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3)',
            'shadow_xl': '0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3)',
            'shadow_glow': '0 0 40px rgba(139, 92, 246, 0.3)',
            'hero_bg': 'radial-gradient(ellipse at top, rgba(139, 92, 246, 0.15) 0%, transparent 50%)',
            'card_hover_border': '#8b5cf6',
            'chat_bubble_user': 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
            'msg_success_text': '#86efac',
            'msg_warning_text': '#fcd34d',
            'msg_error_text': '#fca5a5',
            'chart_bg': 'rgba(20, 20, 22, 0.95)',
            'chart_plot_bg': 'rgba(30, 30, 34, 0.8)',
            'chart_font': '#a1a1aa',
        }
    else:
        colors = {
            'primary': '#6366f1',
            'primary_light': '#818cf8',
            'primary_glow': 'rgba(99, 102, 241, 0.15)',
            'accent': '#0ea5e9',
            'accent_light': '#38bdf8',
            'success': '#10b981',
            'success_light': '#d1fae5',
            'warning': '#f59e0b',
            'warning_light': '#fef3c7',
            'danger': '#ef4444',
            'danger_light': '#fee2e2',
            'bg_primary': '#ffffff',
            'bg_secondary': '#f8fafc',
            'bg_tertiary': '#f1f5f9',
            'bg_app': 'linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)',
            'text_primary': '#0f172a',
            'text_secondary': '#64748b',
            'text_muted': '#94a3b8',
            'border': '#e2e8f0',
            'border_light': '#f1f5f9',
            'shadow_sm': '0 1px 2px rgba(0, 0, 0, 0.05)',
            'shadow_md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            'shadow_lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            'shadow_xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
            'shadow_glow': '0 0 40px rgba(99, 102, 241, 0.15)',
            'hero_bg': 'linear-gradient(180deg, rgba(99, 102, 241, 0.05) 0%, transparent 100%)',
            'card_hover_border': '#818cf8',
            'chat_bubble_user': 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            'msg_success_text': '#065f46',
            'msg_warning_text': '#92400e',
            'msg_error_text': '#991b1b',
            'chart_bg': 'white',
            'chart_plot_bg': '#f8fafc',
            'chart_font': '#334155',
        }
    
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {{
        --primary: {colors['primary']};
        --primary-light: {colors['primary_light']};
        --primary-glow: {colors['primary_glow']};
        --accent: {colors['accent']};
        --accent-light: {colors['accent_light']};
        --success: {colors['success']};
        --success-light: {colors['success_light']};
        --warning: {colors['warning']};
        --warning-light: {colors['warning_light']};
        --danger: {colors['danger']};
        --danger-light: {colors['danger_light']};
        --bg-primary: {colors['bg_primary']};
        --bg-secondary: {colors['bg_secondary']};
        --bg-tertiary: {colors['bg_tertiary']};
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
        --text-muted: {colors['text_muted']};
        --border: {colors['border']};
        --border-light: {colors['border_light']};
        --shadow-sm: {colors['shadow_sm']};
        --shadow-md: {colors['shadow_md']};
        --shadow-lg: {colors['shadow_lg']};
        --shadow-xl: {colors['shadow_xl']};
        --shadow-glow: {colors['shadow_glow']};
    }}
    
    .stApp {{
        background: {colors['bg_app']};
    }}
    
    #MainMenu, footer {{visibility: hidden;}}
    
    /* Keep sidebar toggle visible */
    [data-testid="collapsedControl"] {{
        visibility: visible !important;
        display: flex !important;
    }}
    
    [data-testid="stSidebarCollapsedControl"] {{
        visibility: visible !important;
        color: var(--text-primary) !important;
    }}
    
    button[kind="header"] {{
        visibility: visible !important;
    }}
    
    /* Hero */
    .hero {{
        text-align: center;
        padding: 4rem 2rem 3rem;
        background: {colors['hero_bg']};
        margin-bottom: 2rem;
        position: relative;
    }}
    
    .hero::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 600px;
        height: 300px;
        background: radial-gradient(ellipse, {colors['primary_glow']} 0%, transparent 70%);
        pointer-events: none;
    }}
    
    .hero h1 {{
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {colors['primary']} 0%, #8b5cf6 50%, {colors['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.03em;
        text-shadow: 0 4px 30px {colors['primary_glow']};
    }}
    
    .hero p {{
        color: var(--text-secondary);
        font-size: 1.125rem;
        margin-top: 0.75rem;
        font-weight: 400;
    }}
    
    /* Premium Cards */
    .card {{
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.75rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
    }}
    
    .card:hover {{
        border-color: {colors['card_hover_border']};
        box-shadow: var(--shadow-glow);
        transform: translateY(-2px);
    }}
    
    .card-header {{
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }}
    
    /* Premium Metrics */
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.25rem;
        margin-bottom: 2rem;
    }}
    
    .metric {{
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }}
    
    .metric::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        opacity: 0;
        transition: opacity 0.3s;
    }}
    
    .metric:hover {{
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-light);
    }}
    
    .metric:hover::before {{
        opacity: 1;
    }}
    
    .metric-value {{
        font-family: 'Inter', sans-serif;
        font-size: 2.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .metric-label {{
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.5rem;
        font-weight: 600;
    }}
    
    /* Premium Chatbot */
    .chat-container {{
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 24px;
        overflow: hidden;
        height: 500px;
        display: flex;
        flex-direction: column;
        box-shadow: var(--shadow-lg);
    }}
    
    .chat-header {{
        background: linear-gradient(135deg, {colors['primary']} 0%, #8b5cf6 50%, {colors['accent']} 100%);
        padding: 1.25rem 1.75rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}
    
    .chat-header-dot {{
        width: 10px;
        height: 10px;
        background: #22c55e;
        border-radius: 50%;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.7; transform: scale(1.1); }}
    }}
    
    .chat-header-title {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: white;
        font-size: 1rem;
        letter-spacing: -0.01em;
    }}
    
    .chat-messages {{
        flex: 1;
        padding: 1.5rem;
        overflow-y: auto;
        background: var(--bg-secondary);
    }}
    
    .chat-message {{
        margin-bottom: 1rem;
        display: flex;
        gap: 0.75rem;
    }}
    
    .chat-message.user {{
        flex-direction: row-reverse;
    }}
    
    .chat-avatar {{
        width: 36px;
        height: 36px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        flex-shrink: 0;
        box-shadow: var(--shadow-sm);
    }}
    
    .chat-avatar.ai {{
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white;
    }}
    
    .chat-avatar.user {{
        background: var(--bg-tertiary);
        border: 1px solid var(--border);
    }}
    
    .chat-bubble {{
        max-width: 80%;
        padding: 1rem 1.25rem;
        border-radius: 18px;
        font-size: 0.925rem;
        line-height: 1.6;
        box-shadow: var(--shadow-sm);
    }}
    
    .chat-bubble.ai {{
        background: var(--bg-primary);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-bottom-left-radius: 6px;
    }}
    
    .chat-bubble.user {{
        background: {colors['chat_bubble_user']};
        color: white;
        border-bottom-right-radius: 6px;
    }}
    
    .chat-input-area {{
        padding: 1rem 1.25rem;
        border-top: 1px solid var(--border);
        background: var(--bg-primary);
    }}
    
    /* Premium Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--bg-primary) !important;
        border-right: 1px solid var(--border);
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background: var(--bg-primary) !important;
    }}
    
    /* Sidebar toggle button - always visible */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    [data-testid="baseButton-header"],
    [data-testid="stSidebarNavCollapseIcon"],
    .st-emotion-cache-1dp5vir {{
        visibility: visible !important;
        display: block !important;
    }}
    
    /* Collapsed sidebar expand button */
    [data-testid="collapsedControl"] {{
        background: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-md) !important;
    }}
    
    [data-testid="collapsedControl"]:hover {{
        background: var(--bg-secondary) !important;
        border-color: var(--primary) !important;
    }}
    
    .sidebar-brand {{
        text-align: center;
        padding: 2rem 1.5rem;
        border-bottom: 1px solid var(--border);
        background: linear-gradient(180deg, {colors['primary_glow']} 0%, transparent 100%);
    }}
    
    .sidebar-brand-icon {{
        font-size: 2.75rem;
        margin-bottom: 0.75rem;
    }}
    
    .sidebar-brand-text {{
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .sidebar-section {{
        padding: 1.5rem 1.25rem;
        border-bottom: 1px solid var(--border);
    }}
    
    .sidebar-label {{
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.75rem;
    }}
    
    /* Theme Toggle Button */
    .theme-toggle {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border);
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s;
        margin: 1rem;
        font-size: 0.875rem;
        color: var(--text-secondary);
    }}
    
    .theme-toggle:hover {{
        background: var(--primary-glow);
        border-color: var(--primary);
        color: var(--primary);
    }}
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 0.5rem;
        gap: 0.25rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        color: var(--text-secondary);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.2s;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: var(--bg-tertiary);
        color: var(--text-primary);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, var(--primary), #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 4px 15px {colors['primary_glow']};
    }}
    
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{
        display: none;
    }}
    
    /* Premium Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary) 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.75rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px {colors['primary_glow']};
        letter-spacing: -0.01em;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px {colors['primary_glow']};
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Premium Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background: var(--bg-primary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-glow) !important;
    }}
    
    /* Data display */
    .stat-row {{
        display: flex;
        justify-content: space-between;
        padding: 0.875rem 0;
        border-bottom: 1px solid var(--border-light);
        transition: background 0.2s;
    }}
    
    .stat-row:hover {{
        background: var(--bg-secondary);
        margin: 0 -0.5rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        border-radius: 8px;
    }}
    
    .stat-label {{
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
    }}
    
    .stat-value {{
        color: var(--text-primary);
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }}
    
    .stat-positive {{ color: var(--success); }}
    .stat-negative {{ color: var(--danger); }}
    
    /* Section */
    .section-title {{
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: -0.02em;
    }}
    
    /* Quick actions */
    .quick-action {{
        background: var(--bg-primary);
        border: 2px solid var(--border);
        border-radius: 12px;
        padding: 0.875rem 1.25rem;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-secondary);
    }}
    
    .quick-action:hover {{
        border-color: var(--primary);
        color: var(--primary);
        background: var(--primary-glow);
    }}
    
    /* Divider */
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 1.75rem 0;
    }}
    
    /* Premium Feature Grid */
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2.5rem 0;
    }}
    
    .feature-item {{
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }}
    
    .feature-item::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        transform: scaleX(0);
        transition: transform 0.3s;
    }}
    
    .feature-item:hover {{
        transform: translateY(-8px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-light);
    }}
    
    .feature-item:hover::before {{
        transform: scaleX(1);
    }}
    
    .feature-icon {{
        font-size: 2.75rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px {colors['primary_glow']});
    }}
    
    .feature-title {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }}
    
    .feature-desc {{
        font-size: 0.825rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }}
    
    /* Premium Data Tables */
    .stDataFrame {{
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }}
    
    .stDataFrame table {{
        background: var(--bg-primary) !important;
    }}
    
    .stDataFrame th {{
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 1rem !important;
    }}
    
    .stDataFrame td {{
        color: var(--text-primary) !important;
        padding: 0.875rem 1rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.875rem !important;
        border-bottom: 1px solid var(--border-light) !important;
    }}
    
    .stDataFrame tr:hover td {{
        background: var(--bg-secondary) !important;
    }}
    
    /* Premium Download Buttons */
    .stDownloadButton > button {{
        background: var(--bg-primary) !important;
        color: var(--primary) !important;
        border: 2px solid var(--primary) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }}
    
    .stDownloadButton > button:hover {{
        background: var(--primary) !important;
        color: white !important;
    }}
    
    /* Premium Expanders */
    .streamlit-expanderHeader {{
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }}
    
    .streamlit-expanderContent {{
        background: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background: var(--bg-secondary);
        border: 2px dashed var(--border);
        border-radius: 16px;
        padding: 1rem;
        transition: all 0.3s;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: var(--primary);
        background: var(--primary-glow);
    }}
    
    /* Premium Progress Bar */
    .stProgress > div > div {{
        background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
        border-radius: 8px !important;
    }}
    
    /* Plotly Charts Premium Styling */
    .js-plotly-plot {{
        border-radius: 16px;
        overflow: hidden;
        box-shadow: var(--shadow-md);
    }}
    
    /* Success/Warning/Error Messages */
    .stSuccess {{
        background: var(--success-light) !important;
        border: 1px solid var(--success) !important;
        border-radius: 12px !important;
        color: {colors['msg_success_text']} !important;
    }}
    
    .stWarning {{
        background: var(--warning-light) !important;
        border: 1px solid var(--warning) !important;
        border-radius: 12px !important;
        color: {colors['msg_warning_text']} !important;
    }}
    
    .stError {{
        background: var(--danger-light) !important;
        border: 1px solid var(--danger) !important;
        border-radius: 12px !important;
        color: {colors['msg_error_text']} !important;
    }}
    
    /* Premium Selectbox */
    .stSelectbox [data-baseweb="select"] {{
        background: var(--bg-primary) !important;
    }}
    
    .stSelectbox [data-baseweb="select"] > div {{
        background: var(--bg-primary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
    }}
    
    /* Premium Labels */
    .stTextInput label,
    .stSelectbox label,
    .stNumberInput label,
    .stDateInput label {{
        color: var(--text-secondary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}
    
    /* Premium scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--bg-secondary);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, var(--primary), #8b5cf6);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--primary);
    }}
    
    /* Info/KPI Boxes - Light Theme Compatible */
    .info-box {{
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
    }}
    
    .kpi-box {{
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s;
    }}
    
    .kpi-box:hover {{
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }}
    
    .kpi-label {{
        font-size: 0.7rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
    }}
    
    .kpi-value {{
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }}
    
    /* Getting Started Box */
    .getting-started {{
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem;
        max-width: 500px;
        margin: 0 auto;
        box-shadow: 0 4px 15px {colors['primary_glow']};
    }}
    
    .getting-started-title {{
        color: var(--text-primary);
        font-weight: 700;
        margin-bottom: 0.75rem;
        font-size: 1.125rem;
    }}
    
    .getting-started-step {{
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }}
</style>
"""

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# Helper function for chart colors
def get_chart_colors():
    if st.session_state.theme == 'dark':
        return {
            'paper_bgcolor': 'rgba(20, 20, 22, 0.95)',
            'plot_bgcolor': 'rgba(30, 30, 34, 0.8)',
            'font_color': '#a1a1aa'
        }
    else:
        return {
            'paper_bgcolor': 'white',
            'plot_bgcolor': '#f8fafc',
            'font_color': '#334155'
        }

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
if 'eda_engine' not in st.session_state:
    st.session_state.eda_engine = None
if 'eda_results' not in st.session_state:
    st.session_state.eda_results = None
if 'auto_charts' not in st.session_state:
    st.session_state.auto_charts = None
if 'date_filter_start' not in st.session_state:
    st.session_state.date_filter_start = None
if 'date_filter_end' not in st.session_state:
    st.session_state.date_filter_end = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None


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
        
        # Theme Toggle
        col1, col2 = st.columns([3, 1])
        with col1:
            current_theme = "🌙 Dark" if st.session_state.theme == 'dark' else "☀️ Light"
            st.markdown(f"<div style='padding: 0.5rem 1rem; font-size: 0.8rem; color: var(--text-secondary);'>Theme: {current_theme}</div>", unsafe_allow_html=True)
        with col2:
            theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
            if st.button(theme_icon, key="theme_toggle", help="Switch theme"):
                st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
                st.rerun()
        
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
                    <div style="padding: 2rem; text-align: center;">
                        <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">👋</div>
                        <div style="font-size: 1rem; font-weight: 600; color: var(--text-primary);">Hi! I'm your Excel assistant</div>
                        <div style="font-size: 0.85rem; margin-top: 0.5rem; color: var(--text-secondary);">Ask questions like:</div>
                        <div style="font-size: 0.8rem; margin-top: 0.25rem; color: var(--primary); font-weight: 500;">"What if we increase marketing by 20%?"</div>
                        <div style="font-size: 0.8rem; margin-top: 0.25rem; color: var(--primary); font-weight: 500;">"Analyze my sales trends"</div>
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
            # Tabs for different views - ENHANCED
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Overview", "🔍 EDA", "📈 Charts", "🎯 Simulate", "📄 Reports", "📧 Email"])
            
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
                
                # Date Filter Section
                date_cols = summary.get('date_columns', [])
                if date_cols:
                    st.markdown('<div class="section-title">📅 Date Filter</div>', unsafe_allow_html=True)
                    date_col = st.selectbox("Select Date Column", date_cols, key="date_filter_col")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        start_date = st.date_input("Start Date", key="start_date")
                    with col2:
                        end_date = st.date_input("End Date", key="end_date")
                    
                    if st.button("Apply Date Filter", use_container_width=True):
                        try:
                            df = st.session_state.processor.df.copy()
                            df[date_col] = pd.to_datetime(df[date_col])
                            mask = (df[date_col] >= pd.to_datetime(start_date)) & (df[date_col] <= pd.to_datetime(end_date))
                            st.session_state.filtered_df = df[mask]
                            st.success(f"Filtered to {len(st.session_state.filtered_df)} rows")
                        except Exception as e:
                            st.error(f"Error filtering: {e}")
                    
                    if st.button("Clear Filter", use_container_width=True):
                        st.session_state.filtered_df = None
                        st.success("Filter cleared")
                    
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Data preview
                st.markdown('<div class="section-title">📋 Data</div>', unsafe_allow_html=True)
                display_df = st.session_state.filtered_df if st.session_state.filtered_df is not None else st.session_state.processor.df
                st.dataframe(display_df, use_container_width=True, height=200, hide_index=True)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Correlation heatmap
                st.markdown('<div class="section-title">🔥 Correlations</div>', unsafe_allow_html=True)
                fig = create_correlation_heatmap(st.session_state.processor.df)
                chart_colors = get_chart_colors()
                fig.update_layout(
                    paper_bgcolor=chart_colors['paper_bgcolor'],
                    plot_bgcolor=chart_colors['plot_bgcolor'],
                    font_color=chart_colors['font_color'],
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # EDA - Exploratory Data Analysis
                st.markdown('<div class="section-title">🔍 Exploratory Data Analysis</div>', unsafe_allow_html=True)
                
                if st.button("🚀 Run Full EDA Analysis", use_container_width=True, type="primary"):
                    with st.spinner("Analyzing your data..."):
                        eda = EDAEngine(st.session_state.processor.df)
                        st.session_state.eda_engine = eda
                        st.session_state.eda_results = eda.get_full_eda_report()
                    st.success("EDA Complete!")
                
                if st.session_state.eda_results:
                    eda_results = st.session_state.eda_results
                    
                    # Data Quality Score
                    quality = eda_results.get('data_quality', {})
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #8b5cf6, #06b6d4); padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 2.5rem; font-weight: bold; color: white;">{quality.get('overall_score', 0)}%</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Data Quality Score - Grade: {quality.get('grade', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Quality metrics
                    qcols = st.columns(3)
                    with qcols[0]:
                        st.metric("Completeness", f"{quality.get('completeness', 100)}%")
                    with qcols[1]:
                        st.metric("Uniqueness", f"{quality.get('uniqueness', 100)}%")
                    with qcols[2]:
                        st.metric("Consistency", f"{quality.get('consistency', 100)}%")
                    
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    
                    # Smart Insights
                    st.markdown('<div class="section-title">💡 Smart Insights</div>', unsafe_allow_html=True)
                    insights = st.session_state.eda_engine.get_smart_insights()
                    
                    for insight in insights[:5]:
                        insight_type = insight.get('type', 'info')
                        color_map = {'success': '#10b981', 'warning': '#f59e0b', 'danger': '#ef4444', 'info': '#6366f1'}
                        icon_map = {'success': '✅', 'warning': '⚠️', 'danger': '❌', 'info': 'ℹ️'}
                        
                        st.markdown(f"""
                        <div style="background: {color_map.get(insight_type, '#6366f1')}15; border-left: 4px solid {color_map.get(insight_type, '#6366f1')}; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <strong style="color: var(--text-primary);">{icon_map.get(insight_type, '📊')} {insight.get('title', '')}</strong><br>
                            <span style="color: var(--text-secondary);">{insight.get('message', '')}</span><br>
                            <span style="color: var(--primary); font-size: 0.85rem; font-weight: 500;">💡 {insight.get('suggestion', '')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    
                    # Distribution Analysis
                    st.markdown('<div class="section-title">📊 Distribution Analysis</div>', unsafe_allow_html=True)
                    numeric_cols = summary.get('numeric_columns', [])
                    if numeric_cols:
                        dist_col = st.selectbox("Select Column", numeric_cols, key="dist_col")
                        dist_type = st.radio("Chart Type", ["histogram", "box", "violin"], horizontal=True, key="dist_type")
                        
                        fig = create_distribution_chart(st.session_state.processor.df, dist_col, dist_type)
                        chart_colors = get_chart_colors()
                        fig.update_layout(
                            paper_bgcolor=chart_colors['paper_bgcolor'],
                            plot_bgcolor=chart_colors['plot_bgcolor'],
                            font_color=chart_colors['font_color'],
                            height=300
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Outlier Summary
                    st.markdown('<div class="section-title">🎯 Outlier Detection</div>', unsafe_allow_html=True)
                    outliers = eda_results.get('outliers', {})
                    if outliers and 'message' not in outliers:
                        outlier_df = pd.DataFrame([
                            {"Column": col, "Outliers": data['count'], "Percentage": f"{data['percentage']}%"}
                            for col, data in outliers.items()
                        ])
                        st.dataframe(outlier_df, use_container_width=True, hide_index=True)
            
            with tab3:
                # Auto Charts & Visualization
                st.markdown('<div class="section-title">📈 Auto-Generated Charts</div>', unsafe_allow_html=True)
                
                if st.button("🎨 Generate Smart Charts", use_container_width=True, type="primary"):
                    with st.spinner("Creating visualizations..."):
                        st.session_state.auto_charts = auto_generate_charts(st.session_state.processor.df)
                    st.success(f"Generated {len(st.session_state.auto_charts)} charts!")
                
                if st.session_state.auto_charts:
                    for chart_info in st.session_state.auto_charts:
                        st.markdown(f"**{chart_info.get('title', 'Chart')}**")
                        st.markdown(f"<span style='color: var(--text-secondary); font-size: 0.85rem;'>{chart_info.get('description', '')}</span>", unsafe_allow_html=True)
                        
                        fig = chart_info.get('chart')
                        if fig:
                            chart_colors = get_chart_colors()
                            fig.update_layout(
                                paper_bgcolor=chart_colors['paper_bgcolor'],
                                plot_bgcolor=chart_colors['plot_bgcolor'],
                                font_color=chart_colors['font_color'],
                                height=350
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Custom Chart Builder
                st.markdown('<div class="section-title">🔧 Custom Chart Builder</div>', unsafe_allow_html=True)
                
                chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Pie", "Area"], key="custom_chart_type")
                
                col1, col2 = st.columns(2)
                numeric_cols = summary.get('numeric_columns', [])
                categorical_cols = summary.get('categorical_columns', [])
                all_cols = list(st.session_state.processor.df.columns)
                
                with col1:
                    x_col = st.selectbox("X-Axis", all_cols, key="x_axis")
                with col2:
                    y_col = st.selectbox("Y-Axis", numeric_cols if numeric_cols else all_cols, key="y_axis")
                
                if st.button("Create Chart", use_container_width=True):
                    df = st.session_state.processor.df
                    
                    if chart_type == "Bar":
                        fig = create_bar_chart(df, x_col, y_col)
                    elif chart_type == "Line":
                        fig = create_timeline_chart(df, x_col, [y_col])
                    elif chart_type == "Scatter":
                        fig = create_scatter_plot(df, x_col, y_col)
                    elif chart_type == "Pie":
                        fig = create_pie_chart(df, x_col, y_col if y_col else None)
                    elif chart_type == "Area":
                        fig = create_area_chart(df, x_col, [y_col])
                    
                    chart_colors = get_chart_colors()
                    fig.update_layout(
                        paper_bgcolor=chart_colors['paper_bgcolor'],
                        plot_bgcolor=chart_colors['plot_bgcolor'],
                        font_color=chart_colors['font_color'],
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
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
                            chart_colors = get_chart_colors()
                            fig.update_layout(
                                paper_bgcolor=chart_colors['paper_bgcolor'],
                                plot_bgcolor=chart_colors['plot_bgcolor'],
                                font_color=chart_colors['font_color']
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
                    chart_colors = get_chart_colors()
                    fig.update_layout(
                        paper_bgcolor=chart_colors['paper_bgcolor'],
                        plot_bgcolor=chart_colors['plot_bgcolor'],
                        font_color=chart_colors['font_color'],
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                # Simulation (formerly tab3)
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
                        chart_colors = get_chart_colors()
                        fig.update_layout(
                            paper_bgcolor=chart_colors['paper_bgcolor'],
                            plot_bgcolor=chart_colors['plot_bgcolor'],
                            font_color=chart_colors['font_color'],
                            height=250
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Timeline Explorer
                st.markdown('<div class="section-title">📈 Timeline Explorer</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    input_var = st.selectbox("Variable", options=summary['numeric_columns'], key="tl_in")
                with col2:
                    steps = st.slider("Points", 5, 30, 15)
                
                current_mean = st.session_state.processor.df[input_var].mean()
                current_std = st.session_state.processor.df[input_var].std()
                
                if st.button("Generate Timeline", use_container_width=True):
                    min_v = max(0, current_mean - 2*current_std)
                    max_v = current_mean + 2*current_std
                    sim_df = st.session_state.processor.get_simulation_data(input_var, (min_v, max_v), steps)
                    
                    if not sim_df.empty and len(sim_df.columns) > 1:
                        output_cols = [c for c in sim_df.columns if c.startswith('predicted_')]
                        if output_cols:
                            fig = create_what_if_slider_chart(sim_df, 'input_value', output_cols, f"Impact of {input_var}")
                            chart_colors = get_chart_colors()
                            fig.update_layout(
                                paper_bgcolor=chart_colors['paper_bgcolor'],
                                plot_bgcolor=chart_colors['plot_bgcolor'],
                                font_color=chart_colors['font_color']
                            )
                            st.plotly_chart(fig, use_container_width=True)
            
            with tab5:
                # Reports Tab
                st.markdown('<div class="section-title">📄 Auto Report Generation</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: linear-gradient(135deg, var(--primary-glow), rgba(14, 165, 233, 0.08)); padding: 1.25rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid rgba(99, 102, 241, 0.2);">
                    <strong style="color: var(--text-primary);">Generate comprehensive reports in multiple formats!</strong><br>
                    <span style="color: var(--text-secondary);">Includes data summary, statistics, visualizations, and AI insights.</span>
                </div>
                """, unsafe_allow_html=True)
                
                report_format = st.selectbox("Report Format", ["HTML Report", "Excel Dashboard", "CSV Export", "Markdown"], key="report_format")
                
                include_charts = st.checkbox("Include Auto-Generated Charts", value=True, key="include_charts")
                include_eda = st.checkbox("Include EDA Analysis", value=True, key="include_eda")
                
                if st.button("📄 Generate Report", use_container_width=True, type="primary"):
                    with st.spinner("Generating report..."):
                        # Run EDA if not already done
                        if st.session_state.eda_results is None and include_eda:
                            eda = EDAEngine(st.session_state.processor.df)
                            st.session_state.eda_results = eda.get_full_eda_report()
                        
                        report_gen = ReportGenerator(
                            st.session_state.processor.df,
                            st.session_state.eda_results,
                            st.session_state.analysis
                        )
                        
                        if report_format == "HTML Report":
                            content = report_gen.generate_html_report()
                            st.download_button(
                                "📥 Download HTML Report",
                                content,
                                file_name=f"techxcel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                                mime="text/html",
                                use_container_width=True
                            )
                            st.success("Report generated! Click to download.")
                            
                            # Preview
                            with st.expander("Preview Report"):
                                st.components.v1.html(content, height=600, scrolling=True)
                        
                        elif report_format == "Excel Dashboard":
                            content = report_gen.generate_excel_dashboard()
                            if content:
                                st.download_button(
                                    "📥 Download Excel Dashboard",
                                    content,
                                    file_name=f"techxcel_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                                st.success("Excel dashboard generated!")
                            else:
                                st.warning("Excel generation requires openpyxl. Generating CSV instead...")
                                content = report_gen.generate_csv_report()
                                st.download_button(
                                    "📥 Download CSV",
                                    content,
                                    file_name="data.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                        
                        elif report_format == "CSV Export":
                            content = report_gen.generate_csv_report()
                            st.download_button(
                                "📥 Download CSV",
                                content,
                                file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                            st.success("CSV exported!")
                        
                        elif report_format == "Markdown":
                            content = report_gen.generate_markdown_report()
                            st.download_button(
                                "📥 Download Markdown",
                                content,
                                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                            st.success("Markdown report generated!")
                            
                            # Preview
                            with st.expander("Preview Markdown"):
                                st.markdown(content)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Dashboard Builder Section
                st.markdown('<div class="section-title">📊 Dashboard KPIs</div>', unsafe_allow_html=True)
                
                dashboard = DashboardBuilder(st.session_state.processor.df)
                kpis = dashboard.get_kpi_cards()
                
                if kpis:
                    kpi_cols = st.columns(min(4, len(kpis)))
                    for i, kpi in enumerate(kpis[:4]):
                        with kpi_cols[i]:
                            trend_color = "var(--success)" if kpi['trend_direction'] == 'up' else "var(--danger)" if kpi['trend_direction'] == 'down' else "var(--text-secondary)"
                            trend_icon = "↑" if kpi['trend_direction'] == 'up' else "↓" if kpi['trend_direction'] == 'down' else "→"
                            st.markdown(f"""
                            <div class="kpi-box">
                                <div class="kpi-label">{kpi['name']}</div>
                                <div class="kpi-value">{kpi['value']:,.0f}</div>
                                <div style="font-size: 0.85rem; color: {trend_color}; font-weight: 600;">{trend_icon} {kpi['trend']:+.1f}%</div>
                            </div>
                            """, unsafe_allow_html=True)
            
            with tab6:
                # Email Tab
                st.markdown('<div class="section-title">📧 Email Report</div>', unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: linear-gradient(135deg, var(--primary-glow), rgba(14, 165, 233, 0.08)); padding: 1.25rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid rgba(99, 102, 241, 0.2);">
                    <strong style="color: var(--text-primary);">Send reports directly via email!</strong><br>
                    <span style="color: var(--text-secondary);">Configure your SMTP settings in .env file for full functionality.</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Email configuration status
                email_service = EmailService()
                config_status = email_service.get_configuration_status()
                
                if config_status['configured']:
                    st.success("✅ Email service configured")
                else:
                    st.info("ℹ️ Email not configured. Add SMTP settings to .env file:")
                    st.code("""
SMTP_SERVER=smtp.gmail.com
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
                    """)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Email form
                recipient_emails = st.text_input("Recipient Email(s)", placeholder="email@example.com, another@example.com", key="email_recipients")
                email_subject = st.text_input("Subject (optional)", placeholder="TechXcel Data Report", key="email_subject")
                email_message = st.text_area("Message (optional)", placeholder="Please find the attached report...", key="email_message")
                
                attachment_type = st.selectbox("Attachment Type", ["HTML Report", "CSV Data", "Both"], key="email_attachment")
                
                if st.button("📧 Send Email", use_container_width=True, type="primary"):
                    if not recipient_emails:
                        st.error("Please enter recipient email(s)")
                    elif not config_status['configured']:
                        st.error("Email service not configured. Please add SMTP settings to .env file.")
                    else:
                        with st.spinner("Sending email..."):
                            recipients = [e.strip() for e in recipient_emails.split(",")]
                            
                            # Generate report
                            report_gen = ReportGenerator(
                                st.session_state.processor.df,
                                st.session_state.eda_results,
                                st.session_state.analysis
                            )
                            
                            html_report = report_gen.generate_html_report()
                            
                            additional_attachments = []
                            if attachment_type in ["CSV Data", "Both"]:
                                additional_attachments.append({
                                    'filename': f'data_{datetime.now().strftime("%Y%m%d")}.csv',
                                    'content': report_gen.generate_csv_report(),
                                    'content_type': 'text/csv'
                                })
                            
                            result = email_service.send_report_email(
                                to_emails=recipients,
                                report_html=html_report,
                                report_title=email_subject or "TechXcel Report",
                                additional_attachments=additional_attachments if additional_attachments else None
                            )
                            
                            if result['success']:
                                st.success(f"✅ {result['message']}")
                            else:
                                st.error(f"❌ {result['message']}")
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Quick Share Options
                st.markdown('<div class="section-title">🔗 Quick Share</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy Data Link", use_container_width=True):
                        st.info("Feature coming soon: Generate shareable link")
                with col2:
                    if st.button("📱 Generate QR Code", use_container_width=True):
                        st.info("Feature coming soon: QR code for report access")
    
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
            <div class="getting-started">
                <div style="font-size: 2rem; margin-bottom: 0.75rem;">🚀</div>
                <div class="getting-started-title">Get Started in 2 Steps</div>
                <div class="getting-started-step">1. Upload your Excel file (sidebar)</div>
                <div class="getting-started-step">2. Ask any question!</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success("👈 **Start here:** Upload an Excel file or try **Demo Data**")


if __name__ == "__main__":
    main()
