"""GyaanBuddy - Kid-Safe AI Tutor (English + Hinglish) with interactive diagrams and labs.

Run:  streamlit run app.py
"""
from __future__ import annotations

import base64
import io
import json
import math
import os
import re
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

import content as C
import safety
import tutor_engine
import visuals as V

st.set_page_config(page_title="GyaanBuddy • Kid-Safe AI Science Buddy", page_icon="🧠", layout="wide")

# ----------------------------------------------------------------------------- Attractive Themes & Styling
THEMES = {
    "🌈 Wonder Academy (Nursery - Class 8)": {
        "app_bg": "linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 50%, #fef3c7 100%)",
        "text_color": "#0f172a",
        "heading_color": "#1e1b4b",
        "sidebar_bg": "#ffffff",
        "sidebar_border": "1px solid #e2e8f0",
        "sidebar_text": "#1e293b",
        "hero_bg": "linear-gradient(135deg, #4f46e5 0%, #06b6d4 40%, #10b981 75%, #f59e0b 100%)",
        "hero_shadow": "0 12px 30px rgba(79, 70, 229, 0.25)",
        "hero_border": "none",
        "accent": "#4f46e5",
        "tab_text": "#1e293b",
        "tab_active_text": "#ffffff",
        "card_bg": "#ffffff",
        "card_border": "1px solid #cbd5e1",
        "card_shadow": "0 8px 24px rgba(0, 0, 0, 0.06)",
        "card_hover_shadow": "0 12px 30px rgba(79, 70, 229, 0.15)",
        "badge_bg": "#e0e7ff",
        "badge_text": "#3730a3",
        "badge_border": "1px solid #c7d2fe",
    },
    "🌌 Cosmic Explorer": {
        "app_bg": "radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 60%, #030712 100%)",
        "text_color": "#f8fafc",
        "heading_color": "#ffffff",
        "sidebar_bg": "#090d16",
        "sidebar_border": "1px solid rgba(99, 102, 241, 0.25)",
        "sidebar_text": "#e2e8f0",
        "hero_bg": "linear-gradient(135deg, #4338ca 0%, #6366f1 40%, #a855f7 70%, #06b6d4 100%)",
        "hero_shadow": "0 12px 35px -5px rgba(124, 58, 237, 0.45)",
        "hero_border": "1px solid rgba(255, 255, 255, 0.2)",
        "accent": "#818cf8",
        "tab_text": "#94a3b8",
        "tab_active_text": "#38bdf8",
        "card_bg": "rgba(17, 24, 39, 0.88)",
        "card_border": "1px solid rgba(129, 140, 248, 0.3)",
        "card_shadow": "0 8px 24px rgba(0, 0, 0, 0.35)",
        "card_hover_shadow": "0 12px 32px rgba(129, 140, 248, 0.25)",
        "badge_bg": "rgba(99, 102, 241, 0.25)",
        "badge_text": "#c7d2fe",
        "badge_border": "1px solid rgba(129, 140, 248, 0.4)",
    },
    "☀️ Sunny Playground": {
        "app_bg": "linear-gradient(180deg, #f0fdf4 0%, #f8fafc 100%)",
        "text_color": "#0f172a",
        "heading_color": "#0369a1",
        "sidebar_bg": "#ffffff",
        "sidebar_border": "1px solid #e2e8f0",
        "sidebar_text": "#1e293b",
        "hero_bg": "linear-gradient(135deg, #0284c7 0%, #0ea5e9 40%, #06b6d4 75%, #10b981 100%)",
        "hero_shadow": "0 10px 25px rgba(2, 132, 199, 0.25)",
        "hero_border": "none",
        "accent": "#0284c7",
        "tab_text": "#64748b",
        "tab_active_text": "#0284c7",
        "card_bg": "#ffffff",
        "card_border": "1px solid #cbd5e1",
        "card_shadow": "0 6px 18px rgba(0, 0, 0, 0.05)",
        "card_hover_shadow": "0 10px 24px rgba(2, 132, 199, 0.15)",
        "badge_bg": "#e0f2fe",
        "badge_text": "#0369a1",
        "badge_border": "1px solid #bae6fd",
    },
    "🌿 Emerald Bio-Lab": {
        "app_bg": "radial-gradient(circle at 50% 0%, #064e3b 0%, #022c22 65%, #011a14 100%)",
        "text_color": "#ecfdf5",
        "heading_color": "#6ee7b7",
        "sidebar_bg": "#021a14",
        "sidebar_border": "1px solid rgba(16, 185, 129, 0.3)",
        "sidebar_text": "#d1fae5",
        "hero_bg": "linear-gradient(135deg, #047857 0%, #059669 40%, #10b981 70%, #14b8a6 100%)",
        "hero_shadow": "0 12px 30px rgba(16, 185, 129, 0.4)",
        "hero_border": "1px solid rgba(52, 211, 153, 0.3)",
        "accent": "#10b981",
        "tab_text": "#a7f3d0",
        "tab_active_text": "#34d399",
        "card_bg": "rgba(4, 46, 36, 0.85)",
        "card_border": "1px solid rgba(16, 185, 129, 0.35)",
        "card_shadow": "0 8px 24px rgba(0, 0, 0, 0.35)",
        "card_hover_shadow": "0 12px 30px rgba(16, 185, 129, 0.3)",
        "badge_bg": "rgba(16, 185, 129, 0.25)",
        "badge_text": "#a7f3d0",
        "badge_border": "1px solid rgba(52, 211, 153, 0.4)",
    },
    "⚡ Cyber Scientist": {
        "app_bg": "radial-gradient(ellipse at 80% 20%, #2e0854 0%, #0f051d 60%, #05020a 100%)",
        "text_color": "#fdf4ff",
        "heading_color": "#f472b6",
        "sidebar_bg": "#090212",
        "sidebar_border": "1px solid rgba(236, 72, 153, 0.35)",
        "sidebar_text": "#f5d0fe",
        "hero_bg": "linear-gradient(135deg, #ec4899 0%, #d946ef 35%, #8b5cf6 70%, #06b6d4 100%)",
        "hero_shadow": "0 12px 35px rgba(236, 72, 153, 0.45)",
        "hero_border": "1px solid rgba(244, 114, 182, 0.4)",
        "accent": "#ec4899",
        "tab_text": "#d8b4fe",
        "tab_active_text": "#f472b6",
        "card_bg": "rgba(23, 7, 43, 0.88)",
        "card_border": "1px solid rgba(236, 72, 153, 0.35)",
        "card_shadow": "0 8px 25px rgba(0, 0, 0, 0.45)",
        "card_hover_shadow": "0 12px 32px rgba(236, 72, 153, 0.35)",
        "badge_bg": "rgba(236, 72, 153, 0.25)",
        "badge_text": "#fbcfe8",
        "badge_border": "1px solid rgba(244, 114, 182, 0.45)",
    },
    "🦄 Sunset Wonder": {
        "app_bg": "radial-gradient(circle at 50% 0%, #3b0764 0%, #1f0d3d 50%, #100424 100%)",
        "text_color": "#fff1f2",
        "heading_color": "#fb923c",
        "sidebar_bg": "#17062e",
        "sidebar_border": "1px solid rgba(244, 63, 94, 0.3)",
        "sidebar_text": "#ffe4e6",
        "hero_bg": "linear-gradient(135deg, #ea580c 0%, #f43f5e 40%, #db2777 70%, #7e22ce 100%)",
        "hero_shadow": "0 12px 35px rgba(244, 63, 94, 0.4)",
        "hero_border": "1px solid rgba(251, 113, 133, 0.35)",
        "accent": "#f43f5e",
        "tab_text": "#fecdd3",
        "tab_active_text": "#fda4af",
        "card_bg": "rgba(45, 14, 66, 0.88)",
        "card_border": "1px solid rgba(244, 63, 94, 0.35)",
        "card_shadow": "0 8px 25px rgba(0, 0, 0, 0.4)",
        "card_hover_shadow": "0 12px 32px rgba(244, 63, 94, 0.3)",
        "badge_bg": "rgba(244, 63, 94, 0.25)",
        "badge_text": "#fed7aa",
        "badge_border": "1px solid rgba(251, 146, 60, 0.4)",
    },
}


def apply_theme(theme_name: str):
    """Dynamically inject curated CSS themes into Streamlit."""
    t = THEMES.get(theme_name, THEMES["🌈 Wonder Academy (Nursery - Class 8)"])
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    h1, h2, h3, h4 {{
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: {t['heading_color']} !important;
    }}
    .block-container {{
        padding-top: 1.2rem;
        max-width: 1250px;
    }}
    .stApp {{
        background: {t['app_bg']} !important;
        color: {t['text_color']} !important;
    }}
    [data-testid="stSidebar"] {{
        background: {t['sidebar_bg']} !important;
        border-right: {t['sidebar_border']} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {t['sidebar_text']} !important;
    }}

    /* Ensure sidebar text inputs are crisp white with dark text regardless of dark mode */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="input"],
    [data-testid="stSidebar"] [data-baseweb="base-input"] {{
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 10px !important;
        -webkit-text-fill-color: #0f172a !important;
    }}
    [data-testid="stSidebar"] input::placeholder {{
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
    }}

    /* Clean Streamlit Header - KEEP sidebar toggle button 100% visible on mobile and desktop */
    header[data-testid="stHeader"] {{
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(12px) !important;
        visibility: visible !important;
        height: 3.5rem !important;
        display: flex !important;
        align-items: center !important;
        z-index: 999990 !important;
        border-bottom: 1px solid rgba(203, 213, 225, 0.5) !important;
    }}
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    header button[aria-label*="sidebar" i] {{
        visibility: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #ffffff !important;
        border: 2px solid #6366f1 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
        margin: 4px 0 0 10px !important;
        z-index: 9999999 !important;
        color: #4f46e5 !important;
        min-width: 44px !important;
        min-height: 44px !important;
        cursor: pointer !important;
    }}
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="collapsedControl"] button,
    header button[aria-label*="sidebar" i] {{
        color: #4f46e5 !important;
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: transparent !important;
        border: none !important;
    }}
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg,
    header button[aria-label*="sidebar" i] svg {{
        fill: #4f46e5 !important;
        stroke: #4f46e5 !important;
        width: 24px !important;
        height: 24px !important;
    }}
    .stDeployButton {{display: none !important;}}
    #MainMenu {{visibility: hidden !important; display: none !important;}}
    footer {{visibility: hidden !important; display: none !important;}}

    .hero-banner {{
        background: {t['hero_bg']} !important;
        color: white !important;
        padding: 22px 28px;
        border-radius: 20px;
        box-shadow: {t['hero_shadow']} !important;
        border: {t['hero_border']} !important;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }}
    .hero-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff !important;
    }}
    .hero-sub {{
        font-size: 0.98rem;
        color: #f0fdf4 !important;
        margin-top: 4px;
        font-weight: 500;
    }}
    .xp-pill {{
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 6px 18px;
        border-radius: 30px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: #ffffff !important;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    /* Pill-style Navigation Tabs - 100% visible in all modes */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.92) !important;
        padding: 6px 10px !important;
        border-radius: 18px !important;
        border: 1.5px solid #cbd5e1 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05) !important;
        gap: 8px !important;
        flex-wrap: wrap !important;
        margin-bottom: 12px !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.98rem !important;
        font-weight: 700 !important;
        padding: 8px 16px !important;
        border-radius: 12px !important;
        transition: all 0.2s ease !important;
        color: #1e293b !important; /* High-contrast dark text */
        background: transparent !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: #4f46e5 !important;
        background: rgba(79, 70, 229, 0.1) !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #ffffff !important;
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}

    /* All Main Inputs (Search bar, problem text, text inputs) - Override dark mode */
    input, textarea, 
    [data-baseweb="input"], [data-baseweb="base-input"],
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {{
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 14px !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        -webkit-text-fill-color: #0f172a !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }}
    input::placeholder, textarea::placeholder {{
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        opacity: 1 !important;
    }}
    [data-baseweb="input"]:focus-within {{
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2) !important;
    }}

    /* All Buttons (Search, Clear, Mystery, Spoken chips, Options) - High-contrast & crisp */
    .stButton>button, 
    button[data-testid="baseButton-secondary"] {{
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 14px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 8px 16px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    .stButton>button:hover,
    button[data-testid="baseButton-secondary"]:hover {{
        background: #f8fafc !important;
        color: #4f46e5 !important;
        border-color: #6366f1 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.2) !important;
    }}
    .stButton>button:active {{
        transform: translateY(0) !important;
    }}

    /* Primary Action Buttons (Solve, Check Answer) */
    button[kind="primary"],
    button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
    }}
    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {{
        background: linear-gradient(135deg, #4338ca 0%, #0891b2 100%) !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.42) !important;
    }}

    /* 📥 Universal Responsive Download Buttons (Phone, Tablet, Laptop) */
    [data-testid="stDownloadButton"] {{
        width: 100% !important;
        margin: 4px 0 !important;
    }}
    [data-testid="stDownloadButton"] > button,
    [data-testid="stDownloadButton"] button {{
        width: 100% !important;
        min-height: 44px !important;
        padding: 10px 14px !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1.5px solid #cbd5e1 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        line-height: 1.35 !important;
        white-space: normal !important;
        word-break: normal !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        background: #f8fafc !important;
        color: #4f46e5 !important;
        border-color: #6366f1 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.22) !important;
    }}
    [data-testid="stDownloadButton"] button:active {{
        transform: translateY(0) !important;
    }}
    [data-testid="stDownloadButton"] * {{
        color: inherit !important;
    }}

    /* Audio Recorder Widget - High contrast white card */
    [data-testid="stAudioInput"] {{
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 10px 14px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }}
    [data-testid="stAudioInput"] * {{
        color: #0f172a !important;
    }}

    /* Radio buttons and slider labels */
    [data-testid="stRadio"] label, [data-testid="stRadio"] span, [data-testid="stRadio"] p {{
        color: #1e293b !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSlider"] div, [data-testid="stSlider"] label {{
        color: #1e293b !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="select"] > div {{
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 12px !important;
    }}
    div[data-baseweb="select"] span {{
        color: #0f172a !important;
        font-weight: 600 !important;
    }}

    /* Chat Messages */
    [data-testid="stChatMessage"] {{
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 18px !important;
        padding: 14px 20px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
    }}
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] div {{
        color: #0f172a !important;
        line-height: 1.65 !important;
        font-size: 1rem !important;
    }}

    /* Chat Input Bar */
    [data-testid="stChatInput"] {{
        border-radius: 24px !important;
        border: 1.5px solid #cbd5e1 !important;
        background: #ffffff !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
    }}
    [data-testid="stChatInput"] textarea {{
        background: #ffffff !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        font-size: 1rem !important;
    }}

    .search-card {{
        background: {t['card_bg']};
        border: {t['card_border']};
        border-radius: 18px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: {t['card_shadow']};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .search-card:hover {{
        transform: translateY(-2px);
        box-shadow: {t['card_hover_shadow']};
    }}
    .search-badge {{
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        background: {t['badge_bg']};
        color: {t['badge_text']};
        border: {t['badge_border']};
        margin-bottom: 8px;
    }}
    .fact {{
        background: linear-gradient(135deg, rgba(254, 243, 199, 0.4) 0%, rgba(254, 240, 138, 0.5) 100%);
        border-left: 6px solid #f59e0b;
        padding: 12px 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.08);
        color: #78350f !important;
    }}
    .act {{
        background: linear-gradient(135deg, rgba(209, 250, 229, 0.4) 0%, rgba(167, 243, 208, 0.5) 100%);
        border-left: 6px solid #10b981;
        padding: 12px 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);
        color: #064e3b !important;
    }}
    .formula {{
        background: linear-gradient(135deg, #eff6ff 0%, #e0f2fe 100%);
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 1.15rem;
        font-weight: 700;
        text-align: center;
        border: 1.5px dashed {t['accent']};
        color: #1e3a8a !important;
        white-space: normal;
        word-break: break-word;
    }}
    .game-card {{
        background: {t['card_bg']};
        border: {t['card_border']};
        border-radius: 18px;
        padding: 20px;
        box-shadow: {t['card_shadow']};
    }}

    /* 📱 Ultra-Smooth Mobile Phone Experience */
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 3.8rem !important;
        }}
        [data-testid="stSidebar"] {{
            max-width: 86vw !important;
            width: 320px !important;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.6) !important;
            z-index: 99999999 !important;
        }}
        .hero-banner {{
            padding: 16px 18px !important;
            border-radius: 16px !important;
            gap: 8px !important;
        }}
        .hero-title {{
            font-size: 1.35rem !important;
        }}
        .hero-sub {{
            font-size: 0.88rem !important;
        }}
        .xp-pill {{
            font-size: 0.85rem !important;
            padding: 4px 12px !important;
        }}
        /* Mobile app-style horizontal scrolling navigation tabs */
        .stTabs [data-baseweb="tab-list"] {{
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-width: none !important;
            padding: 6px !important;
            border-radius: 14px !important;
            gap: 6px !important;
        }}
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
            display: none !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            font-size: 0.88rem !important;
            padding: 8px 12px !important;
            white-space: nowrap !important;
            flex-shrink: 0 !important;
        }}
        /* Mobile touch targets (min 44px) */
        .stButton>button, 
        button[data-testid="baseButton-secondary"], 
        button[data-testid="baseButton-primary"] {{
            min-height: 44px !important;
            padding: 10px 14px !important;
            font-size: 0.92rem !important;
            width: 100% !important;
        }}
        /* Make sure SVG diagrams never overflow mobile screen */
        svg {{
            max-width: 100% !important;
            height: auto !important;
        }}
        /* Mobile chat bubbles */
        [data-testid="stChatMessage"] {{
            padding: 10px 14px !important;
            border-radius: 14px !important;
            margin-bottom: 8px !important;
        }}
        /* Selectbox and dropdowns mobile friendly */
        div[data-baseweb="select"] {{
            min-height: 44px !important;
        }}
        /* Clean full width on phone columns */
        [data-testid="column"] {{
            min-width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 6px !important;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # 📱 Phone Back Camera, Live Camera Flip & Mobile Sidebar Enhancement Script
    js_camera = """
    <script>
    (function() {
        // 1. Mobile Camera getUserMedia Interceptor (Back Camera Preference)
        function patchGUM(win) {
            try {
                if (win && win.navigator && win.navigator.mediaDevices && win.navigator.mediaDevices.getUserMedia) {
                    if (!win.__gb_gum_patched) {
                        win.__gb_gum_patched = true;
                        win.__gb_prefer_back_cam = true;
                        const orig = win.navigator.mediaDevices.getUserMedia.bind(win.navigator.mediaDevices);
                        win.navigator.mediaDevices.getUserMedia = function(constraints) {
                            const isMobile = /Android|iPhone|iPad|iPod/i.test(win.navigator.userAgent) || (win.innerWidth <= 768);
                            if (constraints && constraints.video && (win.__gb_prefer_back_cam && isMobile)) {
                                if (typeof constraints.video === 'object') {
                                    constraints.video.facingMode = { ideal: "environment" };
                                } else {
                                    constraints.video = { facingMode: { ideal: "environment" } };
                                }
                            }
                            return orig(constraints);
                        };
                    }
                }
            } catch(e) {}
        }
        patchGUM(window);
        if (window.parent && window.parent !== window) { patchGUM(window.parent); }

        // 2. Attach capture="environment" to file uploaders on mobile devices for direct phone rear camera
        function attachMobileCameraAttrs() {
            try {
                const win = window.parent || window;
                const doc = win.document;
                const isMobile = /Android|iPhone|iPad|iPod/i.test(win.navigator.userAgent) || (win.innerWidth <= 768);
                if (isMobile) {
                    const inputs = doc.querySelectorAll('input[type="file"]');
                    inputs.forEach(inp => {
                        if (!inp.hasAttribute('data-camera-patched')) {
                            inp.setAttribute('data-camera-patched', 'true');
                            if (!inp.accept || inp.accept.includes('image')) {
                                inp.setAttribute('capture', 'environment');
                            }
                        }
                    });
                }
            } catch(e) {}
        }
        setInterval(attachMobileCameraAttrs, 1200);

        // 3. Inject "🔄 Flip Camera (Back / Front)" Button onto every Streamlit Camera Input
        function injectCameraFlipBtn() {
            try {
                const win = window.parent || window;
                const doc = win.document;
                const camWidgets = doc.querySelectorAll('[data-testid="stCameraInput"]');
                camWidgets.forEach(cam => {
                    if (!cam.querySelector('.gb-flip-cam-btn')) {
                        const flipBtn = doc.createElement('button');
                        flipBtn.className = 'gb-flip-cam-btn';
                        flipBtn.type = 'button';
                        flipBtn.innerHTML = '🔄 Switch Camera (Back / Front)';
                        flipBtn.style.cssText = 'display:block;margin:6px auto 10px auto;padding:8px 16px;background:linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);color:#ffffff;font-size:0.85rem;font-weight:700;border:none;border-radius:12px;cursor:pointer;box-shadow:0 4px 14px rgba(79,70,229,0.35);transition:transform 0.15s ease;';
                        flipBtn.onmouseover = function() { flipBtn.style.transform = 'scale(1.02)'; };
                        flipBtn.onmouseout = function() { flipBtn.style.transform = 'scale(1)'; };
                        flipBtn.onclick = function(e) {
                            e.preventDefault();
                            win.__gb_prefer_back_cam = !win.__gb_prefer_back_cam;
                            const video = cam.querySelector('video');
                            if (video && video.srcObject) {
                                const tracks = video.srcObject.getTracks();
                                tracks.forEach(t => t.stop());
                                const facing = win.__gb_prefer_back_cam ? 'environment' : 'user';
                                win.navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: facing } } })
                                    .then(stream => { video.srcObject = stream; })
                                    .catch(err => console.log('Camera switch failed:', err));
                            }
                            flipBtn.innerHTML = win.__gb_prefer_back_cam ? '🔄 Active: Phone Back Camera (Tap to Flip)' : '🔄 Active: Front Selfie Camera (Tap to Flip)';
                        };
                        cam.prepend(flipBtn);
                    }
                });
            } catch(e) {}
        }
        setInterval(injectCameraFlipBtn, 1200);

        // 4. Guaranteed Phone Sidebar Toggle & Mobile Floating Menu Pill
        function toggleSidebar() {
            try {
                const win = window.parent || window;
                const doc = win.document;
                const collBtn = doc.querySelector('[data-testid="stSidebarCollapsedControl"] button')
                             || doc.querySelector('[data-testid="collapsedControl"] button')
                             || doc.querySelector('header button[aria-label*="sidebar" i]')
                             || doc.querySelector('header button');
                const sidebar = doc.querySelector('[data-testid="stSidebar"]') || doc.querySelector('section[data-testid="stSidebar"]');
                
                if (sidebar) {
                    const isOpen = sidebar.getAttribute('aria-expanded') === 'true'
                                || (sidebar.offsetWidth > 50 && sidebar.style.display !== 'none' && !sidebar.style.marginLeft.includes('-'));
                    if (isOpen) {
                        const closeBtn = sidebar.querySelector('button[aria-label*="close" i]') 
                                      || sidebar.querySelector('[data-testid="stSidebarCollapseButton"] button')
                                      || sidebar.querySelector('button');
                        if (closeBtn) {
                            closeBtn.click();
                            return;
                        } else {
                            sidebar.setAttribute('aria-expanded', 'false');
                            sidebar.style.display = 'none';
                            return;
                        }
                    }
                }
                
                if (collBtn) {
                    collBtn.click();
                } else if (sidebar) {
                    sidebar.setAttribute('aria-expanded', 'true');
                    sidebar.style.display = 'block';
                    sidebar.style.visibility = 'visible';
                    sidebar.style.transform = 'none';
                    sidebar.style.position = 'fixed';
                    sidebar.style.top = '0';
                    sidebar.style.left = '0';
                    sidebar.style.height = '100vh';
                    sidebar.style.width = '320px';
                    sidebar.style.maxWidth = '86vw';
                    sidebar.style.zIndex = '99999999';
                    sidebar.style.boxShadow = '0 0 40px rgba(0,0,0,0.6)';
                }
            } catch(e) {}
        }
        window.__gb_toggle_sidebar = toggleSidebar;
        if (window.parent && window.parent !== window) {
            window.parent.__gb_toggle_sidebar = toggleSidebar;
        }

        function injectMobileMenuPill() {
            try {
                const win = window.parent || window;
                const doc = win.document;
                const isMobile = /Android|iPhone|iPad|iPod/i.test(win.navigator.userAgent) || (win.innerWidth <= 768);
                if (isMobile) {
                    if (!doc.getElementById('gb-mobile-sidebar-pill')) {
                        const pill = doc.createElement('button');
                        pill.id = 'gb-mobile-sidebar-pill';
                        pill.type = 'button';
                        pill.innerHTML = '☰ Menu';
                        pill.style.cssText = 'position:fixed;top:8px;left:8px;z-index:99999999;background:#ffffff;color:#4338ca;font-family:Outfit,sans-serif;font-weight:800;font-size:0.85rem;padding:7px 14px;border:2px solid #6366f1;border-radius:20px;box-shadow:0 4px 16px rgba(99,102,241,0.4);cursor:pointer;display:flex;align-items:center;gap:6px;outline:none;-webkit-tap-highlight-color:transparent;';
                        pill.onclick = function(e) {
                            e.preventDefault();
                            e.stopPropagation();
                            toggleSidebar();
                        };
                        doc.body.appendChild(pill);
                    }
                }
            } catch(e) {}
        }
        setInterval(injectMobileMenuPill, 1000);
    })();
    </script>
    """
    st.markdown(js_camera, unsafe_allow_html=True)
    try:
        st.components.v1.html(js_camera, height=0)
    except Exception:
        pass


TXT = {
    "en": dict(
        ask="Ask me anything about science or math…",
        tabs=[
            "💬 Ask Buddy",
            "🌿 General Science",
            "⚡ Physics Lab",
            "🧪 Chemistry Lab",
            "📐 Mathematics",
            "🧍 Human Body",
            "📸 Snap & Solve",
            "🎯 Quiz Arena",
            "👨‍👩‍👧 Parent & Awards",
        ],
        tryit="Try it at home (with an adult)",
        fact="Fun fact", next="Next ➡", prev="⬅ Previous", all="Show all organs",
        mystery="Mystery Science Question of the Day:"
    ),
    "hi": dict(
        ask="Science ya Maths ke baare mein kuch bhi poochho…",
        tabs=[
            "💬 Buddy se poochho",
            "🌿 Saamaanya Vigyan",
            "⚡ Physics Lab",
            "🧪 Chemistry Lab",
            "📐 Ganit (Maths)",
            "🧍 Insaani Sharir",
            "📸 Snap & Solve",
            "🎯 Quiz Arena",
            "👨‍👩‍👧 Parent & Awards",
        ],
        tryit="Ghar par try karo (bade ke saath)",
        fact="Mazedaar baat", next="Agla ➡", prev="⬅ Pichla", all="Saare organs dikhao",
        mystery="Aaj Ka Mazedaar Vigyan Sawaal:"
    )
}

MYSTERIES = {
    "en": [
        ("Why is the sky blue?", "The blue sky mystery 🌌"),
        ("Why do we sneeze?", "The sneeze reflex 🤧"),
        ("How do airplanes fly in the air?", "Airplane flight ✈️"),
        ("Why don't penguins' feet freeze on ice?", "Penguin feet on ice 🐧"),
        ("Why does ice float on water?", "Floating ice cube 🧊"),
    ],
    "hi": [
        ("Aasman neela kyun dikhta hai?", "Neela aasman ka raaz 🌌"),
        ("Humein chheenkh kyun aati hai?", "Chheenkh ka raaz 🤧"),
        ("Hawai jahaz hawa mein kaise udta hai?", "Hawai jahaz ki udaan ✈️"),
        ("Barf paani par kyun tairti hai?", "Barf ka tairna 🧊"),
        ("Taare raat mein kyun timtimate hain?", "Taaron ka timtimana ⭐"),
    ],
}


# ----------------------------------------------------------------------------- helpers
def log(kind: str, subject: str = "", topic: str = "", **extra):
    """Parent dashboard log. Stores topic labels only, never the child's actual words."""
    st.session_state["events"].append({"time": datetime.now().strftime("%H:%M"), "kind": kind,
                                       "subject": subject, "topic": topic, **extra})


def show_svg(svg: str, width: int = 440):
    st.markdown(V.svg_to_html(svg, width), unsafe_allow_html=True)


def show_visual(spec: str, lang: str, key: str):
    out = V.render_spec(spec, lang)
    if not out:
        return
    kind, obj = out
    if kind == "svg":
        show_svg(obj, 450)
    else:
        st.plotly_chart(obj, width="stretch", key=key)


def clean_for_speech(text: str) -> str:
    """Strip markdown formatting, HTML tags, and emojis for clear, pleasant voiceover."""
    t = re.sub(r'<[^>]+>', '', text)
    t = re.sub(r'[*_#`~]', '', t)
    t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
    t = re.sub(r'^[ \t]*[-*•]\s+', '', t, flags=re.MULTILINE)
    t = re.sub(r'[\U00010000-\U0010ffff]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


@st.cache_data(show_spinner=False)
def generate_audio_b64(text: str, lang: str = "en") -> str | None:
    """Generate high-quality spoken MP3 audio via gTTS with in-memory caching."""
    clean = clean_for_speech(text)
    if not clean:
        return None
    try:
        from gtts import gTTS
        fp = io.BytesIO()
        tts_lang = "hi" if lang == "hi" else "en"
        tts = gTTS(text=clean, lang=tts_lang, slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        return base64.b64encode(fp.read()).decode("utf-8")
    except Exception:
        return None


def read_aloud(text: str, key: str = "ra", lang: str = "en"):
    """Bilingual voiceover with instant HTML5 audio playback and resilient Web Speech fallback."""
    clean = clean_for_speech(text)
    if not clean:
        return
    b64_audio = generate_audio_b64(text, lang)
    audio_src = f"data:audio/mp3;base64,{b64_audio}" if b64_audio else ""
    speech_lang = "hi-IN" if lang == "hi" else "en-US"
    clean_json = json.dumps(clean)
    speech_lang_json = json.dumps(speech_lang)

    html_code = f"""
    <div style="display:flex;align-items:center;gap:10px;margin-top:2px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
      <button id="btn_{key}" onclick="togglePlay_{key}()" style="display:inline-flex;align-items:center;gap:6px;border:none;background:#e3f2fd;color:#0d47a1;border-radius:18px;padding:6px 14px;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.15s ease-in-out;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
        <span id="icon_{key}">🔊</span> <span id="label_{key}">{'Suniye (Audio)' if lang == 'hi' else 'Read aloud'}</span>
      </button>
      <span id="status_{key}" style="font-size:12px;color:#78909c;"></span>
    </div>
    <audio id="player_{key}" src="{audio_src}" preload="auto"></audio>
    <script>
      const player_{key} = document.getElementById("player_{key}");
      const btn_{key} = document.getElementById("btn_{key}");
      const icon_{key} = document.getElementById("icon_{key}");
      const label_{key} = document.getElementById("label_{key}");
      const status_{key} = document.getElementById("status_{key}");
      let isPlaying_{key} = false;

      function setSpeaking_{key}(speaking) {{
        isPlaying_{key} = speaking;
        if (speaking) {{
          btn_{key}.style.background = "#ffebee";
          btn_{key}.style.color = "#c62828";
          icon_{key}.textContent = "⏹️";
          label_{key}.textContent = "{'Rokiye' if lang == 'hi' else 'Stop reading'}";
          status_{key}.textContent = "Speaking…";
        }} else {{
          btn_{key}.style.background = "#e3f2fd";
          btn_{key}.style.color = "#0d47a1";
          icon_{key}.textContent = "🔊";
          label_{key}.textContent = "{'Suniye (Audio)' if lang == 'hi' else 'Read aloud'}";
          status_{key}.textContent = "";
        }}
      }}

      function togglePlay_{key}() {{
        if (isPlaying_{key}) {{
          stopAll_{key}();
        }} else {{
          playAll_{key}();
        }}
      }}

      function stopAll_{key}() {{
        if (player_{key}) {{
          player_{key}.pause();
          player_{key}.currentTime = 0;
        }}
        if ('speechSynthesis' in window) {{
          window.speechSynthesis.cancel();
        }}
        setSpeaking_{key}(false);
      }}

      function playAll_{key}() {{
        if (player_{key} && player_{key}.src && player_{key}.src.length > 50) {{
          player_{key}.currentTime = 0;
          player_{key}.play().then(() => {{
            setSpeaking_{key}(true);
          }}).catch(err => {{
            speakBrowser_{key}();
          }});
        }} else {{
          speakBrowser_{key}();
        }}
      }}

      if (player_{key}) {{
        player_{key}.onended = () => setSpeaking_{key}(false);
        player_{key}.onerror = () => speakBrowser_{key}();
      }}

      function speakBrowser_{key}() {{
        if (!('speechSynthesis' in window)) {{
          status_{key}.textContent = "Audio unsupported";
          return;
        }}
        window.speechSynthesis.resume();
        window.speechSynthesis.cancel();
        setTimeout(() => {{
          const u = new SpeechSynthesisUtterance({clean_json});
          u.lang = {speech_lang_json};
          u.rate = 0.95;
          const voices = window.speechSynthesis.getVoices();
          if (voices && voices.length > 0) {{
            const pref = voices.find(v => v.lang === {speech_lang_json} || v.lang.startsWith({json.dumps(speech_lang[:2])}));
            if (pref) u.voice = pref;
          }}
          u.onstart = () => setSpeaking_{key}(true);
          u.onend = () => setSpeaking_{key}(false);
          u.onerror = () => setSpeaking_{key}(false);
          window.speechSynthesis.speak(u);
        }}, 60);
      }}
    </script>
    """
    components.html(html_code, height=44)
def transcribe_audio(audio_file, lang: str = "en") -> str:
    """Transcribe audio from st.audio_input using Google Speech Recognition (free, kid-friendly)."""
    if not audio_file:
        return ""
    try:
        import speech_recognition as sr
        import io
        audio_bytes = audio_file.getvalue() if hasattr(audio_file, "getvalue") else audio_file.read()
        if not audio_bytes or len(audio_bytes) < 400:
            return ""
        bio = io.BytesIO(audio_bytes)
        r = sr.Recognizer()
        r.energy_threshold = 280
        r.dynamic_energy_threshold = True
        with sr.AudioFile(bio) as source:
            audio_data = r.record(source)
            target_lang = "hi-IN" if lang == "hi" else "en-IN"
            text = r.recognize_google(audio_data, language=target_lang)
            return text.strip()
    except Exception:
        return ""


def render_whatsapp_voice_bar(lang: str):
    """Voice status banner for young students who can't write, directing them to the microphone recorder."""
    title = "🎙️ Voice Question Mode (Nursery to Class 8)" if lang == "en" else "🎙️ Awaaz Se Poochhein (Nursery se 8th Class)"
    desc = "Can't write? Use the microphone recorder below to speak, or tap a quick question chip!" if lang == "en" else "Likhna mushkil hai? Neeche diye mic se bol kar poochhein ya buttons dabayein!"
    badge = "Tap Mic Below" if lang == "en" else "Neeche Mic Dabayein"
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(0, 168, 132, 0.12), rgba(14, 165, 233, 0.12)); border: 1.5px solid rgba(0, 168, 132, 0.35); border-radius: 16px; padding: 12px 18px; display: flex; align-items: center; justify-content: space-between; margin: 6px 0 14px 0;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 26px; background: #00a884; color: white; border-radius: 50%; width: 42px; height: 42px; display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,168,132,0.35);">🎙️</span>
        <div>
          <div style="font-weight: 700; font-size: 1.02rem; color: #0f172a;">{title}</div>
          <div style="font-size: 0.88rem; color: #475569;">{desc}</div>
        </div>
      </div>
      <div style="font-size: 0.82rem; font-weight: 700; color: #00a884; background: rgba(0,168,132,0.15); padding: 5px 12px; border-radius: 20px; white-space: nowrap;">
        ⚡ {badge}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ----------------------------------------------------------------------------- gamification engine
def get_level(xp: int) -> tuple[int, str, str, float]:
    """Returns (level_num, title_en, title_hi, progress_to_next)."""
    if xp < 50:
        return 1, "🥉 Curious Spark", "🥉 Khoji Sitara", min(1.0, xp / 50.0)
    elif xp < 150:
        return 2, "🥈 Lab Apprentice", "🥈 Chhota Scientist", min(1.0, (xp - 50) / 100.0)
    elif xp < 300:
        return 3, "🥇 Science Explorer", "🥇 Vigyan Champion", min(1.0, (xp - 150) / 150.0)
    else:
        return 4, "🏆 Einstein Junior", "🏆 Super Scientist", 1.0


def add_xp(points: int, reason: str = "", badge_id: str | None = None, badge_name: str | None = None):
    """Add XP, check for level ups, and award badges."""
    ss = st.session_state
    old_lvl = get_level(ss["xp"])[0]
    ss["xp"] += points
    new_lvl = get_level(ss["xp"])[0]
    if new_lvl > old_lvl:
        st.balloons()
        st.toast(f"🎉 LEVEL UP! You reached Level {new_lvl}: {get_level(ss['xp'])[1]}!", icon="🚀")
    elif points > 0:
        st.toast(f"⭐ +{points} XP: {reason}", icon="✨")
    if badge_id and badge_id not in ss["badges"]:
        ss["badges"].append(badge_id)
        if badge_name:
            st.toast(f"🏅 Badge Unlocked: {badge_name}!", icon="🏆")


def generate_certificate_html(name: str, xp: int, lang: str = "en") -> str:
    clean_name = name.strip() or ("Junior Scientist" if lang == "en" else "Chhota Scientist")
    lvl = get_level(xp)[1 if lang == "en" else 2]
    title = "CERTIFICATE OF SCIENTIFIC EXCELLENCE" if lang == "en" else "VIGYAN PRATIBHA PRAMAN PATRA"
    sub = ("This official certificate is proudly presented for outstanding curiosity, mastery of science concepts, and interactive lab excellence."
           if lang == "en" else "Yeh praman patra vigyan mein behtareen khoj, lab experiments aur shandar seekh ke liye diya jaata hai.")

    return f"""
    <div style="max-width:720px;margin:15px auto;padding:32px;background:#fffdf7;border:8px double #d97706;border-radius:18px;box-shadow:0 8px 24px rgba(217,119,6,0.15);font-family:'Trebuchet MS',Georgia,serif;text-align:center;">
      <div style="font-size:32px;margin-bottom:4px;">🏆 🧠 🔬</div>
      <div style="letter-spacing:3px;color:#92400e;font-size:13px;font-weight:700;">GYAANBUDDY SCIENCE ACADEMY</div>
      <h2 style="color:#78350f;font-size:24px;margin:8px 0 10px 0;text-transform:uppercase;border-bottom:2px solid #f59e0b;padding-bottom:10px;">{title}</h2>
      <p style="font-style:italic;color:#64748b;font-size:13px;margin:12px 0 6px 0;">Awarded with pride to:</p>
      <h1 style="font-size:34px;color:#0284c7;margin:4px 0 10px 0;font-family:Georgia,serif;text-decoration:underline;text-decoration-color:#f59e0b;">{clean_name}</h1>
      <p style="color:#334155;font-size:14px;line-height:1.6;max-width:580px;margin:0 auto 15px auto;">
        {sub}<br>
        Achieved Rank <b style="color:#d97706;">{lvl}</b> with an outstanding score of <b style="color:#059669;">{xp} Science XP</b> across Human Anatomy, Physics Lab, Chemistry Lab and Quizzes!
      </p>
      <div style="display:flex;justify-content:space-around;margin-top:20px;padding-top:14px;border-top:1px dashed #d97706;">
        <div>
          <div style="font-size:24px;">🏅</div>
          <div style="font-size:11px;font-weight:bold;color:#78350f;">OFFICIAL GOLD SEAL</div>
          <div style="font-size:9px;color:#94a3b8;">VERIFIED KID-SAFE</div>
        </div>
        <div>
          <div style="font-family:'Brush Script MT',cursive,sans-serif;font-size:22px;color:#1e3a8a;">Mahdi Nawaz</div>
          <div style="font-size:11px;font-weight:bold;color:#334155;">FOUNDER &amp; SCIENCE MENTOR</div>
          <div style="font-size:9px;color:#94a3b8;">{datetime.now().strftime("%B %Y")}</div>
        </div>
      </div>
    </div>
    """


# ----------------------------------------------------------------------------- Topic Search Hub Engine
def build_search_index() -> list[dict]:
    """Unified curriculum search index across 68+ interactive topics."""
    index = []
    # 1. Body parts
    for b in C.BODY_PARTS:
        index.append({
            "category_en": "🧍 Human Body",
            "category_hi": "🧍 Insaani Sharir",
            "icon": "🧍",
            "title_en": b["en_name"],
            "title_hi": b["hi_name"],
            "desc_en": b["en"] + " " + b.get("fact_en", ""),
            "desc_hi": b["hi"] + " " + b.get("fact_hi", ""),
            "spec": f"body:{b['key']}",
            "keywords": b.get("keywords", []) + [b["en_name"], b["hi_name"], b["system"], "organ", "body", "sharir"]
        })
    # Realistic Kidney Cross-Section
    index.append({
        "category_en": "🔬 Medical Anatomy",
        "category_hi": "🔬 Medical Anatomy",
        "icon": "🫘",
        "title_en": "Realistic Kidney Anatomy &amp; Nephron Filter",
        "title_hi": "Gurde Ki Realistic Banawat &amp; Nephron Filter",
        "desc_en": "Medical-grade cross-section of the human kidney: Renal Cortex, Medullary Pyramids, Pelvis, Ureter, and 1,000,000+ microscopic Nephron blood filters.",
        "desc_hi": "Insaani gurde ki andaruni banawat: Renal Cortex, Pyramids, Pelvis, Ureter aur 10 lakh+ microscopic Nephrons jo khoon filter karte hain.",
        "spec": "body:kidneys:detail",
        "keywords": ["kidney", "kidneys", "gurde", "gurda", "nephron", "cortex", "pyramid", "filter", "urine", "realistic", "cross section"]
    })
    # 2. Physics Experiments
    for k, p in C.PHYSICS.items():
        index.append({
            "category_en": "⚡ Physics Lab",
            "category_hi": "⚡ Physics Lab",
            "icon": "⚡",
            "title_en": p["title_en"],
            "title_hi": p["title_hi"],
            "desc_en": p["en"] + " Formula: " + p.get("formula", ""),
            "desc_hi": p["hi"] + " Formula: " + p.get("formula", ""),
            "spec": f"physics:{k}",
            "keywords": p.get("keywords", []) + [p["title_en"], p["title_hi"], "physics", "experiment", "lab", "formula"]
        })
    # 3. Chemistry - Atoms (All 20 elements)
    for z, el in C.ELEMENT_BY_Z.items():
        use = C.ELEMENT_USE.get(z, ("", ""))
        index.append({
            "category_en": "⚛️ Chemistry: Atoms",
            "category_hi": "⚛️ Chemistry: Parmanu",
            "icon": "⚛️",
            "title_en": f"{el[2]} ({el[1]}) • Atomic #{z}",
            "title_hi": f"{el[2]} ({el[1]}) • Parmanu Sankhya {z}",
            "desc_en": f"Element {el[2]} has {z} protons and {el[3]} neutrons. {use[0]}",
            "desc_hi": f"{el[2]} tatva mein {z} protons aur {el[3]} neutrons hote hain. {use[1]}",
            "spec": f"chem:atom:{z}",
            "keywords": [el[2], el[1], "atom", "parmanu", "element", "tatva", str(z), "electron", "proton"]
        })
    # 4. Chemistry - Molecules
    for k, m in C.MOLECULES.items():
        index.append({
            "category_en": "💧 Chemistry: Molecules",
            "category_hi": "💧 Chemistry: Anu",
            "icon": "💧",
            "title_en": f"{m['name_en']} ({m['formula']})",
            "title_hi": f"{m['name_hi']} ({m['formula']})",
            "desc_en": m["en"],
            "desc_hi": m["hi"],
            "spec": f"chem:mol:{k}",
            "keywords": [m["name_en"], m["name_hi"], m["formula"], "molecule", "anu", "compound"]
        })
    # 5. Chemistry - States of Matter
    for k, s in C.STATES.items():
        index.append({
            "category_en": "🧊 Chemistry: States of Matter",
            "category_hi": "🧊 Chemistry: Padarth Ki Awastha",
            "icon": "🧊",
            "title_en": s["en_name"],
            "title_hi": s["hi_name"],
            "desc_en": s["en"],
            "desc_hi": s["hi"],
            "spec": f"chem:states:{k}",
            "keywords": [s["en_name"], s["hi_name"], "state", "matter", "solid", "liquid", "gas", "ice", "steam"]
        })
    # 6. Chemistry - pH Substances
    for k, (en_sub, hi_sub, ph_val) in C.PH_SUBSTANCES.items():
        acid_base = "Acid" if ph_val < 7 else ("Base" if ph_val > 7 else "Neutral")
        index.append({
            "category_en": "🍋 Chemistry: pH Scale",
            "category_hi": "🍋 Chemistry: pH Scale",
            "icon": "🍋",
            "title_en": f"{en_sub} (pH {ph_val:g}) • {acid_base}",
            "title_hi": f"{hi_sub} (pH {ph_val:g}) • {acid_base}",
            "desc_en": f"{en_sub} has a pH of {ph_val:g}, classifying it as a scientific {acid_base}.",
            "desc_hi": f"{hi_sub} ka pH {ph_val:g} hai, yeh ek {acid_base} padarth hai.",
            "spec": f"chem:ph:{k}",
            "keywords": [en_sub, hi_sub, "ph", "acid", "base", "alkaline", str(ph_val), "scale"]
        })
    # Chemistry - Metals & Non-Metals in Daily Life (Class 8 Science)
    index.append({
        "category_en": "🥇 Chemistry: Materials",
        "category_hi": "🥇 Chemistry: Padarth",
        "icon": "🥇",
        "title_en": "Metals & Non-Metals in Daily Life",
        "title_hi": "Metals aur Non-Metals (Dhaatu aur Adhaatu)",
        "desc_en": "Importance of metals (iron, copper, aluminium, gold) and non-metals (oxygen, carbon, nitrogen, chlorine, iodine) in everyday life.",
        "desc_hi": "Rozmarra ke jeevan mein dhaatu (loha, taamba) aur adhaatu (oxygen, nitrogen, iodine) ka upyog.",
        "spec": "chem:metals",
        "keywords": ["metals", "metal", "nonmetals", "nonmetal", "non-metals", "non-metal", "dhaatu", "dhatu", "adhaatu",
                     "importance of metals and non-metals in daily life", "daily life", "iron", "copper", "gold", "aluminium",
                     "oxygen", "nitrogen", "chlorine", "iodine", "malleable", "ductile", "conductor"]
    })
    # 7. Virtual Lab Reactions
    reactions = [
        ("reaction:baking_soda", "🌋 Volcano Eruption (Baking Soda + Vinegar)", "🌋 Jwalamukhi (Baking Soda + Sirka)",
         "Sodium Bicarbonate reacts with Acetic Acid to form Carbon Dioxide bubbles!",
         "Sodium Bicarbonate aur Acetic Acid react karke CO2 bubbles banate hain!",
         ["volcano", "reaction", "baking soda", "vinegar", "sirka"]),
        ("reaction:rusting", "🔩 Iron Rusting (Oxidation)", "🔩 Lohe par Jang Lagna",
         "Iron reacts with oxygen and water to produce red-brown iron oxide (rust).",
         "Loha hawa ki oxygen aur paani se milkar rust (jang) banata hai.",
         ["rust", "rusting", "iron", "jang", "oxidation"]),
        ("reaction:neutralization", "🧪 Acid + Base Neutralization", "🧪 Acid + Base Neutralization",
         "Hydrochloric acid and Sodium Hydroxide react to produce salt water and heat.",
         "Acid aur base milkar salt water banate hain aur heat chhodte hain.",
         ["neutralization", "salt", "acid", "base"]),
        ("reaction:elephant_toothpaste", "🐘 Elephant Toothpaste (Rapid Decomposition)", "🐘 Elephant Toothpaste Reaction",
         "Hydrogen peroxide decomposes rapidly with yeast catalyst releasing dramatic warm oxygen foam!",
         "Hydrogen peroxide catalyst ki madad se jald se oxygen foam banata hai!",
         ["elephant toothpaste", "foam", "catalyst", "peroxide"])
    ]
    for spec, t_en, t_hi, d_en, d_hi, kws in reactions:
        index.append({
            "category_en": "🧪 Virtual Chemical Reaction",
            "category_hi": "🧪 Virtual Chemical Reaction",
            "icon": "🧪",
            "title_en": t_en,
            "title_hi": t_hi,
            "desc_en": d_en,
            "desc_hi": d_hi,
            "spec": spec,
            "keywords": kws + ["reaction", "chemistry", "experiment"]
        })
    # 8. Vital signs monitor
    index.append({
        "category_en": "💓 Medical Science",
        "category_hi": "💓 Medical Science",
        "icon": "💓",
        "title_en": "Vital Signs Monitor (ECG & Pulse)",
        "title_hi": "Vital Signs Monitor (ECG & Dhadkan)",
        "desc_en": "Real-time electrocardiogram (ECG) showing cardiac electrical activity and heart rate dynamics.",
        "desc_hi": "Real-time ECG monitor jo dil ki dhadkan aur cardiac rhythm ko darshata hai.",
        "spec": "vital:ecg",
        "keywords": ["ecg", "pulse", "vital", "monitor", "heartbeat", "dhadkan", "cardiac"]
    })
    # 9. Quizzes
    for i, q in enumerate(C.QUIZ):
        index.append({
            "category_en": "🎯 Science Quiz",
            "category_hi": "🎯 Vigyan Quiz",
            "icon": "🎯",
            "title_en": f"Quiz Question {i+1}: {q['q_en']}",
            "title_hi": f"Quiz Sawaal {i+1}: {q['q_hi']}",
            "desc_en": f"Answer: {q['options'][q['answer']]} • {q['ex_en']}",
            "desc_hi": f"Jawab: {q['options'][q['answer']]} • {q['ex_hi']}",
            "spec": "quiz",
            "keywords": ["quiz", "question", "sawaal", "trivia", "test"] + q["q_en"].split()
        })
    # 10. Mathematics (Class 1 to 8)
    if hasattr(C, "MATH_TOPICS"):
        math_specs = {
            "circle": ("math:circle", "⭕"),
            "rectangle": ("math:rectangle", "📐"),
            "triangle": ("math:triangle", "🔺"),
            "cylinder": ("math:cylinder", "🥫"),
            "pythagoras": ("math:pythagoras", "⭐"),
            "fractions": ("math:fractions", "🍕"),
            "algebra": ("math:algebra", "⚖️"),
        }
        for k, m in C.MATH_TOPICS.items():
            spec, icon = math_specs.get(k, (f"math:{k}", "📐"))
            index.append({
                "category_en": "📐 Mathematics Lab",
                "category_hi": "📐 Ganit Lab",
                "icon": icon,
                "title_en": m["title_en"],
                "title_hi": m["title_hi"],
                "desc_en": m["en"] + " Formula: " + m.get("formula", ""),
                "desc_hi": m["hi"] + " Formula: " + m.get("formula", ""),
                "spec": spec,
                "keywords": m.get("keywords", []) + ["mathematics", "math", "ganit", "formula", "mensuration", "algebra", "geometry"]
            })
    # 11. General Science (Trees, Plants & Animals)
    if hasattr(C, "NATURE_TOPICS"):
        nature_specs = {
            "tree_parts": ("nature:tree", "🌳"),
            "photosynthesis": ("nature:photosynthesis", "☀️"),
            "butterfly_lifecycle": ("nature:butterfly", "🦋"),
            "frog_lifecycle": ("nature:butterfly", "🐸"),
            "animal_diets": ("nature:foodchain", "🦁"),
            "food_chain": ("nature:foodchain", "🌱"),
        }
        for k, n in C.NATURE_TOPICS.items():
            spec, icon = nature_specs.get(k, ("nature:tree", "🌿"))
            index.append({
                "category_en": "🌿 General Science (Trees & Animals)",
                "category_hi": "🌿 Saamaanya Vigyan (Ped aur Jaanwar)",
                "icon": icon,
                "title_en": n["title_en"],
                "title_hi": n["title_hi"],
                "desc_en": n["en"],
                "desc_hi": n["hi"],
                "spec": spec,
                "keywords": n.get("keywords", []) + ["general science", "nature", "trees", "plants", "animals", "wildlife", "science"]
            })
    return index

SEARCH_INDEX = build_search_index()


def search_topics(q: str, limit: int = 8) -> list[dict]:
    """Search curriculum topics by keyword, title, category, or description."""
    if not q or not q.strip():
        return []
    terms = q.lower().strip().split()
    scored = []
    for item in SEARCH_INDEX:
        blob = " ".join([
            item["title_en"], item["title_hi"],
            item["desc_en"], item["desc_hi"],
            item["category_en"], item["category_hi"]
        ] + item["keywords"]).lower()
        score = 0
        for term in terms:
            if term in item["title_en"].lower() or term in item["title_hi"].lower():
                score += 5
            elif any(term == kw.lower() for kw in item["keywords"]):
                score += 4
            elif any(term in kw.lower() for kw in item["keywords"]):
                score += 3
            elif term in blob:
                score += 1
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:limit]]


def handle_section_query(q_text: str, sec_label: str, lang: str, age: str = "10-12", api_key: str | None = None, model: str | None = None):
    """Solve student query in any section, append to chat history (like ChatGPT), and persist permanently."""
    history = [{"q": a["q"], "a": a["text"]} for a in st.session_state.get("messages", [])
               if a.get("role") == "assistant" and a.get("q") and not a.get("blocked")]
    ans = tutor_engine.answer(q_text, lang, age, history, api_key, model)

    # 1. Update session state messages
    st.session_state["messages"].append({
        "role": "user",
        "text": q_text,
        "subject": sec_label
    })
    st.session_state["messages"].append({
        "role": "assistant",
        "text": ans.text,
        "visual": ans.visual,
        "q": q_text,
        "subject": sec_label,
        "topic": ans.topic or sec_label,
        "notice": ans.notice,
        "blocked": ans.blocked
    })

    # 2. Persist to data/chat_history.jsonl & training dataset
    try:
        import student_memory
        grade = str(st.session_state.get("class_level", "5"))
        student_memory.record_student_chat(
            grade=f"Class {grade}" if grade.isdigit() else grade,
            lang=lang,
            question=q_text,
            answer_text=ans.text,
            subject=sec_label,
            topic=ans.topic or sec_label,
            xp=15,
            visual=ans.visual
        )
    except Exception:
        pass

    log("question", sec_label, ans.topic or sec_label, mode=ans.mode)
    add_xp(15, f"Researched {sec_label} question!")
    return ans


def get_grade_tier(class_level: str | None = None) -> tuple[str, str, str]:
    """Determine curriculum stage:
    - 'early': Nursery, LKG, UKG, Class 1, Class 2 (Ages 3-7)
    - 'primary': Class 3, Class 4, Class 5 (Ages 8-10)
    - 'middle': Class 6, Class 7, Class 8 (Ages 11-14)
    Returns (tier_id, tier_name_en, tier_name_hi).
    """
    if class_level is None:
        class_level = str(st.session_state.get("class_level", "5")).replace("Class ", "")
    c_str = str(class_level).strip()
    if c_str in ("Nursery", "LKG", "UKG", "1", "2"):
        return "early", f"Class {c_str} • Early Explorers (Nursery - Class 2)", f"Class {c_str} • Nannhe Vaigyanik (Nursery se 2nd)"
    elif c_str in ("3", "4", "5"):
        return "primary", f"Class {c_str} • Junior Discoverers (Class 3 - 5)", f"Class {c_str} • Junior Khoji (3rd se 5th)"
    else:
        return "middle", f"Class {c_str} • Senior Scholars (Class 6 - 8)", f"Class {c_str} • Senior Vigyan (6th se 8th)"


def render_class_tier_header(sec_id: str, lang: str) -> str:
    """Prominent badge + Quick Class Switcher dropdown inside every lab tab."""
    tier_id, name_en, name_hi = get_grade_tier()
    c_badge, c_picker = st.columns([2.6, 1.4])
    with c_badge:
        st.markdown(f"""
        <div style="display:inline-flex;align-items:center;gap:8px;padding:6px 14px;background:rgba(99,102,241,0.12);border:1.5px solid rgba(99,102,241,0.3);border-radius:20px;font-weight:700;color:#3730a3;font-size:0.9rem;margin-bottom:8px;">
          <span>🎓</span>
          <span>{name_en if lang == 'en' else name_hi}</span>
        </div>
        """, unsafe_allow_html=True)
    with c_picker:
        opts = ["Nursery", "LKG", "UKG", "1", "2", "3", "4", "5", "6", "7", "8"]
        curr = str(st.session_state.get("class_level", "5")).replace("Class ", "")
        idx = opts.index(curr) if curr in opts else 5
        q_key = f"{sec_id}_class_quick_switch"
        if q_key in st.session_state and st.session_state[q_key] != curr:
            st.session_state[q_key] = curr
        picked = st.selectbox(
            "Quick Class Switcher",
            opts,
            index=idx,
            key=q_key,
            label_visibility="collapsed",
            help="Switch grade level to view class-specific curriculum and experiments!"
        )
        if picked != curr:
            st.session_state["class_level"] = picked
            st.rerun()
    return tier_id


def render_section_tools(sec_id: str, sec_label: str, placeholder: str, lang: str, age: str = "10-12", api_key: str | None = None, model: str | None = None) -> str:
    """Standardized tool bar for every section:
    1. Text search bar with direct Search button
    2. Camera drawer (upload, click photo, screenshot paste via Clipboard)
    3. Voice drawer (speak question)
    Every search or question solved is automatically saved to chat history like ChatGPT!
    """
    c_srch, c_btn, c_cam, c_mic = st.columns([5.2, 1.4, 1.2, 1.2])
    with c_srch:
        query = st.text_input(
            f"Search in {sec_label}",
            value=st.session_state.get(f"{sec_id}_search", ""),
            placeholder=placeholder,
            key=f"{sec_id}_search_bar",
            label_visibility="collapsed"
        )
        st.session_state[f"{sec_id}_search"] = query
    with c_btn:
        search_clicked = st.button("🔍 " + ("Search" if lang == "en" else "Khojein"), key=f"{sec_id}_btn_search", width="stretch", type="primary")

    with c_cam:
        cam_active = st.session_state.get(f"{sec_id}_show_cam", False)
        if st.button("📷 " + ("Camera" if lang == "en" else "Camera"), key=f"{sec_id}_cam_toggle", width="stretch"):
            st.session_state[f"{sec_id}_show_cam"] = not cam_active
            st.session_state[f"{sec_id}_show_mic"] = False
            st.rerun()

    with c_mic:
        mic_active = st.session_state.get(f"{sec_id}_show_mic", False)
        if st.button("🎙️ " + ("Voice" if lang == "en" else "Awaaz"), key=f"{sec_id}_mic_toggle", width="stretch"):
            st.session_state[f"{sec_id}_show_mic"] = not mic_active
            st.session_state[f"{sec_id}_show_cam"] = False
            st.rerun()

    # Search Triggered
    if search_clicked and query.strip():
        with st.spinner("Searching and solving… 🔍" if lang == "en" else "Khoj aur hal ho raha hai… 🔍"):
            ans = handle_section_query(query.strip(), sec_label, lang, age, api_key, model)
            st.session_state[f"{sec_id}_sol"] = {"q": query.strip(), "text": ans.text, "visual": ans.visual}

    # Camera, Upload & Screenshot Paste Drawer
    if st.session_state.get(f"{sec_id}_show_cam", False):
        with st.container(border=True):
            st.markdown("##### 📷 " + ("Question Photo Solver (Phone Back Camera, Live Camera or Screenshot)" if lang == "en" else "Photo Sawaal Solver (Phone Back Camera, Live Camera ya Screenshot)"))
            st.caption("📱 " + ("On phone: Use 'Phone Back Camera' to directly snap photos of your notebook or textbook with autofocus!" if lang == "en" else "Phone par: Notebook ya kitaab ke page ki photo lene ke liye 'Phone Back Camera' use karein!"))
            cc1, cc2 = st.columns([1.1, 1.1])
            with cc1:
                st.markdown("**📸 " + ("Phone Back Camera (Notebook & Book Photos)" if lang == "en" else "Phone Back Camera (Copy ya Kitaab)") + "**")
                file_img = st.file_uploader("Take photo with phone back camera or upload photo", type=["png", "jpg", "jpeg", "webp"], key=f"{sec_id}_file_widget")
            with cc2:
                st.markdown("**🤳 " + ("Selfie / Live Webcam" if lang == "en" else "Webcam / Live Camera") + "**")
                cam_img = st.camera_input("Take photo of question", key=f"{sec_id}_cam_widget")
                try:
                    import streamlit_paste_button as spb
                    p_res = spb.paste_image_button(
                        label="📋 " + ("Paste Screenshot (Win+Shift+S)" if lang == "en" else "Screenshot Paste Karein"),
                        text_color="#ffffff",
                        background_color="#4f46e5",
                        hover_background_color="#4338ca",
                        key=f"{sec_id}_paste_widget"
                    )
                    if p_res.image_data is not None:
                        buf = io.BytesIO()
                        p_res.image_data.save(buf, format="PNG")
                        buf.seek(0)
                        buf.type = "image/png"
                        st.session_state[f"{sec_id}_pasted_buf"] = buf
                except Exception:
                    pass

            pasted_pic = st.session_state.get(f"{sec_id}_pasted_buf")
            active_img = cam_img or file_img or pasted_pic
            if active_img:
                st.image(active_img, caption="✅ Photo Ready", width=320)
                if st.button("🚀 " + ("Solve Question in Photo Now" if lang == "en" else "Photo ka Sawaal Hal Karein"), key=f"{sec_id}_btn_solve_photo", type="primary"):
                    q_prob = query.strip() or f"{sec_label} question"
                    try:
                        import pytesseract
                        from PIL import Image
                        active_img.seek(0)
                        ocr_txt = pytesseract.image_to_string(Image.open(active_img)).strip()
                        if len(ocr_txt) >= 4:
                            q_prob = " ".join(ocr_txt.split())
                    except Exception:
                        pass
                    ans = handle_section_query(q_prob, sec_label, lang, age, api_key, model)
                    st.session_state[f"{sec_id}_sol"] = {"q": q_prob, "text": ans.text, "visual": ans.visual}

    # Voice Recording Drawer
    if st.session_state.get(f"{sec_id}_show_mic", False):
        with st.container(border=True):
            st.markdown("##### 🎙️ " + ("Voice Question (Speak to Buddy)" if lang == "en" else "Awaaz Se Poochhein"))
            v_in = st.audio_input("Record voice question", key=f"{sec_id}_audio_widget")
            if v_in:
                with st.spinner("🎧 Listening..."):
                    spoken = transcribe_audio(v_in, lang)
                if spoken:
                    st.success(f"🗣️ " + (f"Heard: \"{spoken}\"" if lang == "en" else f"Suna: \"{spoken}\""))
                    ans = handle_section_query(spoken, sec_label, lang, age, api_key, model)
                    st.session_state[f"{sec_id}_sol"] = {"q": spoken, "text": ans.text, "visual": ans.visual}
                    st.session_state[f"{sec_id}_show_mic"] = False
                    st.rerun()

    # If this section has a solved query:
    if st.session_state.get(f"{sec_id}_sol"):
        c_sol = st.session_state[f"{sec_id}_sol"]
        with st.container(border=True):
            st.markdown(f"#### 🎯 " + (f"Solution for: *\"{c_sol['q']}\"*" if lang == "en" else f"Hal: *\"{c_sol['q']}\"*"))
            st.markdown(c_sol["text"])
            if c_sol.get("visual"):
                show_visual(c_sol["visual"], lang, f"{sec_id}_sol_vis")
            read_aloud(c_sol["text"], key=f"{sec_id}_sol_aud", lang=lang)
            st.caption("💾 " + ("Saved to your chat history! You can also view all saved chats in 💬 Ask Buddy." if lang == "en" else "Chat history mein save ho gaya! Aap '💬 Buddy se poochho' mein bhi dekh sakte hain."))
            if st.button("✖️ " + ("Close Solution" if lang == "en" else "Band karein"), key=f"{sec_id}_sol_close"):
                st.session_state[f"{sec_id}_sol"] = None
                st.rerun()

    return query.strip()


def init_state():
    ss = st.session_state
    ss.setdefault("messages", [])
    ss.setdefault("events", [])
    ss.setdefault("body_i", 0)
    ss.setdefault("body_highlight", None)
    ss.setdefault("quiz_done", {})
    ss.setdefault("xp", 35)
    ss.setdefault("badges", ["curious_spark"])
    ss.setdefault("learned_organs", [])
    ss.setdefault("experiments_tried", [])
    ss.setdefault("student_name", "Junior Scientist")
    ss.setdefault("avatar", "🧑‍🚀 Astro Kid")
    ss.setdefault("theme", "🌈 Wonder Academy (Nursery - Class 8)")
    ss.setdefault("class_level", "5")
    ss.setdefault("snap_rotation", 0)
    ss.setdefault("snap_subject", "all")
    ss.setdefault("search_query", "")
    ss.setdefault("global_search_q", "")
    ss.setdefault("show_top_cam", False)
    ss.setdefault("show_top_voice", False)
    ss.setdefault("body_active_key", "brain")
    ss.setdefault("phys_active_key", "force")
    ss.setdefault("chem_active_key", "atom")
    ss.setdefault("math_active_key", "pythagoras")
    ss.setdefault("top_cam_sol", None)
    ss.setdefault("top_cam_hint_text", "")



# ----------------------------------------------------------------------------- sidebar
def sidebar():
    st.sidebar.title("🧠 GyaanBuddy")
    st.sidebar.caption("Your friendly, kid-safe science & math buddy")

    # IMPORTANT: Keep Language radio as the very first radio in sidebar for AppTest compatibility
    lang_label = st.sidebar.radio("Language / Bhasha", ["English", "Hinglish"], horizontal=True)
    lang = "hi" if lang_label == "Hinglish" else "en"

    # Class Filter (Nursery to 8th Class: Nursery, LKG, UKG, 1, 2, 3, 4, 5, 6, 7, 8)
    class_options = ["Nursery", "LKG", "UKG", "1", "2", "3", "4", "5", "6", "7", "8"]
    saved_class = st.session_state.get("class_level", "5")
    if saved_class not in class_options:
        saved_class = "5"
    chosen_class = st.sidebar.select_slider(
        "🎓 " + ("Class Filter (Nursery to 8th)" if lang == "en" else "Class Filter (Nursery se 8th)"),
        options=class_options,
        value=saved_class,
        help="Adjusts explanation complexity and vocabulary for your child's class level."
    )
    st.session_state["class_level"] = chosen_class
    class_to_age = {
        "Nursery": "3-5",
        "LKG": "4-6",
        "UKG": "5-7",
        "1": "6-8",
        "2": "6-8",
        "3": "8-10",
        "4": "9-11",
        "5": "10-12",
        "6": "11-13",
        "7": "12-14",
        "8": "13-15",
    }
    age = class_to_age.get(chosen_class, "10-12")

    # 🎓 Persistent Student Learning Profile & Training Dataset Memory
    try:
        import student_memory
        prof = student_memory.load_student_profile()
        with st.sidebar.expander("🎓 " + ("Student Profile & AI Sign-In" if lang == "en" else "Student Profile & Sign-In"), expanded=True):
            st.markdown("##### 👤 " + ("Student Sign-In Details" if lang == "en" else "Student Sign-In Details"))
            s_name = st.text_input(
                "Student Name / Naam:",
                value=st.session_state.get("student_name", prof.get("student_name", "Junior Scientist")),
                key="sb_prof_name",
                placeholder="e.g. Aarav, Ananya, Kabir..."
            )
            class_options = ["Nursery", "LKG", "UKG", "1", "2", "3", "4", "5", "6", "7", "8"]
            curr_cls = str(st.session_state.get("class_level", prof.get("student_grade", "5"))).replace("Class ", "")
            cls_idx = class_options.index(curr_cls) if curr_cls in class_options else 5

            s_grade = st.selectbox(
                "Class / Grade:",
                options=class_options,
                index=cls_idx,
                key="sb_prof_grade"
            )
            s_focus = st.text_input(
                "Learning Goals / Focus:",
                value=st.session_state.get("student_focus", prof.get("learning_focus", "NCERT Science & Math")),
                key="sb_prof_focus",
                placeholder="e.g. Science, Trees & Animals, Maths..."
            )
            if st.button("💾 " + ("Save & Sign In" if lang == "en" else "Save & Sign In Karein"), key="btn_save_student_prof", type="primary", width="stretch"):
                st.session_state["student_name"] = s_name
                st.session_state["class_level"] = s_grade
                st.session_state["student_focus"] = s_focus
                prof["student_name"] = s_name
                prof["student_grade"] = f"Class {s_grade}"
                prof["learning_focus"] = s_focus
                prof["assessed_level"] = student_memory.assess_student_level(f"Class {s_grade}", prof.get("total_chats", 0), prof.get("topics_mastered", []))
                student_memory.save_student_profile(prof)
                st.toast(f"🌟 Welcome, {s_name}! Profile saved for Class {s_grade}.", icon="🎉")
                st.rerun()

            st.divider()
            st.markdown(f"**👤 Student:** `{prof.get('student_name', s_name)}`")
            st.markdown(f"**🎓 Class:** `Class {s_grade}`")
            st.markdown(f"**🌟 Level:** `{prof.get('assessed_level', 'Rising Explorer')}`")
            st.markdown(f"**💬 Chats Logged:** `{prof.get('total_chats', len(st.session_state.get('messages', [])))}`")
            if st.button("🔄 " + ("Reset Profile Memory" if lang == "en" else "Profile Reset Karein"), key="btn_reset_student_prof", use_container_width=True):
                student_memory.reset_student_profile()
                st.toast("Student profile memory reset!")
                st.rerun()
    except Exception:
        pass


    st.sidebar.divider()
    env_api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not env_api_key:
        try:
            env_api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            env_api_key = ""
    api_key = st.sidebar.text_input("Anthropic API key (optional, for parents)", type="password",
                                    value=env_api_key,
                                    help="Without a key GyaanBuddy answers from its built-in lessons.")
    model = st.sidebar.text_input("Model", value=tutor_engine.DEFAULT_MODEL)
    st.sidebar.success("AI mode on" if api_key else "Built-in lessons mode")
    st.sidebar.info("🛡️ Safety filter is always on. Private details are hidden and unsafe topics are blocked.")
    if st.sidebar.button("Clear chat"):
        try:
            import student_memory
            student_memory.clear_chat_history()
        except Exception:
            pass
        st.session_state["messages"] = []
        st.rerun()
    st.sidebar.markdown("""
    <div style="text-align: center; margin-top: 25px; padding-top: 15px; border-top: 1px solid rgba(0, 0, 0, 0.08);">
      <span style="font-size: 0.85rem; opacity: 0.85;">🚀 Created by <b>Mahdi Nawaz</b></span>
    </div>
    """, unsafe_allow_html=True)
    return lang, age, (api_key or None), model


# ----------------------------------------------------------------------------- chat tab
def tab_chat(lang, age, api_key, model):
    t = TXT[lang]
    st.subheader(t["tabs"][0])

    # 🎤 Optional Voice Question Input
    with st.expander("🎙️ " + ("Voice Question (Speak to Buddy)" if lang == "en" else "Awaaz Se Poochhein (Bol kar sawaal karein)"), expanded=False):
        voice_rec = st.audio_input(
            "Record voice question",
            key="voice_rec_input",
            label_visibility="collapsed"
        )
        if voice_rec:
            with st.spinner("🎧 Listening to your voice recording… 🎙️" if lang == "en" else "Awaaz sun raha hoon… 🎙️"):
                spoken_text = transcribe_audio(voice_rec, lang)
            if spoken_text:
                st.success(f"🗣️ " + (f"Heard: \"{spoken_text}\"" if lang == "en" else f"Suna: \"{spoken_text}\""))
                st.session_state["pending"] = spoken_text
                st.rerun()

    if not st.session_state["messages"]:
        st.info("👋 " + ("Hello! Ask any question about Science or Math below, or explore the interactive labs above!"
                         if lang == "en" else "Namaste! Science ya Maths ke baare mein kuch bhi poochhein ya upar labs explore karein!"))

    for i, m in enumerate(st.session_state["messages"]):
        with st.chat_message(m["role"], avatar="🧒" if m["role"] == "user" else "🧠"):
            if m.get("subject") and m["role"] == "user":
                st.caption(f"📚 {m['subject']}")
            st.markdown(m["text"])
            if m.get("notice"):
                st.caption(m["notice"])
            if m.get("visual"):
                show_visual(m["visual"], lang, f"chatvis{i}")

    last = next((m for m in reversed(st.session_state["messages"]) if m["role"] == "assistant"), None)
    if last and not last.get("blocked"):
        read_aloud(last["text"], key="ra", lang=lang)

    q = st.chat_input(t["ask"]) or st.session_state.pop("pending", None)
    if q:
        history = [{"q": a["q"], "a": a["text"]} for a in st.session_state["messages"]
                   if a.get("role") == "assistant" and a.get("q") and not a.get("blocked")]
        with st.spinner("Thinking… 🤔" if lang == "en" else "Soch raha hoon… 🤔"):
            r = tutor_engine.answer(q, lang, age, history, api_key, model)
        st.session_state["messages"].append({"role": "user", "text": q})
        st.session_state["messages"].append({
            "role": "assistant",
            "text": r.text,
            "visual": r.visual,
            "q": q,
            "topic": r.topic or "General",
            "notice": r.notice,
            "blocked": r.blocked
        })

        # Persist interaction to Chat history & training dataset like ChatGPT
        try:
            import student_memory
            grade = str(st.session_state.get("class_level", "5"))
            student_memory.record_student_chat(
                grade=f"Class {grade}" if grade.isdigit() else grade,
                lang=lang,
                question=q,
                answer_text=r.text,
                subject=r.subject or "General",
                topic=r.topic or "General",
                xp=10,
                visual=r.visual
            )
        except Exception:
            pass

        if r.blocked:
            log("blocked", topic=r.category or "")
        else:
            log("question", r.subject, r.topic, mode=r.mode)
            add_xp(10, "Great science question!", badge_id="curious_spark", badge_name="Curious Spark")
        st.rerun()


# ----------------------------------------------------------------------------- snap & solve tab
def tab_snap_solve(lang, age, api_key, model):
    st.subheader(TXT[lang]["tabs"][6])
    st.caption("📸 " + ("Take a photo of your notebook or textbook question, or choose a subject below for step-by-step guidance!"
                        if lang == "en" else "Apni textbook ya copy ke sawaal ki photo kheencho ya subject chuno aur solution pao!"))

    # Subject Section Filter ("this should be separate for all sections")
    subjects = [
        ("🌟 All Science & Math", "all"),
        ("📐 Mathematics", "math"),
        ("⚡ Physics", "physics"),
        ("🧍 Human Body", "body"),
        ("🧪 Chemistry", "chem"),
    ] if lang == "en" else [
        ("🌟 Sabhi Subjects", "all"),
        ("📐 Ganit (Maths)", "math"),
        ("⚡ Physics", "physics"),
        ("🧍 Sharir (Biology)", "body"),
        ("🧪 Chemistry", "chem"),
    ]
    s_cols = st.columns(len(subjects))
    for s_idx, (s_label, s_key) in enumerate(subjects):
        is_sel = (st.session_state.get("snap_subject", "all") == s_key)
        if s_cols[s_idx].button(s_label, key=f"snap_subj_btn_{s_idx}", width="stretch", type="primary" if is_sel else "secondary"):
            st.session_state["snap_subject"] = s_key
            st.rerun()

    active_subj = st.session_state.get("snap_subject", "all")

    # Camera & Image Upload
    snap_col1, snap_col2 = st.columns([1, 1])
    with snap_col1:
        st.markdown("**📸 " + ("Phone Back Camera (Notebook & Book Photos)" if lang == "en" else "Phone Back Camera (Copy ya Kitaab)") + "**")
        file_img = st.file_uploader("📁 " + ("Take photo with back camera or choose photo" if lang == "en" else "Back camera se photo lein ya upload karein"), type=["png", "jpg", "jpeg", "webp"], key="snap_file_input")
    with snap_col2:
        st.markdown("**🤳 " + ("Selfie / Live Webcam" if lang == "en" else "Webcam / Live Camera") + "**")
        cam_img = st.camera_input("📷 " + ("Live camera snapshot" if lang == "en" else "Live camera snapshot"), key="snap_cam_input")

    active_img = cam_img or file_img
    if active_img:
        from PIL import Image
        pil_img = Image.open(active_img)
        rot = st.session_state.get("snap_rotation", 0)
        if rot != 0:
            pil_img = pil_img.rotate(rot, expand=True)

        img_col1, img_col2 = st.columns([1.5, 1])
        with img_col1:
            st.image(pil_img, caption="Question Photo Preview", width=330)
            st.success("✅ Image ready!" if lang == "en" else "✅ Photo tayyar hai!")
        with img_col2:
            st.markdown("##### ⚙️ " + ("Photo Tools" if lang == "en" else "Photo Tools"))
            if st.button("🔄 " + ("Rotate 90°" if lang == "en" else "90° Ghumaayein"), key="btn_rot_snap"):
                st.session_state["snap_rotation"] = (st.session_state.get("snap_rotation", 0) + 90) % 360
                st.rerun()
            if rot != 0 and st.button("↩️ " + ("Reset Rotation" if lang == "en" else "Reset Ghumaav"), key="btn_rot_reset"):
                st.session_state["snap_rotation"] = 0
                st.rerun()



    user_prob = st.text_input(
        "Question text",
        value=st.session_state.get("snap_problem_text", ""),
        placeholder="Type question or paste text here (e.g., Importance of metals and non-metals in daily life)..." if lang == "en" else "Sawaal likhein ya upar se preset chunein...",
        key="snap_problem_input",
        label_visibility="collapsed"
    )
    st.caption("📋 " + ("Tip: Use Win + Shift + S to screenshot from PDF or textbook, save as image to upload above, or paste question text!" if lang == "en" else "Tip: Win + Shift + S se screenshot lein, photo upload karein ya text paste karein!"))

    solve_btn = st.button("🔍 " + ("Search & Solve Question from Photo / Screenshot" if lang == "en" else "Photo / Screenshot se Sawaal Khojein aur Hal Karein"), key="btn_do_snap_solve", type="primary")
    if solve_btn:
        q_to_solve = user_prob.strip()
        if not q_to_solve and not active_img:
            st.warning("⚠️ " + ("Please take a photo with the camera, upload an image, or pick a question preset above!" if lang == "en" else "⚠️ Kripya photo lein ya upar se sawaal chunein!"))
        else:
            effective_api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not effective_api_key:
                try:
                    effective_api_key = st.secrets.get("ANTHROPIC_API_KEY")
                except Exception:
                    effective_api_key = None

            with st.spinner("🤖 Scanning question and calculating solution... 🔍" if lang == "en" else "🤖 Sawaal scan ho raha hai aur hal kiya ja raha hai... 🔍"):
                sol_text = ""
                visual_spec = None
                was_ai = False

                # 1. AI Vision if key is available
                if active_img and effective_api_key:
                    try:
                        import anthropic
                        client = anthropic.Anthropic(api_key=effective_api_key)
                        active_img.seek(0)
                        img_bytes = active_img.getvalue()
                        b64_data = base64.b64encode(img_bytes).decode("utf-8")
                        mime = getattr(active_img, "type", "image/jpeg") or "image/jpeg"
                        sys_prompt = (
                            f"You are GyaanBuddy, a friendly, encouraging AI tutor for school students (Nursery to Class 8) in India. "
                            f"Language: {'English' if lang == 'en' else 'Hinglish'}. "
                            f"Carefully examine the student's photo. Extract and read the math problem, science question, diagram, or textbook exercise. "
                            f"Provide a complete, step-by-step solution formatted with simple child-friendly language, clear steps (Step 1, Step 2, ...), "
                            f"formulas, final answer highlighted, and encouraging emojis."
                        )
                        v_prompt = q_to_solve or "Please solve the question or exercise shown in this photo step-by-step for a school student."
                        resp = client.messages.create(
                            model=model or "claude-3-5-sonnet-20241022",
                            max_tokens=650,
                            system=sys_prompt,
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64_data}},
                                    {"type": "text", "text": v_prompt}
                                ]
                            }]
                        )
                        sol_text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
                        was_ai = True
                    except Exception:
                        sol_text = ""

                # 2. Try OCR if Vision was not used or failed and no question typed
                if not sol_text and active_img and not q_to_solve:
                    try:
                        import pytesseract
                        from PIL import Image
                        active_img.seek(0)
                        ocr_p = Image.open(active_img)
                        rot = st.session_state.get("snap_rotation", 0)
                        if rot != 0:
                            ocr_p = ocr_p.rotate(rot, expand=True)
                        ocr_out = pytesseract.image_to_string(ocr_p)
                        cleaned_ocr = " ".join(ocr_out.split()).strip()
                        if len(cleaned_ocr) >= 3:
                            q_to_solve = cleaned_ocr
                    except Exception:
                        pass

                # 3. If still no specific question text, infer from subject or use core problem
                if not sol_text:
                    if not q_to_solve:
                        subject_defaults = {
                            "math": "In a right triangle with legs 3 cm and 4 cm, find the hypotenuse",
                            "physics": "What is force and Newton's law?",
                            "body": "How does the heart pump blood?",
                            "chem": "What is an atom of oxygen?",
                            "all": "In a right triangle with legs 3 cm and 4 cm, find the hypotenuse",
                        }
                        q_to_solve = subject_defaults.get(active_subj, "In a right triangle with legs 3 cm and 4 cm, find the hypotenuse")

                    r = tutor_engine.answer(q_to_solve, lang, age)
                    sol_text = r.text
                    visual_spec = r.visual

                # 4. Attach relevant visual diagram if not yet set
                if not visual_spec and sol_text:
                    comb = (q_to_solve + " " + sol_text).lower()
                    if any(w in comb for w in ["pythagor", "hypotenuse", "right triangle", "triangle"]):
                        visual_spec = "math:pythagoras"
                    elif any(w in comb for w in ["circle", "radius", "circumference"]):
                        visual_spec = "math:circle"
                    elif any(w in comb for w in ["cylinder", "volume"]):
                        visual_spec = "math:cylinder"
                    elif any(w in comb for w in ["fraction", "pizza"]):
                        visual_spec = "math:fractions"
                    elif any(w in comb for w in ["linear equation", "solve for x", "2x +", "algebra"]):
                        visual_spec = "math:algebra"
                    elif any(w in comb for w in ["heart", "pump blood", "circulatory"]):
                        visual_spec = "body:heart"
                    elif any(w in comb for w in ["lung", "breathe", "oxygen", "respiratory"]):
                        visual_spec = "body:lungs"
                    elif any(w in comb for w in ["brain", "cerebrum", "thinking"]):
                        visual_spec = "body:brain"
                    elif any(w in comb for w in ["kidney", "nephron", "filter blood"]):
                        visual_spec = "body:kidneys:detail"
                    elif any(w in comb for w in ["atom", "electron", "proton"]):
                        visual_spec = "chem:atom:8"
                    elif any(w in comb for w in ["water molecule", "h2o"]):
                        visual_spec = "chem:mol:H2O"
                    elif any(w in comb for w in ["force", "newton", "motion"]):
                        visual_spec = "physics:force"
                    elif any(w in comb for w in ["gravity", "free fall", "weight"]):
                        visual_spec = "physics:gravity"
                    elif any(w in comb for w in ["pendulum", "oscillation"]):
                        visual_spec = "physics:pendulum"

                # Store solution in state
                st.session_state["snap_last_solution"] = {
                    "q": q_to_solve or ("Photo Question" if lang == "en" else "Photo ka Sawaal"),
                    "text": sol_text,
                    "visual": visual_spec,
                    "is_vision": was_ai,
                }
                # Also save to messages history
                st.session_state["messages"].append({
                    "role": "user",
                    "text": f"📸 [Photo Question]: {q_to_solve or 'Question in photo'}"
                })
                st.session_state["messages"].append({
                    "role": "assistant",
                    "text": sol_text,
                    "visual": visual_spec,
                    "q": q_to_solve
                })
                add_xp(20, "Solved photo question!", badge_id="curious_spark")
                st.toast("🎉 Question Solved! +20 XP awarded", icon="🚀")

    # Render Solution Card directly in the Snap & Solve Tab
    last_sol = st.session_state.get("snap_last_solution")
    if last_sol:
        st.markdown("---")
        mode_badge = "🤖 " + ("AI Vision Solved" if last_sol.get("is_vision") else "Interactive Step-by-Step Solution")
        st.markdown(f"### 🎯 {mode_badge}")
        with st.container(border=True):
            st.markdown(f"**❓ " + ("Question:" if lang == "en" else "Sawaal:") + f"** {last_sol['q']}")
            st.markdown(last_sol["text"])
            read_aloud(last_sol["text"], key="snap_sol_audio_play", lang=lang)

            if last_sol.get("visual"):
                st.markdown("##### 🖼️ " + ("Interactive Model / Diagram:" if lang == "en" else "Interactive Diagram:"))
                show_visual(last_sol["visual"], lang, "snap_solution_visual")

            st.divider()
            c_s1, c_s2 = st.columns([1, 1])
            with c_s1:
                if st.button("💬 " + ("Ask follow-up in Buddy Chat" if lang == "en" else "Buddy se Chat mein aur poochhein"), key="btn_snap_chat_fwd", width="stretch"):
                    st.session_state["pending"] = f"Explain more about: {last_sol['q']}"
                    st.rerun()
            with c_s2:
                if st.button("🔄 " + ("Solve Another Question" if lang == "en" else "Dusra Sawaal Hal Karein"), key="btn_snap_clear_sol", width="stretch"):
                    st.session_state["snap_last_solution"] = None
                    st.session_state["snap_problem_text"] = ""
                    st.session_state["snap_problem_input"] = ""
                    st.rerun()


# ----------------------------------------------------------------------------- nature tab (General Science: Trees & Animals)
def tab_nature(lang, age="10-12", api_key=None, model=None):
    t = TXT[lang]
    st.subheader(t["tabs"][1])

    # 1. Section Tools: Search + Direct Search Button + Camera (Upload/Photo/Screenshot) + Voice
    render_section_tools(
        "nature",
        "General Science",
        "Search parts of tree, photosynthesis, butterfly life cycle, frog, food chain..." if lang == "en" else "Ped ke bhaag, photosynthesis, titli, mendhak, food chain khojein...",
        lang, age, api_key, model
    )

    # 2. Dynamic Class-Tier Curriculum
    tier_id = render_class_tier_header("nature", lang)

    if tier_id == "early":
        st.markdown("#### 🐣 " + ("Early Nature Explorers (Nursery to Class 2)" if lang == "en" else "Nannhe Khoji: Ped, Paudhe aur Jaanwar (Nursery se 2nd)"))
        e_topics = [
            ("🐶 " + ("Cute Animals & Their Babies" if lang == "en" else "Pyare Jaanwar aur Unke Bachhe"), "cute_animals"),
            ("🌱 " + ("How a Tiny Seed Grows into a Sunflower" if lang == "en" else "Beej se Sunflower Kaise Khilta Hai"), "seed_growth"),
            ("🍎 " + ("Yummy Fruits & Healthy Veggies" if lang == "en" else "Mazedaar Phal aur Sabziyan"), "fruits"),
            ("🌈 " + ("Nature Senses & Rainbow Colors" if lang == "en" else "Rainbow ke Rang aur 5 Senses"), "rainbow_senses"),
        ]
        e_pick = st.selectbox("Choose Activity", range(len(e_topics)), format_func=lambda idx: e_topics[idx][0], key="nat_early_topic")
        key = e_topics[e_pick][1]

        if key == "cute_animals":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                a_sub = st.radio("Choose Animal Friend", ["🐶 Dog & Puppy", "🐱 Cat & Kitten", "🐮 Cow & Calf", "🦁 Lion & Cub"], horizontal=True, key="nat_animal_sub")
                a_key = "dog" if "Dog" in a_sub else ("cat" if "Cat" in a_sub else ("cow" if "Cow" in a_sub else "lion"))
                show_svg(V.cute_animals_svg(a_key, lang), 480)
            with col2:
                st.markdown(f"### {a_sub}")
                st.markdown("Animals care for their babies just like our families care for us! They feed them, teach them to play, and keep them cozy and safe.")
                read_aloud(f"Animal friend: {a_sub}", key=f"aud_a_{a_key}", lang=lang)
                if st.button("⭐ " + ("I Learned This! (+15 XP)" if lang == "en" else "Maine Seekha! (+15 XP)"), key=f"btn_xp_a_{a_key}"):
                    add_xp(15, f"Learned about {a_sub}!", badge_id="animal_friend", badge_name="Animal Friend")

        elif key == "seed_growth":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                stage = st.slider("Plant Growth Stage", 1, 4, 3, format_func=lambda s: f"Stage {s}: {'Seed in Soil 🌰' if s==1 else ('Baby Sprout 🌱' if s==2 else ('Growing Stem 🌿' if s==3 else 'Sunflower Bloom! 🌻'))}")
                show_svg(V.seed_plant_svg(stage, lang), 480)
            with col2:
                st.markdown("### 🌱 From Tiny Seed to Big Sunflower!")
                st.markdown("1. **Seed**: Sleeps warm in dark brown soil.<br>2. **Sprout**: Roots drink water, green shoot pops up!<br>3. **Stem**: Green leaves catch golden sunshine.<br>4. **Bloom**: Bright yellow flower turns to face the Sun!", unsafe_allow_html=True)
                read_aloud("Seed growth cycle", key="aud_seed", lang=lang)
                if st.button("⭐ " + ("I Learned This! (+15 XP)" if lang == "en" else "Maine Seekha! (+15 XP)"), key="btn_xp_seed"):
                    add_xp(15, "Learned how seeds grow into plants!", badge_id="green_thumb", badge_name="Green Thumb")

        elif key == "fruits":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.counting_fruits_svg(6, lang), 480)
            with col2:
                st.markdown("### 🍎 Healthy Fruits and Vegetables")
                st.markdown("Fruits like juicy sweet apples, yellow bananas, and oranges give us vitamins! Crunchy carrots grow under the soil.")
                if st.button("⭐ " + ("I Learned This! (+15 XP)" if lang == "en" else "Maine Seekha! (+15 XP)"), key="btn_xp_fruit"):
                    add_xp(15, "Learned healthy fruits and veggies!")

        else:
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.five_senses_body_svg("all", lang), 480)
            with col2:
                st.markdown("### 🌈 Nature's 5 Senses")
                st.markdown("Your eyes see colorful butterflies, your ears hear singing birds, your nose smells sweet roses, your tongue tastes juicy mangoes, and your hands touch soft puppy fur!")
                if st.button("⭐ " + ("I Learned This! (+15 XP)" if lang == "en" else "Maine Seekha! (+15 XP)"), key="btn_xp_nat_sens"):
                    add_xp(15, "Learned nature's 5 senses!")

    elif tier_id == "primary":
        st.markdown("#### 🌳 " + ("Junior Nature & Environmental Science (Class 3 - 5)" if lang == "en" else "Junior Vigyan: Ped, Titli aur Jal Chakra (3rd se 5th)"))
        p_topics = [
            ("🌳 " + ("Parts of a Tree & Plant Anatomy" if lang == "en" else "Ped ke Hisse (Jad, Tana, Patti)"), "tree_parts"),
            ("🦋 " + ("Butterfly Metamorphosis Life Cycle" if lang == "en" else "Titli Ka Jeevan Chakra (4 Stages)"), "butterfly_lifecycle"),
            ("💧 " + ("The Water Cycle: Evaporation, Clouds & Rain" if lang == "en" else "Jal Chakra (Evaporation, Baadal, Baarish)"), "water_cycle"),
            ("🦁 " + ("Animal Diets (Herbivores, Carnivores, Omnivores)" if lang == "en" else "Jaanwaron Ka Khana (Shakahari, Mansahari)"), "animal_diets"),
            ("🐸 " + ("Frog Amphibian Life Cycle" if lang == "en" else "Mendhak Ka Jeevan Chakra"), "frog_lifecycle"),
        ]
        p_pick = st.selectbox("Choose Junior Topic", range(len(p_topics)), format_func=lambda idx: p_topics[idx][0], key="nat_prim_topic")
        p_key = p_topics[p_pick][1]

        col1, col2 = st.columns([1.2, 1])
        with col1:
            if p_key == "tree_parts":
                show_svg(V.tree_plant_svg(lang), 480)
            elif p_key == "butterfly_lifecycle":
                show_svg(V.butterfly_lifecycle_svg(lang), 480)
            elif p_key == "water_cycle":
                show_svg(V.water_cycle_svg(lang), 480)
            elif p_key == "frog_lifecycle":
                show_svg(V.butterfly_lifecycle_svg(lang), 480)
            else:
                show_svg(V.nature_foodchain_svg(lang), 480)
        with col2:
            info = C.NATURE_TOPICS.get(p_key, {})
            t_title = info.get("title_hi" if lang == "hi" else "title_en", "")
            t_desc = info.get("hi" if lang == "hi" else "en", "")
            t_form = info.get("formula", "")
            st.markdown(f"### {t_title}")
            st.markdown(t_desc)
            if t_form:
                st.markdown(f"<div class='formula'>{t_form}</div>", unsafe_allow_html=True)
            read_aloud(f"{t_title}. {t_desc}", key=f"aud_prim_{p_key}", lang=lang)
            if st.button("⭐ " + ("I Mastered This! (+15 XP)" if lang == "en" else "Maine Seekh Liya! (+15 XP)"), key=f"xp_prim_{p_key}"):
                add_xp(15, f"Mastered {t_title}!", badge_id="nature_explorer", badge_name="Nature Explorer")

    else:
        st.markdown("#### 🔬 " + ("Middle School Biology & Ecology Lab (Class 6 - 8)" if lang == "en" else "Middle School Biology & Ecology Lab (6th se 8th)"))
        m_topics = [
            ("☀️ " + ("Photosynthesis Bio-Reaction & Chemical Flow" if lang == "en" else "Photosynthesis: Rasayanik Kriya aur Urja"), "photosynthesis"),
            ("🌱 " + ("Forest Food Chains, Trophic Levels & 10% Energy Rule" if lang == "en" else "Khaadya Shrinkhala aur Trophic Levels"), "food_chain"),
            ("🐸 " + ("Amphibian Metamorphosis & Ecology" if lang == "en" else "Mendhak Ka Jeevan Chakra aur Ecology"), "frog_lifecycle"),
            ("🌳 " + ("Advanced Plant Anatomy & Vascular Transport" if lang == "en" else "Paudhon Ki Xylem aur Phloem Naliyan"), "tree_parts"),
        ]
        m_pick = st.selectbox("Middle School Biology Topic", range(len(m_topics)), format_func=lambda idx: m_topics[idx][0], key="nat_mid_topic")
        m_key = m_topics[m_pick][1]

        col1, col2 = st.columns([1.2, 1])
        with col1:
            if m_key == "photosynthesis":
                show_svg(V.photosynthesis_svg(lang), 480)
            elif m_key == "food_chain":
                show_svg(V.nature_foodchain_svg(lang), 480)
            elif m_key == "frog_lifecycle":
                show_svg(V.butterfly_lifecycle_svg(lang), 480)
            else:
                show_svg(V.tree_plant_svg(lang), 480)
        with col2:
            info = C.NATURE_TOPICS.get(m_key, {})
            t_title = info.get("title_hi" if lang == "hi" else "title_en", "")
            t_desc = info.get("hi" if lang == "hi" else "en", "")
            t_form = info.get("formula", "")
            st.markdown(f"### {t_title}")
            st.markdown(t_desc)
            if t_form:
                st.markdown(f"<div class='formula'>{t_form}</div>", unsafe_allow_html=True)
            read_aloud(f"{t_title}. {t_desc}", key=f"aud_mid_{m_key}", lang=lang)
            if st.button("⭐ " + ("I Mastered This! (+20 XP)" if lang == "en" else "Maine Seekh Liya! (+20 XP)"), key=f"xp_mid_{m_key}"):
                add_xp(20, f"Mastered {t_title}!", badge_id="bio_scholar", badge_name="Bio Scholar")


# ----------------------------------------------------------------------------- body tab
def tab_body(lang, age="10-12", api_key=None, model=None):
    t = TXT[lang]
    st.subheader(t["tabs"][5])

    render_section_tools(
        "body",
        "Human Body",
        "Search brain lobes, heart pumping, lungs, kidneys nephron, skeleton..." if lang == "en" else "Sharir ka sawaal khojein (dimaag, dil, fefde, gurde)...",
        lang, age, api_key, model
    )

    tier_id = render_class_tier_header("body", lang)

    if tier_id == "early":
        st.markdown("#### 👶 " + ("Early Body & Wonder Senses (Nursery to Class 2)" if lang == "en" else "Nannha Sharir aur 5 Senses (Nursery se 2nd)"))
        e_b_topics = [
            ("👀 " + ("My 5 Wonder Senses" if lang == "en" else "Meri 5 Wonder Senses"), "senses"),
            ("🪥 " + ("Clean Teeth & Sparkly Smile" if lang == "en" else "Saaf Daant aur Chamakti Smile"), "teeth"),
            ("💓 " + ("Feeling My Thump-Thump Heart" if lang == "en" else "Dil Ki Dhadkan Suno"), "heartbeat"),
        ]
        e_pick = st.selectbox("Choose Body Wonder", range(len(e_b_topics)), format_func=lambda idx: e_b_topics[idx][0], key="body_early_pick")
        e_key = e_b_topics[e_pick][1]

        if e_key == "senses":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                s_pick = st.radio("Pick a Sense", ["🌈 All 5 Senses", "👀 Eyes (Sight)", "👂 Ears (Sound)", "👃 Nose (Smell)", "👅 Tongue (Taste)", "✋ Skin (Touch)"], horizontal=True, key="early_sense_rad")
                s_code = "eyes" if "Eyes" in s_pick else ("ears" if "Ears" in s_pick else ("nose" if "Nose" in s_pick else ("tongue" if "Tongue" in s_pick else ("hands" if "Skin" in s_pick else "all"))))
                show_svg(V.five_senses_body_svg(s_code, lang), 480)
            with col2:
                st.markdown(f"### {s_pick}")
                st.markdown("Your body is an amazing machine! Your 5 senses send secret messages to your brain every millisecond to help you explore the world.")
                read_aloud(f"My 5 Wonder Senses. {s_pick}", key=f"aud_s_{s_code}", lang=lang)
                if st.button("⭐ " + ("I Learned My Senses! (+15 XP)" if lang == "en" else "Maine Senses Seekhein! (+15 XP)"), key=f"btn_xp_s_{s_code}"):
                    add_xp(15, "Learned the 5 senses!", badge_id="body_explorer", badge_name="Body Wonder")

        elif e_key == "teeth":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.clean_teeth_svg(lang), 480)
            with col2:
                st.markdown("### 🪥 Brushing for Strong, Happy Teeth!")
                st.markdown("• Brush in little circles twice a day (morning & before bed).<br>• Clean the front, back, and chewing tops!<br>• Keep sugar bugs away with fresh water!", unsafe_allow_html=True)
                read_aloud("Brush your teeth twice a day in gentle circles.", key="aud_teeth", lang=lang)
                if st.button("⭐ " + ("I Brushed Today! (+15 XP)" if lang == "en" else "Maine Daant Saaf Kiye! (+15 XP)"), key="btn_xp_teeth"):
                    add_xp(15, "Learned healthy dental hygiene!", badge_id="clean_smile", badge_name="Bright Smile")

        else:
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.vital_signs_svg(75, lang), 440)
            with col2:
                st.markdown("### 💓 Lub-Dub! Put Your Hand on Your Chest")
                st.markdown("Your heart is a strong muscle about the size of your fist. It beats around 80 times every minute to send fresh blood all the way to your toes!")
                read_aloud("Your heart beats steadily to keep you energized.", key="aud_hb_early", lang=lang)
                if st.button("⭐ " + ("I Felt My Heartbeat! (+15 XP)" if lang == "en" else "Maine Dhadkan Mehsoos Ki! (+15 XP)"), key="btn_xp_hb_early"):
                    add_xp(15, "Discovered how the heart pumps blood!")

    elif tier_id == "primary":
        st.markdown("#### 👤 " + ("Junior Anatomy & Organ Systems (Class 3 - 5)" if lang == "en" else "Junior Sharir Vigyan (3rd se 5th)"))
        parts = C.BODY_PARTS

        # Body System Filters
        systems = [
            ("🌟 " + ("All Organs" if lang == "en" else "Sabhi Organs"), None),
            ("🫀 Circulatory", "Circulatory system"),
            ("🫁 Respiratory", "Respiratory system"),
            ("🍕 Digestive", "Digestive system"),
            ("🧠 Nervous", "Nervous system"),
            ("🦴 Skeletal", "Skeletal system"),
        ]
        sys_cols = st.columns(len(systems))
        for s_idx, (s_label, s_sys) in enumerate(systems):
            if sys_cols[s_idx].button(s_label, key=f"body_p_sys_{s_idx}", width="stretch"):
                if s_sys is not None:
                    for o_idx, bp in enumerate(parts):
                        if bp.get("system") == s_sys:
                            st.session_state["body_i"] = o_idx
                            break
                st.rerun()

        i = st.session_state.get("body_i", 0) % len(parts)
        c1, c2, c3 = st.columns([1, 1, 4])
        if c1.button(t["prev"], key="b_p_prev"):
            st.session_state["body_i"] = (i - 1) % len(parts)
            st.rerun()
        if c2.button(t["next"], key="b_p_next"):
            st.session_state["body_i"] = (i + 1) % len(parts)
            st.rerun()
        names = [(b["hi_name"] if lang == "hi" else b["en_name"]) for b in parts]
        pick = c3.selectbox("Part", names, index=i, label_visibility="collapsed", key="b_p_select")
        if names.index(pick) != i:
            st.session_state["body_i"] = names.index(pick)
            st.rerun()

        b = parts[i]
        left, right = st.columns([1.1, 1])
        with left:
            show_svg(V.body_svg(b["key"], lang), 470)
        with right:
            st.markdown(f"### {names[i]}")
            st.caption(f"{b['system']} • {i + 1}/{len(parts)}")
            st.write(b[lang])
            st.markdown(f"<div class='fact'>💡 <b>{t['fact']}:</b> {b['fact_' + lang]}</div>", unsafe_allow_html=True)
            read_aloud(f"{names[i]}. {b[lang]}", key=f"body_p_ra_{b['key']}", lang=lang)
            if st.button("✅ " + ("I Learned This (+15 XP)" if lang == "en" else "Maine Seekh Liya (+15 XP)"), key=f"learn_p_{b['key']}"):
                add_xp(15, f"Mastered {names[i]}!", badge_id="anatomy_ace", badge_name="Anatomy Ace")
                st.toast("Great job! 🌟")

        st.divider()
        st.markdown("#### 💓 " + ("Heartbeat & Exercise Simulator" if lang == "en" else "Dil Ki Dhadkan Simulator"))
        v1, v2 = st.columns([1, 1.2])
        with v1:
            bpm = st.select_slider("Activity", options=[70, 95, 125, 160], value=70, key="b_p_bpm",
                                   format_func=lambda v: "🛋️ Resting (70 BPM)" if v==70 else ("🚶 Walking (95 BPM)" if v==95 else ("🏃 Running (125 BPM)" if v==125 else "⚡ Sprint (160 BPM)")))
        with v2:
            show_svg(V.vital_signs_svg(bpm, lang), 420)

    else:
        st.markdown("#### 🔬 " + ("Middle School Anatomy & Physiology (Class 6 - 8)" if lang == "en" else "Middle School Sharir Vigyan & Physiology (6th se 8th)"))
        parts = C.BODY_PARTS

        systems = [
            ("🌟 " + ("All Organs" if lang == "en" else "Sabhi Organs"), None),
            ("🫀 " + ("Circulatory" if lang == "en" else "Circulatory (Dil)"), "Circulatory system"),
            ("🫁 " + ("Respiratory" if lang == "en" else "Respiratory (Fefde)"), "Respiratory system"),
            ("🍕 " + ("Digestive" if lang == "en" else "Digestive (Pet/Jigar)"), "Digestive system"),
            ("🧠 " + ("Nervous" if lang == "en" else "Nervous (Dimaag)"), "Nervous system"),
            ("🦴 " + ("Skeletal" if lang == "en" else "Skeletal (Haddiyan)"), "Skeletal system"),
            ("🫘 " + ("Urinary" if lang == "en" else "Urinary (Gurde)"), "Urinary system"),
        ]
        sys_cols = st.columns(len(systems))
        for s_idx, (s_label, s_sys) in enumerate(systems):
            if sys_cols[s_idx].button(s_label, key=f"body_m_sys_{s_idx}", width="stretch"):
                if s_sys is not None:
                    for o_idx, bp in enumerate(parts):
                        if bp.get("system") == s_sys:
                            st.session_state["body_i"] = o_idx
                            break
                st.rerun()

        learned_count = len(st.session_state["learned_organs"])
        st.markdown(f"🏆 **Organs Mastered:** {learned_count}/{len(parts)} " +
                    ("• Master all 8 to become an Anatomy Ace!" if lang == "en" else "• Saare 8 seekh kar Anatomy Ace bano!"))

        i = st.session_state.get("body_i", 0) % len(parts)
        c1, c2, c3 = st.columns([1, 1, 4])
        if c1.button(t["prev"], key="b_m_prev"):
            st.session_state["body_i"] = (i - 1) % len(parts)
            st.rerun()
        if c2.button(t["next"], key="b_m_next"):
            st.session_state["body_i"] = (i + 1) % len(parts)
            st.rerun()
        names = [(b["hi_name"] if lang == "hi" else b["en_name"]) for b in parts]
        pick = c3.selectbox("Part", names, index=i, label_visibility="collapsed", key="b_m_select")
        if names.index(pick) != i:
            st.session_state["body_i"] = names.index(pick)
            st.rerun()

        b = parts[i]
        if b["key"] == "brain":
            b_view = st.radio("Brain View Mode", ["🔬 " + ("Detailed Brain Lobes & Functions" if lang == "en" else "Dimaag Ki Banawat & Lobes"), "👤 Whole Body Position"], horizontal=True, key="brain_m_sel")
            left, right = st.columns([1.2, 1])
            with left:
                show_svg(V.body_svg(b["key"], lang) if "Whole Body" in b_view else V.brain_detail_svg(lang), 520)
        elif b["key"] == "kidneys":
            k_view = st.radio("Kidney View Mode", ["🔬 " + ("Realistic Cross-Section & Nephron" if lang == "en" else "Nephron Banawat"), "👤 Whole Body Position"], horizontal=True, key="kidney_m_sel")
            left, right = st.columns([1.2, 1])
            with left:
                show_svg(V.body_svg(b["key"], lang) if "Whole Body" in k_view else V.kidney_detail_svg(lang), 520)
        else:
            left, right = st.columns([1.1, 1])
            with left:
                show_svg(V.body_svg(b["key"], lang), 470)

        with right:
            st.markdown(f"### {names[i]}")
            st.caption(f"{b['system']} • {i + 1}/{len(parts)}")
            st.write(b[lang])
            st.markdown(f"<div class='fact'>💡 <b>{t['fact']}:</b> {b['fact_' + lang]}</div>", unsafe_allow_html=True)
            read_aloud(f"{names[i]}. {b[lang]} {b['fact_' + lang]}", key=f"body_m_ra_{b['key']}", lang=lang)

            already_learned = b["key"] in st.session_state["learned_organs"]
            btn_label = ("🌟 Mastered!" if already_learned else ("✅ I learned this" if lang == "en" else "✅ Maine seekh liya"))
            if st.button(btn_label, key=f"learn_m_{b['key']}", disabled=already_learned):
                st.session_state["learned_organs"].append(b["key"])
                log("learned", "Human body", b["en_name"])
                add_xp(20, f"Mastered {names[i]}!", badge_id="anatomy_ace", badge_name="Anatomy Ace")
                st.toast("Great job! 🌟")
                st.rerun()

        st.divider()
        st.markdown("#### 💓 " + ("Clinical Vital Signs & Cardiac Pumping Simulator" if lang == "en" else "Clinical Vital Signs Simulator"))
        v1, v2 = st.columns([1, 1.3])
        with v1:
            bpm = st.select_slider("Physiological State", options=[70, 95, 125, 160], value=70, key="b_m_bpm",
                                   format_func=lambda v: "🛋️ Basal Resting (70 BPM)" if v==70 else ("🚶 Moderate Ambulation (95 BPM)" if v==95 else ("🏃 Aerobic Exercise (125 BPM)" if v==125 else "⚡ Peak VO2 Max Sprint (160 BPM)")))
            if bpm >= 125:
                st.info("💪 Sympathetic autonomic system increases stroke volume and respiration frequency.")
            else:
                st.success("🧘 Parasympathetic vagus nerve maintains homeostasis.")
        with v2:
            show_svg(V.vital_signs_svg(bpm, lang), 440)


# ----------------------------------------------------------------------------- physics tab
def tab_physics(lang, age="10-12", api_key=None, model=None):
    t = TXT[lang]
    st.subheader(t["tabs"][2])

    render_section_tools(
        "physics",
        "Physics Lab",
        "Search projectile, newton, gravity, friction, ohm's law, pendulum, light..." if lang == "en" else "Physics sawaal khojein (gravity, projectile, pendulum, light)...",
        lang, age, api_key, model
    )

    tier_id = render_class_tier_header("physics", lang)

    if tier_id == "early":
        st.markdown("#### 🎈 " + ("Early Physics: Forces & Light (Nursery to Class 2)" if lang == "en" else "Nannha Physics: Push, Pull aur Roshni (Nursery se 2nd)"))
        e_p_topics = [
            ("🛒 " + ("Push vs Pull: How Things Move" if lang == "en" else "Push aur Pull: Cheezein Kaise Hilti Hain"), "push_pull"),
            ("💡 " + ("Light Bulb & Battery Switch" if lang == "en" else "Bulb aur Battery Switch"), "bulb_switch"),
            ("🍎 " + ("Why Things Fall Down (Gravity Magic)" if lang == "en" else "Cheezein Niche Kyun Girti Hain"), "gravity_magic"),
        ]
        e_pick = st.selectbox("Choose Activity", range(len(e_p_topics)), format_func=lambda idx: e_p_topics[idx][0], key="phys_early_pick")
        e_key = e_p_topics[e_pick][1]

        if e_key == "push_pull":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                action = st.radio("Choose Action", ["🛒 Pushing a Toy Forward", "🛞 Pulling a Wagon Closer"], horizontal=True, key="early_push_pull_rad")
                a_mode = "push" if "Pushing" in action else "pull"
                show_svg(V.push_pull_svg(a_mode, lang), 480)
            with col2:
                st.markdown(f"### {action}")
                st.markdown("• **Push:** Moves things AWAY from you (kicking a ball, rolling a toy car).<br>• **Pull:** Brings things CLOSER to you (pulling a wagon, opening a door)!", unsafe_allow_html=True)
                read_aloud(f"Push moves things away. Pull brings things closer.", key=f"aud_pp_{a_mode}", lang=lang)
                if st.button("⭐ " + ("I Mastered Push & Pull! (+15 XP)" if lang == "en" else "Maine Push Pull Seekha! (+15 XP)"), key=f"btn_xp_pp_{a_mode}"):
                    add_xp(15, "Learned push and pull forces!", badge_id="physics_wizard", badge_name="Physics Pro")

        elif e_key == "bulb_switch":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                switch_on = st.toggle("🔌 Switch ON / OFF", value=True, key="early_bulb_switch")
                show_svg(V.circuit_bulb_svg(switch_on, lang), 480)
            with col2:
                st.markdown("### 💡 Click the Switch to Glow!")
                st.markdown("When the switch is closed, invisible electricity flows in a complete loop from the battery into the bulb's tiny wire, making it glow bright sunny yellow!")
                read_aloud("Electricity flows in a complete circuit to light up the bulb.", key="aud_bulb", lang=lang)
                if st.button("⭐ " + ("I Made the Bulb Glow! (+15 XP)" if lang == "en" else "Maine Bulb Jalaya! (+15 XP)"), key="btn_xp_bulb"):
                    add_xp(15, "Explored electric circuits and switches!")

        else:
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.gravity_svg(lang), 480)
            with col2:
                st.markdown("### 🍎 Sir Isaac Newton & The Falling Apple")
                st.markdown("Whenever you jump up in the air or drop a red apple, Earth's invisible superpower called **Gravity** gently pulls you right back down to the ground!")
                if st.button("⭐ " + ("I Learned Gravity! (+15 XP)" if lang == "en" else "Maine Gravity Seekhi! (+15 XP)"), key="btn_xp_grav"):
                    add_xp(15, "Learned about Earth's gravity!")

    elif tier_id == "primary":
        st.markdown("#### ⚡ " + ("Junior Physics & Energy (Class 3 - 5)" if lang == "en" else "Junior Physics aur Urja (3rd se 5th)"))
        p_topics = [
            ("⚡ " + ("Electric Circuits & Resistance" if lang == "en" else "Bijli Ka Circuit aur Resistance"), "circuits"),
            ("⛸️ " + ("Friction on Different Surfaces" if lang == "en" else "Friction (Gharshan)"), "friction"),
            ("🍎 " + ("Earth's Gravity & Free Fall" if lang == "en" else "Gravity aur Free Fall"), "gravity"),
            ("🌤️ " + ("Why is the Sky Blue?" if lang == "en" else "Aasman Neela Kyun Hai?"), "sky"),
        ]
        p_pick = st.selectbox("Choose Experiment", range(len(p_topics)), format_func=lambda idx: p_topics[idx][0], key="phys_prim_pick")
        p_key = p_topics[p_pick][1]

        if p_key == "circuits":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                v = st.slider("Battery Voltage V (volts)", 1, 12, 6, key="p_prim_v")
                r = st.slider("Bulb Resistance R (ohms)", 1, 15, 3, key="p_prim_r")
                show_svg(V.circuit_svg(v, r), 440)
            with col2:
                current = v / r
                st.markdown(f"### ⚡ Electric Flow: {current:.1f} Amps")
                st.markdown("Higher voltage pushes more electric current, making the bulb brighter! Higher resistance slows current down.")
                read_aloud(f"Battery voltage {v} volts produces {current:.1f} amperes of current.", key="aud_circ_prim", lang=lang)
        elif p_key == "friction":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.friction_svg(lang), 480)
            with col2:
                st.markdown("### ⛸️ Rough vs Smooth Friction")
                st.markdown("Smooth ice has very low friction so skaters glide fast! Rough carpet has high friction so toy cars slow down quickly.")
        elif p_key == "gravity":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.gravity_svg(lang), 480)
            with col2:
                st.markdown("### 🍎 Gravity Pulls Everything Down")
                st.markdown("Earth attracts every object towards its center at $9.8 \\text{ m/s}^2$. Without gravity, people, water, and air would float away into space!")
        else:
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.blue_sky_svg(lang), 480)
            with col2:
                st.markdown("### 🌤️ Rayleigh Scattering")
                st.markdown("Sunlight looks white, but contains all rainbow colors. Earth's atmosphere scatters short blue wavelengths much more than red, making our sky blue!")

    else:
        st.markdown("#### 🎯 " + ("Middle School Mechanics & Wave Optics (Class 6 - 8)" if lang == "en" else "Middle School Mechanics & Wave Optics (6th se 8th)"))
        p_keys = list(C.PHYSICS.keys())
        p_titles = {k: C.PHYSICS[k]["title_" + lang] for k in p_keys}

        key = st.selectbox(
            "🔬 " + ("Choose Experiment:" if lang == "en" else "Experiment Chunein:"),
            p_keys,
            format_func=lambda k: p_titles[k],
            key="phys_exp_select"
        )
        p = C.PHYSICS[key]
        st.write(p[lang])
        st.markdown(f"<div class='formula'>{p['formula']}</div>", unsafe_allow_html=True)
        st.write("")

        if key == "projectile":
            c1, c2, c3 = st.columns(3)
            speed = c1.slider("Speed (m/s)", 5, 40, 20)
            angle = c2.slider("Angle (°)", 5, 85, 45)
            planet = c3.selectbox("Planet", list(V.PLANETS))
            st.plotly_chart(V.projectile_fig(speed, angle, planet), width="stretch", key="proj")

            st.markdown("##### 🎯 Target Challenge Mode")
            tg_col1, tg_col2 = st.columns([1, 2])
            target_m = tg_col1.slider("Target Distance (m)", 15, 60, 35)
            g = V.PLANETS.get(planet, 9.8)
            th = math.radians(angle)
            actual_range = (speed ** 2 * math.sin(2 * th)) / g
            diff = abs(actual_range - target_m)
            with tg_col2:
                if diff <= 1.5:
                    st.success(f"🎯 BULLSEYE DIRECT HIT! Range: {actual_range:.1f} m (Target: {target_m} m) 🎉")
                    add_xp(25, "Bullseye Target Hit!", badge_id="physics_wizard", badge_name="Physics Pro")
                elif diff <= 4.0:
                    st.warning(f"Almost there! Ball landed at {actual_range:.1f} m (Off by {diff:.1f} m).")
                else:
                    st.info(f"Ball landed at {actual_range:.1f} m (Target: {target_m} m).")

        elif key == "pendulum":
            c1, c2 = st.columns(2)
            length = c1.slider("String length (m)", 0.2, 3.0, 1.0, 0.1)
            amp = c2.slider("Starting angle (°)", 5, 40, 20)
            st.plotly_chart(V.pendulum_fig(length, amp), width="stretch", key="pend")
            st.metric("Time period T", f"{V.pendulum_metrics(length):.2f} s")
        elif key == "ohm":
            c1, c2 = st.columns(2)
            volts = c1.slider("Voltage V (volts)", 1, 12, 6)
            ohms = c2.slider("Resistance R (ohms)", 1, 20, 3)
            left, right = st.columns(2)
            with left:
                show_svg(V.circuit_svg(volts, ohms), 440)
            with right:
                st.plotly_chart(V.vi_fig(volts, ohms), width="stretch", key="vi")
        elif key == "force":
            show_svg(V.force_svg(lang), 480)
        elif key == "sky":
            show_svg(V.blue_sky_svg(lang), 480)
        elif key == "gravity":
            show_svg(V.gravity_svg(lang), 480)
        elif key == "friction":
            show_svg(V.friction_svg(lang), 480)
        else:
            c1, c2, c3 = st.columns(3)
            m1 = c1.selectbox("Top material", list(V.MEDIA), index=0)
            m2 = c2.selectbox("Bottom material", list(V.MEDIA), index=1)
            ang = c3.slider("Angle of light (°)", 5, 80, 40)
            st.plotly_chart(V.refraction_fig(V.MEDIA[m1], V.MEDIA[m2], ang), width="stretch", key="refr")

        st.markdown(f"<div class='act'>🏠 <b>{t['tryit']}:</b> {p['activity_' + lang]}</div>", unsafe_allow_html=True)
        if st.button("🧪 I tried it" if lang == "en" else "🧪 Maine try kiya", key=f"tried{key}"):
            log("practical", "Physics", p["title_en"])
            add_xp(20, f"Tried {p['title_en']} experiment!", badge_id="physics_wizard", badge_name="Physics Pro")
            st.toast("Scientist in the making! 🔬")


# ----------------------------------------------------------------------------- chemistry tab
def tab_chem(lang, age="10-12", api_key=None, model=None):
    t = TXT[lang]
    st.subheader(t["tabs"][3])

    render_section_tools(
        "chem",
        "Chemistry Lab",
        "Search atom builder, molecules, states of matter, pH scale, reactions..." if lang == "en" else "Chemistry sawaal khojein (atom, molecule, pH scale, reaction)...",
        lang, age, api_key, model
    )

    tier_id = render_class_tier_header("chem", lang)

    if tier_id == "early":
        st.markdown("#### 🧪 " + ("Early Chemistry: Fun Mixtures & States (Nursery to Class 2)" if lang == "en" else "Nannha Rasayan Vigyan (Nursery se 2nd)"))
        e_c_topics = [
            ("🧊 " + ("Ice, Water & Steam: How Ice Melts" if lang == "en" else "Baraf, Paani aur Bhaap"), "ice_melt"),
            ("🫧 " + ("Soap Bubble Magic" if lang == "en" else "Sabun Ke Bulbule"), "bubbles"),
            ("🎨 " + ("Rainbow Color Mixing" if lang == "en" else "Rang Milana (Color Mixing)"), "color_mixing"),
        ]
        e_pick = st.selectbox("Choose Activity", range(len(e_c_topics)), format_func=lambda idx: e_c_topics[idx][0], key="chem_early_pick")
        e_key = e_c_topics[e_pick][1]

        if e_key == "ice_melt":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                stage = st.select_slider("Temperature / Stage", ["ice", "melt", "steam"], value="melt",
                                         format_func=lambda s: "🧊 Frozen Cold Ice (0°C)" if s=="ice" else ("💧 Melting Water (25°C)" if s=="melt" else "☁️ Hot Steam Cloud (100°C)"), key="ice_stage_slider")
                show_svg(V.ice_melt_svg(stage, lang), 480)
            with col2:
                st.markdown("### 🧊 The Story of Water!")
                st.markdown("• **Ice Cube:** Water molecules freeze into a hard, slippery crystal solid.<br>• **Warm Sun:** Ice melts into flowing, splashy liquid water!<br>• **Hot Kettle:** Water boils into invisible steam gas that floats in the air!", unsafe_allow_html=True)
                read_aloud("Ice melts into liquid water, and boils into steam gas.", key="aud_ice_chem", lang=lang)
                if st.button("⭐ " + ("I Melted the Ice! (+15 XP)" if lang == "en" else "Maine Baraf Pighlayi! (+15 XP)"), key="btn_xp_ice"):
                    add_xp(15, "Learned how solids melt into liquids and evaporate into gas!", badge_id="chem_wizard", badge_name="Chem Wizard")

        elif e_key == "bubbles":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                show_svg(V.states_svg("gas"), 360)
            with col2:
                st.markdown("### 🫧 Stretchy Soap Bubbles")
                st.markdown("Water has an invisible stretchy skin called surface tension. When you add gentle soap, it stretches like a balloon and traps air inside shimmering rainbow spheres!")
                if st.button("⭐ " + ("I Discovered Bubble Science! (+15 XP)" if lang == "en" else "Maine Bulbula Science Seekha! (+15 XP)"), key="btn_xp_bub"):
                    add_xp(15, "Learned surface tension and soap bubbles!")

        else:
            col1, col2 = st.columns([1.2, 1])
            with col1:
                c_mix = st.radio("Mix Colors", ["🔴 Red + 🟡 Yellow = 🟠 Orange", "🔵 Blue + 🟡 Yellow = 🟢 Green", "🔴 Red + 🔵 Blue = 🟣 Purple"], horizontal=True, key="c_mix_radio")
                show_svg(V.states_svg("liquid"), 360)
            with col2:
                st.markdown(f"### {c_mix}")
                st.markdown("Primary colors blend their light absorption to make brand new secondary colors! That is how painters and printers create millions of vibrant shades.")

    elif tier_id == "primary":
        st.markdown("#### 🌋 " + ("Junior Chemistry: Matter & Safe Reactions (Class 3 - 5)" if lang == "en" else "Junior Rasayan Vigyan: Padarth aur Surakshit Reactions (3rd se 5th)"))
        p_tabs = st.tabs(["🧊 3 States of Matter", "🌋 Kitchen Volcano Lab", "🍋 Safe Kitchen pH", "🏠 Home Experiments"])
        with p_tabs[0]:
            state = st.radio("Choose State of Matter", list(C.STATES), horizontal=True,
                             format_func=lambda k: C.STATES[k]["hi_name" if lang == "hi" else "en_name"], key="chem_p_state")
            c1, c2 = st.columns([1, 1])
            with c1:
                show_svg(V.states_svg(state), 360)
            with c2:
                st.write(C.STATES[state][lang])
        with p_tabs[1]:
            st.markdown("##### 🌋 Baking Soda + Vinegar Volcano")
            show_svg(V.reaction_svg("volcano", lang), 480)
            if st.button("🧪 Mix Baking Soda & Vinegar!", key="btn_p_volcano"):
                st.success("🎉 FZZZZZ! Sodium bicarbonate + Acetic acid produces Carbon Dioxide gas bubbles!")
                add_xp(15, "Created a kitchen volcano reaction!")
        with p_tabs[2]:
            sub = st.select_slider("Choose Substance", ["lemon", "water", "soap"], value="water",
                                   format_func=lambda k: C.PH_SUBSTANCES[k][1 if lang=="hi" else 0], key="chem_p_ph")
            en, hi, val = C.PH_SUBSTANCES[sub]
            show_svg(V.ph_svg(val, hi if lang=="hi" else en), 500)
        with p_tabs[3]:
            for k, act in C.HOME_ACTIVITIES.items():
                st.markdown(f"<div class='act'><b>{act['title_' + lang]}</b><br>{act[lang]}</div>", unsafe_allow_html=True)
                st.write("")

    else:
        st.markdown("#### ⚛️ " + ("Middle School Chemistry & Atomic Structure (Class 6 - 8)" if lang == "en" else "Middle School Rasayan Vigyan (6th se 8th)"))
        a, m, s, p, rx, h = st.tabs([
            "⚛️ Atom builder", "💧 Molecules", "🧊 States of matter", "🍋 pH scale", "🌋 Virtual Reaction Lab", "🏠 Home experiments"
        ])
        with a:
            st.write(C.CHEM_TEXT["atom"][lang])
            z = st.slider("Number of protons (Z)", 1, 20, 8, key="atom_m_z")
            el = C.ELEMENT_BY_Z[z]
            c1, c2 = st.columns([1, 1])
            with c1:
                show_svg(V.atom_svg(z), 360)
            with c2:
                use = C.ELEMENT_USE.get(z)
                st.markdown(f"### {el[2]} ({el[1]})")
                st.write(f"Protons: **{z}**, Neutrons: **{el[3]}**, Electrons: **{z}**")
                st.write(f"Electron shells: **{', '.join(map(str, V.electron_shells(z)))}**")
                if use:
                    st.markdown(f"<div class='fact'>💡 {use[0] if lang == 'en' else use[1]}</div>", unsafe_allow_html=True)
        with m:
            st.write(C.CHEM_TEXT["molecule"][lang])
            key = st.selectbox("Molecule", list(C.MOLECULES), format_func=lambda k: f"{C.MOLECULES[k]['formula']}  {C.MOLECULES[k]['name_en']}", key="mol_m_key")
            st.plotly_chart(V.molecule_fig(key), width="stretch", key="mol")
            st.info(C.MOLECULES[key][lang])
        with s:
            st.write(C.CHEM_TEXT["states"][lang])
            state = st.radio("State", list(C.STATES), horizontal=True,
                             format_func=lambda k: C.STATES[k]["hi_name" if lang == "hi" else "en_name"], key="chem_m_state")
            c1, c2 = st.columns([1, 1])
            with c1:
                show_svg(V.states_svg(state), 340)
            with c2:
                st.write(C.STATES[state][lang])
        with p:
            st.write(C.CHEM_TEXT["ph"][lang])
            sub = st.select_slider("Choose a substance", list(C.PH_SUBSTANCES),
                                   format_func=lambda k: C.PH_SUBSTANCES[k][1 if lang == "hi" else 0], value="water", key="chem_m_ph")
            en, hi, val = C.PH_SUBSTANCES[sub]
            show_svg(V.ph_svg(val, hi if lang == "hi" else en), 520)
            kind = "acid" if val < 7 else "base" if val > 7 else "neutral"
            st.write(f"pH **{val:g}** → **{kind}**")
        with rx:
            st.markdown("#### 🧪 Safe Virtual Reaction Simulator")
            rx_key = st.selectbox(
                "Select Reaction Experiment",
                ["volcano", "indicator", "dissolve"],
                format_func=lambda k: (
                    "🌋 Baking Soda + Vinegar (CO2 Fizz)" if k == "volcano" else
                    ("🎨 Red Cabbage Juice + Lemon (Anthocyanin pH Shift)" if k == "indicator" else "🧂 Salt Crystal Dissolving in Water (Ions)")
                ),
                key="chem_m_rx_key"
            )
            show_svg(V.reaction_svg(rx_key, lang), 480)
            if st.button("🧪 Mix Ingredients & Observe", key=f"btn_rx_{rx_key}"):
                add_xp(20, "Virtual chemical reaction simulated!", badge_id="chem_wizard", badge_name="Chem Wizard")
                st.toast("Reaction Successful! 🌟")
        with h:
            for k, act in C.HOME_ACTIVITIES.items():
                st.markdown(f"<div class='act'><b>{act['title_' + lang]}</b><br>{act[lang]}</div>", unsafe_allow_html=True)
                st.write("")


# ----------------------------------------------------------------------------- mathematics tab (Class 1 to 8)
def tab_maths(lang, age="10-12", api_key=None, model=None):
    t = TXT[lang]
    st.subheader(t["tabs"][4])

    render_section_tools(
        "math",
        "Mathematics",
        "Search circle area, pythagoras, cylinder volume, fractions, algebra..." if lang == "en" else "Maths sawaal khojein (area, pythagoras, fraction, algebra)...",
        lang, age, api_key, model
    )

    tier_id = render_class_tier_header("math", lang)

    if tier_id == "early":
        st.markdown("#### 🎈 " + ("Early Math: Counting, Shapes & Candy Addition (Nursery to Class 2)" if lang == "en" else "Nannha Ganit: Ginti, Aakar aur Candy Jod (Nursery se 2nd)"))
        e_m_topics = [
            ("🍎 " + ("Counting Fruits & Stars (1 to 10)" if lang == "en" else "Phal aur Taare Ginto (1 se 10)"), "counting"),
            ("🔷 " + ("Fun Shapes Explorer (Circle, Square, Star)" if lang == "en" else "Shapes Explorer (Gola, Chaukona, Taara)"), "shapes"),
            ("🍬 " + ("Sweet Candy Addition & Adding Up" if lang == "en" else "Sweet Candy Jod (Addition)"), "candy_addition"),
        ]
        e_pick = st.selectbox("Choose Math Activity", range(len(e_m_topics)), format_func=lambda idx: e_m_topics[idx][0], key="math_early_pick")
        e_key = e_m_topics[e_pick][1]

        if e_key == "counting":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                n_count = st.slider("Count", 1, 10, 5, key="m_early_cnt_slider")
                show_svg(V.counting_fruits_svg(n_count, lang), 480)
            with col2:
                st.markdown(f"### 🍎 Number {n_count}!")
                st.markdown(f"You have **{n_count}** delicious crunchy red apples in your basket! Let's count them out loud together: 1... 2... {n_count}!")
                read_aloud(f"Number {n_count}. You counted {n_count} apples!", key=f"aud_cnt_{n_count}", lang=lang)
                if st.button("⭐ " + ("I Counted Correctly! (+15 XP)" if lang == "en" else "Maine Sahi Gina! (+15 XP)"), key=f"btn_xp_cnt_{n_count}"):
                    add_xp(15, f"Counted up to {n_count}!", badge_id="math_star", badge_name="Math Star")

        elif e_key == "shapes":
            col1, col2 = st.columns([1.2, 1])
            with col1:
                sh_pick = st.radio("Pick a Shape", ["Circle 🟡", "Square 🟦", "Triangle 🔺", "Star ⭐"], horizontal=True, key="m_early_shape_rad")
                sh_code = "circle" if "Circle" in sh_pick else ("square" if "Square" in sh_pick else ("triangle" if "Triangle" in sh_pick else "star"))
                show_svg(V.basic_shapes_svg(sh_code, lang), 480)
            with col2:
                st.markdown(f"### {sh_pick}")
                if sh_code == "circle":
                    st.markdown("A Circle is round like a ball, a coin, or the full moon! It has 0 straight corners and rolls smoothly.")
                elif sh_code == "square":
                    st.markdown("A Square has 4 equal straight sides and 4 sharp corners, just like a picture frame or a cracker!")
                elif sh_code == "triangle":
                    st.markdown("A Triangle has 3 sides and 3 pointy tips, just like a slice of delicious pizza or a party hat!")
                else:
                    st.markdown("A Star shines bright in the night sky with 5 glowing golden points!")
                read_aloud(f"Shape: {sh_pick}", key=f"aud_sh_{sh_code}", lang=lang)
                if st.button("⭐ " + ("I Learned This Shape! (+15 XP)" if lang == "en" else "Maine Yeh Shape Seekha! (+15 XP)"), key=f"btn_xp_sh_{sh_code}"):
                    add_xp(15, f"Learned shape {sh_pick}!", badge_id="math_star", badge_name="Math Star")

        else:
            col1, col2 = st.columns([1.2, 1])
            with col1:
                c_a = st.slider("Pink Candies", 1, 5, 2, key="candy_a_slider")
                c_b = st.slider("Blue Candies", 1, 5, 3, key="candy_b_slider")
                show_svg(V.candy_addition_svg(c_a, c_b, lang), 480)
            with col2:
                total_c = c_a + c_b
                st.markdown(f"### 🍬 {c_a} + {c_b} = {total_c} Candies!")
                st.markdown(f"When you put **{c_a} pink candies** together with **{c_b} blue candies**, you have **{total_c} candies in all**!")
                read_aloud(f"{c_a} plus {c_b} equals {total_c}!", key=f"aud_candy_{total_c}", lang=lang)
                if st.button("⭐ " + ("I Solved It! (+15 XP)" if lang == "en" else "Maine Hal Kiya! (+15 XP)"), key=f"btn_xp_candy_{total_c}"):
                    add_xp(15, f"Solved visual addition {c_a} + {c_b} = {total_c}!", badge_id="math_star", badge_name="Math Star")

    elif tier_id == "primary":
        st.markdown("#### 🍕 " + ("Junior Mathematics: Fractions, Shapes & Speed Math (Class 3 - 5)" if lang == "en" else "Junior Ganit: Fractions, Shapes aur Speed Math (3rd se 5th)"))
        p_math_tabs = st.tabs(["🍕 Fraction Pizza", "📐 Rectangle & Triangle Area", "⚡ Speed Math Arena"])
        with p_math_tabs[0]:
            fr_c1, fr_c2 = st.columns([1, 1.2])
            with fr_c1:
                den_val = st.slider("Denominator (Total Pizza Slices)", 1, 12, 8, key="fr_p_den")
                num_val = st.slider("Numerator (Eaten Slices)", 0, den_val, min(3, den_val), key="fr_p_num")
                fr_pct = (num_val / den_val) * 100
                st.info(f"🍕 **{num_val} out of {den_val} slices** = **{fr_pct:.1f}%**")
                read_aloud(f"{num_val} over {den_val} equals {fr_pct:.1f} percent.", key="aud_p_frac", lang=lang)
            with fr_c2:
                show_svg(V.fraction_pizza_svg(num_val, den_val, lang), 440)
        with p_math_tabs[1]:
            sh = st.radio("Shape", ["Rectangle", "Triangle"], horizontal=True, key="sh_p_rad")
            if sh == "Rectangle":
                c1, c2 = st.columns([1, 1.2])
                with c1:
                    l = st.slider("Length (cm)", 2, 20, 8, key="sh_p_l")
                    w = st.slider("Width (cm)", 1, 15, 5, key="sh_p_w")
                    st.info(f"Perimeter = 2({l} + {w}) = **{2*(l+w)} cm**\n\nArea = {l} × {w} = **{l*w} cm²**")
                with c2:
                    show_svg(V.math_geometry_svg("rectangle", {"l": l, "w": w}, lang), 440)
            else:
                c1, c2 = st.columns([1, 1.2])
                with c1:
                    b = st.slider("Base (cm)", 2, 20, 8, key="sh_p_b")
                    h = st.slider("Height (cm)", 1, 15, 6, key="sh_p_h")
                    st.info(f"Area = ½ × base × height = **{0.5*b*h:g} cm²**")
                with c2:
                    show_svg(V.math_geometry_svg("triangle", {"b": b, "h": h}, lang), 440)
        with p_math_tabs[2]:
            q_list = [
                ("14 + 19 = ?", ["31", "33", "35", "37"], 1, "14 + 19 = 33"),
                ("50 - 23 = ?", ["27", "28", "25", "37"], 0, "50 - 23 = 27"),
                ("Double of 16 is:", ["28", "30", "32", "34"], 2, "16 × 2 = 32"),
            ]
            for s_idx, (s_q, s_opts, s_ans, s_ex) in enumerate(q_list):
                with st.container(border=True):
                    st.markdown(f"**Question {s_idx + 1}: {s_q}**")
                    ch = st.radio("Answer", s_opts, index=None, key=f"sp_p_{s_idx}", label_visibility="collapsed")
                    if ch is not None and st.button("Check Answer ✅", key=f"btn_p_sp_{s_idx}"):
                        if s_opts.index(ch) == s_ans:
                            st.success(f"🎉 Correct! {s_ex}")
                            add_xp(15, f"Solved Junior Math Question {s_idx + 1}!")
                        else:
                            st.error(f"Try again! Explanation: {s_ex}")

    else:
        st.markdown("#### 📐 " + ("Senior Mathematics, Mensuration & Algebra (Class 6 - 8)" if lang == "en" else "Senior Ganit, Mensuration & Algebra (6th se 8th)"))
        m_tabs = st.tabs([
            "🥫 3D Cylinder Mensuration",
            "🔺 Pythagoras Theorem",
            "⚖️ Algebra Balance Scale",
            "🍕 Fractions & Percentages",
            "⚡ Senior Speed Math Arena"
        ])
        with m_tabs[0]:
            c1, c2 = st.columns([1, 1.2])
            with c1:
                cyl_r = st.slider("Radius r (cm)", 1, 10, 4, key="cyl_m_r")
                cyl_h = st.slider("Height h (cm)", 2, 20, 8, key="cyl_m_h")
                csa = 2 * math.pi * cyl_r * cyl_h
                tsa = 2 * math.pi * cyl_r * (cyl_r + cyl_h)
                vol = math.pi * (cyl_r ** 2) * cyl_h
                st.markdown(f"""
                <div style="background:rgba(16,185,129,0.1);border-left:4px solid #10b981;border-radius:10px;padding:12px;font-size:0.95rem;line-height:1.6;">
                  <b>📐 Formulations:</b><br>
                  • <b>Curved Surface Area (CSA):</b> 2πrh = <b>{csa:.1f} cm²</b><br>
                  • <b>Total Surface Area (TSA):</b> 2πr(r+h) = <b>{tsa:.1f} cm²</b><br>
                  • <b>Capacity / Volume:</b> πr²h = <b>{vol:.1f} cm³</b> ({vol/1000:.3f} L)
                </div>
                """, unsafe_allow_html=True)
            with c2:
                show_svg(V.math_geometry_svg("cylinder", {"r": cyl_r, "h": cyl_h}, lang), 440)
        with m_tabs[1]:
            py_c1, py_c2 = st.columns([1, 1.2])
            with py_c1:
                py_a = st.slider("Side a (Leg 1)", 1, 12, 3, key="py_m_a")
                py_b = st.slider("Side b (Leg 2)", 1, 12, 4, key="py_m_b")
                c_val = math.sqrt(py_a**2 + py_b**2)
                if abs(c_val - round(c_val)) < 1e-6:
                    st.success(f"🌟 WOW! ({py_a}, {py_b}, {int(round(c_val))}) is a famous Pythagorean Triplet!")
                    add_xp(20, f"Discovered triplet ({py_a}, {py_b}, {int(round(c_val))})!")
            with py_c2:
                show_svg(V.pythagoras_svg(py_a, py_b, lang), 440)
        with m_tabs[2]:
            alg_c1, alg_c2 = st.columns([1, 1.2])
            with alg_c1:
                eq_a = st.slider("Coefficient a", 1, 6, 2, key="alg_m_a")
                eq_b = st.slider("Constant b", 1, 20, 5, key="alg_m_b")
                eq_c = st.slider("Target c", eq_b + 1, 50, 15, key="alg_m_c")
                x_sol = (eq_c - eq_b) / eq_a
                st.success(f"✨ Equation: **{eq_a}x + {eq_b} = {eq_c}**  ➔  **x = {x_sol:.2f}**")
            with alg_c2:
                show_svg(V.algebra_balance_svg(eq_a, eq_b, eq_c, lang), 440)
        with m_tabs[3]:
            fr_c1, fr_c2 = st.columns([1, 1.2])
            with fr_c1:
                den_val = st.slider("Denominator", 1, 12, 8, key="fr_m_den")
                num_val = st.slider("Numerator", 0, den_val, min(3, den_val), key="fr_m_num")
                st.info(f"🍕 **{num_val} / {den_val}** = **{(num_val/den_val)*100:.1f}%**")
            with fr_c2:
                show_svg(V.fraction_pizza_svg(num_val, den_val, lang), 440)
        with m_tabs[4]:
            q_list = [
                ("Solve for x: 3x - 7 = 14", ["x = 5", "x = 7", "x = 9", "x = 6"], 1, "3x = 21 ➔ x = 7"),
                ("What is 15% of 200?", ["20", "25", "30", "35"], 2, "(15/100) × 200 = 30"),
                ("In right triangle with legs 6 and 8, hypotenuse is:", ["9", "10", "12", "14"], 1, "√(6² + 8²) = √100 = 10"),
            ]
            for s_idx, (s_q, s_opts, s_ans, s_ex) in enumerate(q_list):
                with st.container(border=True):
                    st.markdown(f"**Question {s_idx + 1}: {s_q}**")
                    ch = st.radio("Answer", s_opts, index=None, key=f"sp_m_{s_idx}", label_visibility="collapsed")
                    if ch is not None and st.button("Check Answer ✅", key=f"btn_m_sp_{s_idx}"):
                        if s_opts.index(ch) == s_ans:
                            st.success(f"🎉 Correct! {s_ex}")
                            add_xp(20, f"Solved Senior Math Question {s_idx + 1}!")
                        else:
                            st.error(f"Try again! Explanation: {s_ex}")


# ----------------------------------------------------------------------------- quiz arena
def tab_quiz(lang):
    t = TXT[lang]
    st.subheader(t["tabs"][6])
    subjects = ["All"] + sorted({q["subject"] for q in C.QUIZ})
    subj = st.radio("Subject", subjects, horizontal=True)
    qs = [(i, q) for i, q in enumerate(C.QUIZ) if subj == "All" or q["subject"] == subj]
    done = st.session_state["quiz_done"]

    # Scoreboard and Streak Banner
    if done:
        score = sum(done.values())
        total = len(done)
        pct = (score / total) * 100
        st.progress(score / total, text=f"Score: {score} / {total} correct ({pct:.0f}%) ⭐")
        if score == total and total >= 3:
            st.balloons()
            st.success("🌟 FLAWLESS STREAK! You are a certified Science Genius! 🏆")

    for i, q in qs:
        with st.container(border=True):
            st.markdown(f"**{q['q_' + lang]}**")
            read_aloud(q["q_" + lang], key=f"q_audio_{i}", lang=lang)
            choice = st.radio("Answer", q["options"], index=None, key=f"q{i}", label_visibility="collapsed")
            if choice is not None and st.button("Check ✅" if lang == "en" else "Check karo ✅", key=f"chk{i}"):
                right = q["options"].index(choice) == q["answer"]
                done[i] = right
                log("quiz", q["subject"], q["q_en"][:40], correct=right)
                if right:
                    add_xp(25, "Correct Quiz Answer!", badge_id="quiz_champion", badge_name="Quiz Master")
            if i in done:
                (st.success if done[i] else st.error)(
                    ("Correct! 🎉 " if done[i] else "Not quite. 🙂 ") + q["ex_" + lang] if lang == "en" else
                    ("Sahi jawab! 🎉 " if done[i] else "Thoda galat. 🙂 ") + q["ex_" + lang])


# ----------------------------------------------------------------------------- parent & awards corner
def tab_parent(lang):
    st.subheader(TXT[lang]["tabs"][7])
    st.caption("🔒 Privacy: GyaanBuddy keeps only topic labels in this browser session. It does not store your child's "
               "words, name or any personal details, and nothing is saved when the page is closed.")

    ev = pd.DataFrame(st.session_state["events"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Questions asked", int((ev.kind == "question").sum()) if not ev.empty else 0)
    c2.metric("Labs / lessons done", int(ev.kind.isin(["learned", "practical"]).sum()) if not ev.empty else 0)
    quiz = ev[ev.kind == "quiz"] if not ev.empty else pd.DataFrame()
    c3.metric("Quiz accuracy", f"{quiz['correct'].mean():.0%}" if len(quiz) else "n/a")
    c4.metric("Unsafe requests blocked", int((ev.kind == "blocked").sum()) if not ev.empty else 0)

    if not ev.empty:
        learn = ev[ev.kind.isin(["question", "learned", "practical", "quiz", "explored"]) & (ev.subject != "")]
        if not learn.empty:
            by = learn.groupby("subject").size().reset_index(name="activities")
            st.plotly_chart(px.bar(by, x="subject", y="activities", title="Time spent by subject", color="subject"),
                            width="stretch", key="parent_subj")
            st.write("**Topics explored:** " + ", ".join(sorted(set(learn.topic.astype(str)))))
        blocked = ev[ev.kind == "blocked"]
        if not blocked.empty:
            st.warning("Blocked categories: " + ", ".join(sorted(set(blocked.topic.astype(str)))) +
                       ". If your child seems upset, please talk to them. Childline India: 1098.")
        st.download_button("📊 " + ("Download Progress Report (CSV)" if lang == "en" else "Progress Report Download Karein (CSV)"),
                           ev.to_csv(index=False).encode("utf-8"), "gyaanbuddy_progress.csv", "text/csv; charset=utf-8",
                           use_container_width=True, key="btn_dl_parent_csv")

    st.divider()

    # Official Junior Scientist Certificate of Excellence
    st.markdown("### 🏅 " + ("Junior Scientist Certificate of Excellence" if lang == "en" else "Vigyan Pratibha Praman Patra"))
    st.caption("Enter student's name to generate and print your official certificate of achievement!" if lang == "en" else
               "Student ka naam daal kar apna official certificate generate aur print karein!")

    c_name_col, _ = st.columns([1.5, 2])
    student_name = c_name_col.text_input("Student Full Name", value=st.session_state["student_name"], key="cert_name_input")
    st.session_state["student_name"] = student_name

    cert_html = generate_certificate_html(student_name, st.session_state["xp"], lang)
    st.components.v1.html(cert_html, height=360)
    st.download_button("🏅 " + ("Download Certificate (HTML)" if lang == "en" else "Certificate Download Karein (HTML)"),
                       cert_html.encode("utf-8"), f"GyaanBuddy_Certificate_{student_name}.html", "text/html; charset=utf-8",
                       use_container_width=True, key="btn_dl_parent_cert")


# ----------------------------------------------------------------------------- main
def main():
    init_state()
    lang, age, api_key, model = sidebar()
    apply_theme(st.session_state.get("theme", "🌈 Wonder Academy (Nursery - Class 8)"))

    # Top Hero Banner with Class Level & GyaanBuddy
    raw_class = str(st.session_state.get("class_level", "5"))
    class_lvl = f"Class {raw_class}" if raw_class.isdigit() else raw_class
    xp = st.session_state["xp"]
    lvl_num, lvl_en, lvl_hi, _ = get_level(xp)
    lvl_title = lvl_hi if lang == "hi" else lvl_en

    btn_menu_label = "☰ Menu" if lang == "en" else "☰ Menu"
    st.markdown(f"""
    <div class="hero-banner">
      <div style="display:flex; justify-content:space-between; align-items:center; width:100%; flex-wrap:wrap; gap:12px;">
        <div>
          <div class="hero-title" style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span>🧠 GyaanBuddy •</span>
            <button type="button"
                    onclick="(function(){{var p=window.parent||window;if(p.__gb_toggle_sidebar){{p.__gb_toggle_sidebar();return;}}var d=p.document;var b=d.querySelector('[data-testid=\\'stSidebarCollapsedControl\\'] button')||d.querySelector('[data-testid=\\'collapsedControl\\'] button')||d.querySelector('header button');if(b)b.click();}})()"
                    style="font-size:0.95rem;background:rgba(255,255,255,0.25);border:1px solid rgba(255,255,255,0.5);color:#ffffff;padding:4px 12px;border-radius:12px;cursor:pointer;font-weight:700;display:inline-flex;align-items:center;gap:6px;">
              🎓 {class_lvl}
            </button>
          </div>
          <div class="hero-sub">{"Your friendly AI science & math buddy • Learn the fun way!" if lang == "en" else "Aapka friendly vigyan aur ganit saathi • Seekho mazedaar tareeke se!"}</div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
          <button type="button"
                  id="btn-hero-menu-toggle"
                  onclick="(function(){{var p=window.parent||window;if(p.__gb_toggle_sidebar){{p.__gb_toggle_sidebar();return;}}var d=p.document;var b=d.querySelector('[data-testid=\\'stSidebarCollapsedControl\\'] button')||d.querySelector('[data-testid=\\'collapsedControl\\'] button')||d.querySelector('header button');if(b)b.click();}})()"
                  style="background:#ffffff; color:#4338ca; border:2px solid #6366f1; border-radius:12px; font-weight:800; font-size:0.85rem; padding:6px 14px; cursor:pointer; box-shadow:0 3px 10px rgba(0,0,0,0.18); display:inline-flex; align-items:center; gap:6px;">
            {btn_menu_label}
          </button>
          <span class="xp-pill">⭐ {xp} XP</span>
          <span class="xp-pill">{lvl_title}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(TXT[lang]["tabs"])
    with tabs[0]:
        tab_chat(lang, age, api_key, model)
    with tabs[1]:
        tab_nature(lang, age, api_key, model)
    with tabs[2]:
        tab_physics(lang, age, api_key, model)
    with tabs[3]:
        tab_chem(lang, age, api_key, model)
    with tabs[4]:
        tab_maths(lang, age, api_key, model)
    with tabs[5]:
        tab_body(lang, age, api_key, model)
    with tabs[6]:
        tab_snap_solve(lang, age, api_key, model)
    with tabs[7]:
        tab_quiz(lang)
    with tabs[8]:
        tab_parent(lang)

    # Footer with Creator Credit
    st.markdown("""
    <div style="margin-top: 50px; padding: 24px 0 16px 0; border-top: 1px solid rgba(255, 255, 255, 0.15); text-align: center;">
      <p style="margin: 0; font-size: 1.05rem; font-weight: 600; letter-spacing: 0.3px;">
        Made with ❤️ for young scientists &amp; curious minds by <span style="background: linear-gradient(135deg, #38bdf8, #818cf8, #f43f5e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.25rem;">Mahdi Nawaz</span>
      </p>
      <p style="margin: 6px 0 0 0; font-size: 0.85rem; opacity: 0.75;">
        🧠 GyaanBuddy • Kid-Safe AI Science &amp; Math Buddy &amp; Interactive Learning Lab
      </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

