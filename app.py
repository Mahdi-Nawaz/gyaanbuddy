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

    /* Hide Streamlit default clutter and badges that overlap mobile footer */
    #MainMenu {{visibility: hidden !important; display: none !important;}}
    footer {{visibility: hidden !important; display: none !important;}}
    header {{visibility: hidden !important;}}
    .viewerBadge_container {{display: none !important;}}
    .stDeployButton {{display: none !important;}}
    div[data-testid="stToolbar"] {{visibility: hidden !important;}}

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
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

TXT = {
    "en": dict(
        ask="Ask me anything about science or math…",
        tabs=["💬 Ask Buddy", "📸 Snap & Solve", "🧍 Human Body", "⚡ Physics Lab", "🧪 Chemistry Lab", "📐 Mathematics", "🎯 Quiz Arena", "👨‍👩‍👧 Parent & Awards"],
        tryit="Try it at home (with an adult)",
        fact="Fun fact", next="Next ➡", prev="⬅ Previous", all="Show all organs",
        mystery="Mystery Science Question of the Day:"
    ),
    "hi": dict(
        ask="Science ya Maths ke baare mein kuch bhi poochho…",
        tabs=["💬 Buddy se poochho", "📸 Snap & Solve", "🧍 Insaani Sharir", "⚡ Physics Lab", "🧪 Chemistry Lab", "📐 Ganit (Maths)", "🎯 Quiz Arena", "👨‍👩‍👧 Parent & Awards"],
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


def render_search_hub(lang: str):
    """Unified Topic Search Hub with fast indexing, interactive diagram viewer and voiceover."""
    st.markdown("### 🔍 " + ("Explore & Search Topics" if lang == "en" else "Vigyan Topics Khojein"))
    st.caption("Search across 68+ interactive topics: Human Body, Physics Labs, Chemical Elements, Reactions, and Quizzes!" if lang == "en" else
               "68+ interactive topics khojein: Insaani Sharir, Physics Labs, Elements, Reactions aur Quizzes!")

    # Search bar row with Search and Clear buttons
    col_input, col_search, col_clear = st.columns([5.5, 1.2, 1.2])
    with col_input:
        current_q = st.session_state.get("search_query", "")
        query_val = st.text_input(
            "Topic Search Input",
            value=current_q,
            placeholder="🔍 " + ("Type any topic: Heart, Lungs, Gravity, Pendulum, Circuit, Oxygen, Water, Acid, Volcano..." if lang == "en" else "Topic likhein: Dil, Fefde, Pendulum, Circuit, Oxygen, Paani, Acid, Volcano..."),
            key="topic_search_input",
            label_visibility="collapsed"
        )
    with col_search:
        if st.button("🔍 " + ("Search" if lang == "en" else "Khojein"), key="btn_do_search", width="stretch"):
            st.session_state["search_query"] = query_val
            st.rerun()
    with col_clear:
        if st.button("✖️ " + ("Clear" if lang == "en" else "Saaf"), key="btn_clear_search", width="stretch"):
            st.session_state["search_query"] = ""
            st.rerun()

    # Active Query Results
    active_q = (st.session_state.get("search_query") or query_val).strip()
    if active_q:
        results = search_topics(active_q, limit=8)
        if results:
            st.markdown(f"#### 🎯 " + (f"Found {len(results)} topics for **'{active_q}'**:" if lang == "en" else f"**'{active_q}'** ke liye {len(results)} topics mile:"))
            for r_idx, item in enumerate(results):
                title = item["title_hi"] if lang == "hi" else item["title_en"]
                cat = item["category_hi"] if lang == "hi" else item["category_en"]
                desc = item["desc_hi"] if lang == "hi" else item["desc_en"]

                with st.container():
                    st.markdown(f"""
                    <div class="search-card">
                      <span class="search-badge">{cat}</span>
                      <h3 style="margin:4px 0 8px 0;font-size:1.25rem;">{item['icon']} {title}</h3>
                      <p style="margin:0 0 10px 0;font-size:0.95rem;line-height:1.5;">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    btn_c1, btn_c2, _ = st.columns([1.5, 1.5, 2])
                    with btn_c1:
                        read_aloud(desc, key=f"srch_aud_{r_idx}", lang=lang)
                    with btn_c2:
                        ask_q = f"Tell me more about {item['title_en']}" if lang == "en" else f"{item['title_hi']} ke baare mein aur batao"
                        if st.button("💬 " + ("Ask Buddy" if lang == "en" else "Buddy se poochhein"), key=f"srch_ask_{r_idx}", width="stretch"):
                            st.session_state["pending"] = ask_q
                            st.toast("Redirecting to Buddy Chat...", icon="💬")
                            st.rerun()

                    # Interactive Diagram Inline Preview
                    spec = item.get("spec")
                    if spec and spec != "quiz":
                        with st.expander("🖼️ " + ("View Interactive Diagram / Model" if lang == "en" else "Interactive Model / Diagram Dekhein")):
                            show_visual(spec, lang, key=f"srch_vis_{r_idx}")
                            add_xp(5, f"Explored {title} diagram in search", "curious_spark")
                st.divider()
        else:
            st.info("💡 " + (f"No direct matches found for '{active_q}'. Try searching for: 'heart', 'lungs', 'circuit', 'acid', 'atom', 'water' or ask Buddy in the chat below!"
                             if lang == "en" else f"'{active_q}' ke liye koi topic nahi mila. 'dil', 'fefde', 'circuit', 'acid', 'atom', 'paani' dhoondhein ya neeche Buddy se poochhein!"))
            if st.button("💬 " + (f"Ask Buddy: \"{active_q}\"" if lang == "en" else f"Buddy se poochhein: \"{active_q}\""), key="srch_ask_fallback"):
                st.session_state["pending"] = active_q
                st.rerun()
        st.write("")


def render_subject_search(subject_key: str, subject_title: str, placeholder: str, chips: list[tuple[str, str]], lang: str):
    """Dedicated, subject-specific search bar with fast topic chips and immediate inline previews."""
    ss_query_key = f"srch_query_{subject_key}"
    st.markdown(f"""
    <div style="background: rgba(99, 102, 241, 0.07); border: 1px solid rgba(99, 102, 241, 0.22); border-radius: 14px; padding: 10px 14px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
      <span style="font-size: 0.95rem; font-weight: 700; color: #4338ca;">
        🔍 {('Search ' + subject_title if lang == 'en' else subject_title + ' Mein Khojein')}
      </span>
      <span style="font-size: 0.8rem; opacity: 0.75;">
        {('Class 1–8 Curriculum Focus' if lang == 'en' else 'Class 1–8 Syllabus Focus')}
      </span>
    </div>
    """, unsafe_allow_html=True)

    col_in, col_btn, col_clr = st.columns([5.5, 1.2, 1.2])
    with col_in:
        curr_val = st.session_state.get(ss_query_key, "")
        in_val = st.text_input(
            f"Input Search {subject_title}",
            value=curr_val,
            placeholder="🔍 " + placeholder,
            key=f"in_{ss_query_key}",
            label_visibility="collapsed"
        )
    with col_btn:
        if st.button("🔍 " + ("Search" if lang == "en" else "Khojein"), key=f"btn_go_{subject_key}", width="stretch"):
            st.session_state[ss_query_key] = in_val
            st.rerun()
    with col_clr:
        if st.button("✖️ " + ("Clear" if lang == "en" else "Saaf"), key=f"btn_clr_{subject_key}", width="stretch"):
            st.session_state[ss_query_key] = ""
            st.rerun()

    # Topic Shortcut Chips
    if chips:
        c_cols = st.columns(len(chips))
        for c_idx, (c_label, c_term) in enumerate(chips):
            if c_cols[c_idx].button(c_label, key=f"chip_{subject_key}_{c_idx}", width="stretch"):
                st.session_state[ss_query_key] = c_term
                st.rerun()

    active_q = (st.session_state.get(ss_query_key) or in_val).strip()
    if active_q:
        results = search_topics(active_q, limit=6)
        subj_results = [
            r for r in results
            if subject_key in r.get("spec", "")
            or subject_key in r.get("category_en", "").lower()
            or any(subject_key in kw.lower() for kw in r.get("keywords", []))
        ]
        display_results = subj_results if subj_results else results[:2]
        if display_results:
            st.markdown(f"##### 🎯 " + (f"Matches for '{active_q}' in {subject_title}:" if lang == "en" else f"{subject_title} mein '{active_q}' ke matches:"))
            for r_idx, r_item in enumerate(display_results):
                title = r_item["title_hi"] if lang == "hi" else r_item["title_en"]
                desc = r_item["desc_hi"] if lang == "hi" else r_item["desc_en"]
                st.markdown(f"""
                <div class="search-card" style="padding:10px 14px; margin-bottom:8px;">
                  <b>{r_item['icon']} {title}</b>
                  <p style="margin:2px 0 6px 0; font-size:0.9rem; line-height:1.4;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
                sp = r_item.get("spec")
                if sp and sp != "quiz":
                    with st.expander("🖼️ " + ("Preview Model / Diagram" if lang == "en" else "Diagram Dekhein")):
                        show_visual(sp, lang, key=f"subj_res_{subject_key}_{r_idx}")
            st.divider()
        else:
            st.info(f"💡 No direct topic found for '{active_q}' in {subject_title}. Try one of the topic chips above!")


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
    ss.setdefault("class_level", "Class 3 - 5")
    ss.setdefault("snap_rotation", 0)
    ss.setdefault("snap_subject", "all")
    ss.setdefault("search_query", "")


# ----------------------------------------------------------------------------- sidebar
def sidebar():
    st.sidebar.title("🧠 GyaanBuddy")
    st.sidebar.caption("Your friendly, kid-safe science & math buddy")

    # IMPORTANT: Keep Language radio as the very first radio in sidebar for AppTest compatibility
    lang_label = st.sidebar.radio("Language / Bhasha", ["English", "Hinglish"], horizontal=True)
    lang = "hi" if lang_label == "Hinglish" else "en"

    # Class Filter (Nursery to 8th Class)
    class_options = ["Nursery - KG", "Class 1 - 2", "Class 3 - 5", "Class 6 - 8"]
    chosen_class = st.sidebar.select_slider(
        "🎓 " + ("Class Filter (Nursery to 8th)" if lang == "en" else "Class Filter (Nursery se 8th)"),
        options=class_options,
        value=st.session_state.get("class_level", "Class 3 - 5"),
        help="Adjusts explanation complexity and vocabulary for your child's class level."
    )
    st.session_state["class_level"] = chosen_class
    class_to_age = {
        "Nursery - KG": "6-8",
        "Class 1 - 2": "6-8",
        "Class 3 - 5": "9-12",
        "Class 6 - 8": "13-15",
    }
    age = class_to_age.get(chosen_class, "9-12")

    st.sidebar.divider()
    api_key = st.sidebar.text_input("Anthropic API key (optional, for parents)", type="password",
                                    value=os.getenv("ANTHROPIC_API_KEY", ""),
                                    help="Without a key GyaanBuddy answers from its built-in lessons.")
    model = st.sidebar.text_input("Model", value=tutor_engine.DEFAULT_MODEL)
    st.sidebar.success("AI mode on" if api_key else "Built-in lessons mode")
    st.sidebar.info("🛡️ Safety filter is always on. Private details are hidden and unsafe topics are blocked.")
    if st.sidebar.button("Clear chat"):
        st.session_state["messages"] = []
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

    # Interactive Mystery Science Prompt Starter
    mysteries = MYSTERIES[lang]
    st.markdown(f"💡 **{t['mystery']}**")
    m_cols = st.columns(min(len(mysteries), 3))
    for i, (q_text, label) in enumerate(mysteries[:3]):
        if m_cols[i % len(m_cols)].button(label, key=f"myst_{i}", width="stretch"):
            st.session_state["pending"] = q_text
            st.rerun()

    # 🎤 Voice Question Input for Young Students (Nursery to 8th Class)
    st.markdown("##### 🎙️ " + ("Voice Question (Can't write? Speak to Buddy!)" if lang == "en" else "Awaaz Se Poochhein (Likhna mushkil hai? Bol kar poochhein!)"))
    render_whatsapp_voice_bar(lang)

    v_c1, v_c2 = st.columns([1.2, 1])
    with v_c1:
        voice_rec = st.audio_input(
            "🎤 " + ("Record voice question (auto-transcribed)" if lang == "en" else "Awaaz record karein (auto-transcribed)"),
            key="voice_rec_input"
        )
        if voice_rec:
            with st.spinner("🎧 Listening to your voice recording… 🎙️" if lang == "en" else "Awaaz sun raha hoon… 🎙️"):
                spoken_text = transcribe_audio(voice_rec, lang)
            if spoken_text:
                st.success(f"🗣️ " + (f"Heard: \"{spoken_text}\"" if lang == "en" else f"Suna: \"{spoken_text}\""))
                st.session_state["pending"] = spoken_text
                st.rerun()
            else:
                st.info("💡 " + ("Voice recorded! Buddy is listening. Tap a quick question below or ask in chat:" if lang == "en" else "Awaaz record ho gayi!"))
    with v_c2:
        st.caption("⚡ " + ("Quick Spoken Questions (tap to ask):" if lang == "en" else "Bolne Wale Sawaal (tap karein):"))
        spoken_prompts = [
            ("⚡ What is force?", "What is force and motion?"),
            ("🌌 Why is the sky blue?", "Why is the sky blue?"),
            ("🫀 How does the heart pump blood?", "What does the heart do in our body?"),
            ("🍎 Why do things fall down?", "How does gravity pull things down?"),
            ("🍕 What is 1/2 of a pizza?", "Explain fractions with pizza"),
        ] if lang == "en" else [
            ("⚡ Force kya hota hai?", "Explain force"),
            ("🌌 Aasman neela kyun hai?", "Why is the sky blue?"),
            ("🫀 Dil kaise dhadakta hai?", "Dil kya kaam karta hai?"),
            ("🍎 Cheezein neeche kyun girti hain?", "Gravity kya hai?"),
            ("🍕 Pizza ka 1/2 kya hota hai?", "Fractions samjhao"),
        ]
        sp_c1, sp_c2 = st.columns(2)
        for s_i, (s_label, s_q) in enumerate(spoken_prompts):
            target_col = sp_c1 if s_i % 2 == 0 else sp_c2
            if target_col.button(s_label, key=f"sp_p_{s_i}", width="stretch"):
                st.session_state["pending"] = s_q
                st.rerun()

    st.divider()

    for i, m in enumerate(st.session_state["messages"]):
        with st.chat_message(m["role"], avatar="🧒" if m["role"] == "user" else "🧠"):
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
                   if a["role"] == "assistant" and a.get("q") and not a.get("blocked")]
        with st.spinner("Thinking… 🤔" if lang == "en" else "Soch raha hoon… 🤔"):
            r = tutor_engine.answer(q, lang, age, history, api_key, model)
        st.session_state["messages"].append({"role": "user", "text": q})
        st.session_state["messages"].append({"role": "assistant", "text": r.text, "visual": r.visual, "q": q,
                                             "notice": r.notice, "blocked": r.blocked})
        if r.blocked:
            log("blocked", topic=r.category or "")
        else:
            log("question", r.subject, r.topic, mode=r.mode)
            add_xp(10, "Great science question!", badge_id="curious_spark", badge_name="Curious Spark")
        st.rerun()


# ----------------------------------------------------------------------------- snap & solve tab
def tab_snap_solve(lang, age, api_key, model):
    st.subheader(TXT[lang]["tabs"][1])
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
        cam_img = st.camera_input("📷 " + ("Take photo of question" if lang == "en" else "Sawaal ki photo lein"), key="snap_cam_input")
    with snap_col2:
        file_img = st.file_uploader("📁 " + ("Or upload question photo" if lang == "en" else "Ya image upload karein"), type=["png", "jpg", "jpeg", "webp"], key="snap_file_input")

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

    # Subject-specific Presets
    subject_presets = {
        "physics": [
            ("⚡ What is force & motion?", "What is force and Newton's law?"),
            ("🌌 Why is the sky blue?", "Why is the sky blue?"),
            ("🍎 How does gravity work?", "How does gravity work and why do things fall?"),
            ("💡 Ohm's Law (V = I × R)", "Explain Ohm's law with voltage, current and resistance"),
            ("🕰️ Time period of a pendulum", "Calculate the time period of a pendulum"),
        ],
        "math": [
            ("📐 Hypotenuse of 3 & 4 cm triangle", "In a right triangle with legs 3 cm and 4 cm, find the hypotenuse"),
            ("⭕ Area of circle with radius 7 cm", "What is the area and circumference of a circle with radius 7 cm?"),
            ("⚖️ Solve linear equation 2x + 6 = 16", "Solve the linear equation 2x + 6 = 16 for x"),
            ("🍕 Convert fraction 3/8 to % and decimal", "Convert 3/8 into decimal and percentage"),
            ("🥫 3D Cylinder surface area & volume", "Calculate surface area and volume of cylinder r=4 h=8"),
        ],
        "body": [
            ("🫀 How does the heart pump blood?", "What does the heart do in the circulatory system?"),
            ("🫁 How do lungs breathe oxygen?", "How do lungs take in oxygen and breathe out carbon dioxide?"),
            ("🧠 What are the parts of the brain?", "What are the parts and functions of the brain?"),
            ("🫘 How do kidneys filter blood?", "How do kidney nephrons filter blood and make urine?"),
            ("🦴 How many bones in the body?", "How many bones are in the human skeleton?"),
        ],
        "chem": [
            ("⚛️ Oxygen atom: protons & electrons", "What is an atom of oxygen?"),
            ("💧 Water molecule (H2O) structure", "What is water H2O made of?"),
            ("🍋 What is pH of lemon juice?", "What is the pH of lemon juice?"),
            ("🌋 Baking soda & vinegar reaction", "Explain baking soda and vinegar fizz reaction"),
            ("🧊 Ice, liquid water and steam states", "What are the three states of matter?"),
        ],
    }
    if active_subj == "all":
        cur_presets = [
            ("⚡ What is force?", "What is force and Newton's law?"),
            ("🌌 Why is the sky blue?", "Why is the sky blue?"),
            ("📐 Hypotenuse of 3 & 4 cm triangle", "In a right triangle with legs 3 cm and 4 cm, find the hypotenuse"),
            ("⚖️ Solve linear equation 2x + 6 = 16", "Solve the linear equation 2x + 6 = 16 for x"),
            ("🫀 How does the heart pump blood?", "What does the heart do in the circulatory system?"),
            ("⚛️ Oxygen atom structure", "What is an atom of oxygen?"),
        ]
    else:
        cur_presets = subject_presets.get(active_subj, [])

    st.markdown("##### ⚡ " + ("Quick Question Presets (or type your question):" if lang == "en" else "Quick Sawaal Presets (ya apna sawaal likhein):"))
    p_cols = st.columns(min(len(cur_presets), 3))
    for p_idx, (p_title, p_query) in enumerate(cur_presets):
        col_idx = p_idx % len(p_cols)
        if p_cols[col_idx].button(p_title, key=f"snap_p_{active_subj}_{p_idx}", width="stretch"):
            st.session_state["snap_problem_text"] = p_query
            st.rerun()

    user_prob = st.text_input(
        "Question text",
        value=st.session_state.get("snap_problem_text", ""),
        placeholder="Type question or select a preset above..." if lang == "en" else "Sawaal likhein ya upar se preset chunein...",
        key="snap_problem_input",
        label_visibility="collapsed"
    )

    solve_btn = st.button("🚀 " + ("Solve This Question" if lang == "en" else "Yeh Sawaal Hal Karein"), key="btn_do_snap_solve", type="primary")
    if solve_btn:
        q_to_solve = user_prob.strip()
        if not q_to_solve and not active_img:
            st.warning("Please take a photo or select a question to solve!" if lang == "en" else "Kripya photo lein ya koi sawaal chunein!")
        elif not q_to_solve and active_img and not api_key:
            st.info("💡 Please type what question is in your photo or click a preset above, and GyaanBuddy will solve it with formulas and diagrams!" if lang == "en" else
                    "💡 Kripya batayein photo mein kya sawaal hai ya upar se topic chunein!")
        else:
            if api_key and active_img:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                img_bytes = active_img.getvalue()
                b64_data = base64.b64encode(img_bytes).decode("utf-8")
                mime = getattr(active_img, "type", "image/jpeg") or "image/jpeg"
                sys_prompt = f"You are GyaanBuddy, a friendly tutor for school students up to Class 8 in India. Language: {'English' if lang == 'en' else 'Hinglish'}. Carefully read the question in the image and solve it step-by-step with simple explanations, formulas, and encouraging emojis."
                try:
                    resp = client.messages.create(
                        model=model or "claude-3-5-sonnet-20241022",
                        max_tokens=600,
                        system=sys_prompt,
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64_data}},
                                {"type": "text", "text": q_to_solve or "Please solve this question step-by-step for a school student."}
                            ]
                        }]
                    )
                    sol_text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
                    st.session_state["messages"].append({"role": "user", "text": f"📸 [Photo Question]: {q_to_solve or 'School Problem in Image'}"})
                    st.session_state["messages"].append({"role": "assistant", "text": sol_text, "q": q_to_solve})
                    add_xp(20, "Solved photo question!", badge_id="curious_spark")
                    st.rerun()
                except Exception as e:
                    st.info(f"AI Vision Helper falling back to offline tutor: {e}")

            if not q_to_solve:
                q_to_solve = "What is force and Newton's law?"
            r = tutor_engine.answer(q_to_solve, lang, age)
            st.session_state["messages"].append({"role": "user", "text": f"📸 [Question]: {q_to_solve}"})
            st.session_state["messages"].append({"role": "assistant", "text": r.text, "visual": r.visual, "q": q_to_solve})
            add_xp(20, "Solved question!", badge_id="curious_spark")
            st.rerun()


# ----------------------------------------------------------------------------- body tab
def tab_body(lang):
    t = TXT[lang]
    st.subheader(t["tabs"][2])

    body_chips = [
        ("🧠 Brain", "brain"),
        ("🫁 Lungs", "lungs"),
        ("💓 Heart", "heart"),
        ("🫘 Kidneys", "kidney"),
        ("🦴 Skeleton", "bones"),
        ("🍕 Stomach", "stomach"),
        ("🩸 Liver", "liver"),
        ("🔬 Nephron", "nephron"),
    ]
    render_subject_search("body", "Human Body Anatomy", "Heart, Lungs, Brain, Kidneys, Bones, Digestion...", body_chips, lang)

    parts = C.BODY_PARTS

    # Body System Filters (per Bing anatomical diagram categories)
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
        if sys_cols[s_idx].button(s_label, key=f"body_sys_{s_idx}", width="stretch"):
            if s_sys is not None:
                for o_idx, bp in enumerate(parts):
                    if bp.get("system") == s_sys:
                        st.session_state["body_i"] = o_idx
                        break
            st.rerun()

    # Organ Mastered Progress Counter
    learned_count = len(st.session_state["learned_organs"])
    st.markdown(f"🏆 **Organs Mastered:** {learned_count}/{len(parts)} " +
                ("• Master all 8 to become an Anatomy Ace!" if lang == "en" else "• Saare 8 seekh kar Anatomy Ace bano!"))

    show_all = st.toggle(t["all"], value=False)
    if show_all:
        left, right = st.columns([1.1, 1])
        with left:
            show_svg(V.body_svg(None, lang), 470)
        with right:
            for b in parts:
                st.markdown(f"**{b['hi_name'] if lang == 'hi' else b['en_name']}**: {b[lang].split('.')[0]}.")
        return

    i = st.session_state["body_i"] % len(parts)
    c1, c2, c3 = st.columns([1, 1, 4])
    if c1.button(t["prev"], key="bprev"):
        st.session_state["body_i"] = (i - 1) % len(parts)
        st.rerun()
    if c2.button(t["next"], key="bnext"):
        st.session_state["body_i"] = (i + 1) % len(parts)
        st.rerun()
    names = [(b["hi_name"] if lang == "hi" else b["en_name"]) for b in parts]
    pick = c3.selectbox("Part", names, index=i, label_visibility="collapsed")
    if names.index(pick) != i:
        st.session_state["body_i"] = names.index(pick)
        st.rerun()

    b = parts[i]
    if b["key"] == "kidneys":
        k_view = st.radio(
            "Kidney View Mode",
            ["🔬 " + ("Realistic Cross-Section & Nephron" if lang == "en" else "Realistic Banawat & Nephron"),
             "👤 " + ("Whole Body Position" if lang == "en" else "Sharir Mein Sthiti")],
            horizontal=True,
            key="kidney_view_selector"
        )
        left, right = st.columns([1.2, 1])
        with left:
            if "Whole Body" in k_view or "Sharir Mein" in k_view:
                show_svg(V.body_svg(b["key"], lang), 470)
            else:
                show_svg(V.kidney_detail_svg(lang), 540)
    else:
        left, right = st.columns([1.1, 1])
        with left:
            show_svg(V.body_svg(b["key"], lang), 470)

    with right:
        st.markdown(f"### {names[i]}")
        st.caption(f"{b['system']}  •  {i + 1}/{len(parts)}")
        st.write(b[lang])
        st.markdown(f"<div class='fact'>💡 <b>{t['fact']}:</b> {b['fact_' + lang]}</div>", unsafe_allow_html=True)

        if b["key"] == "kidneys":
            st.markdown(f"""
            <div style="margin-top:12px;padding:12px 14px;background:rgba(220,38,38,0.12);border-left:4px solid #dc2626;border-radius:10px;font-size:0.9rem;">
              <b>🔬 {('Internal Kidney Anatomy' if lang == 'en' else 'Gurde Ki Andaruni Banawat')}:</b><br>
              • <b>{('Renal Cortex' if lang == 'en' else 'Renal Cortex')}:</b> {('Outer filtration zone with 1,000,000+ microscopic nephrons.' if lang == 'en' else 'Bahar ka hissa jahan 10 lakh+ nephrons khoon chhaante hain.')}<br>
              • <b>{('Renal Pyramids' if lang == 'en' else 'Renal Pyramids')}:</b> {('Medullary lobes collecting filtered urine.' if lang == 'en' else 'Peshab ko ikattha karne wale medullary lobes.')}<br>
              • <b>{('Pelvis &amp; Ureter' if lang == 'en' else 'Pelvis aur Ureter')}:</b> {('Central funnel draining urine down into the urinary bladder.' if lang == 'en' else 'Peshab ko bladder tak pahunchane wali nali.')}
            </div>
            """, unsafe_allow_html=True)

        read_aloud(f"{names[i]}. {b[lang]} {b['fact_' + lang]}", key=f"body_ra_{b['key']}", lang=lang)

        already_learned = b["key"] in st.session_state["learned_organs"]
        btn_label = ("🌟 Mastered!" if already_learned else ("✅ I learned this" if lang == "en" else "✅ Maine seekh liya"))
        if st.button(btn_label, key=f"learn{b['key']}", disabled=already_learned):
            st.session_state["learned_organs"].append(b["key"])
            log("learned", "Human body", b["en_name"])
            badge = "anatomy_master" if len(st.session_state["learned_organs"]) >= 6 else None
            add_xp(15, f"Mastered {names[i]}!", badge_id=badge, badge_name="Anatomy Ace")
            st.toast("Great job! 🌟" if lang == "en" else "Shabaash! 🌟")
            st.rerun()

    st.divider()

    # Interactive Vital Signs / Live Heartbeat Simulator
    st.markdown("#### 💓 " + ("Live Heartbeat & Breathing Simulator" if lang == "en" else "Live Dil Ki Dhadkan & Saans Simulator"))
    st.caption("Slide to change physical activity and watch the heart pump and lungs breathe faster!" if lang == "en" else
               "Activity badal kar dekho ki exercise karne par dil kitna tezi se khoon pump karta hai!")
    v_col1, v_col2 = st.columns([1, 1.3])
    with v_col1:
        bpm = st.select_slider(
            "Physical Activity State",
            options=[70, 95, 125, 160],
            value=70,
            format_func=lambda v: (
                "🛋️ Resting on Couch (70 BPM)" if v == 70 else
                ("🚶 Walking to School (95 BPM)" if v == 95 else
                 ("🏃 Jogging in Park (125 BPM)" if v == 125 else "⚡ Full Sprint Race (160 BPM)"))
            )
        )
        if bpm >= 125:
            st.info("💪 When exercising, your muscles need 3x more oxygen, so the brain commands your heart and lungs to speed up!")
        else:
            st.success("🧘 When resting, your heart pumps steadily and saves energy for thinking and cell growth.")
    with v_col2:
        show_svg(V.vital_signs_svg(bpm, lang), 440)


# ----------------------------------------------------------------------------- physics tab
def tab_physics(lang):
    t = TXT[lang]
    st.subheader(t["tabs"][3])

    physics_chips = [
        ("⚽ Projectile", "projectile"),
        ("⚡ Force", "force"),
        ("🌌 Blue Sky", "sky"),
        ("🍎 Gravity", "gravity"),
        ("🕰️ Pendulum", "pendulum"),
        ("💡 Ohm's Law", "ohm"),
        ("🌈 Refraction", "refraction"),
    ]
    render_subject_search("physics", "Physics Lab", "Force, Sky, Gravity, Friction, Projectile, Pendulum, Circuit...", physics_chips, lang)

    key = st.radio("Experiment", list(C.PHYSICS), horizontal=True,
                   format_func=lambda k: C.PHYSICS[k]["title_" + lang])
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

        # Interactive Target Practice Challenge Game
        st.markdown("##### 🎯 Target Challenge Mode")
        st.caption("Can you calculate the right angle and speed to hit the flag target?" if lang == "en" else
                   "Sahi angle aur speed chun kar target flag ko hit karo!")
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
                st.warning(f"Almost there! Ball landed at {actual_range:.1f} m (Off by {diff:.1f} m). Adjust angle slightly!")
            else:
                st.info(f"Ball landed at {actual_range:.1f} m (Target: {target_m} m). Try adjusting your speed or angle!")

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
        st.caption("Make R bigger and watch the bulb get dimmer!" if lang == "en" else
                   "R badhao aur dekho bulb dim hota jaata hai!")
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
        st.toast("Scientist in the making! 🔬" if lang == "en" else "Chhota scientist! 🔬")


# ----------------------------------------------------------------------------- chemistry tab
def tab_chem(lang):
    t = TXT[lang]
    st.subheader(t["tabs"][4])

    chem_chips = [
        ("⚛️ Atom", "atom"),
        ("💧 Water Molecule", "water"),
        ("🧊 States of Matter", "solid"),
        ("🍋 pH Scale", "acid"),
        ("🌋 Volcano Reaction", "volcano"),
        ("🔩 Rusting", "rust"),
    ]
    render_subject_search("chem", "Chemistry Lab", "Atom, Oxygen, Water, States, Acid, Base, Volcano reaction...", chem_chips, lang)

    a, m, s, p, rx, h = st.tabs([
        "⚛️ Atom builder", "💧 Molecules", "🧊 States of matter", "🍋 pH scale", "🌋 Virtual Reaction Lab", "🏠 Home experiments"
    ])
    with a:
        st.write(C.CHEM_TEXT["atom"][lang])
        z = st.slider("Number of protons (Z)", 1, 20, 8)
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
        key = st.selectbox("Molecule", list(C.MOLECULES), format_func=lambda k: f"{C.MOLECULES[k]['formula']}  {C.MOLECULES[k]['name_en']}")
        st.plotly_chart(V.molecule_fig(key), width="stretch", key="mol")
        st.info(C.MOLECULES[key][lang])
    with s:
        st.write(C.CHEM_TEXT["states"][lang])
        state = st.radio("State", list(C.STATES), horizontal=True,
                         format_func=lambda k: C.STATES[k]["hi_name" if lang == "hi" else "en_name"])
        c1, c2 = st.columns([1, 1])
        with c1:
            show_svg(V.states_svg(state), 340)
        with c2:
            st.write(C.STATES[state][lang])
    with p:
        st.write(C.CHEM_TEXT["ph"][lang])
        sub = st.select_slider("Choose a substance", list(C.PH_SUBSTANCES),
                               format_func=lambda k: C.PH_SUBSTANCES[k][1 if lang == "hi" else 0], value="water")
        en, hi, val = C.PH_SUBSTANCES[sub]
        show_svg(V.ph_svg(val, hi if lang == "hi" else en), 520)
        kind = "acid" if val < 7 else "base" if val > 7 else "neutral"
        st.write(f"pH **{val:g}** → **{kind}**")
    with rx:
        st.markdown("#### 🧪 Safe Virtual Reaction Simulator")
        st.caption("Mix substances safely on screen and observe the chemical reaction!" if lang == "en" else
                   "Screen par surakshit tareeke se chemicals milakar reaction dekho!")
        rx_key = st.selectbox(
            "Select Reaction Experiment",
            ["volcano", "indicator", "dissolve"],
            format_func=lambda k: (
                "🌋 Baking Soda + Vinegar (CO2 Fizz)" if k == "volcano" else
                ("🎨 Red Cabbage Juice + Lemon (Anthocyanin pH Shift)" if k == "indicator" else "🧂 Salt Crystal Dissolving in Water (Ions)")
            )
        )
        show_svg(V.reaction_svg(rx_key, lang), 480)
        if st.button("🧪 Mix Ingredients & Observe", key=f"btn_rx_{rx_key}"):
            add_xp(20, "Virtual chemical reaction simulated!", badge_id="chem_wizard", badge_name="Chem Wizard")
            st.toast("Reaction Successful! 🌟")
    with h:
        for k, act in C.HOME_ACTIVITIES.items():
            st.markdown(f"<div class='act'><b>{act['title_' + lang]}</b><br>{act[lang]}</div>", unsafe_allow_html=True)
            st.write("")
        st.warning("Always do experiments with an adult. Never taste or mix unknown chemicals!" if lang == "en" else
                   "Experiments hamesha kisi bade ke saath karo. Anjaan chemicals ko kabhi chakho ya milao mat!")


# ----------------------------------------------------------------------------- mathematics tab (Class 1 to 8)
def tab_maths(lang):
    t = TXT[lang]
    st.subheader(t["tabs"][5])
    st.caption("Interactive Visual Geometry, Pythagoras Theorem, Fraction Pizza, Algebra Balance Scale, and Speed Math Arena!" if lang == "en" else
               "Visual Geometry, Pythagoras Pramey, Fraction Pizza, Algebra Tarazu Scale aur Speed Math Challenge!")

    # Dedicated Subject Search for Mathematics
    math_chips = [
        ("⭕ Circle", "circle"),
        ("📐 Rectangle", "rectangle"),
        ("🔺 Pythagoras", "pythagoras"),
        ("🥫 Cylinder", "cylinder"),
        ("🍕 Fractions", "fraction"),
        ("⚖️ Algebra", "algebra"),
    ]
    render_subject_search(
        "math",
        "Mathematics / गणित",
        "Search Circle, Rectangle, Cylinder, Pythagoras, Fractions, Linear Equations...",
        math_chips,
        lang
    )

    m_tabs = st.tabs([
        "📐 2D Geometry",
        "🥫 3D Mensuration",
        "🔺 Pythagoras Theorem",
        "🍕 Fractions & Percentages",
        "⚖️ Algebra Balance Scale",
        "⚡ Speed Math Arena"
    ] if lang == "en" else [
        "📐 2D Geometry (Shapes)",
        "🥫 3D Mensuration (Cylinder)",
        "🔺 Pythagoras Pramey",
        "🍕 Fractions & Percentages",
        "⚖️ Algebra Balance Scale",
        "⚡ Speed Math Arena"
    ])

    # 1. 2D Geometry
    with m_tabs[0]:
        st.markdown("#### 📐 " + ("Visual 2D Shapes & Mensuration" if lang == "en" else "Visual 2D Shapes aur Kshetraphal"))
        shape = st.radio("Choose 2D Shape", ["Circle (Vritt)", "Rectangle (Aayat)", "Triangle (Tribhuj)"], horizontal=True, key="math_2d_shape")
        if "Circle" in shape:
            c1, c2 = st.columns([1, 1.2])
            with c1:
                r = st.slider("Radius r (cm)", 1, 15, 7, key="geo_circ_r")
                st.info("💡 " + (f"Diameter = 2 × {r} = {2*r} cm\n\nCircumference = 2πr = {2*math.pi*r:.2f} cm\n\nArea = πr² = {math.pi*r**2:.2f} cm²" if lang == "en" else
                                 f"Vyas (Diameter) = 2 × {r} = {2*r} cm\n\nParidhi = 2πr = {2*math.pi*r:.2f} cm\n\nKshetraphal = πr² = {math.pi*r**2:.2f} cm²"))
                read_aloud(f"Circle with radius {r} cm has circumference {2*math.pi*r:.2f} cm and area {math.pi*r**2:.2f} square cm.", key="aud_circ", lang=lang)
            with c2:
                show_svg(V.math_geometry_svg("circle", {"r": r}, lang), 440)
        elif "Rectangle" in shape:
            c1, c2 = st.columns([1, 1.2])
            with c1:
                l = st.slider("Length l (cm)", 2, 20, 8, key="geo_rect_l")
                w = st.slider("Width w (cm)", 1, 15, 5, key="geo_rect_w")
                peri = 2 * (l + w)
                area = l * w
                diag = math.sqrt(l**2 + w**2)
                st.info("💡 " + (f"Perimeter = 2({l} + {w}) = {peri} cm\n\nArea = {l} × {w} = {area} cm²\n\nDiagonal = √({l}² + {w}²) = {diag:.2f} cm" if lang == "en" else
                                 f"Perimeter = 2({l} + {w}) = {peri} cm\n\nArea = {l} × {w} = {area} cm²\n\nDiagonal = {diag:.2f} cm"))
                read_aloud(f"Rectangle with length {l} and width {w} cm has perimeter {peri} cm and area {area} square cm.", key="aud_rect", lang=lang)
            with c2:
                show_svg(V.math_geometry_svg("rectangle", {"l": l, "w": w}, lang), 440)
        else:
            c1, c2 = st.columns([1, 1.2])
            with c1:
                b = st.slider("Base b (cm)", 2, 20, 8, key="geo_tri_b")
                h = st.slider("Height h (cm)", 1, 15, 6, key="geo_tri_h")
                area = 0.5 * b * h
                st.info("💡 " + (f"Area = ½ × base × height = ½ × {b} × {h} = {area:g} cm²" if lang == "en" else
                                 f"Kshetraphal = ½ × {b} × {h} = {area:g} cm²"))
                read_aloud(f"Triangle with base {b} and height {h} cm has area {area:g} square cm.", key="aud_tri", lang=lang)
            with c2:
                show_svg(V.math_geometry_svg("triangle", {"b": b, "h": h}, lang), 440)

    # 2. 3D Mensuration
    with m_tabs[1]:
        st.markdown("#### 🥫 " + ("Class 8 Mensuration: 3D Cylinder" if lang == "en" else "Class 8 Mensuration: 3D Belan (Cylinder)"))
        c1, c2 = st.columns([1, 1.2])
        with c1:
            cyl_r = st.slider("Radius r (cm)", 1, 10, 4, key="cyl_r_slider")
            cyl_h = st.slider("Height h (cm)", 2, 20, 8, key="cyl_h_slider")
            csa = 2 * math.pi * cyl_r * cyl_h
            tsa = 2 * math.pi * cyl_r * (cyl_r + cyl_h)
            vol = math.pi * (cyl_r ** 2) * cyl_h
            liters = vol / 1000.0
            st.markdown(f"""
            <div style="background:rgba(16,185,129,0.1);border-left:4px solid #10b981;border-radius:10px;padding:12px;font-size:0.95rem;line-height:1.6;">
              <b>📐 Formulations (Syllabus Class 8):</b><br>
              • <b>Curved Surface Area (CSA):</b> 2πrh = <b>{csa:.1f} cm²</b><br>
              • <b>Total Surface Area (TSA):</b> 2πr(r+h) = <b>{tsa:.1f} cm²</b><br>
              • <b>Capacity / Volume:</b> πr²h = <b>{vol:.1f} cm³</b> ({liters:.3f} Liters)
            </div>
            """, unsafe_allow_html=True)
            read_aloud(f"Cylinder with radius {cyl_r} cm and height {cyl_h} cm has volume {vol:.1f} cubic cm, which is {liters:.3f} liters.", key="aud_cyl", lang=lang)
        with c2:
            show_svg(V.math_geometry_svg("cylinder", {"r": cyl_r, "h": cyl_h}, lang), 440)

    # 3. Pythagoras Theorem
    with m_tabs[2]:
        st.markdown("#### 🔺 " + ("Pythagoras Theorem & Triplets (Class 7 & 8)" if lang == "en" else "Pythagoras Pramey & Triplets"))
        st.caption("In any right-angled triangle, a² + b² = c². Discover triplets like (3, 4, 5) and (5, 12, 13)!" if lang == "en" else
                   "Right-angled triangle mein a² + b² = c² hota hai. Triplets jaise (3, 4, 5) aur (5, 12, 13) khojein!")
        py_c1, py_c2 = st.columns([1, 1.2])
        with py_c1:
            py_a = st.slider("Side a (Leg 1)", 1, 12, 3, key="py_slider_a")
            py_b = st.slider("Side b (Leg 2)", 1, 12, 4, key="py_slider_b")
            c_val = math.sqrt(py_a**2 + py_b**2)
            is_trip = (abs(c_val - round(c_val)) < 1e-6)
            if is_trip:
                st.balloons()
                st.success(f"🌟 WOW! ({py_a}, {py_b}, {int(round(c_val))}) is a famous Pythagorean Triplet!")
                add_xp(20, f"Discovered Pythagorean triplet ({py_a}, {py_b}, {int(round(c_val))})!", badge_id="physics_wizard")
            read_aloud(f"For sides {py_a} and {py_b}, the hypotenuse is {c_val:.2f}.", key="aud_pyth", lang=lang)
        with py_c2:
            show_svg(V.pythagoras_svg(py_a, py_b, lang), 440)

    # 4. Fractions & Percentages
    with m_tabs[3]:
        st.markdown("#### 🍕 " + ("Visual Fractions, Decimals & Percentages (Class 3 to 7)" if lang == "en" else "Visual Fractions, Decimals & Percentages"))
        fr_c1, fr_c2 = st.columns([1, 1.2])
        with fr_c1:
            den_val = st.slider("Denominator (Total Pizza Slices)", 1, 12, 8, key="fr_den")
            num_val = st.slider("Numerator (Eaten Slices)", 0, den_val, min(3, den_val), key="fr_num")
            fr_pct = (num_val / den_val) * 100
            fr_dec = num_val / den_val
            st.info(f"🍕 **{num_val} out of {den_val} slices** = **{fr_pct:.1f}%** of the pizza! Decimal = **{fr_dec:.3f}**")
            read_aloud(f"{num_val} over {den_val} equals {fr_pct:.1f} percent, or {fr_dec:.3f} in decimals.", key="aud_frac", lang=lang)
        with fr_c2:
            show_svg(V.fraction_pizza_svg(num_val, den_val, lang), 440)

    # 5. Algebra Balance Scale
    with m_tabs[4]:
        st.markdown("#### ⚖️ " + ("Linear Equations & Balancing Scale (Class 6 to 8)" if lang == "en" else "Linear Equations & Tarazu Balance"))
        st.caption("Learn to solve ax + b = c by keeping both pans of the scale in perfect equilibrium!" if lang == "en" else
                   "Tarazu ke dono pallo ko barabar rakh kar ax + b = c ko step-by-step solve karein!")
        alg_c1, alg_c2 = st.columns([1, 1.2])
        with alg_c1:
            eq_a = st.slider("Coefficient a", 1, 6, 2, key="alg_a")
            eq_b = st.slider("Constant b", 1, 20, 5, key="alg_b")
            eq_c = st.slider("Target c", eq_b + 1, 50, 15, key="alg_c")
            x_sol = (eq_c - eq_b) / eq_a
            st.success(f"✨ Equation: **{eq_a}x + {eq_b} = {eq_c}**  ➔  **x = {x_sol:.2f}**")
            read_aloud(f"For equation {eq_a}x plus {eq_b} equals {eq_c}, subtract {eq_b} and divide by {eq_a} to get x equals {x_sol:.2f}.", key="aud_alg", lang=lang)
        with alg_c2:
            show_svg(V.algebra_balance_svg(eq_a, eq_b, eq_c, lang), 440)

    # 6. Speed Math Challenge Arena
    with m_tabs[5]:
        st.markdown("#### ⚡ " + ("Speed Math Challenge Arena" if lang == "en" else "Speed Math Challenge Arena"))
        st.caption("Rapid-fire mental math challenge to sharpen calculation speed!" if lang == "en" else
                   "Dimag ko tez karne ke liye rapid-fire math quiz!")
        tier = st.selectbox("Grade Difficulty Tier", [
            "🥉 Junior (Class 1–4): Addition, Subtraction & Doubles",
            "🥈 Middle (Class 5–6): Multiplication Tables, Divisions & Squares",
            "🥇 Senior (Class 7–8): Linear Equations, Percentages & Pythagoras"
        ], index=1)

        if "Junior" in tier:
            q_list = [
                ("14 + 19 = ?", ["31", "33", "35", "37"], 1, "14 + 19 = 33"),
                ("50 - 23 = ?", ["27", "28", "25", "37"], 0, "50 - 23 = 27"),
                ("Double of 16 is:", ["28", "30", "32", "34"], 2, "16 × 2 = 32"),
            ]
        elif "Middle" in tier:
            q_list = [
                ("12 × 13 = ?", ["156", "146", "166", "154"], 0, "12 × 13 = 156"),
                ("Square of 14 (14²) = ?", ["186", "196", "206", "176"], 1, "14 × 14 = 196"),
                ("96 ÷ 8 = ?", ["11", "12", "14", "16"], 1, "96 ÷ 8 = 12"),
            ]
        else:
            q_list = [
                ("Solve for x: 3x - 7 = 14", ["x = 5", "x = 7", "x = 9", "x = 6"], 1, "3x = 21 ➔ x = 7"),
                ("What is 15% of 200?", ["20", "25", "30", "35"], 2, "(15/100) × 200 = 30"),
                ("In right triangle with legs 6 and 8, hypotenuse is:", ["9", "10", "12", "14"], 1, "√(6² + 8²) = √100 = 10"),
            ]

        for s_idx, (s_q, s_opts, s_ans, s_ex) in enumerate(q_list):
            with st.container(border=True):
                st.markdown(f"**Question {s_idx + 1}: {s_q}**")
                ch = st.radio("Choose answer", s_opts, index=None, key=f"speed_math_{s_idx}", label_visibility="collapsed")
                if ch is not None and st.button("Check Answer ✅", key=f"btn_spd_chk_{s_idx}"):
                    if s_opts.index(ch) == s_ans:
                        st.success(f"🎉 Correct! {s_ex}")
                        add_xp(20, f"Solved Speed Math Question {s_idx + 1}!", badge_id="quiz_champion")
                    else:
                        st.error(f"Try again! Correct explanation: {s_ex}")


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
        st.download_button("Download progress (CSV)", ev.to_csv(index=False).encode(), "gyaanbuddy_progress.csv", "text/csv")

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
    st.download_button("📥 Download Certificate (HTML)", cert_html.encode("utf-8"), f"GyaanBuddy_Certificate_{student_name}.html", "text/html")


# ----------------------------------------------------------------------------- main
def main():
    init_state()
    lang, age, api_key, model = sidebar()
    apply_theme(st.session_state.get("theme", "🌈 Wonder Academy (Nursery - Class 8)"))

    # Top Hero Banner with Class Level & GyaanBuddy
    class_lvl = st.session_state.get("class_level", "Class 3 - 5")
    xp = st.session_state["xp"]
    lvl_num, lvl_en, lvl_hi, _ = get_level(xp)
    lvl_title = lvl_hi if lang == "hi" else lvl_en

    st.markdown(f"""
    <div class="hero-banner">
      <div>
        <div class="hero-title">🧠 GyaanBuddy • <span style="font-size:1.1rem;background:rgba(255,255,255,0.22);padding:4px 12px;border-radius:12px;">🎓 {class_lvl}</span></div>
        <div class="hero-sub">{"Your friendly AI science & math buddy • Learn the fun way!" if lang == "en" else "Aapka friendly vigyan aur ganit saathi • Seekho mazedaar tareeke se!"}</div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        <span class="xp-pill">⭐ {xp} XP</span>
        <span class="xp-pill">{lvl_title}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(TXT[lang]["tabs"])
    with tabs[0]:
        tab_chat(lang, age, api_key, model)
    with tabs[1]:
        tab_snap_solve(lang, age, api_key, model)
    with tabs[2]:
        tab_body(lang)
    with tabs[3]:
        tab_physics(lang)
    with tabs[4]:
        tab_chem(lang)
    with tabs[5]:
        tab_maths(lang)
    with tabs[6]:
        tab_quiz(lang)
    with tabs[7]:
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

