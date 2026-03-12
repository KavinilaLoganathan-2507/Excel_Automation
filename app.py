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
    page_title="TechXcel Pro | AI Excel Analytics",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def get_theme_css(theme):
    """Generate CSS based on selected theme - Premium Commercial Edition"""
    if theme == 'dark':
        colors = {
            'primary': '#7c3aed',
            'primary_light': '#a78bfa',
            'primary_glow': 'rgba(124, 58, 237, 0.3)',
            'accent': '#06b6d4',
            'accent_light': '#22d3ee',
            'gradient_start': '#7c3aed',
            'gradient_mid': '#a855f7',
            'gradient_end': '#06b6d4',
            'success': '#10b981',
            'success_light': 'rgba(16, 185, 129, 0.15)',
            'warning': '#f59e0b',
            'warning_light': 'rgba(245, 158, 11, 0.15)',
            'danger': '#ef4444',
            'danger_light': 'rgba(239, 68, 68, 0.15)',
            'bg_primary': '#030712',
            'bg_secondary': '#0f172a',
            'bg_tertiary': '#1e293b',
            'bg_app': 'linear-gradient(135deg, #030712 0%, #0f172a 50%, #1e1b4b 100%)',
            'text_primary': '#f8fafc',
            'text_secondary': '#94a3b8',
            'text_muted': '#64748b',
            'border': 'rgba(148, 163, 184, 0.1)',
            'border_light': 'rgba(148, 163, 184, 0.05)',
            'shadow_sm': '0 1px 2px rgba(0, 0, 0, 0.5)',
            'shadow_md': '0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.4)',
            'shadow_lg': '0 10px 25px -3px rgba(0, 0, 0, 0.5), 0 4px 10px -2px rgba(0, 0, 0, 0.4)',
            'shadow_xl': '0 25px 50px -12px rgba(0, 0, 0, 0.6)',
            'shadow_glow': '0 0 60px rgba(124, 58, 237, 0.4)',
            'hero_bg': 'radial-gradient(ellipse 80% 50% at 50% -20%, rgba(124, 58, 237, 0.3) 0%, transparent 60%)',
            'card_hover_border': 'rgba(124, 58, 237, 0.5)',
            'card_bg': 'rgba(15, 23, 42, 0.6)',
            'glass_bg': 'rgba(15, 23, 42, 0.8)',
            'chat_bubble_user': 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
            'msg_success_text': '#6ee7b7',
            'msg_warning_text': '#fcd34d',
            'msg_error_text': '#fca5a5',
            'chart_bg': 'rgba(15, 23, 42, 0.9)',
            'chart_plot_bg': 'rgba(30, 41, 59, 0.5)',
            'chart_font': '#94a3b8',
        }
    else:
        colors = {
            'primary': '#7c3aed',
            'primary_light': '#a78bfa',
            'primary_glow': 'rgba(124, 58, 237, 0.12)',
            'accent': '#0ea5e9',
            'accent_light': '#38bdf8',
            'gradient_start': '#7c3aed',
            'gradient_mid': '#a855f7',
            'gradient_end': '#06b6d4',
            'success': '#059669',
            'success_light': '#d1fae5',
            'warning': '#d97706',
            'warning_light': '#fef3c7',
            'danger': '#dc2626',
            'danger_light': '#fee2e2',
            'bg_primary': '#ffffff',
            'bg_secondary': '#f8fafc',
            'bg_tertiary': '#f1f5f9',
            'bg_app': 'linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f5f3ff 100%)',
            'text_primary': '#0f172a',
            'text_secondary': '#475569',
            'text_muted': '#94a3b8',
            'border': 'rgba(15, 23, 42, 0.08)',
            'border_light': 'rgba(15, 23, 42, 0.04)',
            'shadow_sm': '0 1px 2px rgba(0, 0, 0, 0.04)',
            'shadow_md': '0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04)',
            'shadow_lg': '0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 10px -2px rgba(0, 0, 0, 0.05)',
            'shadow_xl': '0 25px 50px -12px rgba(0, 0, 0, 0.15)',
            'shadow_glow': '0 0 60px rgba(124, 58, 237, 0.15)',
            'hero_bg': 'radial-gradient(ellipse 80% 50% at 50% -20%, rgba(124, 58, 237, 0.08) 0%, transparent 60%)',
            'card_hover_border': 'rgba(124, 58, 237, 0.3)',
            'card_bg': 'rgba(255, 255, 255, 0.8)',
            'glass_bg': 'rgba(255, 255, 255, 0.9)',
            'chat_bubble_user': 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
            'msg_success_text': '#047857',
            'msg_warning_text': '#b45309',
            'msg_error_text': '#b91c1c',
            'chart_bg': 'white',
            'chart_plot_bg': '#fafafa',
            'chart_font': '#334155',
        }
    
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
    
    :root {{
        --primary: {colors['primary']};
        --primary-light: {colors['primary_light']};
        --primary-glow: {colors['primary_glow']};
        --accent: {colors['accent']};
        --accent-light: {colors['accent_light']};
        --gradient-start: {colors['gradient_start']};
        --gradient-mid: {colors['gradient_mid']};
        --gradient-end: {colors['gradient_end']};
        --success: {colors['success']};
        --success-light: {colors['success_light']};
        --warning: {colors['warning']};
        --warning-light: {colors['warning_light']};
        --danger: {colors['danger']};
        --danger-light: {colors['danger_light']};
        --bg-primary: {colors['bg_primary']};
        --bg-secondary: {colors['bg_secondary']};
        --bg-tertiary: {colors['bg_tertiary']};
        --card-bg: {colors['card_bg']};
        --glass-bg: {colors['glass_bg']};
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
    
    * {{
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    
    .stApp {{
        background: {colors['bg_app']};
        min-height: 100vh;
    }}
    
    #MainMenu, footer {{visibility: hidden;}}
    
    /* Premium Animations */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        25% {{ transform: translateY(-8px) rotate(1deg); }}
        75% {{ transform: translateY(-4px) rotate(-1deg); }}
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
    }}
    
    @keyframes pulse-glow {{
        0%, 100% {{ box-shadow: 0 0 20px {colors['primary_glow']}; }}
        50% {{ box-shadow: 0 0 40px {colors['primary_glow']}, 0 0 60px {colors['primary_glow']}; }}
    }}
    
    @keyframes gradient-flow {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes fadeInScale {{
        from {{ opacity: 0; transform: scale(0.95); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    
    @keyframes slideInRight {{
        from {{ opacity: 0; transform: translateX(30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    @keyframes rotate-gradient {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    @keyframes border-dance {{
        0%, 100% {{ border-color: var(--primary); }}
        25% {{ border-color: var(--accent); }}
        50% {{ border-color: var(--primary-light); }}
        75% {{ border-color: var(--gradient-end); }}
    }}
    
    /* Keep sidebar toggle visible - Fix Material Icons */
    [data-testid="collapsedControl"] {{
        visibility: visible !important;
        display: flex !important;
        background: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-md) !important;
        padding: 0.5rem !important;
        transition: all 0.3s !important;
    }}
    
    [data-testid="collapsedControl"]:hover {{
        background: var(--bg-secondary) !important;
        border-color: var(--primary) !important;
        box-shadow: var(--shadow-glow) !important;
    }}
    
    [data-testid="collapsedControl"] span,
    [data-testid="collapsedControl"] svg {{
        font-family: 'Material Icons', 'Material Symbols Rounded', sans-serif !important;
        font-size: 24px !important;
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stSidebarCollapsedControl"] {{
        visibility: visible !important;
        color: var(--text-primary) !important;
    }}
    
    /* Sidebar collapse button inside sidebar */
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebarCollapseButton"] {{
        visibility: visible !important;
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
        margin: 0.5rem !important;
        transition: all 0.3s !important;
    }}
    
    [data-testid="stSidebar"] button[kind="header"]:hover,
    [data-testid="stSidebarCollapseButton"]:hover {{
        background: var(--primary-glow) !important;
        border-color: var(--primary) !important;
    }}
    
    [data-testid="stSidebar"] button[kind="header"] span,
    [data-testid="stSidebarCollapseButton"] span {{
        font-family: 'Material Icons', 'Material Symbols Rounded', sans-serif !important;
        font-size: 20px !important;
        color: var(--text-primary) !important;
    }}
    
    button[kind="header"] {{
        visibility: visible !important;
    }}
    
    /* Premium Hero */
    .hero {{
        text-align: center;
        padding: 3rem 2rem 2.5rem;
        background: {colors['hero_bg']};
        margin-bottom: 1.5rem;
        position: relative;
        border-radius: 24px;
        border: 1px solid var(--border);
        backdrop-filter: blur(10px);
        overflow: hidden;
    }}
    
    .hero::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg at 50% 50%, {colors['primary_glow']} 0deg, transparent 60deg, {colors['primary_glow']} 180deg, transparent 240deg, {colors['primary_glow']} 360deg);
        animation: gradient-shift 8s linear infinite;
        opacity: 0.3;
        pointer-events: none;
    }}
    
    .hero::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--bg-primary);
        opacity: 0.85;
        z-index: 0;
    }}
    
    .hero > * {{
        position: relative;
        z-index: 1;
    }}
    
    .hero h1 {{
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, {colors['primary']} 0%, #c084fc 30%, {colors['accent']} 60%, #22d3ee 100%);
        background-size: 300% 300%;
        animation: gradient-shift 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.04em;
    }}
    
    .hero p {{
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }}
    
    /* Premium Glass Cards */
    .card {{
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.75rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-md);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }}
    
    .card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary-light), transparent);
        opacity: 0;
        transition: opacity 0.3s;
    }}
    
    .card:hover {{
        border-color: {colors['card_hover_border']};
        box-shadow: var(--shadow-glow), 0 20px 40px -10px rgba(0, 0, 0, 0.2);
        transform: translateY(-4px);
    }}
    
    .card:hover::before {{
        opacity: 1;
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
    
    /* Premium Metrics with Glass Effect */
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .metric {{
        background: linear-gradient(145deg, var(--bg-primary), var(--bg-secondary));
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(5px);
    }}
    
    .metric::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), {colors['accent']}, var(--primary));
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
        opacity: 0;
        transition: opacity 0.3s;
    }}
    
    .metric::after {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 120%;
        height: 120%;
        background: radial-gradient(circle, {colors['primary_glow']} 0%, transparent 70%);
        transform: translate(-50%, -50%);
        opacity: 0;
        transition: opacity 0.4s;
        pointer-events: none;
    }}
    
    .metric:hover {{
        transform: translateY(-6px) scale(1.02);
        box-shadow: var(--shadow-xl), 0 0 30px {colors['primary_glow']};
        border-color: var(--primary);
    }}
    
    .metric:hover::before {{
        opacity: 1;
    }}
    
    .metric:hover::after {{
        opacity: 0.3;
    }}
    
    .metric-value {{
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary) 0%, #c084fc 50%, var(--accent) 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite;
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
        background: linear-gradient(135deg, var(--primary), #c084fc) !important;
        color: white !important;
        box-shadow: 0 4px 20px {colors['primary_glow']};
    }}
    
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{
        display: none;
    }}
    
    /* Premium Animated Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary) 0%, #c084fc 50%, var(--accent) 100%);
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.9rem 1.75rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px {colors['primary_glow']};
        letter-spacing: -0.01em;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 30px {colors['primary_glow']}, 0 0 0 2px rgba(255,255,255,0.1);
        background-position: 100% 0;
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px);
    }}
    
    /* Premium Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background: var(--bg-primary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 14px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 4px var(--primary-glow) !important;
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
        transition: all 0.3s;
        text-align: center;
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        position: relative;
        overflow: hidden;
    }}
    
    .quick-action::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: var(--primary-glow);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.4s, height 0.4s;
        z-index: 0;
    }}
    
    .quick-action:hover {{
        border-color: var(--primary);
        color: var(--primary);
        transform: scale(1.02);
    }}
    
    .quick-action:hover::before {{
        width: 200%;
        height: 200%;
    }}
    
    /* Premium Divider */
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary-light), var(--accent), var(--primary-light), transparent);
        margin: 1.5rem 0;
        opacity: 0.5;
    }}
    
    /* Premium Feature Grid - Landing Page */
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }}
    
    .feature-item {{
        background: linear-gradient(145deg, var(--bg-primary), var(--bg-secondary));
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 2rem 1.25rem;
        text-align: center;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease forwards;
        opacity: 0;
    }}
    
    .feature-item:nth-child(1) {{ animation-delay: 0.1s; }}
    .feature-item:nth-child(2) {{ animation-delay: 0.2s; }}
    .feature-item:nth-child(3) {{ animation-delay: 0.3s; }}
    .feature-item:nth-child(4) {{ animation-delay: 0.4s; }}
    
    .feature-item::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        transform: scaleX(0);
        transition: transform 0.4s;
        transform-origin: left;
    }}
    
    .feature-item::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        top: 0;
        background: radial-gradient(circle at center, {colors['primary_glow']} 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s;
    }}
    
    .feature-item:hover {{
        transform: translateY(-12px) scale(1.02);
        box-shadow: var(--shadow-xl), 0 0 40px {colors['primary_glow']};
        border-color: var(--primary);
    }}
    
    .feature-item:hover::before {{
        transform: scaleX(1);
    }}
    
    .feature-item:hover::after {{
        opacity: 0.4;
    }}
    
    .feature-icon {{
        font-size: 3rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 8px 16px {colors['primary_glow']});
        animation: float 3s ease-in-out infinite;
        position: relative;
        z-index: 2;
    }}
    
    .feature-item:nth-child(1) .feature-icon {{ animation-delay: 0s; }}
    .feature-item:nth-child(2) .feature-icon {{ animation-delay: 0.3s; }}
    .feature-item:nth-child(3) .feature-icon {{ animation-delay: 0.6s; }}
    .feature-item:nth-child(4) .feature-icon {{ animation-delay: 0.9s; }}
    
    .feature-title {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        font-size: 1rem;
        position: relative;
        z-index: 2;
    }}
    
    .feature-desc {{
        font-size: 0.8rem;
        color: var(--text-secondary);
        line-height: 1.5;
        position: relative;
        z-index: 2;
    }}
    
    /* Premium Data Tables */
    .stDataFrame {{
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
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
    
    /* File Uploader - Light Theme Compatible */
    [data-testid="stFileUploader"] {{
        background: var(--bg-primary) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        transition: all 0.3s !important;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: var(--primary) !important;
        background: var(--primary-glow) !important;
    }}
    
    [data-testid="stFileUploader"] section {{
        background: var(--bg-primary) !important;
        border: none !important;
    }}
    
    [data-testid="stFileUploader"] section > div {{
        background: var(--bg-primary) !important;
    }}
    
    [data-testid="stFileUploader"] section button {{
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
    }}
    
    [data-testid="stFileUploader"] small {{
        color: var(--text-secondary) !important;
    }}
    
    [data-testid="stFileUploaderDropzone"] {{
        background: var(--bg-primary) !important;
        border: none !important;
    }}
    
    [data-testid="stFileUploaderDropzoneInstructions"] {{
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stFileUploaderDropzoneInstructions"] div {{
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stFileUploaderDropzoneInstructions"] span {{
        color: var(--text-secondary) !important;
    }}
    
    /* File uploader inner content */
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {{
        color: var(--text-primary) !important;
    }}
    
    /* Force all nested divs in uploader to use theme colors */
    [data-testid="stFileUploader"] div {{
        background-color: transparent !important;
    }}
    
    [data-testid="stFileUploader"] > section {{
        background: var(--bg-primary) !important;
    }}
    
    [data-testid="stFileUploader"] > section > div {{
        background: var(--bg-primary) !important;
    }}
    
    [data-testid="stFileUploader"] > section > div > div {{
        background: var(--bg-primary) !important;
    }}
    
    /* Browse files button */
    [data-testid="stFileUploader"] button[kind="secondary"],
    [data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] {{
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }}
    
    [data-testid="stFileUploader"] button[kind="secondary"]:hover,
    [data-testid="stFileUploader"] button[data-testid="baseButton-secondary"]:hover {{
        background: var(--primary-glow) !important;
        border-color: var(--primary) !important;
        color: var(--primary) !important;
    }}
    
    /* File drop text styling */
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span {{
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"] small {{
        color: var(--text-secondary) !important;
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
        <style>
            .premium-brand {
                text-align: center;
                padding: 2rem 1.5rem;
                background: linear-gradient(180deg, var(--primary-glow) 0%, transparent 100%);
                border-bottom: 1px solid var(--border);
                position: relative;
                overflow: hidden;
            }
            
            .premium-brand::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle at 50% 100%, var(--primary-glow) 0%, transparent 50%);
                animation: rotate-gradient 15s linear infinite;
                pointer-events: none;
            }
            
            .premium-brand > * {
                position: relative;
                z-index: 2;
            }
            
            .brand-logo {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, var(--primary), #a855f7, var(--accent));
                background-size: 200% 200%;
                animation: gradient-flow 4s ease infinite;
                border-radius: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.75rem;
                margin: 0 auto 1rem;
                box-shadow: 0 10px 30px var(--primary-glow), 0 0 0 1px rgba(255,255,255,0.1) inset;
            }
            
            .brand-name {
                font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
                font-size: 1.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, var(--primary) 0%, #a855f7 50%, var(--accent) 100%);
                background-size: 200% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: gradient-flow 4s ease infinite;
                letter-spacing: -0.02em;
            }
            
            .brand-tagline {
                font-size: 0.75rem;
                color: var(--text-secondary);
                margin-top: 0.5rem;
                font-weight: 500;
                letter-spacing: 0.02em;
            }
            
            .brand-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                background: var(--success-light);
                color: var(--success);
                padding: 0.35rem 0.75rem;
                border-radius: 20px;
                font-size: 0.65rem;
                font-weight: 700;
                margin-top: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
        </style>
        <div class="premium-brand">
            <div class="brand-logo" style="font-family: 'codicon', 'Segoe Fluent Icons', sans-serif;">TX</div>
            <div class="brand-name">TechXcel Pro</div>
            <div class="brand-tagline">Enterprise AI Analytics</div>
            <div class="brand-badge">PRO</div>
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
        st.markdown('<div class="sidebar-label">UPLOAD FILE</div>', unsafe_allow_html=True)
        
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
                st.success("Data loaded successfully")
            except Exception as e:
                st.error(f"Error: {e}")
        
        if st.button("Try Demo Data", use_container_width=True, help="Load sample sales data to explore features"):
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
        
        # Premium Stats Cards
        if st.session_state.processor is not None:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-label">DATA OVERVIEW</div>', unsafe_allow_html=True)
            s = st.session_state.summary
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 0.5rem;">
                <div style="background: linear-gradient(135deg, var(--card-bg), var(--glass-bg)); border: 1px solid var(--border); border-radius: 14px; padding: 1rem; text-align: center; transition: all 0.3s;">
                    <div style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, var(--primary), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{s['rows']}</div>
                    <div style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Rows</div>
                </div>
                <div style="background: linear-gradient(135deg, var(--card-bg), var(--glass-bg)); border: 1px solid var(--border); border-radius: 14px; padding: 1rem; text-align: center; transition: all 0.3s;">
                    <div style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, var(--accent), #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{s['columns']}</div>
                    <div style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Columns</div>
                </div>
                <div style="background: linear-gradient(135deg, var(--card-bg), var(--glass-bg)); border: 1px solid var(--border); border-radius: 14px; padding: 1rem; text-align: center; transition: all 0.3s;">
                    <div style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, var(--success), #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{len(s['numeric_columns'])}</div>
                    <div style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Numeric</div>
                </div>
                <div style="background: linear-gradient(135deg, var(--card-bg), var(--glass-bg)); border: 1px solid var(--border); border-radius: 14px; padding: 1rem; text-align: center; transition: all 0.3s;">
                    <div style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, var(--warning), var(--danger)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{len(st.session_state.relationships.get('correlations', {}))}</div>
                    <div style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Links</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    if st.session_state.processor is not None:
        # Premium header with gradient
        st.markdown("""
        <style>
            .dashboard-header {
                background: linear-gradient(135deg, var(--glass-bg) 0%, var(--card-bg) 100%);
                border: 1px solid var(--border);
                border-radius: 24px;
                padding: 1.5rem 2rem;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                justify-content: space-between;
                position: relative;
                overflow: hidden;
            }
            
            .dashboard-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--primary), #a855f7, var(--accent));
                background-size: 200% 100%;
                animation: shimmer 3s linear infinite;
            }
            
            .dashboard-title {
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 1.75rem;
                font-weight: 800;
                background: linear-gradient(135deg, var(--primary), #a855f7, var(--accent));
                background-size: 200% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: gradient-flow 4s ease infinite;
                letter-spacing: -0.02em;
                margin: 0;
            }
            
            .dashboard-subtitle {
                color: var(--text-secondary);
                font-size: 0.9rem;
                margin-top: 0.25rem;
            }
            
            .dashboard-status {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                background: var(--success-light);
                color: var(--success);
                padding: 0.5rem 1rem;
                border-radius: 12px;
                font-size: 0.8rem;
                font-weight: 600;
            }
            
            .status-dot {
                width: 8px;
                height: 8px;
                background: var(--success);
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
        </style>
        <div class="dashboard-header">
            <div>
                <h1 class="dashboard-title">TechXcel Pro</h1>
                <p class="dashboard-subtitle">Your AI-powered data analyst — insights in seconds</p>
            </div>
            <div class="dashboard-status">
                <div class="status-dot"></div>
                Data Loaded
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis tabs first (full width)
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Dashboard", "Explore", "Visualize", "Simulate", "Reports", "Share"])
        
        with tab1:
            # Dashboard Metrics
            summary = st.session_state.summary
            st.markdown('<div class="section-title">Key Metrics</div>', unsafe_allow_html=True)
            cols = st.columns(4)
            metrics = [
                (summary['rows'], "Total Rows"),
                (summary['columns'], "Columns"),
                (len(summary['numeric_columns']), "Numeric"),
                (len(st.session_state.relationships.get('correlations', {})), "Correlations")
            ]
            for i, (val, label) in enumerate(metrics):
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
                st.markdown('<div class="section-title">Date Filter</div>', unsafe_allow_html=True)
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
            st.markdown('<div class="section-title">Data</div>', unsafe_allow_html=True)
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
            # EDA - Exploratory Data Analysis - Premium
            st.markdown("""
            <div style="background: linear-gradient(135deg, var(--primary-glow), transparent); padding: 1rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid var(--border);">
                <div class="section-title" style="margin-bottom: 0.25rem;">Data Explorer</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">Deep dive into your data with AI-powered analysis</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Run Full Analysis", use_container_width=True, type="primary"):
                with st.spinner("🔍 Analyzing your data..."):
                    eda = EDAEngine(st.session_state.processor.df)
                    st.session_state.eda_engine = eda
                    st.session_state.eda_results = eda.get_full_eda_report()
                st.success("Analysis Complete")
            
            if st.session_state.eda_results:
                eda_results = st.session_state.eda_results
                
                # Premium Data Quality Score
                quality = eda_results.get('data_quality', {})
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #a855f7, #c084fc, #06b6d4); padding: 1.5rem; border-radius: 16px; text-align: center; margin-bottom: 1rem; position: relative; overflow: hidden;">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at top right, rgba(255,255,255,0.2) 0%, transparent 50%);"></div>
                    <div style="position: relative; z-index: 1;">
                        <div style="font-size: 3rem; font-weight: 800; color: white; text-shadow: 0 4px 20px rgba(0,0,0,0.3);">{quality.get('overall_score', 0)}%</div>
                        <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; font-weight: 600;">Data Quality Score • Grade: {quality.get('grade', 'N/A')}</div>
                    </div>
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
                st.markdown('<div class="section-title">Smart Insights</div>', unsafe_allow_html=True)
                insights = st.session_state.eda_engine.get_smart_insights()
                
                for insight in insights[:5]:
                    insight_type = insight.get('type', 'info')
                    color_map = {'success': '#10b981', 'warning': '#f59e0b', 'danger': '#ef4444', 'info': '#6366f1'}
                    icon_map = {'success': '+', 'warning': '!', 'danger': 'x', 'info': 'i'}
                    
                    st.markdown(f"""
                    <div style="background: {color_map.get(insight_type, '#6366f1')}15; border-left: 4px solid {color_map.get(insight_type, '#6366f1')}; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <strong style="color: var(--text-primary);">[{icon_map.get(insight_type, 'i')}] {insight.get('title', '')}</strong><br>
                        <span style="color: var(--text-secondary);">{insight.get('message', '')}</span><br>
                        <span style="color: var(--primary); font-size: 0.85rem; font-weight: 500;">{insight.get('suggestion', '')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Distribution Analysis
                st.markdown('<div class="section-title">Distribution Analysis</div>', unsafe_allow_html=True)
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
                st.markdown('<div class="section-title">Outlier Detection</div>', unsafe_allow_html=True)
                outliers = eda_results.get('outliers', {})
                if outliers and 'message' not in outliers:
                    outlier_df = pd.DataFrame([
                        {"Column": col, "Outliers": data['count'], "Percentage": f"{data['percentage']}%"}
                        for col, data in outliers.items()
                    ])
                    st.dataframe(outlier_df, use_container_width=True, hide_index=True)
            
        with tab3:
            # Auto Charts & Visualization - Premium
            st.markdown("""
            <div style="background: linear-gradient(135deg, var(--primary-glow), transparent); padding: 1rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid var(--border);">
                <div class="section-title" style="margin-bottom: 0.25rem;">Smart Visualizations</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">AI-generated charts tailored to your data</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Generate Smart Charts", use_container_width=True, type="primary"):
                with st.spinner("🎨 Creating beautiful visualizations..."):
                    st.session_state.auto_charts = auto_generate_charts(st.session_state.processor.df)
                st.success(f"Generated {len(st.session_state.auto_charts)} charts")
            
            if st.session_state.auto_charts:
                for chart_info in st.session_state.auto_charts:
                    st.markdown(f"""
                    <div style="background: var(--bg-secondary); padding: 0.75rem 1rem; border-radius: 12px; margin-bottom: 0.5rem; border: 1px solid var(--border);">
                        <strong style="color: var(--text-primary);">{chart_info.get('title', 'Chart')}</strong>
                        <span style="color: var(--text-secondary); font-size: 0.8rem; margin-left: 0.5rem;">{chart_info.get('description', '')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
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
            
            # Custom Chart Builder - Premium
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), transparent); padding: 1rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid var(--border);">
                <div class="section-title" style="margin-bottom: 0.25rem;">🛠️ Custom Chart Builder</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">Create your own visualizations</div>
            </div>
            """, unsafe_allow_html=True)
            
            chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Pie", "Area"], key="custom_chart_type")
            
            col1, col2 = st.columns(2)
            numeric_cols = summary.get('numeric_columns', [])
            categorical_cols = summary.get('categorical_columns', [])
            all_cols = list(st.session_state.processor.df.columns)
            
            with col1:
                x_col = st.selectbox("X-Axis", all_cols, key="x_axis")
            with col2:
                y_col = st.selectbox("Y-Axis", numeric_cols if numeric_cols else all_cols, key="y_axis")
            
            if st.button("🎨 Create Chart", use_container_width=True):
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
            # Simulation Tab - Premium
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), transparent); padding: 1rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid var(--border);">
                <div class="section-title" style="margin-bottom: 0.25rem;">What-If Simulator</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">Explore scenarios and predict outcomes</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                var = st.selectbox("Change Variable", summary['numeric_columns'], key="sim_var")
            
            current = st.session_state.processor.df[var].mean()
            
            with col2:
                orig = st.number_input("Current Value", value=float(current), key="sim_from")
            
            with col3:
                new = st.number_input("New Value", value=float(current * 1.3), key="sim_to")
            
            if st.button("Run Simulation", use_container_width=True, type="primary"):
                simulation = st.session_state.processor.simulate_what_if(var, orig, new)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Results - Premium Cards
                st.markdown('<div class="section-title">Predicted Impact</div>', unsafe_allow_html=True)
                result_cols = st.columns(2)
                
                with result_cols[0]:
                    change_pct = simulation.get('change_percent', 0)
                    color = "var(--success)" if change_pct > 0 else "var(--danger)"
                    st.markdown(f"""
                    <div style="background: var(--bg-secondary); padding: 1.25rem; border-radius: 16px; text-align: center; border: 1px solid var(--border);">
                        <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">Input Change</div>
                        <div style="font-size: 1.75rem; font-weight: 800; color: var(--primary); margin: 0.5rem 0;">{new:,.0f}</div>
                        <div style="font-size: 0.85rem; color: {color}; font-weight: 600;">{change_pct:+.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_cols[1]:
                    for impact in simulation.get('impacts', [])[:1]:
                        impact_color = "var(--success)" if impact['percent_change'] > 0 else "var(--danger)"
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); padding: 1.25rem; border-radius: 16px; text-align: center; border: 1px solid var(--border);">
                            <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">{impact['target_variable']}</div>
                            <div style="font-size: 1.75rem; font-weight: 800; color: var(--accent); margin: 0.5rem 0;">{impact['predicted_value']:,.0f}</div>
                            <div style="font-size: 0.85rem; color: {impact_color}; font-weight: 600;">{impact['percent_change']:+.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                
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
            st.markdown('<div class="section-title">Timeline Explorer</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                input_var = st.selectbox("Variable", options=summary['numeric_columns'], key="tl_in_2")
            with col2:
                steps = st.slider("Points", 5, 30, 15, key="tl_steps_2")
            
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
            # Reports Tab - Premium
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), transparent); padding: 1rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid var(--border);">
                <div class="section-title" style="margin-bottom: 0.25rem;">Report Generator</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">Export professional reports in multiple formats</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Format Cards
            st.markdown("""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-bottom: 1rem;">
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid var(--border);">
                    <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary);">HTML</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">HTML</div>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid var(--border);">
                    <div style="font-size: 1.5rem;">📗</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">Excel</div>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid var(--border);">
                    <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary);">XLSX</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">CSV</div>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid var(--border);">
                    <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary);">MD</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">Markdown</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            report_format = st.selectbox("📁 Report Format", ["HTML Report", "Excel Dashboard", "CSV Export", "Markdown"], key="report_format")
            
            col1, col2 = st.columns(2)
            with col1:
                include_charts = st.checkbox("Include Charts", value=True, key="include_charts")
            with col2:
                include_eda = st.checkbox("Include Analysis", value=True, key="include_eda")
            
            if st.button("Generate Report", use_container_width=True, type="primary"):
                with st.spinner("Generating your report..."):
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
                            "Download HTML Report",
                            content,
                            file_name=f"techxcel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html",
                            use_container_width=True
                        )
                        st.success("Report generated. Click to download.")
                        
                        # Preview
                        with st.expander("👁️ Preview Report"):
                            st.components.v1.html(content, height=600, scrolling=True)
                    
                    elif report_format == "Excel Dashboard":
                        content = report_gen.generate_excel_dashboard()
                        if content:
                            st.download_button(
                                "Download Excel Dashboard",
                                content,
                                file_name=f"techxcel_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                            st.success("Excel dashboard generated")
                        else:
                                st.warning("Excel generation requires openpyxl. Generating CSV instead...")
                                content = report_gen.generate_csv_report()
                                st.download_button(
                                    "Download CSV",
                                    content,
                                    file_name="data.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                        
                    elif report_format == "CSV Export":
                        content = report_gen.generate_csv_report()
                        st.download_button(
                            "Download CSV",
                            content,
                            file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        st.success("CSV exported!")
                    
                    elif report_format == "Markdown":
                            content = report_gen.generate_markdown_report()
                            st.download_button(
                                "Download Markdown",
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
                st.markdown('<div class="section-title">Dashboard KPIs</div>', unsafe_allow_html=True)
                
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
            # Share Tab - Premium
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), transparent); padding: 1rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid var(--border);">
                <div class="section-title" style="margin-bottom: 0.25rem;">Share & Export</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">Send reports directly to your team</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Email configuration status
            email_service = EmailService()
            config_status = email_service.get_configuration_status()
            
            if config_status['configured']:
                st.markdown("""
                <div style="background: var(--success-light); border: 1px solid var(--success); padding: 0.75rem 1rem; border-radius: 12px; margin-bottom: 1rem;">
                    <span style="color: var(--success); font-weight: 600;">Email service ready</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: var(--warning-light); border: 1px solid var(--warning); padding: 0.75rem 1rem; border-radius: 12px; margin-bottom: 1rem;">
                    <span style="color: var(--warning); font-weight: 600;">Email not configured</span>
                    <span style="color: var(--text-secondary); font-size: 0.85rem; margin-left: 0.5rem;">Add SMTP settings to .env file</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Email form with premium styling
            st.markdown('<div style="background: var(--bg-secondary); padding: 1.25rem; border-radius: 16px; border: 1px solid var(--border);">', unsafe_allow_html=True)
            
            recipient_emails = st.text_input("Recipient Email(s)", placeholder="email@example.com, another@example.com", key="email_recipients")
            
            col1, col2 = st.columns(2)
            with col1:
                email_subject = st.text_input("Subject", placeholder="TechXcel Data Report", key="email_subject")
            with col2:
                attachment_type = st.selectbox("Attachment", ["HTML Report", "CSV Data", "Both"], key="email_attachment")
            
            email_message = st.text_area("Message", placeholder="Please find the attached report...", height=80, key="email_message")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Send Email", use_container_width=True, type="primary"):
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
                            st.success(f"{result['message']}")
                        else:
                                st.error(f"❌ {result['message']}")
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # Quick Share Options - Premium Cards
            st.markdown('<div class="section-title">Quick Actions</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Copy Data Link", use_container_width=True):
                    st.info("Feature coming soon: Generate shareable link")
            with col2:
                if st.button("Generate QR Code", use_container_width=True):
                    st.info("Feature coming soon: QR code for report access")
        
        # AI Chatbot Section (at the bottom after scrolling)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <style>
            .copilot-panel {
                background: var(--bg-primary);
                border: 1px solid var(--border);
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 24px rgba(0,0,0,0.15);
                margin-top: 1rem;
            }
            
            .copilot-header {
                background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
                padding: 16px 20px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .copilot-icon {
                width: 32px;
                height: 32px;
                background: rgba(255,255,255,0.2);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                font-weight: 700;
                color: white;
            }
            
            .copilot-title {
                font-family: 'Inter', -apple-system, sans-serif;
                font-size: 15px;
                font-weight: 600;
                color: white;
                flex: 1;
            }
            
            .copilot-status {
                font-size: 12px;
                color: rgba(255,255,255,0.9);
                display: flex;
                align-items: center;
                gap: 6px;
            }
            
            .copilot-status::before {
                content: '';
                width: 8px;
                height: 8px;
                background: #22c55e;
                border-radius: 50%;
                box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
            }
            
            .copilot-body {
                min-height: 300px;
                max-height: 400px;
                overflow-y: auto;
                padding: 20px;
                background: var(--bg-primary);
            }
            
            .copilot-welcome {
                text-align: center;
                padding: 40px 24px;
            }
            
            .copilot-welcome-icon {
                width: 64px;
                height: 64px;
                background: linear-gradient(135deg, var(--primary), var(--accent));
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                color: white;
                margin: 0 auto 20px;
                box-shadow: 0 8px 24px var(--primary-glow);
            }
            
            .copilot-welcome-title {
                font-size: 18px;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 8px;
            }
            
            .copilot-welcome-desc {
                font-size: 14px;
                color: var(--text-secondary);
                line-height: 1.6;
                max-width: 400px;
                margin: 0 auto;
            }
            
            .copilot-suggestions {
                margin-top: 24px;
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: center;
            }
            
            .copilot-suggestion {
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 13px;
                color: var(--text-secondary);
                cursor: pointer;
                transition: all 0.2s;
            }
            
            .copilot-suggestion:hover {
                background: var(--primary-glow);
                border-color: var(--primary);
                color: var(--primary);
            }
            
            .msg-row {
                display: flex;
                gap: 12px;
                margin-bottom: 16px;
            }
            
            .msg-row.user {
                flex-direction: row-reverse;
            }
            
            .msg-avatar {
                width: 32px;
                height: 32px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: 600;
                flex-shrink: 0;
            }
            
            .msg-avatar.ai {
                background: linear-gradient(135deg, var(--primary), var(--accent));
                color: white;
            }
            
            .msg-avatar.user {
                background: var(--bg-tertiary);
                color: var(--text-secondary);
                border: 1px solid var(--border);
            }
            
            .msg-content {
                max-width: 75%;
                padding: 12px 16px;
                border-radius: 12px;
                font-size: 14px;
                line-height: 1.6;
            }
            
            .msg-content.ai {
                background: var(--bg-secondary);
                color: var(--text-primary);
                border: 1px solid var(--border);
                border-bottom-left-radius: 4px;
            }
            
            .msg-content.user {
                background: linear-gradient(135deg, var(--primary), var(--accent));
                color: white;
                border-bottom-right-radius: 4px;
            }
        </style>
        
        <div class="section-title">AI Assistant</div>
        <div class="copilot-panel">
            <div class="copilot-header">
                <div class="copilot-icon">AI</div>
                <div class="copilot-title">Data Copilot</div>
                <div class="copilot-status">Online</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Chat messages container
        chat_container = st.container()
        
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div class="copilot-body">
                    <div class="copilot-welcome">
                        <div class="copilot-welcome-icon">🤖</div>
                        <div class="copilot-welcome-title">How can I help you today?</div>
                        <div class="copilot-welcome-desc">Ask me to analyze your data, find trends, run simulations, or answer any questions about your dataset.</div>
                        <div class="copilot-suggestions">
                            <div class="copilot-suggestion">Show key trends</div>
                            <div class="copilot-suggestion">What-if analysis</div>
                            <div class="copilot-suggestion">Find correlations</div>
                            <div class="copilot-suggestion">Optimize metrics</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="copilot-body">', unsafe_allow_html=True)
                for msg in st.session_state.chat_history[-10:]:
                    if msg['role'] == 'user':
                        st.markdown(f"""
                        <div class="msg-row user">
                            <div class="msg-avatar user">U</div>
                            <div class="msg-content user">{msg['content']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="msg-row">
                            <div class="msg-avatar ai">AI</div>
                            <div class="msg-content ai">{msg['content'][:800]}{'...' if len(msg['content']) > 800 else ''}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input (inline, not fixed)
        st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_input = st.text_input("Ask anything about your data...", key="chat_text_input", label_visibility="collapsed", placeholder="Ask anything about your data...")
        with btn_col:
            send_clicked = st.button("Send", use_container_width=True, type="primary", key="send_chat_btn")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if send_clicked and user_input:
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            with st.spinner("Analyzing..."):
                response = process_chat(user_input)
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
        
        # Quick action buttons
        qa_cols = st.columns(4)
        quick_questions = ["Trends", "Predict", "Optimize", "Relations"]
        
        for i, label in enumerate(quick_questions):
            with qa_cols[i]:
                if st.button(label, use_container_width=True, key=f"qa_{i}"):
                    query_map = {
                        "Trends": "Analyze my data and show key trends",
                        "Predict": "What if we doubled our marketing spend?",
                        "Optimize": "How can we optimize and increase revenue?",
                        "Relations": "Show me the relationships between variables"
                    }
                    actual_query = query_map.get(label, label)
                    st.session_state.chat_history.append({'role': 'user', 'content': actual_query})
                    with st.spinner("Analyzing..."):
                        response = process_chat(actual_query)
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    st.rerun()
    
    else:
        # Premium Commercial Landing page
        st.markdown("""
        <style>
            .commercial-hero {
                position: relative;
                text-align: center;
                padding: 5rem 2rem 4rem;
                background: linear-gradient(135deg, var(--glass-bg) 0%, var(--card-bg) 100%);
                border: 1px solid var(--border);
                border-radius: 32px;
                margin-bottom: 3rem;
                overflow: hidden;
            }
            
            .commercial-hero::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle at 30% 50%, var(--primary-glow) 0%, transparent 50%),
                            radial-gradient(circle at 70% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 40%);
                animation: rotate-gradient 20s linear infinite;
                pointer-events: none;
            }
            
            .commercial-hero > * {
                position: relative;
                z-index: 2;
            }
            
            .hero-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                background: linear-gradient(135deg, var(--primary), var(--accent));
                color: white;
                padding: 0.5rem 1.25rem;
                border-radius: 50px;
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                animation: fadeInUp 0.6s ease forwards;
                box-shadow: 0 4px 20px var(--primary-glow);
            }
            
            .hero-title {
                font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
                font-size: 4.5rem;
                font-weight: 900;
                line-height: 1.1;
                margin: 0 0 1rem;
                letter-spacing: -0.04em;
                animation: fadeInUp 0.6s ease 0.1s forwards;
                opacity: 0;
            }
            
            .hero-title span {
                background: linear-gradient(135deg, var(--primary) 0%, #a855f7 30%, var(--accent) 60%, #22d3ee 100%);
                background-size: 300% 300%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: gradient-flow 4s ease infinite;
            }
            
            .hero-subtitle {
                font-size: 1.35rem;
                color: var(--text-secondary);
                max-width: 600px;
                margin: 0 auto 2rem;
                line-height: 1.7;
                animation: fadeInUp 0.6s ease 0.2s forwards;
                opacity: 0;
            }
            
            .hero-tags {
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
                animation: fadeInUp 0.6s ease 0.3s forwards;
                opacity: 0;
            }
            
            .hero-tag {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                background: var(--glass-bg);
                backdrop-filter: blur(10px);
                border: 1px solid var(--border);
                color: var(--text-primary);
                padding: 0.75rem 1.25rem;
                border-radius: 12px;
                font-size: 0.875rem;
                font-weight: 600;
                transition: all 0.3s;
            }
            
            .hero-tag:hover {
                border-color: var(--primary);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px var(--primary-glow);
            }
            
            .hero-tag-icon {
                font-size: 1.1rem;
            }
            
            /* Premium Feature Cards */
            .premium-features {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 1.5rem;
                margin-bottom: 3rem;
            }
            
            .premium-feature-card {
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 24px;
                padding: 2rem 1.5rem;
                text-align: center;
                position: relative;
                overflow: hidden;
                transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                animation: fadeInScale 0.6s ease forwards;
                opacity: 0;
            }
            
            .premium-feature-card:nth-child(1) { animation-delay: 0.1s; }
            .premium-feature-card:nth-child(2) { animation-delay: 0.2s; }
            .premium-feature-card:nth-child(3) { animation-delay: 0.3s; }
            .premium-feature-card:nth-child(4) { animation-delay: 0.4s; }
            
            .premium-feature-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--primary), var(--accent));
                transform: scaleX(0);
                transition: transform 0.4s;
                transform-origin: left;
            }
            
            .premium-feature-card:hover {
                transform: translateY(-10px);
                border-color: var(--primary);
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 30px var(--primary-glow);
            }
            
            .premium-feature-card:hover::before {
                transform: scaleX(1);
            }
            
            .premium-feature-icon {
                width: 64px;
                height: 64px;
                margin: 0 auto 1.25rem;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                background: linear-gradient(135deg, var(--primary-glow), rgba(6, 182, 212, 0.1));
                box-shadow: 0 8px 20px var(--primary-glow);
                animation: float 4s ease-in-out infinite;
            }
            
            .premium-feature-card:nth-child(1) .premium-feature-icon { animation-delay: 0s; }
            .premium-feature-card:nth-child(2) .premium-feature-icon { animation-delay: 0.4s; }
            .premium-feature-card:nth-child(3) .premium-feature-icon { animation-delay: 0.8s; }
            .premium-feature-card:nth-child(4) .premium-feature-icon { animation-delay: 1.2s; }
            
            .premium-feature-title {
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 0.75rem;
            }
            
            .premium-feature-desc {
                font-size: 0.875rem;
                color: var(--text-secondary);
                line-height: 1.6;
            }
            
            /* Stats Row */
            .stats-row {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1.5rem;
                margin-bottom: 3rem;
            }
            
            .stat-card {
                background: linear-gradient(135deg, var(--card-bg) 0%, var(--glass-bg) 100%);
                border: 1px solid var(--border);
                border-radius: 20px;
                padding: 2rem;
                text-align: center;
                position: relative;
                overflow: hidden;
                animation: fadeInUp 0.6s ease forwards;
                opacity: 0;
            }
            
            .stat-card:nth-child(1) { animation-delay: 0.4s; }
            .stat-card:nth-child(2) { animation-delay: 0.5s; }
            .stat-card:nth-child(3) { animation-delay: 0.6s; }
            
            .stat-card::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--primary), var(--accent));
            }
            
            .stat-number {
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 3rem;
                font-weight: 900;
                background: linear-gradient(135deg, var(--primary) 0%, #a855f7 50%, var(--accent) 100%);
                background-size: 200% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: gradient-flow 3s ease infinite;
            }
            
            .stat-label {
                color: var(--text-secondary);
                font-size: 0.95rem;
                font-weight: 600;
                margin-top: 0.5rem;
            }
            
            /* CTA Section */
            .cta-section {
                background: linear-gradient(135deg, var(--primary-glow) 0%, var(--card-bg) 50%, rgba(6, 182, 212, 0.1) 100%);
                border: 2px solid var(--primary);
                border-radius: 28px;
                padding: 3rem;
                text-align: center;
                position: relative;
                overflow: hidden;
                animation: fadeInUp 0.6s ease 0.7s forwards, pulse-glow 3s ease infinite;
                opacity: 0;
            }
            
            .cta-title {
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 1.5rem;
                font-weight: 800;
                color: var(--text-primary);
                margin-bottom: 2rem;
            }
            
            .cta-steps {
                display: flex;
                gap: 2rem;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
            }
            
            .cta-step {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.75rem;
            }
            
            .cta-step-number {
                width: 52px;
                height: 52px;
                background: linear-gradient(135deg, var(--primary), var(--accent));
                color: white;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.25rem;
                font-weight: 800;
                box-shadow: 0 8px 20px var(--primary-glow);
                transition: transform 0.3s;
            }
            
            .cta-step:hover .cta-step-number {
                transform: scale(1.1) rotate(5deg);
            }
            
            .cta-step-text {
                color: var(--text-secondary);
                font-weight: 600;
                font-size: 0.95rem;
            }
            
            .cta-arrow {
                font-size: 1.5rem;
                color: var(--primary);
                animation: slideInRight 0.5s ease infinite alternate;
            }
            
            /* Bottom CTA */
            .bottom-cta {
                background: linear-gradient(135deg, var(--success-light), var(--card-bg));
                border: 2px solid var(--success);
                border-radius: 16px;
                padding: 1.5rem 2rem;
                text-align: center;
                margin-top: 2rem;
                animation: fadeInUp 0.6s ease 0.8s forwards;
                opacity: 0;
            }
            
            .bottom-cta-text {
                color: var(--success);
                font-weight: 700;
                font-size: 1.1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
            }
            
            @media (max-width: 768px) {
                .hero-title { font-size: 2.5rem; }
                .premium-features { grid-template-columns: repeat(2, 1fr); }
                .stats-row { grid-template-columns: 1fr; }
                .cta-steps { flex-direction: column; }
                .cta-arrow { display: none; }
            }
        </style>
        
        <div class="commercial-hero">
            <div class="hero-badge">🚀 Powered by AI</div>
            <h1 class="hero-title"><span>TechXcel Pro</span></h1>
            <p class="hero-subtitle">Transform your Excel data into actionable insights with enterprise-grade AI analytics. No coding required.</p>
            <div class="hero-tags">
                <div class="hero-tag"><span class="hero-tag-icon">⚡</span> Lightning Fast</div>
                <div class="hero-tag"><span class="hero-tag-icon">🤖</span> AI-Powered</div>
                <div class="hero-tag"><span class="hero-tag-icon">🔒</span> Secure & Private</div>
                <div class="hero-tag"><span class="hero-tag-icon">📊</span> Auto-Insights</div>
            </div>
        </div>
        
        <div class="premium-features">
            <div class="premium-feature-card">
                <div class="premium-feature-icon">⚡</div>
                <div class="premium-feature-title">Instant Analysis</div>
                <div class="premium-feature-desc">Upload any Excel file and get comprehensive AI-powered insights in seconds</div>
            </div>
            <div class="premium-feature-card">
                <div class="premium-feature-icon">💬</div>
                <div class="premium-feature-title">Chat with Data</div>
                <div class="premium-feature-desc">Ask questions in natural language and get intelligent, contextual answers</div>
            </div>
            <div class="premium-feature-card">
                <div class="premium-feature-icon">🎯</div>
                <div class="premium-feature-title">What-If Scenarios</div>
                <div class="premium-feature-desc">Simulate changes and predict business outcomes before taking action</div>
            </div>
            <div class="premium-feature-card">
                <div class="premium-feature-icon">📊</div>
                <div class="premium-feature-title">Smart Visualizations</div>
                <div class="premium-feature-desc">Beautiful, interactive charts automatically generated from your data</div>
            </div>
        </div>
        
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-number">10x</div>
                <div class="stat-label">Faster Analysis</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">Automated Insights</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">∞</div>
                <div class="stat-label">Possibilities</div>
            </div>
        </div>
        
        <div class="cta-section">
            <div class="cta-title">✨ Get Started in 3 Simple Steps</div>
            <div class="cta-steps">
                <div class="cta-step">
                    <div class="cta-step-number">1</div>
                    <div class="cta-step-text">Upload Excel</div>
                </div>
                <div class="cta-arrow">→</div>
                <div class="cta-step">
                    <div class="cta-step-number">2</div>
                    <div class="cta-step-text">Ask Questions</div>
                </div>
                <div class="cta-arrow">→</div>
                <div class="cta-step">
                    <div class="cta-step-number">3</div>
                    <div class="cta-step-text">Get Insights</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="bottom-cta">
                <div class="bottom-cta-text">Start Now: Upload an Excel file or click "Try Demo Data" in the sidebar</div>
            </div>
            """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
