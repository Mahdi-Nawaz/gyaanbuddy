"""Diagrams and simulations: SVG (body, atom, states of matter, pH, circuit) and Plotly (physics, molecules)."""
from __future__ import annotations

import base64
import math
import random

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import content as C

SKIN, OUTLINE = "#fde7d3", "#c9a27e"


def svg_to_html(svg: str, max_width: int = 420) -> str:
    """Wrap an SVG string in an <img> data-URI so Streamlit renders it reliably."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode()
    return (f'<div style="text-align:center"><img style="max-width:{max_width}px;width:100%" '
            f'src="data:image/svg+xml;base64,{b64}"/></div>')


# ============================================================================= HUMAN BODY
def _organs() -> dict[str, dict]:
    return {
        "brain": dict(
            color="#ec407a",
            anchor=(180, 50),
            sub_en="Cerebrum • Cerebellum • Brainstem",
            sub_hi="Sochna • Santulan • Nerves",
            svg="""
            <g id="organ-brain">
              <path d="M152 52 C152 28 164 22 180 22 C196 22 208 28 208 52 C208 66 202 72 180 72 C158 72 152 66 152 52 Z"
                    fill="url(#brain-grad)" stroke="#880e4f" stroke-width="2.5"/>
              <path d="M158 42 Q168 34 178 42 M156 52 Q166 44 176 52 M160 62 Q170 54 176 60"
                    fill="none" stroke="#ad1457" stroke-width="2" stroke-linecap="round"/>
              <path d="M182 42 Q192 34 202 42 M184 52 Q194 44 204 52 M182 60 Q188 54 198 60"
                    fill="none" stroke="#ad1457" stroke-width="2" stroke-linecap="round"/>
              <line x1="180" y1="24" x2="180" y2="70" stroke="#880e4f" stroke-width="2" stroke-linecap="round"/>
              <path d="M192 64 C204 64 210 72 204 80 C198 84 190 82 188 74 Z" fill="#ad1457" stroke="#880e4f" stroke-width="1.8"/>
              <line x1="192" y1="70" x2="202" y2="72" stroke="#f8bbd0" stroke-width="1.2"/>
              <line x1="192" y1="75" x2="200" y2="77" stroke="#f8bbd0" stroke-width="1.2"/>
              <path d="M176 72 L176 92 M184 72 L184 92" stroke="#c2185b" stroke-width="2.5" fill="none"/>
              <circle cx="166" cy="38" r="1.8" fill="#ffffff" opacity="0.8"/>
              <circle cx="194" cy="38" r="1.8" fill="#ffffff" opacity="0.8"/>
            </g>"""),
        "lungs": dict(
            color="#0288d1",
            anchor=(236, 175),
            sub_en="Windpipe (Trachea) • Bronchi • Lobes • Diaphragm",
            sub_hi="Saans nali • Fefde • Diaphragm",
            svg="""
            <g id="organ-lungs">
              <!-- Trachea (windpipe) with cartilage rings -->
              <rect x="174" y="96" width="12" height="44" rx="3" fill="#e0f7fa" stroke="#0277bd" stroke-width="2"/>
              <line x1="174" y1="104" x2="186" y2="104" stroke="#0277bd" stroke-width="1.5"/>
              <line x1="174" y1="111" x2="186" y2="111" stroke="#0277bd" stroke-width="1.5"/>
              <line x1="174" y1="118" x2="186" y2="118" stroke="#0277bd" stroke-width="1.5"/>
              <line x1="174" y1="125" x2="186" y2="125" stroke="#0277bd" stroke-width="1.5"/>
              <line x1="174" y1="132" x2="186" y2="132" stroke="#0277bd" stroke-width="1.5"/>
              <!-- Primary Bronchi -->
              <path d="M176 140 Q168 152 156 164" fill="none" stroke="#0277bd" stroke-width="4.5" stroke-linecap="round"/>
              <path d="M184 140 Q192 152 204 164" fill="none" stroke="#0277bd" stroke-width="4.5" stroke-linecap="round"/>
              <!-- Right Lung (3 lobes) -->
              <path d="M170 138 C166 126 150 126 140 136 C128 150 122 176 122 200 C122 218 132 228 148 228 C162 228 170 218 172 204 C174 188 174 154 170 138 Z"
                    fill="url(#lung-grad)" stroke="#01579b" stroke-width="2.5"/>
              <path d="M124 182 Q146 186 168 180" fill="none" stroke="#01579b" stroke-width="1.5" stroke-dasharray="3 2"/>
              <path d="M130 206 Q150 208 170 200" fill="none" stroke="#01579b" stroke-width="1.5" stroke-dasharray="3 2"/>
              <!-- Left Lung (2 lobes + Cardiac Notch for heart) -->
              <path d="M190 138 C194 126 210 126 220 136 C232 150 238 176 238 200 C238 218 228 228 212 228 C198 228 190 218 188 206 C182 192 186 154 190 138 Z"
                    fill="url(#lung-grad)" stroke="#01579b" stroke-width="2.5"/>
              <path d="M190 188 Q210 190 236 184" fill="none" stroke="#01579b" stroke-width="1.5" stroke-dasharray="3 2"/>
              <!-- Bronchial tree branches -->
              <path d="M156 164 Q146 174 138 190 M156 164 Q162 176 160 194 M146 174 Q140 182 136 198"
                    fill="none" stroke="#e1f5fe" stroke-width="2" stroke-linecap="round"/>
              <path d="M204 164 Q214 174 222 190 M204 164 Q198 176 200 194 M214 174 Q220 182 224 198"
                    fill="none" stroke="#e1f5fe" stroke-width="2" stroke-linecap="round"/>
              <!-- Alveoli dots -->
              <circle cx="136" cy="198" r="2.5" fill="#e1f5fe"/>
              <circle cx="138" cy="190" r="2.5" fill="#e1f5fe"/>
              <circle cx="160" cy="194" r="2.5" fill="#e1f5fe"/>
              <circle cx="224" cy="198" r="2.5" fill="#e1f5fe"/>
              <circle cx="222" cy="190" r="2.5" fill="#e1f5fe"/>
              <circle cx="200" cy="194" r="2.5" fill="#e1f5fe"/>
              <!-- Diaphragm muscle base -->
              <path d="M118 232 Q180 218 242 232" fill="none" stroke="#e91e63" stroke-width="3" stroke-linecap="round"/>
            </g>"""),
        "heart": dict(
            color="#e53935",
            anchor=(204, 186),
            sub_en="Aorta • Ventricles • Atria • Coronary arteries",
            sub_hi="Aorta • Khoon pump • Dhadkan",
            svg="""
            <g id="organ-heart">
              <!-- Superior Vena Cava (Blue - deoxygenated blood) -->
              <rect x="166" y="146" width="10" height="28" rx="3" fill="#1565c0" stroke="#0d47a1" stroke-width="1.5"/>
              <!-- Aortic Arch (Bright Red - oxygenated blood to body) with 3 branches -->
              <path d="M178 168 C178 148 186 142 198 142 C208 142 212 150 212 164"
                    fill="none" stroke="#d32f2f" stroke-width="10" stroke-linecap="round"/>
              <line x1="188" y1="143" x2="186" y2="134" stroke="#d32f2f" stroke-width="3.5" stroke-linecap="round"/>
              <line x1="196" y1="142" x2="196" y2="132" stroke="#d32f2f" stroke-width="3.5" stroke-linecap="round"/>
              <line x1="204" y1="144" x2="206" y2="134" stroke="#d32f2f" stroke-width="3.5" stroke-linecap="round"/>
              <!-- Pulmonary Artery Trunk (Blue) -->
              <path d="M182 166 Q194 162 208 166" fill="none" stroke="#1976d2" stroke-width="8" stroke-linecap="round"/>
              <!-- Heart Muscular Chambers (Ventricles & Atria) -->
              <path d="M168 174 C160 178 162 192 170 196 C170 208 184 218 198 216 C210 214 214 200 214 188 C214 178 206 172 196 172 C186 172 174 172 168 174 Z"
                    fill="url(#heart-grad)" stroke="#b71c1c" stroke-width="2.5"/>
              <!-- Interventricular septum shadow -->
              <path d="M188 176 Q190 196 198 214" fill="none" stroke="#880e4f" stroke-width="1.8"/>
              <!-- Coronary arteries (red) & veins (blue) -->
              <path d="M184 182 Q192 190 196 204" fill="none" stroke="#ff8a80" stroke-width="1.8" stroke-linecap="round"/>
              <path d="M192 188 Q198 192 204 198" fill="none" stroke="#ff8a80" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M178 184 Q182 194 186 206" fill="none" stroke="#90caf9" stroke-width="1.5" stroke-linecap="round"/>
            </g>"""),
        "stomach": dict(
            color="#ff9800",
            anchor=(212, 250),
            sub_en="Esophagus • Fundus • Gastric folds • Pylorus",
            sub_hi="Food pipe • Acid • Khana pachana",
            svg="""
            <g id="organ-stomach">
              <!-- Esophagus (food pipe) descending from throat -->
              <path d="M178 108 L178 160 Q178 200 184 230" fill="none" stroke="#ffcc80" stroke-width="6" stroke-linecap="round"/>
              <!-- J-shaped stomach with curved fundus, greater curvature and pylorus -->
              <path d="M184 232 C184 222 204 220 212 230 C220 242 220 262 208 272 C194 282 176 278 168 266 C162 254 168 248 178 248 C186 248 194 254 200 252 C204 250 206 242 198 238 C192 234 186 236 184 232 Z"
                    fill="url(#stomach-grad)" stroke="#e65100" stroke-width="2.5"/>
              <!-- Internal gastric rugae folds -->
              <path d="M194 244 Q204 250 202 260 M186 254 Q194 262 198 270 M176 260 Q182 266 190 270"
                    fill="none" stroke="#bf360c" stroke-width="1.8" stroke-linecap="round"/>
              <!-- Duodenum connection (small intestine start) -->
              <path d="M168 266 Q162 272 168 278" fill="none" stroke="#ffe082" stroke-width="6" stroke-linecap="round"/>
            </g>"""),
        "liver": dict(
            color="#8d4f22",
            anchor=(148, 240),
            sub_en="Right &amp; Left Lobes • Gallbladder (Bile)",
            sub_hi="Bada organ • Blood saaf karna • Gallbladder",
            svg="""
            <g id="organ-liver">
              <!-- Wedge-shaped liver spanning upper abdomen -->
              <path d="M136 246 C136 232 152 226 174 226 C194 226 202 232 198 238 C192 244 176 250 168 258 C158 262 144 262 138 256 C136 252 136 248 136 246 Z"
                    fill="url(#liver-grad)" stroke="#4e342e" stroke-width="2.5"/>
              <!-- Falciform ligament division line -->
              <path d="M166 228 Q164 242 160 254" fill="none" stroke="#d7ccc8" stroke-width="1.8"/>
              <!-- Emerald green Gallbladder tucked underneath -->
              <path d="M152 258 C150 266 160 270 162 262 C164 256 158 254 152 258 Z"
                    fill="#43a047" stroke="#1b5e20" stroke-width="1.8"/>
              <path d="M158 262 Q164 268 168 270" fill="none" stroke="#2e7d32" stroke-width="1.5"/>
            </g>"""),
        "kidneys": dict(
            color="#dc2626",
            anchor=(236, 290),
            sub_en="Renal cortex • Medullary pyramids • Ureters to bladder",
            sub_hi="Gurde • Blood filter • 10 lakh nephrons • Bladder",
            svg="""
            <g id="organ-kidneys">
              <!-- Abdominal Aorta & Inferior Vena Cava (Major central vessels) -->
              <line x1="177" y1="262" x2="177" y2="330" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/>
              <line x1="184" y1="262" x2="184" y2="330" stroke="#2563eb" stroke-width="6" stroke-linecap="round"/>
              <!-- Left Renal Artery & Vein -->
              <path d="M177 286 Q194 284 208 288" fill="none" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
              <path d="M208 293 Q196 292 184 292" fill="none" stroke="#3b82f6" stroke-width="3.5" stroke-linecap="round"/>
              <!-- Right Renal Artery & Vein -->
              <path d="M177 294 Q162 292 150 296" fill="none" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
              <path d="M150 301 Q166 298 184 298" fill="none" stroke="#3b82f6" stroke-width="3.5" stroke-linecap="round"/>
              <!-- Left Kidney (anatomical left, viewer's right, higher) -->
              <path d="M212 268 C226 266 237 276 236 292 C235 308 225 313 214 309 C206 304 204 294 207 288 C204 282 206 272 212 268 Z"
                    fill="url(#kidney-grad)" stroke="#450a0a" stroke-width="2.5"/>
              <path d="M226 275 Q232 284 231 296" stroke="#fca5a5" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.6"/>
              <!-- Right Kidney (anatomical right, viewer's left, slightly lower for liver) -->
              <path d="M148 276 C134 274 123 284 124 300 C125 316 135 321 146 317 C154 312 156 302 153 296 C156 290 154 280 148 276 Z"
                    fill="url(#kidney-grad)" stroke="#450a0a" stroke-width="2.5"/>
              <path d="M134 283 Q128 292 129 304" stroke="#fca5a5" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.6"/>
              <!-- Adrenal Glands (Suprarenal Caps contoured on upper pole) -->
              <path d="M208 268 C214 260 226 260 231 268 C224 266 216 266 208 268 Z" fill="#f59e0b" stroke="#b45309" stroke-width="1.2"/>
              <path d="M152 276 C146 268 134 268 129 276 C136 274 144 274 152 276 Z" fill="#f59e0b" stroke="#b45309" stroke-width="1.2"/>
              <!-- Ureters (draining to bladder) -->
              <path d="M150 314 Q158 335 174 350" fill="none" stroke="#fde047" stroke-width="2.2" stroke-linecap="round"/>
              <path d="M210 307 Q202 335 186 350" fill="none" stroke="#fde047" stroke-width="2.2" stroke-linecap="round"/>
              <!-- Urinary Bladder in pelvis -->
              <ellipse cx="180" cy="354" rx="10" ry="7" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
            </g>"""),
        "intestines": dict(
            color="#ffb300",
            anchor=(180, 320),
            sub_en="Small Intestine (nutrients) • Large Colon (water)",
            sub_hi="Chhoti aant (poshan) • Badi aant (paani)",
            svg="""
            <g id="organ-intestines">
              <!-- Large Intestine (Colon) outer frame with haustral pouches -->
              <path d="M142 344 L142 296 Q142 290 150 290 L210 290 Q218 290 218 296 L218 344 Q218 350 210 350 L196 350 L196 364"
                    fill="none" stroke="url(#colon-grad)" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
              <!-- Large intestine segmented contour -->
              <path d="M142 344 L142 296 Q142 290 150 290 L210 290 Q218 290 218 296 L218 344 Q218 350 210 350 L196 350 L196 364"
                    fill="none" stroke="#e65100" stroke-width="1.8" stroke-dasharray="6 3" stroke-linecap="round" stroke-linejoin="round"/>
              <!-- Cecum & Appendix -->
              <circle cx="142" cy="346" r="7" fill="#ffb74d" stroke="#e65100" stroke-width="1.5"/>
              <path d="M140 352 Q136 360 142 362" fill="none" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
              <!-- Small Intestine (intricate coiled inner loops) -->
              <path d="M156 302 H204 Q210 302 210 308 Q210 314 204 314 H156 Q150 314 150 320 Q150 326 156 326 H204 Q210 326 210 332 Q210 338 204 338 H156"
                    fill="none" stroke="#ffd54f" stroke-width="9" stroke-linecap="round"/>
              <path d="M156 302 H204 Q210 302 210 308 Q210 314 204 314 H156 Q150 314 150 320 Q150 326 156 326 H204 Q210 326 210 332 Q210 338 204 338 H156"
                    fill="none" stroke="#f57f17" stroke-width="2" stroke-linecap="round"/>
            </g>"""),
        "bones": dict(
            color="#78909c",
            anchor=(180, 165),
            sub_en="Skull • Rib cage • Spine • Pelvis • Limbs",
            sub_hi="Khopdi • Ribs • Reedh ki haddi • Kankal",
            svg="""
            <g id="organ-bones">
              <!-- Skull (cranium, eye sockets, jaw) -->
              <path d="M158 52 C158 30 202 30 202 52 C202 64 196 68 180 68 C164 68 158 64 158 52 Z"
                    fill="#f5f5f0" stroke="#78909c" stroke-width="2"/>
              <circle cx="170" cy="50" r="4" fill="#37474f"/>
              <circle cx="190" cy="50" r="4" fill="#37474f"/>
              <polygon points="180,54 178,59 182,59" fill="#37474f"/>
              <rect x="174" y="62" width="12" height="6" rx="2" fill="#eceff1" stroke="#78909c" stroke-width="1.5"/>
              <!-- Cervical vertebrae (neck) -->
              <line x1="180" y1="74" x2="180" y2="108" stroke="#90a4ae" stroke-width="6" stroke-linecap="round"/>
              <!-- Clavicles (collarbones) -->
              <path d="M142 116 Q161 122 180 118 Q199 122 218 116" fill="none" stroke="#78909c" stroke-width="3" stroke-linecap="round"/>
              <!-- Sternum (breastbone) in center -->
              <rect x="177" y="132" width="6" height="54" rx="3" fill="#cfd8dc" stroke="#78909c" stroke-width="2"/>
              <!-- Rib cage (6 pairs of contoured ribs) -->
              <path d="M180 138 Q148 142 140 162 M180 138 Q212 142 220 162" fill="none" stroke="#78909c" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M180 150 Q144 154 136 176 M180 150 Q216 154 224 176" fill="none" stroke="#78909c" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M180 162 Q144 168 136 190 M180 162 Q216 168 224 190" fill="none" stroke="#78909c" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M180 174 Q146 182 138 204 M180 174 Q214 182 222 204" fill="none" stroke="#78909c" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M180 186 Q150 194 142 216 M180 186 Q210 194 218 216" fill="none" stroke="#78909c" stroke-width="2.5" stroke-linecap="round"/>
              <!-- Spine (Vertebral column down to pelvis) -->
              <line x1="180" y1="190" x2="180" y2="310" stroke="#90a4ae" stroke-width="7" stroke-dasharray="6 3" stroke-linecap="round"/>
              <!-- Pelvis (Hip bones & Sacrum) -->
              <path d="M148 316 C144 336 158 350 180 348 C202 350 216 336 212 316 C198 310 162 310 148 316 Z"
                    fill="#eceff1" stroke="#78909c" stroke-width="2.5"/>
              <ellipse cx="164" cy="334" rx="8" ry="12" fill="#cfd8dc" stroke="#78909c" stroke-width="1.5"/>
              <ellipse cx="196" cy="334" rx="8" ry="12" fill="#cfd8dc" stroke="#78909c" stroke-width="1.5"/>
              <!-- Arm bones (Humerus, radius, ulna) -->
              <line x1="138" y1="126" x2="114" y2="230" stroke="#78909c" stroke-width="5" stroke-linecap="round"/>
              <line x1="114" y1="230" x2="104" y2="330" stroke="#90a4ae" stroke-width="4" stroke-linecap="round"/>
              <line x1="222" y1="126" x2="246" y2="230" stroke="#78909c" stroke-width="5" stroke-linecap="round"/>
              <line x1="246" y1="230" x2="256" y2="330" stroke="#90a4ae" stroke-width="4" stroke-linecap="round"/>
              <!-- Leg bones (Femur, patella, tibia, fibula) -->
              <line x1="162" y1="346" x2="148" y2="440" stroke="#78909c" stroke-width="6.5" stroke-linecap="round"/>
              <circle cx="148" cy="444" r="5" fill="#cfd8dc" stroke="#78909c" stroke-width="2"/>
              <line x1="148" y1="448" x2="144" y2="530" stroke="#90a4ae" stroke-width="5.5" stroke-linecap="round"/>
              <line x1="198" y1="346" x2="212" y2="440" stroke="#78909c" stroke-width="6.5" stroke-linecap="round"/>
              <circle cx="212" cy="444" r="5" fill="#cfd8dc" stroke="#78909c" stroke-width="2"/>
              <line x1="212" y1="448" x2="216" y2="530" stroke="#90a4ae" stroke-width="5.5" stroke-linecap="round"/>
            </g>"""),
    }


def _body_outline() -> str:
    """Medical-grade anatomical human body silhouette with authentic proportions and cranial contour."""
    return """
    <!-- Medical-grade anatomical human body silhouette -->
    <g id="body-silhouette">
      <!-- Outer cranial vault (anatomical cranium profile, no cartoon face) -->
      <path d="M180 28 
               C198 28 212 40 212 62 
               C212 80 204 94 196 104 
               C192 110 190 118 190 126
               L170 126
               C170 118 168 110 164 104
               C156 94 148 80 148 62
               C148 40 162 28 180 28 Z"
            fill="url(#body-skin)" opacity="0.45" stroke="#94a3b8" stroke-width="2"/>
      <!-- Clavicular Arch & Neck Contour -->
      <path d="M138 134 Q158 140 180 136 Q202 140 222 134" fill="none" stroke="#cbd5e1" stroke-width="2.5" stroke-linecap="round"/>
      <!-- Torso Athletic Muscular Profile (Pectorals, Waist, Pelvic Girdle) -->
      <path d="M138 134 
               C122 155 120 195 126 230 
               C132 265 134 290 128 320 
               C122 345 120 365 132 375 
               C146 385 160 385 180 372 
               C200 385 214 385 228 375 
               C240 365 238 345 232 320 
               C226 290 228 265 234 230 
               C240 195 238 155 222 134 Z" 
            fill="url(#body-skin)" opacity="0.60" stroke="#64748b" stroke-width="2"/>
      <!-- Anatomical Arms (translucent medical contour) -->
      <path d="M124 140 C110 170 102 220 98 270 C94 310 90 350 86 385" stroke="#94a3b8" stroke-width="16" stroke-linecap="round" fill="none" opacity="0.5"/>
      <path d="M236 140 C250 170 258 220 262 270 C266 310 270 350 274 385" stroke="#94a3b8" stroke-width="16" stroke-linecap="round" fill="none" opacity="0.5"/>
      <!-- Anatomical Legs (translucent medical contour) -->
      <path d="M144 375 C140 420 138 475 136 530" stroke="#94a3b8" stroke-width="20" stroke-linecap="round" fill="none" opacity="0.45"/>
      <path d="M216 375 C220 420 222 475 224 530" stroke="#94a3b8" stroke-width="20" stroke-linecap="round" fill="none" opacity="0.45"/>
    </g>"""


def body_svg(highlight: str | None = None, lang: str = "en") -> str:
    """Rich, understandable anatomical body diagram with clear highlights and sub-labels."""
    organs = _organs()
    names = {b["key"]: (b["hi_name"] if lang == "hi" else b["en_name"]) for b in C.BODY_PARTS}
    systems = {b["key"]: b["system"] for b in C.BODY_PARTS}

    # Cardiovascular Great Vessels (Abdominal Aorta & Inferior Vena Cava) context
    vessels_op = "0.85" if highlight is None or highlight in ("heart", "kidneys") else "0.45"
    vessels = f"""
    <!-- Cardiovascular Great Vessels (Aorta & Inferior Vena Cava) -->
    <g id="body-vessels" opacity="{vessels_op}">
      <line x1="177" y1="168" x2="177" y2="330" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/>
      <path d="M177 330 Q168 348 154 365 M177 330 Q186 348 200 365" fill="none" stroke="#dc2626" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="184" y1="160" x2="184" y2="330" stroke="#2563eb" stroke-width="6" stroke-linecap="round"/>
      <path d="M184 330 Q174 348 160 365 M184 330 Q192 348 206 365" fill="none" stroke="#2563eb" stroke-width="4" stroke-linecap="round"/>
    </g>"""

    # Trachea (Cartilaginous airway down to lungs)
    trachea_op = "0.8" if highlight is None or highlight == "lungs" else "0.45"
    trachea = f"""
    <!-- Trachea (Airway with cartilage rings) -->
    <g id="body-trachea" opacity="{trachea_op}">
      <rect x="175" y="100" width="10" height="38" rx="2" fill="#bae6fd" stroke="#0284c7" stroke-width="1.8"/>
      <line x1="175" y1="107" x2="185" y2="107" stroke="#0284c7" stroke-width="1.5"/>
      <line x1="175" y1="114" x2="185" y2="114" stroke="#0284c7" stroke-width="1.5"/>
      <line x1="175" y1="121" x2="185" y2="121" stroke="#0284c7" stroke-width="1.5"/>
      <line x1="175" y1="128" x2="185" y2="128" stroke="#0284c7" stroke-width="1.5"/>
    </g>"""

    parts = [_body_outline(), vessels, trachea]
    order = ["bones", "brain", "lungs", "heart", "stomach", "liver", "kidneys", "intestines"]

    for key in order:
        o = organs[key]
        if highlight is None:
            op, extra = (0.35 if key == "bones" else 1.0), ""
        elif key == highlight:
            op, extra = 1.0, ' filter="url(#glow)"'
        else:
            op, extra = 0.45, ""
        parts.append(f'<g opacity="{op}"{extra}>{o["svg"]}</g>')

    labels = []
    if highlight is not None:
        # Single highlighted organ: show rich callout badge on the right
        o = organs[highlight]
        ax, ay = o["anchor"]
        sub = o["sub_hi"] if lang == "hi" else o["sub_en"]
        col = o["color"]
        name = names[highlight]
        sys_name = systems[highlight]
        # Connecting callout polyline to information box
        by = max(80, min(ay, 460))
        labels.append(f"""
        <!-- Highlight Callout Card -->
        <polyline points="{ax},{ay} 265,{ay} 275,{by}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="4 2"/>
        <circle cx="{ax}" cy="{ay}" r="4.5" fill="{col}" stroke="#ffffff" stroke-width="2"/>
        <g transform="translate(275, {by - 42})">
          <rect width="195" height="84" rx="12" fill="#ffffff" stroke="{col}" stroke-width="2"
                filter="url(#card-shadow)"/>
          <rect x="0" y="0" width="8" height="84" rx="4" fill="{col}"/>
          <text x="16" y="22" font-family="'Trebuchet MS', Arial, sans-serif" font-size="11" font-weight="700"
                fill="{col}" letter-spacing="0.5">{sys_name.upper()}</text>
          <text x="16" y="44" font-family="'Trebuchet MS', Arial, sans-serif" font-size="16" font-weight="700"
                fill="#263238">{name}</text>
          <text x="16" y="66" font-family="Arial, sans-serif" font-size="10.5" fill="#546e7a">{sub}</text>
        </g>""")
    else:
        # Show all organs view: neatly branch labels to left and right margins so no lines overlap
        left_keys = ["brain", "liver", "kidneys", "bones"]
        right_keys = ["lungs", "heart", "stomach", "intestines"]

        for i, k in enumerate(left_keys):
            o = organs[k]
            ax, ay = o["anchor"]
            ly = 70 + i * 115
            col = o["color"]
            name = names[k].split("(")[0].strip()
            labels.append(f"""
            <polyline points="{ax},{ay} 85,{ay} 75,{ly}" fill="none" stroke="{col}" stroke-width="2"/>
            <circle cx="{ax}" cy="{ay}" r="3.5" fill="{col}" stroke="#fff" stroke-width="1.5"/>
            <rect x="10" y="{ly - 14}" width="70" height="26" rx="13" fill="#ffffff" stroke="{col}" stroke-width="1.8"/>
            <text x="45" y="{ly + 4}" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif"
                  font-size="11" font-weight="700" fill="#263238">{name}</text>""")

        for i, k in enumerate(right_keys):
            o = organs[k]
            ax, ay = o["anchor"]
            ly = 110 + i * 110
            col = o["color"]
            name = names[k].split("(")[0].strip()
            labels.append(f"""
            <polyline points="{ax},{ay} 275,{ay} 285,{ly}" fill="none" stroke="{col}" stroke-width="2"/>
            <circle cx="{ax}" cy="{ay}" r="3.5" fill="{col}" stroke="#fff" stroke-width="1.5"/>
            <rect x="280" y="{ly - 14}" width="80" height="26" rx="13" fill="#ffffff" stroke="{col}" stroke-width="1.8"/>
            <text x="320" y="{ly + 4}" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif"
                  font-size="11" font-weight="700" fill="#263238">{name}</text>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 570" width="480" height="570">
  <defs>
    <!-- Glow filter for selected organ -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <!-- Soft shadow for cards -->
    <filter id="card-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <!-- Body & Organ Gradients -->
    <linearGradient id="body-skin" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff0e6"/><stop offset="100%" stop-color="#f5d6be"/>
    </linearGradient>
    <linearGradient id="brain-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f48fb1"/><stop offset="100%" stop-color="#c2185b"/>
    </linearGradient>
    <linearGradient id="lung-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#81d4fa"/><stop offset="100%" stop-color="#0288d1"/>
    </linearGradient>
    <linearGradient id="heart-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ef5350"/><stop offset="100%" stop-color="#b71c1c"/>
    </linearGradient>
    <linearGradient id="stomach-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffa726"/><stop offset="100%" stop-color="#e65100"/>
    </linearGradient>
    <linearGradient id="liver-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a1662f"/><stop offset="100%" stop-color="#5d3a14"/>
    </linearGradient>
    <linearGradient id="kidney-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="50%" stop-color="#b91c1c"/>
      <stop offset="100%" stop-color="#581c1c"/>
    </linearGradient>
    <linearGradient id="colon-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffb74d"/><stop offset="100%" stop-color="#f57c00"/>
    </linearGradient>
  </defs>
  <!-- Background Card -->
  <rect width="480" height="570" rx="18" fill="#f8fbfe"/>
  <rect x="8" y="8" width="464" height="554" rx="14" fill="none" stroke="#e1eef8" stroke-width="1.5"/>
  {''.join(parts)}
  {''.join(labels)}
</svg>"""


def kidney_detail_svg(lang: str = "en") -> str:
    """Realistic medical-grade anatomical cross-section of the human kidney and nephron."""
    is_hi = (lang == "hi")
    title = "KIDNEY ANATOMY &amp; CROSS-SECTION" if not is_hi else "GURDE KI ANATOMY AUR CROSS-SECTION"
    sub_title = "Internal Filtration Engine • 1 Million Nephrons per Kidney" if not is_hi else "Sharir Ka Blood Filter • 10 Lakh Nephrons Har Gurde Mein"

    labels = {
        "cortex": ("Renal Cortex (Outer Filter)", "Filters blood &amp; balances salt") if not is_hi else ("Renal Cortex (Bahar Ka Filter)", "Khoon filter karta hai"),
        "pyramids": ("Renal Pyramids (Medulla)", "Collects filtered urine") if not is_hi else ("Renal Pyramids (Medulla)", "Urine ikattha karte hain"),
        "pelvis": ("Renal Pelvis", "Central urine funnel") if not is_hi else ("Renal Pelvis", "Peshab funnel"),
        "ureter": ("Ureter", "Duct carrying urine to bladder") if not is_hi else ("Ureter (Mutravahini)", "Bladder tak peshab le jaata hai"),
        "artery": ("Renal Artery (Dirty blood in)", "Brings unfiltered blood") if not is_hi else ("Renal Artery (Khoon In)", "Filter hone wala khoon"),
        "vein": ("Renal Vein (Clean blood out)", "Returns purified blood") if not is_hi else ("Renal Vein (Saaf Khoon Out)", "Saaf khoon wapas bhejta hai"),
        "adrenal": ("Adrenal Gland", "Hormones: Adrenaline &amp; Cortisol") if not is_hi else ("Adrenal Gland", "Urja aur stress hormones"),
    }

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 420" width="560" height="420">
  <defs>
    <!-- Realistic 3D Kidney Gradients -->
    <linearGradient id="kd-cortex-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#b91c1c"/>
      <stop offset="50%" stop-color="#991b1b"/>
      <stop offset="100%" stop-color="#7f1d1d"/>
    </linearGradient>
    <radialGradient id="kd-capsule-3d" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="40%" stop-color="#b91c1c"/>
      <stop offset="85%" stop-color="#7f1d1d"/>
      <stop offset="100%" stop-color="#450a0a"/>
    </radialGradient>
    <linearGradient id="kd-pyramid-grad" x1="0" y1="0" x2="1" y2="0.8">
      <stop offset="0%" stop-color="#881337"/>
      <stop offset="60%" stop-color="#9f1239"/>
      <stop offset="100%" stop-color="#e11d48"/>
    </linearGradient>
    <linearGradient id="kd-pelvis-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="50%" stop-color="#fde047"/>
      <stop offset="100%" stop-color="#eab308"/>
    </linearGradient>
    <linearGradient id="kd-adrenal-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="40%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
    <linearGradient id="kd-artery" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#b91c1c"/>
    </linearGradient>
    <linearGradient id="kd-vein" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <filter id="kd-shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="560" height="420" rx="16" fill="#0f172a"/>
  <rect x="6" y="6" width="548" height="408" rx="12" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>

  <!-- Header Banner -->
  <text x="28" y="32" font-family="'Outfit', 'Trebuchet MS', sans-serif" font-size="16" font-weight="800" fill="#f87171" letter-spacing="0.5">{title}</text>
  <text x="28" y="48" font-family="'Poppins', Arial, sans-serif" font-size="10" fill="#94a3b8">{sub_title}</text>

  <!-- Stat Badges Top Right -->
  <g transform="translate(360, 16)">
    <rect width="175" height="26" rx="13" fill="rgba(185, 28, 28, 0.25)" stroke="#ef4444" stroke-width="1"/>
    <text x="87" y="17" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#fca5a5">⚡ Filters 180 Liters / Day</text>
  </g>

  <!-- MAIN REALISTIC KIDNEY (Cross-Section Longitudinal Cut) -->
  <g transform="translate(145, 60)" filter="url(#kd-shadow)">
    <!-- Adrenal Gland (Suprarenal Cap) -->
    <path d="M70 12 C85 -4 135 -6 150 14 C132 18 90 22 70 12 Z" fill="url(#kd-adrenal-grad)" stroke="#78350f" stroke-width="1.8"/>
    <path d="M85 4 Q110 12 135 6" fill="none" stroke="#fef08a" stroke-width="1.2" stroke-linecap="round"/>

    <!-- Renal Capsule (Outer 3D Bean Contour) -->
    <path d="M90 14 
             C155 12 210 50 215 130 
             C220 210 175 290 100 295 
             C35 298 10 250 15 190 
             C18 150 48 155 50 135
             C52 110 25 110 35 70
             C45 30 65 15 90 14 Z" 
          fill="url(#kd-capsule-3d)" stroke="#450a0a" stroke-width="3"/>

    <!-- Renal Cortex (Outer Filtration Band Layer) -->
    <path d="M90 22 
             C148 20 198 55 202 130 
             C206 202 165 276 100 282 
             C48 284 25 240 28 188 
             C30 155 58 155 60 135
             C62 115 38 112 45 74
             C52 40 70 24 90 22 Z" 
          fill="url(#kd-cortex-grad)" stroke="#ef4444" stroke-width="1.2" opacity="0.95"/>

    <!-- Renal Pyramids (Striated Triangular Medullary Lobes) -->
    <!-- Pyramid 1 (Superior) -->
    <path d="M96 38 L125 72 L75 75 Z" fill="url(#kd-pyramid-grad)" stroke="#4c0519" stroke-width="1.5"/>
    <line x1="96" y1="42" x2="98" y2="72" stroke="#fda4af" stroke-width="1" opacity="0.6"/>
    <line x1="88" y1="52" x2="84" y2="73" stroke="#fda4af" stroke-width="1" opacity="0.6"/>
    <line x1="108" y1="52" x2="114" y2="72" stroke="#fda4af" stroke-width="1" opacity="0.6"/>

    <!-- Pyramid 2 (Upper Lateral) -->
    <path d="M140 68 L148 110 L108 100 Z" fill="url(#kd-pyramid-grad)" stroke="#4c0519" stroke-width="1.5"/>
    <line x1="138" y1="74" x2="128" y2="104" stroke="#fda4af" stroke-width="1" opacity="0.6"/>
    <line x1="125" y1="82" x2="116" y2="102" stroke="#fda4af" stroke-width="1" opacity="0.6"/>
    <line x1="144" y1="92" x2="136" y2="108" stroke="#fda4af" stroke-width="1" opacity="0.6"/>

    <!-- Pyramid 3 (Mid Lateral) -->
    <path d="M162 130 L145 158 L114 135 Z" fill="url(#kd-pyramid-grad)" stroke="#4c0519" stroke-width="1.5"/>
    <line x1="156" y1="134" x2="128" y2="148" stroke="#fda4af" stroke-width="1" opacity="0.6"/>
    <line x1="146" y1="142" x2="120" y2="142" stroke="#fda4af" stroke-width="1" opacity="0.6"/>

    <!-- Pyramid 4 (Lower Lateral) -->
    <path d="M152 195 L118 185 L132 225 Z" fill="url(#kd-pyramid-grad)" stroke="#4c0519" stroke-width="1.5"/>
    <line x1="146" y1="198" x2="126" y2="202" stroke="#fda4af" stroke-width="1" opacity="0.6"/>
    <line x1="138" y1="214" x2="122" y2="194" stroke="#fda4af" stroke-width="1" opacity="0.6"/>

    <!-- Pyramid 5 (Inferior) -->
    <path d="M110 265 L76 215 L120 215 Z" fill="url(#kd-pyramid-grad)" stroke="#4c0519" stroke-width="1.5"/>
    <line x1="108" y1="258" x2="98" y2="218" stroke="#fda4af" stroke-width="1" opacity="0.6"/>
    <line x1="98" y1="246" x2="86" y2="218" stroke="#fda4af" stroke-width="1" opacity="0.6"/>
    <line x1="114" y1="246" x2="110" y2="218" stroke="#fda4af" stroke-width="1" opacity="0.6"/>

    <!-- Pyramid 6 (Lower Medial) -->
    <path d="M54 235 L80 196 L58 178 Z" fill="url(#kd-pyramid-grad)" stroke="#4c0519" stroke-width="1.5"/>

    <!-- Pyramid 7 (Upper Medial) -->
    <path d="M52 82 L78 108 L54 126 Z" fill="url(#kd-pyramid-grad)" stroke="#4c0519" stroke-width="1.5"/>

    <!-- Interlobar Arteries (Branching Tree) -->
    <path d="M60 135 Q75 110 100 100 Q125 90 140 68" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M60 145 Q80 145 114 135 Q145 130 162 130" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M60 155 Q80 170 118 185 Q135 200 152 195" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round"/>

    <!-- Interlobar Veins (Accompanying Blue Network) -->
    <path d="M55 130 Q70 105 95 95 Q120 85 135 65" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" opacity="0.85"/>
    <path d="M55 150 Q75 165 112 180 Q130 195 146 190" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" opacity="0.85"/>

    <!-- Calyces (Major and Minor Funnels Collecting Urine) -->
    <path d="M75 75 Q85 85 90 98" fill="none" stroke="#fef08a" stroke-width="4.5" stroke-linecap="round"/>
    <path d="M108 100 Q98 108 90 115" fill="none" stroke="#fef08a" stroke-width="4.5" stroke-linecap="round"/>
    <path d="M114 135 Q98 135 88 138" fill="none" stroke="#fef08a" stroke-width="5" stroke-linecap="round"/>
    <path d="M118 185 Q98 175 88 165" fill="none" stroke="#fef08a" stroke-width="4.5" stroke-linecap="round"/>
    <path d="M76 215 Q82 198 86 175" fill="none" stroke="#fef08a" stroke-width="4.5" stroke-linecap="round"/>

    <!-- Renal Pelvis (Central Golden Urine Funnel) -->
    <path d="M92 110 C96 125 96 160 88 175 L52 190 L40 160 L50 130 Z"
          fill="url(#kd-pelvis-grad)" stroke="#ca8a04" stroke-width="2"/>

    <!-- Renal Hilum Blood Vessels (Entering/Exiting Indentation) -->
    <!-- Renal Artery (Red) with branch -->
    <path d="M-30 138 L45 138 Q55 138 60 145" fill="none" stroke="url(#kd-artery)" stroke-width="9" stroke-linecap="round"/>
    <path d="M-30 138 L25 138 L40 120" fill="none" stroke="url(#kd-artery)" stroke-width="5" stroke-linecap="round"/>

    <!-- Renal Vein (Blue) with branch -->
    <path d="M-30 156 L42 156 Q52 156 58 150" fill="none" stroke="url(#kd-vein)" stroke-width="11" stroke-linecap="round"/>
    <path d="M-30 156 L20 156 L35 170" fill="none" stroke="url(#kd-vein)" stroke-width="6" stroke-linecap="round"/>

    <!-- Ureter (Tubes carrying urine downwards from pelvis) -->
    <path d="M48 185 Q45 220 30 260 Q18 290 20 320" 
          fill="none" stroke="#fde047" stroke-width="8" stroke-linecap="round"/>
    <path d="M48 185 Q45 220 30 260 Q18 290 20 320" 
          fill="none" stroke="#ca8a04" stroke-width="1.8" stroke-linecap="round"/>
  </g>

  <!-- MICRO-NEPHRON CALLOUT LENS (Bottom Right) -->
  <g transform="translate(390, 240)">
    <!-- Circular Magnifier Frame -->
    <circle cx="65" cy="65" r="58" fill="#1e293b" stroke="#38bdf8" stroke-width="3" filter="url(#kd-shadow)"/>
    <text x="65" y="24" text-anchor="middle" font-family="'Outfit', sans-serif" font-size="9" font-weight="700" fill="#38bdf8">NEPHRON FILTER</text>
    
    <!-- Magnified Glomerulus (Bowman's Capsule) -->
    <circle cx="45" cy="50" r="14" fill="#fee2e2" stroke="#ef4444" stroke-width="2.2"/>
    <!-- Glomerular Capillary Knot -->
    <path d="M40 46 C42 42 48 42 50 46 C52 50 44 54 42 52 C40 50 48 48 45 46" fill="none" stroke="#dc2626" stroke-width="2"/>
    <!-- Tubule Loop of Henle -->
    <path d="M58 54 Q75 60 70 80 Q66 100 55 100 Q45 100 48 78 Q50 68 85 70" fill="none" stroke="#facc15" stroke-width="3" stroke-linecap="round"/>
    <!-- Collecting Duct -->
    <line x1="85" y1="40" x2="85" y2="108" stroke="#fb923c" stroke-width="4.5" stroke-linecap="round"/>
    
    <text x="65" y="116" text-anchor="middle" font-family="Arial, sans-serif" font-size="8.5" font-weight="700" fill="#cbd5e1">1 Million Filters</text>
  </g>

  <!-- ANATOMICAL CALLOUT LABELS & ARROWS -->
  <!-- 1. Adrenal Gland -->
  <polyline points="235,65 190,45 80,45" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3 2"/>
  <circle cx="235" cy="65" r="3.5" fill="#f59e0b"/>
  <text x="75" y="42" text-anchor="end" font-family="'Outfit', sans-serif" font-size="11" font-weight="700" fill="#fbbf24">{labels['adrenal'][0]}</text>
  <text x="75" y="54" text-anchor="end" font-family="Arial, sans-serif" font-size="9" fill="#94a3b8">{labels['adrenal'][1]}</text>

  <!-- 2. Renal Artery -->
  <polyline points="115,198 60,198 35,145" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3 2"/>
  <circle cx="115" cy="198" r="3.5" fill="#ef4444"/>
  <text x="30" y="138" font-family="'Outfit', sans-serif" font-size="11" font-weight="700" fill="#f87171">{labels['artery'][0]}</text>
  <text x="30" y="150" font-family="Arial, sans-serif" font-size="9" fill="#94a3b8">{labels['artery'][1]}</text>

  <!-- 3. Renal Vein -->
  <polyline points="115,216 70,216 45,216" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="3 2"/>
  <circle cx="115" cy="216" r="3.5" fill="#3b82f6"/>
  <text x="40" y="228" font-family="'Outfit', sans-serif" font-size="11" font-weight="700" fill="#60a5fa">{labels['vein'][0]}</text>
  <text x="40" y="240" font-family="Arial, sans-serif" font-size="9" fill="#94a3b8">{labels['vein'][1]}</text>

  <!-- 4. Renal Cortex -->
  <polyline points="325,120 380,105 430,105" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3 2"/>
  <circle cx="325" cy="120" r="3.5" fill="#ef4444"/>
  <text x="435" y="102" font-family="'Outfit', sans-serif" font-size="11" font-weight="700" fill="#f87171">{labels['cortex'][0]}</text>
  <text x="435" y="114" font-family="Arial, sans-serif" font-size="9" fill="#94a3b8">{labels['cortex'][1]}</text>

  <!-- 5. Renal Pyramids -->
  <polyline points="295,175 350,150 410,150" fill="none" stroke="#fb7185" stroke-width="1.5" stroke-dasharray="3 2"/>
  <circle cx="295" cy="175" r="3.5" fill="#fb7185"/>
  <text x="415" y="147" font-family="'Outfit', sans-serif" font-size="11" font-weight="700" fill="#fb7185">{labels['pyramids'][0]}</text>
  <text x="415" y="159" font-family="Arial, sans-serif" font-size="9" fill="#94a3b8">{labels['pyramids'][1]}</text>

  <!-- 6. Renal Pelvis -->
  <polyline points="225,205 280,215 365,215" fill="none" stroke="#facc15" stroke-width="1.5" stroke-dasharray="3 2"/>
  <circle cx="225" cy="205" r="3.5" fill="#facc15"/>
  <text x="370" y="212" font-family="'Outfit', sans-serif" font-size="11" font-weight="700" fill="#fde047">{labels['pelvis'][0]}</text>
  <text x="370" y="224" font-family="Arial, sans-serif" font-size="9" fill="#94a3b8">{labels['pelvis'][1]}</text>

  <!-- 7. Ureter -->
  <polyline points="185,350 220,380 320,380" fill="none" stroke="#eab308" stroke-width="1.5" stroke-dasharray="3 2"/>
  <circle cx="185" cy="350" r="3.5" fill="#eab308"/>
  <text x="325" y="377" font-family="'Outfit', sans-serif" font-size="11" font-weight="700" fill="#fef08a">{labels['ureter'][0]}</text>
  <text x="325" y="389" font-family="Arial, sans-serif" font-size="9" fill="#94a3b8">{labels['ureter'][1]}</text>
</svg>"""


# ============================================================================= ATOMS / STATES / pH
def electron_shells(z: int) -> list[int]:
    shells = []
    for cap in (2, 8, 8, 2):
        take = min(z, cap)
        if take:
            shells.append(take)
        z -= take
    return shells


def atom_svg(z: int) -> str:
    """Modern quantum Bohr model atom with 3D nucleus, glowing electron shells, and periodic card."""
    _, sym, name, n = C.ELEMENT_BY_Z[z]
    shells = electron_shells(z)
    cx, cy = 150, 136
    radii = [38, 64, 90, 114]
    shell_names = ["K (max 2)", "L (max 8)", "M (max 8)", "N (max 2)"]

    out = [
        f'<defs>',
        f'<radialGradient id="nuc-glow" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0%" stop-color="#ff8a80"/><stop offset="60%" stop-color="#d32f2f"/><stop offset="100%" stop-color="#880e4f"/>'
        f'</radialGradient>',
        f'<radialGradient id="elec-glow" cx="35%" cy="35%" r="65%">'
        f'<stop offset="0%" stop-color="#ffffff"/><stop offset="50%" stop-color="#00e5ff"/><stop offset="100%" stop-color="#0277bd"/>'
        f'</radialGradient>',
        f'<filter id="atom-glow" x="-30%" y="-30%" width="160%" height="160%">'
        f'<feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f'</filter>',
        f'</defs>',
        f'<rect width="300" height="360" rx="18" fill="#0a1224"/>',
        f'<rect x="6" y="6" width="288" height="348" rx="14" fill="none" stroke="#1e293b" stroke-width="1.5"/>'
    ]

    # Concentric orbital shells with shell labels
    for idx, r in enumerate(radii[:len(shells)]):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#334d7a" stroke-width="1.5" stroke-dasharray="4 3"/>')
        out.append(f'<text x="{cx + r - 4}" y="{cy - 5}" font-family="Arial, sans-serif" font-size="8" fill="#64748b">{shell_names[idx].split()[0]}</text>')

    # Electrons on orbits with glowing negative charge
    for r, cnt in zip(radii, shells):
        for i in range(cnt):
            a = 2 * math.pi * i / cnt - math.pi / 2
            ex = cx + r * math.cos(a)
            ey = cy + r * math.sin(a)
            out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="6" fill="url(#elec-glow)" filter="url(#atom-glow)"/>')
            out.append(f'<text x="{ex:.1f}" y="{ey + 2.5:.1f}" text-anchor="middle" font-family="Arial" font-size="7" font-weight="700" fill="#003756">−</text>')

    # 3D Nucleus at center
    out.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="url(#nuc-glow)" filter="url(#atom-glow)"/>')
    out.append(f'<text x="{cx}" y="{cy - 1}" text-anchor="middle" font-family="\'Trebuchet MS\', Arial" font-size="15" font-weight="700" fill="#ffffff">{sym}</text>')
    out.append(f'<text x="{cx}" y="{cy + 12}" text-anchor="middle" font-family="Arial" font-size="8.5" font-weight="700" fill="#ffebee">{z}p + {n}n</text>')

    # Periodic Element Card at bottom
    mass = z + n
    out.append(f'<g transform="translate(18, 268)">'
               f'<rect width="264" height="74" rx="10" fill="#131e36" stroke="#253556" stroke-width="1.5"/>'
               f'<rect x="10" y="10" width="46" height="54" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>'
               f'<text x="16" y="24" font-family="Arial" font-size="9" fill="#94a3b8">{z}</text>'
               f'<text x="33" y="44" text-anchor="middle" font-family="\'Trebuchet MS\', Arial" font-size="18" font-weight="700" fill="#38bdf8">{sym}</text>'
               f'<text x="33" y="58" text-anchor="middle" font-family="Arial" font-size="8" fill="#94a3b8">{mass}</text>'
               f'<text x="68" y="28" font-family="\'Trebuchet MS\', Arial" font-size="14" font-weight="700" fill="#f8fafc">{name}</text>'
               f'<text x="68" y="46" font-family="Arial" font-size="10.5" fill="#38bdf8">Shells: {", ".join(map(str, shells))}</text>'
               f'<text x="68" y="60" font-family="Arial" font-size="9" fill="#94a3b8">🔴 {z} Protons  ⚪ {n} Neutrons  ⚡ {z} Electrons</text>'
               f'</g>')

    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 360" width="300" height="360">{"".join(out)}</svg>'


def states_svg(state: str) -> str:
    """Rich laboratory beaker demonstrating particle arrangement, vibration, and energy."""
    rnd = random.Random(42)
    w, h = 320, 240
    out = [
        f'<defs>'
        f'<linearGradient id="beaker-glass" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="#e0f2fe" stop-opacity="0.8"/><stop offset="20%" stop-color="#f0f9ff" stop-opacity="0.4"/>'
        f'<stop offset="80%" stop-color="#f0f9ff" stop-opacity="0.4"/><stop offset="100%" stop-color="#bae6fd" stop-opacity="0.8"/>'
        f'</linearGradient>'
        f'<radialGradient id="particle-ball" cx="35%" cy="35%" r="65%">'
        f'<stop offset="0%" stop-color="#93c5fd"/><stop offset="50%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#1d4ed8"/>'
        f'</radialGradient>'
        f'</defs>',
        f'<rect width="{w}" height="{h}" rx="16" fill="#f8fafc"/>',
        f'<rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="12" fill="none" stroke="#e2e8f0" stroke-width="1.5"/>',
        # Laboratory Beaker
        f'<path d="M48 24 L54 165 C54 175 64 182 76 182 L244 182 C256 182 266 175 266 165 L272 24" '
        f'fill="url(#beaker-glass)" stroke="#64748b" stroke-width="2.5" stroke-linecap="round"/>',
        # Measurement tick marks on beaker
        f'<line x1="56" y1="55" x2="72" y2="55" stroke="#94a3b8" stroke-width="1.8"/>'
        f'<text x="76" y="58" font-family="Arial" font-size="8" fill="#64748b">150ml</text>',
        f'<line x1="55" y1="95" x2="72" y2="95" stroke="#94a3b8" stroke-width="1.8"/>'
        f'<text x="76" y="98" font-family="Arial" font-size="8" fill="#64748b">100ml</text>',
        f'<line x1="55" y1="135" x2="72" y2="135" stroke="#94a3b8" stroke-width="1.8"/>'
        f'<text x="76" y="138" font-family="Arial" font-size="8" fill="#64748b">50ml</text>',
    ]

    pts = []
    if state == "solid":
        # Orderly crystal lattice vibrating in place
        for row in range(5):
            for col in range(8):
                pts.append((82 + col * 20, 96 + row * 16))
        energy_badge = "Cold (&lt; 0°C) • Low Energy"
        summary = "Solid: Particles tightly packed in rows, vibrating in place"
        badge_bg = "#e0f2fe"
        badge_col = "#0369a1"
        for x, y in pts:
            # vibration marks
            out.append(f'<path d="M{x - 9} {y - 4} Q{x - 7} {y} {x - 9} {y + 4}" stroke="#93c5fd" stroke-width="1" fill="none"/>')
            out.append(f'<path d="M{x + 9} {y - 4} Q{x + 7} {y} {x + 9} {y + 4}" stroke="#93c5fd" stroke-width="1" fill="none"/>')
    elif state == "liquid":
        # Free sliding fluid droplets at bottom of beaker
        for _ in range(32):
            pts.append((74 + rnd.uniform(0, 172), 115 + rnd.uniform(0, 60)))
        energy_badge = "Room Temp (25°C) • Medium Energy"
        summary = "Liquid: Particles close together, sliding freely past each other"
        badge_bg = "#dcfce7"
        badge_col = "#15803d"
        # Meniscus water level
        out.append(f'<path d="M55 118 Q160 125 265 118 L265 170 Q265 180 250 180 L70 180 Q55 180 55 170 Z" '
                   f'fill="#60a5fa" opacity="0.25"/>')
    else:
        # High speed gas molecules zooming far apart
        for _ in range(12):
            pts.append((68 + rnd.uniform(0, 184), 30 + rnd.uniform(0, 140)))
        energy_badge = "High Heat (&gt; 100°C) • High Energy"
        summary = "Gas: Particles far apart, zooming rapidly in all directions"
        badge_bg = "#fee2e2"
        badge_col = "#b91c1c"
        for x, y in pts:
            dx = rnd.uniform(-14, 14)
            dy = rnd.uniform(-14, 14)
            out.append(f'<line x1="{x}" y1="{y}" x2="{x - dx}" y2="{y - dy}" stroke="#f87171" stroke-width="1.5" stroke-dasharray="2 2"/>')

    for x, y in pts:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="url(#particle-ball)"/>')

    # Energy badge & Summary footer
    out.append(f'<rect x="65" y="194" width="190" height="18" rx="9" fill="{badge_bg}"/>')
    out.append(f'<text x="160" y="206" text-anchor="middle" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="{badge_col}">{energy_badge}</text>')
    out.append(f'<text x="160" y="228" text-anchor="middle" font-family="\'Trebuchet MS\', Arial" font-size="11.5" font-weight="700" fill="#1e293b">{summary}</text>')

    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{"".join(out)}</svg>'


PH_COLORS = ["#e63946", "#e85d3a", "#ee7d32", "#f3a02b", "#f7c325", "#e1d927", "#b6d430", "#7fc97f",
             "#4cbb8a", "#2fa7a0", "#2889b8", "#3a6acb", "#4f4ccf", "#6a39c4", "#7f2ba6"]


def ph_svg(ph: float, label: str = "") -> str:
    """Comprehensive, intuitive visual pH rainbow spectrum with benchmarks and pointer."""
    w, h = 500, 200
    out = [
        f'<defs>'
        f'<filter id="ph-shadow" x="-10%" y="-10%" width="120%" height="120%">'
        f'<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.15"/>'
        f'</filter>'
        f'</defs>',
        f'<rect width="{w}" height="{h}" rx="16" fill="#ffffff"/>',
        f'<rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="12" fill="none" stroke="#e2e8f0" stroke-width="1.5"/>',
        f'<text x="250" y="24" text-anchor="middle" font-family="\'Trebuchet MS\', Arial" font-size="13" font-weight="700" fill="#334155">pH Scale (Acids, Neutral &amp; Bases)</text>',
    ]

    start_x = 25
    cell_w = 30
    bar_y = 65

    # 15 Colored spectrum cells (0 to 14)
    for i, c in enumerate(PH_COLORS):
        bx = start_x + i * cell_w
        out.append(f'<rect x="{bx}" y="{bar_y}" width="{cell_w}" height="42" fill="{c}"/>')
        out.append(f'<text x="{bx + cell_w / 2}" y="{bar_y + 26}" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700" fill="#ffffff">{i}</text>')

    # Border around entire bar
    out.append(f'<rect x="{start_x}" y="{bar_y}" width="{15 * cell_w}" height="42" rx="4" fill="none" stroke="#334155" stroke-width="2"/>')

    # Indicator pointer for current pH
    mx = start_x + (min(max(ph, 0.0), 14.0) + 0.5) * cell_w
    ph_color = PH_COLORS[int(round(min(max(ph, 0.0), 14.0)))]
    badge_x = min(max(mx, 90), 410)

    # Pointer Triangle
    out.append(f'<polygon points="{mx - 8},{bar_y - 2} {mx + 8},{bar_y - 2} {mx},{bar_y + 8}" fill="#1e293b"/>')

    # Active Value Pill
    category = "NEUTRAL" if 6.5 <= ph <= 7.5 else ("STRONG ACID" if ph <= 3 else ("ACID" if ph < 7 else ("STRONG BASE" if ph >= 11 else "BASE")))
    out.append(f'<g transform="translate({badge_x - 65}, {bar_y - 32})" filter="url(#ph-shadow)">'
               f'<rect width="130" height="26" rx="13" fill="{ph_color}"/>'
               f'<text x="65" y="17" text-anchor="middle" font-family="\'Trebuchet MS\', Arial" font-size="11.5" font-weight="700" fill="#ffffff">{label or "Substance"} pH {ph:g}</text>'
               f'</g>')

    # Benchmark Labels below scale
    out.append(f'<text x="{start_x + 3 * cell_w}" y="132" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#dc2626">ACIDIC (0–6)</text>')
    out.append(f'<text x="{start_x + 3 * cell_w}" y="146" text-anchor="middle" font-family="Arial" font-size="9" fill="#64748b">Lemon • Vinegar • Tomato</text>')

    out.append(f'<text x="{start_x + 7 * cell_w + 15}" y="132" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#16a34a">NEUTRAL (7)</text>')
    out.append(f'<text x="{start_x + 7 * cell_w + 15}" y="146" text-anchor="middle" font-family="Arial" font-size="9" fill="#64748b">Pure Water • Blood</text>')

    out.append(f'<text x="{start_x + 11.5 * cell_w}" y="132" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#7c3aed">BASIC / ALKALINE (8–14)</text>')
    out.append(f'<text x="{start_x + 11.5 * cell_w}" y="146" text-anchor="middle" font-family="Arial" font-size="9" fill="#64748b">Baking Soda • Soap • Bleach</text>')

    # Safety advisory footer
    out.append(f'<text x="250" y="178" text-anchor="middle" font-family="Arial" font-size="10" fill="#475569">'
               f'💡 Taste: Acids taste sour, Bases feel slippery. Strong acids and bases can burn skin!</text>')

    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{"".join(out)}</svg>'


def circuit_svg(volts: float, ohms: float) -> str:
    """Authentic, understandable physics bench circuit with battery, resistor, glowing Edison bulb, and ammeter."""
    i = volts / ohms
    glow = min(1.0, i / 2.0)
    brightness_opacity = 0.2 + 0.8 * glow
    glow_radius = 28 + int(32 * glow)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 280" width="460" height="280">
  <defs>
    <filter id="bulb-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="12" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="bulb-light" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fffde7" stop-opacity="1"/>
      <stop offset="40%" stop-color="#ffeb3b" stop-opacity="{brightness_opacity:.2f}"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="battery-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#37474f"/><stop offset="50%" stop-color="#607d8b"/><stop offset="100%" stop-color="#263238"/>
    </linearGradient>
  </defs>
  <!-- Card Background -->
  <rect width="460" height="280" rx="16" fill="#f8fafc"/>
  <rect x="6" y="6" width="448" height="268" rx="12" fill="none" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Circuit Insulated Copper Wire Loop -->
  <path d="M70 65 H150 L160 48 L176 82 L192 48 L208 82 L224 48 L240 82 L250 65 H370 V110"
        fill="none" stroke="#1e293b" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M370 160 V220 H70 V165"
        fill="none" stroke="#1e293b" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="70" y1="105" x2="70" y2="65" stroke="#1e293b" stroke-width="5" stroke-linecap="round"/>

  <!-- Current flow directional arrows -->
  <polygon points="110,61 118,65 110,69" fill="#f59e0b"/>
  <polygon points="310,61 318,65 310,69" fill="#f59e0b"/>
  <polygon points="374,185 370,195 366,185" fill="#f59e0b"/>
  <polygon points="210,224 200,220 210,216" fill="#f59e0b"/>
  <text x="315" y="56" font-family="Arial" font-size="9" font-weight="700" fill="#d97706">Current Flow --&gt;</text>

  <!-- 3D Battery -->
  <g transform="translate(48, 105)">
    <rect x="0" y="0" width="44" height="60" rx="4" fill="url(#battery-grad)"/>
    <rect x="14" y="-8" width="16" height="8" rx="2" fill="#d32f2f"/>
    <text x="22" y="22" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="13" font-weight="700" fill="#ffffff">{volts:g}V</text>
    <text x="22" y="38" text-anchor="middle" font-family="Arial" font-size="8.5" fill="#cfd8dc">BATTERY</text>
    <text x="36" y="-1" font-family="Arial" font-size="12" font-weight="700" fill="#ef4444">+</text>
    <text x="36" y="68" font-family="Arial" font-size="14" font-weight="700" fill="#3b82f6">−</text>
  </g>

  <!-- Resistor Section -->
  <rect x="152" y="38" width="104" height="54" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3 2"/>
  <text x="204" y="30" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="13" font-weight="700" fill="#0f172a">Resistor R = {ohms:g} Ω</text>

  <!-- Lightbulb with dynamic radiance and tungsten filament -->
  <circle cx="370" cy="135" r="{glow_radius}" fill="url(#bulb-light)" filter="url(#bulb-glow)"/>
  <circle cx="370" cy="135" r="24" fill="#ffffff" stroke="#334155" stroke-width="2.5" fill-opacity="0.85"/>
  <rect x="363" y="159" width="14" height="10" rx="2" fill="#94a3b8" stroke="#334155" stroke-width="1.5"/>
  <!-- Filament wires -->
  <path d="M363 145 L367 130 L373 130 L377 145" fill="none" stroke="{ '#f59e0b' if glow > 0.1 else '#64748b' }" stroke-width="2"/>
  <circle cx="370" cy="130" r="3" fill="{ '#ffeb3b' if glow > 0.1 else '#94a3b8' }"/>
  <text x="370" y="185" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="11.5" font-weight="700" fill="#1e293b">Bulb ({int(glow * 100)}% Glow)</text>

  <!-- Digital Multimeter / Ammeter Display -->
  <g transform="translate(140, 238)">
    <rect x="0" y="0" width="180" height="34" rx="8" fill="#0f172a"/>
    <text x="90" y="22" text-anchor="middle" font-family="'Courier New', monospace" font-size="15" font-weight="700" fill="#22c55e">
      I = {i:.2f} A
    </text>
  </g>
  <text x="230" y="214" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="12" font-weight="700" fill="#15803d">
    Ohm's Law: Current I = Voltage (V) ÷ Resistance (R)
  </text>
</svg>"""


# ============================================================================= PLOTLY
PLANETS = {"Earth": 9.8, "Moon": 1.6, "Mars": 3.7, "Jupiter": 24.8}
_LAYOUT = dict(template="plotly_white", margin=dict(l=10, r=10, t=50, b=10), height=380)


def projectile_fig(speed: float = 20, angle: float = 45, planet: str = "Earth", animate: bool = True) -> go.Figure:
    g = PLANETS.get(planet, 9.8)
    th = math.radians(angle)
    t_total = 2 * speed * math.sin(th) / g
    t = np.linspace(0, t_total, 60)
    x, y = speed * math.cos(th) * t, speed * math.sin(th) * t - 0.5 * g * t ** 2
    y = np.maximum(y, 0)
    rng, hmax = x[-1], speed ** 2 * math.sin(th) ** 2 / (2 * g)
    fig = go.Figure(go.Scatter(x=x, y=y, mode="lines", name="Path", line=dict(color="#1976d2", width=3, dash="dot")))
    fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode="markers", name="Ball",
                             marker=dict(size=18, color="#e53935", line=dict(width=2, color="#b71c1c"))))
    if animate:
        step = 3
        fig.frames = [go.Frame(data=[go.Scatter(x=x, y=y), go.Scatter(x=[x[k]], y=[y[k]])], traces=[0, 1])
                      for k in range(0, len(x), step)]
        fig.update_layout(updatemenus=[dict(type="buttons", showactive=False, x=0.02, y=0.98, buttons=[
            dict(label="▶ Throw!", method="animate",
                 args=[None, dict(frame=dict(duration=60, redraw=True), fromcurrent=False)])])])
    fig.update_layout(title=f"Throw at {angle}° with {speed:g} m/s on {planet}: range {rng:.1f} m, "
                            f"max height {hmax:.1f} m, flight {t_total:.1f} s",
                      xaxis=dict(title="Distance (m)", range=[0, max(rng * 1.1, 1)]),
                      yaxis=dict(title="Height (m)", range=[0, max(hmax * 1.4, 1)]), showlegend=False, **_LAYOUT)
    return fig


def pendulum_metrics(length: float, g: float = 9.8) -> float:
    return 2 * math.pi * math.sqrt(length / g)


def pendulum_fig(length: float = 1.0, amp_deg: float = 20, g: float = 9.8) -> go.Figure:
    th0 = math.radians(amp_deg)
    dt, steps = 0.01, 500
    th, om, ts, ths = th0, 0.0, [], []
    for i in range(steps):
        ts.append(i * dt)
        ths.append(math.degrees(th))
        om += -(g / length) * math.sin(th) * dt
        th += om * dt
    fig = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6], subplot_titles=("Pendulum", "Swing angle over time"))
    bx, by = length * math.sin(th0), -length * math.cos(th0)
    fig.add_trace(go.Scatter(x=[0, bx], y=[0, by], mode="lines+markers", line=dict(color="#455a64", width=3),
                             marker=dict(size=[6, 26], color=["#455a64", "#e53935"])), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, -length], mode="lines", line=dict(color="#90a4ae", dash="dash")), row=1, col=1)
    fig.add_trace(go.Scatter(x=ts, y=ths, mode="lines", line=dict(color="#1976d2", width=2.5)), row=1, col=2)
    fig.update_xaxes(range=[-length * 1.2, length * 1.2], row=1, col=1, scaleanchor="y", scaleratio=1, visible=False)
    fig.update_yaxes(range=[-length * 1.15, 0.1 * length], row=1, col=1, visible=False)
    fig.update_xaxes(title="Time (s)", row=1, col=2)
    fig.update_yaxes(title="Angle (°)", row=1, col=2)
    fig.update_layout(showlegend=False, **_LAYOUT)
    return fig


def vi_fig(volts: float, ohms: float) -> go.Figure:
    vs = np.linspace(0, 12, 25)
    fig = go.Figure(go.Scatter(x=vs, y=vs / ohms, mode="lines", line=dict(color="#1976d2", width=3), name=f"R = {ohms:g} Ω"))
    fig.add_trace(go.Scatter(x=[volts], y=[volts / ohms], mode="markers", marker=dict(size=14, color="#e53935"), name="Now"))
    fig.update_layout(title="Current grows in a straight line with voltage", xaxis_title="Voltage (V)",
                      yaxis_title="Current (A)", showlegend=False, **{**_LAYOUT, "height": 300})
    return fig


MEDIA = {"Air": 1.00, "Water": 1.33, "Glass": 1.50, "Diamond": 2.42}


def refraction_fig(n1: float = 1.0, n2: float = 1.33, angle: float = 40) -> go.Figure:
    a1 = math.radians(angle)
    s2 = n1 * math.sin(a1) / n2
    tir = s2 > 1
    fig = go.Figure()
    fig.add_shape(type="rect", x0=-2, x1=2, y0=-2, y1=0, fillcolor="rgba(100,181,246,0.30)", line_width=0)
    fig.add_shape(type="line", x0=0, x1=0, y0=-2, y1=2, line=dict(color="gray", dash="dash"))
    fig.add_trace(go.Scatter(x=[-2 * math.sin(a1), 0], y=[2 * math.cos(a1), 0], mode="lines",
                             line=dict(color="#fbc02d", width=4), name="Incident ray"))
    fig.add_trace(go.Scatter(x=[0, 2 * math.sin(a1)], y=[0, 2 * math.cos(a1)], mode="lines",
                             line=dict(color="#bdbdbd", width=2, dash="dot"), name="Reflected ray"))
    if tir:
        title = "Total internal reflection: the light cannot leave, so it bounces back!"
    else:
        a2 = math.asin(s2)
        fig.add_trace(go.Scatter(x=[0, 2 * math.sin(a2)], y=[0, -2 * math.cos(a2)], mode="lines",
                                 line=dict(color="#e53935", width=4), name="Refracted ray"))
        title = f"Light bends: {angle}° in the top material becomes {math.degrees(a2):.1f}° in the bottom"
    fig.update_layout(title=title, xaxis=dict(range=[-2, 2], visible=False, scaleanchor="y"),
                      yaxis=dict(range=[-2, 2], visible=False), legend=dict(orientation="h", y=-0.02),
                      **{**_LAYOUT, "height": 420})
    fig.add_annotation(x=-1.6, y=1.7, text=f"n₁ = {n1:g}", showarrow=False)
    fig.add_annotation(x=-1.6, y=-1.7, text=f"n₂ = {n2:g}", showarrow=False)
    return fig


ATOM_COLORS = {"H": ("#ffffff", 26), "C": ("#455a64", 34), "O": ("#e53935", 32), "N": ("#1e88e5", 32),
               "Cl": ("#43a047", 38)}


def molecule_fig(key: str) -> go.Figure:
    m = C.MOLECULES[key]
    fig = go.Figure()
    for a, b, order in m["bonds"]:
        (_, x1, y1), (_, x2, y2) = m["atoms"][a], m["atoms"][b]
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        px, py = -dy / ln * 0.07, dx / ln * 0.07
        offs = [0] if order == 1 else [-1, 1]
        for o in offs:
            fig.add_trace(go.Scatter(x=[x1 + px * o, x2 + px * o], y=[y1 + py * o, y2 + py * o], mode="lines",
                                     line=dict(color="#607d8b", width=6), hoverinfo="skip", showlegend=False))
    for sym, x, y in m["atoms"]:
        col, size = ATOM_COLORS[sym]
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[sym], textposition="middle center",
                                 marker=dict(size=size * 1.6, color=col, line=dict(color="#263238", width=2)),
                                 textfont=dict(color="#263238" if sym == "H" else "white", size=15),
                                 hoverinfo="skip", showlegend=False))
    fig.update_layout(title=f"{m['name_en']}  {m['formula']}", xaxis=dict(visible=False, range=[-2, 2], scaleanchor="y"),
                      yaxis=dict(visible=False, range=[-1.6, 1.6]), **{**_LAYOUT, "height": 340})
    return fig


# ============================================================================= INTERACTIVE LAB EXTRAS
def vital_signs_svg(bpm: int = 75, lang: str = "en") -> str:
    """Dynamic ECG & respiratory vital signs monitor for Human Body simulation."""
    state_en = "Resting" if bpm < 85 else ("Walking / Active" if bpm < 125 else "Running / Sprinting!")
    state_hi = "Aaram se" if bpm < 85 else ("Chalte hue" if bpm < 125 else "Daudte hue!")
    state = state_hi if lang == "hi" else state_en
    resp = max(12, int(bpm / 4.5))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 180" width="440" height="180">
  <defs>
    <filter id="ecg-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="screen-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0a121e"/><stop offset="100%" stop-color="#050a12"/>
    </linearGradient>
  </defs>
  <rect width="440" height="180" rx="14" fill="url(#screen-grad)"/>
  <rect x="6" y="6" width="428" height="168" rx="10" fill="none" stroke="#1e293b" stroke-width="1.5"/>
  <g stroke="#132338" stroke-width="1" stroke-dasharray="3 3">
    <line x1="20" y1="45" x2="420" y2="45"/><line x1="20" y1="90" x2="420" y2="90"/><line x1="20" y1="135" x2="420" y2="135"/>
    <line x1="80" y1="20" x2="80" y2="160"/><line x1="160" y1="20" x2="160" y2="160"/><line x1="240" y1="20" x2="240" y2="160"/>
    <line x1="320" y1="20" x2="320" y2="160"/><line x1="400" y1="20" x2="400" y2="160"/>
  </g>
  <path d="M20 90 H50 Q56 82 62 90 H70 L74 96 L82 35 L90 120 L96 90 H110 Q118 78 126 90 H170 Q176 82 182 90 H190 L194 96 L202 35 L210 120 L216 90 H230 Q238 78 246 90 H290 Q296 82 302 90 H310 L314 96 L322 35 L330 120 L336 90 H350 Q358 78 366 90 H420"
        fill="none" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" filter="url(#ecg-glow)"/>
  <g transform="translate(24, 28)">
    <text x="0" y="0" font-family="'Courier New', monospace" font-size="11" font-weight="700" fill="#4ade80">HEART RATE</text>
    <text x="0" y="24" font-family="'Trebuchet MS', Arial" font-size="28" font-weight="700" fill="#22c55e">{bpm}</text>
    <text x="54" y="22" font-family="Arial" font-size="11" fill="#86efac">BPM</text>
  </g>
  <g transform="translate(160, 28)">
    <text x="0" y="0" font-family="'Courier New', monospace" font-size="11" font-weight="700" fill="#38bdf8">BREATHS / MIN</text>
    <text x="0" y="24" font-family="'Trebuchet MS', Arial" font-size="28" font-weight="700" fill="#38bdf8">{resp}</text>
    <text x="44" y="22" font-family="Arial" font-size="11" fill="#bae6fd">RR</text>
  </g>
  <g transform="translate(300, 28)">
    <text x="0" y="0" font-family="'Courier New', monospace" font-size="11" font-weight="700" fill="#fbbf24">OXYGEN SpO2</text>
    <text x="0" y="24" font-family="'Trebuchet MS', Arial" font-size="28" font-weight="700" fill="#fbbf24">99%</text>
  </g>
  <rect x="24" y="145" width="392" height="22" rx="6" fill="#132338"/>
  <text x="220" y="160" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="11" font-weight="700" fill="#f8fafc">
    Activity: {state} • Heart pumps {bpm} times/min, pushing oxygen to every muscle!
  </text>
</svg>"""


def reaction_svg(reaction_key: str = "volcano", lang: str = "en") -> str:
    """Virtual Chemistry Safe Reaction Simulator (Volcano, pH indicator, Ionic Dissolution)."""
    w, h = 480, 260
    if reaction_key == "volcano":
        title = "Baking Soda + Vinegar Fizz (Carbon Dioxide CO2)" if lang == "en" else "Meetha Soda + Sirka Reaction (CO2 Gas)"
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="flask-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#e0f2fe" stop-opacity="0.7"/><stop offset="100%" stop-color="#bae6fd" stop-opacity="0.7"/>
    </linearGradient>
    <linearGradient id="foam-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="16" fill="#f8fafc"/>
  <rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="12" fill="none" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="240" y="28" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="14" font-weight="700" fill="#0f172a">{title}</text>
  <path d="M210 50 L210 90 L140 200 C130 216 142 226 160 226 L320 226 C338 226 350 216 340 200 L270 90 L270 50 Z"
        fill="url(#flask-grad)" stroke="#475569" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M152 205 Q240 210 328 205 L315 180 Q240 185 165 180 Z" fill="#cbd5e1" opacity="0.6"/>
  <ellipse cx="240" cy="180" rx="60" ry="18" fill="url(#foam-grad)" stroke="#e2e8f0"/>
  <ellipse cx="240" cy="140" rx="42" ry="16" fill="url(#foam-grad)" stroke="#e2e8f0"/>
  <ellipse cx="240" cy="95" rx="26" ry="14" fill="url(#foam-grad)" stroke="#e2e8f0"/>
  <ellipse cx="240" cy="46" rx="28" ry="12" fill="url(#foam-grad)" stroke="#e2e8f0"/>
  <circle cx="225" cy="160" r="5" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <circle cx="255" cy="155" r="4" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <circle cx="232" cy="125" r="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <circle cx="250" cy="115" r="5" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <circle cx="236" cy="75" r="7" fill="#ffffff" stroke="#94a3b8" stroke-width="1.2"/>
  <circle cx="246" cy="30" r="8" fill="#ffffff" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="246" y="33" text-anchor="middle" font-family="Arial" font-size="7" font-weight="700" fill="#0284c7">CO2</text>
  <circle cx="218" cy="20" r="6" fill="#ffffff" stroke="#38bdf8" stroke-width="1.2"/>
  <circle cx="265" cy="16" r="7" fill="#ffffff" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="265" y="19" text-anchor="middle" font-family="Arial" font-size="6" font-weight="700" fill="#0284c7">CO2</text>
  <g transform="translate(60, 234)">
    <rect width="360" height="20" rx="10" fill="#0f172a"/>
    <text x="180" y="14" text-anchor="middle" font-family="'Courier New', monospace" font-size="10.5" font-weight="700" fill="#38bdf8">
      NaHCO3 (baking soda) + CH3COOH (vinegar) -&gt; CO2 (gas) + H2O
    </text>
  </g>
</svg>"""
    elif reaction_key == "indicator":
        title = "Red Cabbage pH Color Change (Anthocyanin)" if lang == "en" else "Laal Gobhi pH Color Change"
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="{w}" height="{h}" rx="16" fill="#f8fafc"/>
  <rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="12" fill="none" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="240" y="28" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="14" font-weight="700" fill="#0f172a">{title}</text>
  <g transform="translate(80, 55)">
    <rect x="0" y="0" width="110" height="135" rx="8" fill="#f1f5f9" stroke="#64748b" stroke-width="2.5"/>
    <rect x="6" y="45" width="98" height="84" rx="4" fill="#7c3aed" opacity="0.85"/>
    <text x="55" y="80" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="13" font-weight="700" fill="#ffffff">PURPLE</text>
    <text x="55" y="98" text-anchor="middle" font-family="Arial" font-size="10" fill="#ede9fe">Cabbage Juice (pH 7)</text>
    <text x="55" y="152" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="11" font-weight="700" fill="#475569">Pure Indicator</text>
  </g>
  <g transform="translate(225, 105)">
    <circle cx="15" cy="0" r="16" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
    <polygon points="10,25 20,25 15,35" fill="#ca8a04"/>
    <text x="15" y="46" text-anchor="middle" font-family="Arial" font-size="9" font-weight="700" fill="#a16207">+ Lemon</text>
  </g>
  <g transform="translate(290, 55)">
    <rect x="0" y="0" width="110" height="135" rx="8" fill="#f1f5f9" stroke="#64748b" stroke-width="2.5"/>
    <rect x="6" y="45" width="98" height="84" rx="4" fill="#e11d48" opacity="0.85"/>
    <text x="55" y="80" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="13" font-weight="700" fill="#ffffff">PINK / RED</text>
    <text x="55" y="98" text-anchor="middle" font-family="Arial" font-size="10" fill="#ffe4e6">Acidic (pH 2.5)</text>
    <text x="55" y="152" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="11" font-weight="700" fill="#be123c">Acid Detected!</text>
  </g>
  <g transform="translate(40, 234)">
    <rect width="400" height="20" rx="10" fill="#0f172a"/>
    <text x="200" y="14" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="10.5" font-weight="700" fill="#f43f5e">
      Anthocyanin molecules change their shape in acid, reflecting bright pink light!
    </text>
  </g>
</svg>"""
    else:
        title = "Salt Crystal Dissolving in Water (Ionic Solution)" if lang == "en" else "Namak Ka Paani Mein Ghulna"
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="{w}" height="{h}" rx="16" fill="#f8fafc"/>
  <rect x="6" y="6" width="{w - 12}" height="{h - 12}" rx="12" fill="none" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="240" y="28" text-anchor="middle" font-family="'Trebuchet MS', Arial" font-size="14" font-weight="700" fill="#0f172a">{title}</text>
  <rect x="110" y="55" width="260" height="150" rx="10" fill="#e0f2fe" stroke="#0284c7" stroke-width="2.5" opacity="0.6"/>
  <circle cx="160" cy="100" r="14" fill="#3b82f6"/>
  <text x="160" y="105" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700" fill="#ffffff">Na+</text>
  <circle cx="210" cy="140" r="16" fill="#10b981"/>
  <text x="210" y="145" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700" fill="#ffffff">Cl−</text>
  <circle cx="280" cy="110" r="14" fill="#3b82f6"/>
  <text x="280" y="115" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700" fill="#ffffff">Na+</text>
  <circle cx="320" cy="150" r="16" fill="#10b981"/>
  <text x="320" y="155" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700" fill="#ffffff">Cl−</text>
  <circle cx="230" cy="90" r="16" fill="#10b981"/>
  <text x="230" y="95" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700" fill="#ffffff">Cl−</text>
  <g transform="translate(60, 234)">
    <rect width="360" height="20" rx="10" fill="#0f172a"/>
    <text x="180" y="14" text-anchor="middle" font-family="'Courier New', monospace" font-size="10.5" font-weight="700" fill="#38bdf8">
      NaCl (solid salt) + H2O -&gt; Na+ (aq) + Cl- (aq)
    </text>
  </g>
</svg>"""


# ============================================================================= MATHEMATICS SECTION (Class 1 to 8)
def math_geometry_svg(shape: str, p: dict | None = None, lang: str = "en") -> str:
    """Dynamic 2D/3D geometry shape visualizer with live dimension lines and formulas."""
    p = p or {}
    if shape == "circle":
        r = p.get("r", 5)
        scale = min(110.0 / max(r, 1), 18.0)
        px_r = max(25, int(r * scale))
        cx, cy = 230, 150
        circ = 2 * math.pi * r
        area = math.pi * (r ** 2)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 320" width="460" height="320">
  <defs>
    <radialGradient id="circ-fill" cx="40%" cy="40%" r="70%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </radialGradient>
  </defs>
  <rect width="460" height="320" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <circle cx="{cx}" cy="{cy}" r="{px_r}" fill="url(#circ-fill)" opacity="0.85" stroke="#0369a1" stroke-width="3"/>
  <circle cx="{cx}" cy="{cy}" r="4" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
  <line x1="{cx}" y1="{cy}" x2="{cx + px_r}" y2="{cy}" stroke="#ffffff" stroke-width="2.5" stroke-dasharray="3 2"/>
  <circle cx="{cx + px_r}" cy="{cy}" r="3" fill="#ffffff"/>
  <text x="{cx + px_r / 2}" y="{cy - 8}" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="13" font-weight="700" fill="#ffffff">r = {r:g} cm</text>
  <line x1="{cx - px_r}" y1="{cy + 15}" x2="{cx + px_r}" y2="{cy + 15}" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="{cx}" y="{cy + 30}" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="600" fill="#64748b">d = 2r = {2*r:g} cm</text>
  <g transform="translate(16, 16)">
    <rect width="180" height="28" rx="14" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1"/>
    <text x="90" y="19" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#0369a1">CIRCLE • r = {r:g} cm</text>
  </g>
  <g transform="translate(16, 260)">
    <rect width="200" height="42" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="1.5"/>
    <text x="12" y="18" font-family="'Trebuchet MS', sans-serif" font-size="10" font-weight="700" fill="#64748b">CIRCUMFERENCE (C = 2πr)</text>
    <text x="12" y="34" font-family="'Trebuchet MS', sans-serif" font-size="14" font-weight="800" fill="#0284c7">{circ:.2f} cm</text>
  </g>
  <g transform="translate(244, 260)">
    <rect width="200" height="42" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="1.5"/>
    <text x="12" y="18" font-family="'Trebuchet MS', sans-serif" font-size="10" font-weight="700" fill="#64748b">AREA (A = πr²)</text>
    <text x="12" y="34" font-family="'Trebuchet MS', sans-serif" font-size="14" font-weight="800" fill="#059669">{area:.2f} cm²</text>
  </g>
</svg>"""

    elif shape == "rectangle":
        l = p.get("l", 8)
        w = p.get("w", 5)
        scale = min(240.0 / max(l, 1), 140.0 / max(w, 1), 22.0)
        px_l = max(40, int(l * scale))
        px_w = max(30, int(w * scale))
        x0 = 230 - px_l // 2
        y0 = 145 - px_w // 2
        peri = 2 * (l + w)
        area = l * w
        diag = math.sqrt(l**2 + w**2)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 320" width="460" height="320">
  <defs>
    <linearGradient id="rect-fill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a855f7"/><stop offset="100%" stop-color="#7c3aed"/>
    </linearGradient>
  </defs>
  <rect width="460" height="320" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <rect x="{x0}" y="{y0}" width="{px_l}" height="{px_w}" rx="8" fill="url(#rect-fill)" opacity="0.85" stroke="#6d28d9" stroke-width="3"/>
  <line x1="{x0}" y1="{y0 + px_w}" x2="{x0 + px_l}" y2="{y0}" stroke="#fef08a" stroke-width="2" stroke-dasharray="4 3"/>
  <line x1="{x0}" y1="{y0 - 10}" x2="{x0 + px_l}" y2="{y0 - 10}" stroke="#64748b" stroke-width="1.8"/>
  <text x="{x0 + px_l / 2}" y="{y0 - 16}" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#475569">Length l = {l:g} cm</text>
  <line x1="{x0 + px_l + 10}" y1="{y0}" x2="{x0 + px_l + 10}" y2="{y0 + px_w}" stroke="#64748b" stroke-width="1.8"/>
  <text x="{x0 + px_l + 18}" y="{y0 + px_w / 2 + 4}" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#475569">w = {w:g} cm</text>
  <g transform="translate(16, 16)">
    <rect width="210" height="28" rx="14" fill="#f3e8ff" stroke="#a855f7" stroke-width="1"/>
    <text x="105" y="19" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#7e22ce">RECTANGLE • {l:g} × {w:g} cm</text>
  </g>
  <g transform="translate(16, 260)">
    <rect width="135" height="42" rx="10" fill="#ffffff" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="10" y="16" font-family="'Trebuchet MS', sans-serif" font-size="9.5" font-weight="700" fill="#64748b">PERIMETER 2(l+w)</text>
    <text x="10" y="34" font-family="'Trebuchet MS', sans-serif" font-size="14" font-weight="800" fill="#6d28d9">{peri:g} cm</text>
  </g>
  <g transform="translate(162, 260)">
    <rect width="135" height="42" rx="10" fill="#ffffff" stroke="#059669" stroke-width="1.5"/>
    <text x="10" y="16" font-family="'Trebuchet MS', sans-serif" font-size="9.5" font-weight="700" fill="#64748b">AREA (l × w)</text>
    <text x="10" y="34" font-family="'Trebuchet MS', sans-serif" font-size="14" font-weight="800" fill="#047857">{area:g} cm²</text>
  </g>
  <g transform="translate(308, 260)">
    <rect width="135" height="42" rx="10" fill="#ffffff" stroke="#d97706" stroke-width="1.5"/>
    <text x="10" y="16" font-family="'Trebuchet MS', sans-serif" font-size="9.5" font-weight="700" fill="#64748b">DIAGONAL √(l²+w²)</text>
    <text x="10" y="34" font-family="'Trebuchet MS', sans-serif" font-size="14" font-weight="800" fill="#b45309">{diag:.2f} cm</text>
  </g>
</svg>"""

    elif shape == "cylinder":
        r = p.get("r", 4)
        h = p.get("h", 8)
        csa = 2 * math.pi * r * h
        tsa = 2 * math.pi * r * (r + h)
        vol = math.pi * (r ** 2) * h
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 320" width="460" height="320">
  <defs>
    <linearGradient id="cyl-body" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#059669"/><stop offset="40%" stop-color="#34d399"/><stop offset="80%" stop-color="#10b981"/><stop offset="100%" stop-color="#047857"/>
    </linearGradient>
    <linearGradient id="cyl-top" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6ee7b7"/><stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
  </defs>
  <rect width="460" height="320" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <path d="M170 100 L170 200 C170 216 290 216 290 200 L290 100 Z" fill="url(#cyl-body)" opacity="0.9" stroke="#047857" stroke-width="2.5"/>
  <ellipse cx="230" cy="100" rx="60" ry="16" fill="url(#cyl-top)" stroke="#047857" stroke-width="2.5"/>
  <line x1="230" y1="100" x2="290" y2="100" stroke="#0f172a" stroke-width="2" stroke-dasharray="3 2"/>
  <circle cx="230" cy="100" r="3" fill="#0f172a"/>
  <text x="260" y="93" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="700" fill="#064e3b">r = {r:g} cm</text>
  <line x1="305" y1="100" x2="305" y2="200" stroke="#0284c7" stroke-width="2"/>
  <polyline points="302,106 305,100 308,106" fill="none" stroke="#0284c7" stroke-width="2"/>
  <polyline points="302,194 305,200 308,194" fill="none" stroke="#0284c7" stroke-width="2"/>
  <text x="320" y="154" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#0369a1">h = {h:g} cm</text>
  <g transform="translate(16, 16)">
    <rect width="230" height="28" rx="14" fill="#d1fae5" stroke="#10b981" stroke-width="1"/>
    <text x="115" y="19" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#065f46">3D CYLINDER • r = {r:g}, h = {h:g} cm</text>
  </g>
  <g transform="translate(16, 260)">
    <rect width="135" height="44" rx="10" fill="#ffffff" stroke="#059669" stroke-width="1.5"/>
    <text x="10" y="16" font-family="'Trebuchet MS', sans-serif" font-size="9" font-weight="700" fill="#64748b">CURVED SA (2πrh)</text>
    <text x="10" y="34" font-family="'Trebuchet MS', sans-serif" font-size="13.5" font-weight="800" fill="#047857">{csa:.1f} cm²</text>
  </g>
  <g transform="translate(162, 260)">
    <rect width="135" height="44" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="1.5"/>
    <text x="10" y="16" font-family="'Trebuchet MS', sans-serif" font-size="9" font-weight="700" fill="#64748b">TOTAL SA 2πr(r+h)</text>
    <text x="10" y="34" font-family="'Trebuchet MS', sans-serif" font-size="13.5" font-weight="800" fill="#0284c7">{tsa:.1f} cm²</text>
  </g>
  <g transform="translate(308, 260)">
    <rect width="135" height="44" rx="10" fill="#ffffff" stroke="#d97706" stroke-width="1.5"/>
    <text x="10" y="16" font-family="'Trebuchet MS', sans-serif" font-size="9" font-weight="700" fill="#64748b">VOLUME (πr²h)</text>
    <text x="10" y="34" font-family="'Trebuchet MS', sans-serif" font-size="13.5" font-weight="800" fill="#b45309">{vol:.1f} cm³</text>
  </g>
</svg>"""

    # Triangle
    b = p.get("b", 8)
    h = p.get("h", 6)
    area = 0.5 * b * h
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 320" width="460" height="320">
  <defs>
    <linearGradient id="tri-fill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f59e0b"/><stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
  </defs>
  <rect width="460" height="320" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <polygon points="120,220 340,220 230,80" fill="url(#tri-fill)" opacity="0.85" stroke="#b45309" stroke-width="3"/>
  <line x1="230" y1="80" x2="230" y2="220" stroke="#ffffff" stroke-width="2.5" stroke-dasharray="4 3"/>
  <rect x="230" y="210" width="10" height="10" fill="none" stroke="#ffffff" stroke-width="1.5"/>
  <text x="215" y="155" text-anchor="end" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#ffffff">h = {h:g} cm</text>
  <line x1="120" y1="235" x2="340" y2="235" stroke="#64748b" stroke-width="1.8"/>
  <text x="230" y="250" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#475569">Base b = {b:g} cm</text>
  <g transform="translate(16, 16)">
    <rect width="210" height="28" rx="14" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
    <text x="105" y="19" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#b45309">TRIANGLE • b={b:g}, h={h:g} cm</text>
  </g>
  <g transform="translate(130, 265)">
    <rect width="200" height="42" rx="10" fill="#ffffff" stroke="#d97706" stroke-width="1.5"/>
    <text x="12" y="18" font-family="'Trebuchet MS', sans-serif" font-size="10" font-weight="700" fill="#64748b">TRIANGLE AREA (½ × b × h)</text>
    <text x="12" y="34" font-family="'Trebuchet MS', sans-serif" font-size="14" font-weight="800" fill="#b45309">{area:g} cm²</text>
  </g>
</svg>"""


def pythagoras_svg(a: int = 3, b: int = 4, lang: str = "en") -> str:
    """Pythagoras Theorem visual proof SVG with square areas on all three sides."""
    c_sq = a**2 + b**2
    c = math.sqrt(c_sq)
    is_triplet = (abs(c - round(c)) < 1e-6)
    c_str = f"{int(round(c))}" if is_triplet else f"{c:.2f}"
    
    triplet_badge = ""
    if is_triplet:
        triplet_badge = f"""
        <g transform="translate(140, 282)">
          <rect width="180" height="26" rx="13" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
          <text x="90" y="17" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11.5" font-weight="800" fill="#b45309">⭐ PYTHAGOREAN TRIPLET! ⭐</text>
        </g>
        """
        
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 320" width="460" height="320">
  <defs>
    <linearGradient id="sq-a" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f43f5e"/><stop offset="100%" stop-color="#be123c"/></linearGradient>
    <linearGradient id="sq-b" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#1d4ed8"/></linearGradient>
    <linearGradient id="sq-c" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#10b981"/><stop offset="100%" stop-color="#047857"/></linearGradient>
  </defs>
  <rect width="460" height="320" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <g transform="translate(16, 16)">
    <rect width="260" height="28" rx="14" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1"/>
    <text x="130" y="19" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#6d28d9">PYTHAGORAS THEOREM • a² + b² = c²</text>
  </g>
  <polygon points="150,230 150,120 310,230" fill="#f1f5f9" stroke="#0f172a" stroke-width="3"/>
  <rect x="150" y="215" width="15" height="15" fill="none" stroke="#0f172a" stroke-width="2"/>
  
  <rect x="65" y="120" width="80" height="110" rx="6" fill="url(#sq-a)" opacity="0.9" stroke="#9f1239" stroke-width="2"/>
  <text x="105" y="170" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="13" font-weight="800" fill="#ffffff">a = {a}</text>
  <text x="105" y="190" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="700" fill="#fecdd3">a² = {a**2}</text>
  
  <rect x="150" y="235" width="160" height="42" rx="6" fill="url(#sq-b)" opacity="0.9" stroke="#1e40af" stroke-width="2"/>
  <text x="230" y="258" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="13" font-weight="800" fill="#ffffff">b = {b}  (b² = {b**2})</text>
  
  <g transform="translate(240, 155) rotate(-34)">
    <rect x="-65" y="-18" width="130" height="36" rx="8" fill="url(#sq-c)" stroke="#065f46" stroke-width="2"/>
    <text x="0" y="5" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#ffffff">c = {c_str} (c² = {c_sq})</text>
  </g>
  
  <g transform="translate(325, 45)">
    <rect width="120" height="160" rx="10" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
    <text x="12" y="24" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="800" fill="#475569">CALCULATION:</text>
    <text x="12" y="48" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#be123c">a² = {a}² = {a**2}</text>
    <text x="12" y="70" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="700" fill="#1d4ed8">b² = {b}² = {b**2}</text>
    <line x1="12" y1="80" x2="108" y2="80" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="12" y="100" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#047857">c² = {a**2} + {b**2}</text>
    <text x="12" y="120" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#047857">c² = {c_sq}</text>
    <text x="12" y="145" font-family="'Trebuchet MS', sans-serif" font-size="13" font-weight="900" fill="#0f172a">c = {c_str}</text>
  </g>
  {triplet_badge}
</svg>"""


def fraction_pizza_svg(num: int = 3, den: int = 8, lang: str = "en") -> str:
    """Visual pizza & fraction model connecting fractions to decimals and percentages."""
    den = max(1, den)
    num = min(num, den)
    cx, cy, r = 160, 150, 95
    pct = (num / den) * 100
    dec = num / den
    
    slices_svg = []
    for i in range(den):
        ang1 = 2 * math.pi * i / den - math.pi / 2
        ang2 = 2 * math.pi * (i + 1) / den - math.pi / 2
        x1 = cx + r * math.cos(ang1)
        y1 = cy + r * math.sin(ang1)
        x2 = cx + r * math.cos(ang2)
        y2 = cy + r * math.sin(ang2)
        large_arc = 1 if (ang2 - ang1) > math.pi else 0
        d_path = f"M{cx},{cy} L{x1:.2f},{y1:.2f} A{r},{r} 0 {large_arc},1 {x2:.2f},{y2:.2f} Z"
        
        if i < num:
            mid_ang = (ang1 + ang2) / 2
            px = cx + (r * 0.6) * math.cos(mid_ang)
            py = cy + (r * 0.6) * math.sin(mid_ang)
            slices_svg.append(f"""
            <path d="{d_path}" fill="url(#pizza-cheese)" stroke="#b45309" stroke-width="2"/>
            <circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="#dc2626" stroke="#991b1b" stroke-width="1"/>
            <circle cx="{px+2:.1f}" cy="{py-2:.1f}" r="1.5" fill="#fecaca"/>
            """)
        else:
            slices_svg.append(f"""
            <path d="{d_path}" fill="#f1f5f9" opacity="0.6" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4 2"/>
            """)
            
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 320" width="460" height="320">
  <defs>
    <radialGradient id="pizza-cheese" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#fef08a"/><stop offset="50%" stop-color="#f59e0b"/><stop offset="100%" stop-color="#d97706"/>
    </radialGradient>
  </defs>
  <rect width="460" height="320" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <g transform="translate(16, 16)">
    <rect width="260" height="28" rx="14" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
    <text x="130" y="19" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#b45309">VISUAL FRACTION PIZZA • {num}/{den}</text>
  </g>
  <circle cx="{cx}" cy="{cy}" r="{r+7}" fill="#92400e" stroke="#78350f" stroke-width="2"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="#fffbeb"/>
  {''.join(slices_svg)}
  <circle cx="{cx}" cy="{cy}" r="4" fill="#78350f"/>
  
  <g transform="translate(290, 45)">
    <rect width="155" height="230" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="16" y="28" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="800" fill="#64748b">EQUIVALENT VALUES:</text>
    <rect x="16" y="40" width="123" height="50" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1"/>
    <text x="28" y="58" font-family="'Trebuchet MS', sans-serif" font-size="10" font-weight="700" fill="#2563eb">FRACTION</text>
    <text x="77" y="80" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="20" font-weight="900" fill="#1d4ed8">{num} / {den}</text>
    <rect x="16" y="100" width="123" height="50" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1"/>
    <text x="28" y="118" font-family="'Trebuchet MS', sans-serif" font-size="10" font-weight="700" fill="#059669">PERCENTAGE</text>
    <text x="77" y="140" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="20" font-weight="900" fill="#047857">{pct:.1f}%</text>
    <rect x="16" y="160" width="123" height="50" rx="8" fill="#fdf4ff" stroke="#d946ef" stroke-width="1"/>
    <text x="28" y="178" font-family="'Trebuchet MS', sans-serif" font-size="10" font-weight="700" fill="#a21caf">DECIMAL</text>
    <text x="77" y="200" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="20" font-weight="900" fill="#86198f">{dec:.3f}</text>
  </g>
</svg>"""


def algebra_balance_svg(a: int = 2, b: int = 5, c: int = 15, lang: str = "en") -> str:
    """Interactive visual scale and step-by-step linear equation solver."""
    diff = c - b
    ans = diff / a if a != 0 else 0
    ans_str = f"{int(ans)}" if ans.is_integer() else f"{ans:.2f}"
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 320" width="460" height="320">
  <defs>
    <linearGradient id="metal-beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#94a3b8"/><stop offset="100%" stop-color="#475569"/></linearGradient>
    <linearGradient id="box-x" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#818cf8"/><stop offset="100%" stop-color="#4f46e5"/></linearGradient>
    <linearGradient id="coin-b" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#fbbf24"/><stop offset="100%" stop-color="#d97706"/></linearGradient>
  </defs>
  <rect width="460" height="320" rx="16" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1.5"/>
  <g transform="translate(16, 16)">
    <rect width="250" height="28" rx="14" fill="#ede9fe" stroke="#6366f1" stroke-width="1"/>
    <text x="125" y="19" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#4338ca">EQUATION BALANCE • {a}x + {b} = {c}</text>
  </g>
  <polygon points="230,120 215,160 245,160" fill="#334155" stroke="#1e293b" stroke-width="2"/>
  <rect x="190" y="160" width="80" height="12" rx="4" fill="#1e293b"/>
  <rect x="90" y="116" width="280" height="8" rx="3" fill="url(#metal-beam)"/>
  <circle cx="230" cy="120" r="5" fill="#f8fafc" stroke="#0f172a" stroke-width="2"/>
  
  <line x1="120" y1="122" x2="100" y2="170" stroke="#64748b" stroke-width="1.5"/>
  <line x1="120" y1="122" x2="140" y2="170" stroke="#64748b" stroke-width="1.5"/>
  <path d="M90 170 Q120 185 150 170 Z" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
  <rect x="96" y="142" width="24" height="24" rx="4" fill="url(#box-x)" stroke="#3730a3" stroke-width="1.5"/>
  <text x="108" y="158" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#ffffff">{a}x</text>
  <circle cx="134" cy="154" r="12" fill="url(#coin-b)" stroke="#92400e" stroke-width="1.5"/>
  <text x="134" y="158" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="800" fill="#ffffff">+{b}</text>
  
  <line x1="340" y1="122" x2="320" y2="170" stroke="#64748b" stroke-width="1.5"/>
  <line x1="340" y1="122" x2="360" y2="170" stroke="#64748b" stroke-width="1.5"/>
  <path d="M310 170 Q340 185 370 170 Z" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
  <circle cx="340" cy="154" r="14" fill="url(#coin-b)" stroke="#92400e" stroke-width="1.5"/>
  <text x="340" y="159" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#ffffff">{c}</text>
  
  <g transform="translate(16, 205)">
    <rect width="428" height="95" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="14" y="20" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="800" fill="#475569">STEP-BY-STEP BALANCE SOLVER:</text>
    <text x="14" y="42" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="600" fill="#1e293b">1. Subtract {b} from both pans:  {a}x = {c} - {b}  ➔  <tspan font-weight="800" fill="#d97706">{a}x = {diff}</tspan></text>
    <text x="14" y="65" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="600" fill="#1e293b">2. Divide both pans by {a}:  x = {diff} / {a}  ➔  <tspan font-weight="900" fill="#4f46e5" font-size="14">x = {ans_str}</tspan></text>
    <text x="14" y="86" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="700" fill="#059669">✓ Verification: {a}({ans_str}) + {b} = {a * float(ans) + b:.0f} (Both sides equal {c}!)</text>
  </g>
</svg>"""


def force_svg(lang: str = "en") -> str:
    """Clear, kid-friendly vector diagram of Force & Motion (F = m * a)."""
    is_hi = (lang == "hi")
    title = "FORCE &amp; MOTION • PUSH OR PULL" if not is_hi else "FORCE AUR GATI • DHAKKA YA KHEENCHNA"
    sub = "Sir Isaac Newton's 2nd Law of Motion" if not is_hi else "Sir Isaac Newton Ka Dusra Niyam"
    push_lbl = "Push Force F = 20 N" if not is_hi else "Dhakka (Push) F = 20 N"
    acc_lbl = "Acceleration a = 4 m/s²" if not is_hi else "Gati Badhna a = 4 m/s²"
    fric_lbl = "Friction f = 5 N (resists motion)" if not is_hi else "Gharshan f = 5 N (rokne wali force)"
    weight_lbl = "Weight W = mg" if not is_hi else "Vajan W = mg"
    normal_lbl = "Normal Support N" if not is_hi else "Support Force N"
    summary_1 = "Force can start, stop, speed up, or change the direction of an object." if not is_hi else "Force kisi cheez ko chala sakti hai, rok sakti hai ya disha badal sakti hai."
    summary_2 = "Unit: Newton (N) • 1 Newton = 1 kg × 1 m/s²" if not is_hi else "Unit: Newton (N) • 1 Newton = 1 kg × 1 m/s²"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 340" width="480" height="340">
  <defs>
    <linearGradient id="force-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8fafc"/><stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="box-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#60a5fa"/><stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>
    <linearGradient id="push-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f97316"/><stop offset="100%" stop-color="#ef4444"/>
    </linearGradient>
    <marker id="arrow-push" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,1 L7,4 L0,7 Z" fill="#ef4444"/>
    </marker>
    <marker id="arrow-acc" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,1 L7,4 L0,7 Z" fill="#0284c7"/>
    </marker>
    <marker id="arrow-fric" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,1 L7,4 L0,7 Z" fill="#8b5cf6"/>
    </marker>
    <marker id="arrow-vert" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M0,1 L7,4 L0,7 Z" fill="#10b981"/>
    </marker>
  </defs>

  <rect width="480" height="340" rx="16" fill="url(#force-bg)" stroke="#cbd5e1" stroke-width="1.5"/>

  <!-- Header -->
  <rect x="0" y="0" width="480" height="46" rx="16" fill="#0f172a"/>
  <rect x="0" y="28" width="480" height="18" fill="#0f172a"/>
  <text x="240" y="23" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="13" font-weight="800" fill="#38bdf8" letter-spacing="0.5">{title}</text>
  <text x="240" y="38" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#94a3b8">{sub}</text>

  <!-- Ground surface -->
  <line x1="40" y1="195" x2="440" y2="195" stroke="#475569" stroke-width="3" stroke-linecap="round"/>
  <path d="M60 195 L50 205 M100 195 L90 205 M140 195 L130 205 M180 195 L170 205 M220 195 L210 205 M260 195 L250 205 M300 195 L290 205 M340 195 L330 205 M380 195 L370 205 M420 195 L410 205" stroke="#94a3b8" stroke-width="1.5"/>

  <!-- Block (Mass m = 5 kg) -->
  <rect x="180" y="110" width="85" height="85" rx="8" fill="url(#box-grad)" stroke="#1d4ed8" stroke-width="2"/>
  <text x="222" y="147" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="14" font-weight="800" fill="#ffffff">MASS</text>
  <text x="222" y="167" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="12" font-weight="700" fill="#e0f2fe">m = 5 kg</text>

  <!-- Applied Push Force Arrow (Right) -->
  <line x1="85" y1="152" x2="175" y2="152" stroke="url(#push-grad)" stroke-width="6" marker-end="url(#arrow-push)"/>
  <rect x="70" y="120" width="100" height="22" rx="4" fill="#fee2e2" stroke="#ef4444" stroke-width="1"/>
  <text x="120" y="135" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="10" font-weight="700" fill="#b91c1c">{push_lbl}</text>

  <!-- Acceleration Vector (Above block) -->
  <line x1="222" y1="84" x2="310" y2="84" stroke="#0284c7" stroke-width="4.5" marker-end="url(#arrow-acc)"/>
  <text x="266" y="74" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="11" font-weight="700" fill="#0284c7">{acc_lbl}</text>

  <!-- Friction Arrow (Left opposition) -->
  <line x1="222" y1="200" x2="160" y2="200" stroke="#8b5cf6" stroke-width="4" marker-end="url(#arrow-fric)"/>
  <text x="155" y="217" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#7c3aed">{fric_lbl}</text>

  <!-- Normal Force (Up) & Gravity Weight (Down) -->
  <line x1="222" y1="110" x2="222" y2="60" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrow-vert)"/>
  <text x="232" y="67" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#047857">{normal_lbl}</text>

  <!-- Bottom Explanatory Card -->
  <g transform="translate(18, 235)">
    <rect width="444" height="92" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <rect x="12" y="12" width="135" height="30" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="79" y="32" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="14" font-weight="800" fill="#1d4ed8">F = m × a</text>
    <text x="160" y="24" font-family="'Trebuchet MS', Arial, sans-serif" font-size="11" font-weight="700" fill="#0f172a">{summary_1}</text>
    <text x="160" y="42" font-family="Arial, sans-serif" font-size="10.5" fill="#475569">{summary_2}</text>
    <line x1="16" y1="56" x2="428" y2="56" stroke="#f1f5f9" stroke-width="1"/>
    <text x="16" y="74" font-family="Arial, sans-serif" font-size="10" fill="#64748b">⚽ Kick a ball (push) • 🧲 Magnet pulls iron • 🚗 Car brakes use friction to stop</text>
  </g>
</svg>"""


def blue_sky_svg(lang: str = "en") -> str:
    """Vibrant, educational SVG explaining Rayleigh Scattering (Why the sky is blue)."""
    is_hi = (lang == "hi")
    title = "WHY IS THE SKY BLUE? • RAYLEIGH SCATTERING" if not is_hi else "AASMAN NEELA KYUN HAI? • RAYLEIGH SCATTERING"
    sub = "Sunlight + Earth's Atmosphere = Blue Sky!" if not is_hi else "Suraj Ki Roshni + Atmosphere = Neela Aasman!"
    sun_lbl = "White Sunlight (All Colors)" if not is_hi else "Suraj Ki Roshni (7 Rang)"
    red_lbl = "Red &amp; Yellow waves pass straight through (longer waves)" if not is_hi else "Laal aur peele waves seedhe nikal jaate hain"
    blue_lbl = "Blue waves hit air molecules and scatter everywhere!" if not is_hi else "Blue waves hawa ke kanon se takra kar phailti hain!"
    obs_lbl = "Looking up: We see scattered blue light!" if not is_hi else "Upar dekhne par: Neeli roshni dikhti hai!"
    law_lbl = "Rayleigh's Law: Scattering ∝ 1 / λ⁴ (Blue scatters 10× more than Red)" if not is_hi else "Rayleigh Niyam: Scattering ∝ 1 / λ⁴ (Neela rang 10 guna zyada phailta hai)"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 340" width="480" height="340">
  <defs>
    <linearGradient id="sky-card-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0284c7"/><stop offset="60%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#bae6fd"/>
    </linearGradient>
    <linearGradient id="sun-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fde047"/><stop offset="100%" stop-color="#f59e0b"/>
    </linearGradient>
    <marker id="arrow-blue" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#0284c7"/>
    </marker>
    <marker id="arrow-red" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#ef4444"/>
    </marker>
  </defs>

  <!-- Sky Background -->
  <rect width="480" height="340" rx="16" fill="url(#sky-card-bg)" stroke="#0284c7" stroke-width="1.5"/>

  <!-- Top Dark Header Bar -->
  <rect x="0" y="0" width="480" height="46" rx="16" fill="#0c4a6e"/>
  <rect x="0" y="28" width="480" height="18" fill="#0c4a6e"/>
  <text x="240" y="23" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="13" font-weight="800" fill="#38bdf8" letter-spacing="0.5">{title}</text>
  <text x="240" y="38" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#e0f2fe">{sub}</text>

  <!-- Radiant Sun on Upper Left -->
  <g transform="translate(60, 95)">
    <circle cx="0" cy="0" r="28" fill="url(#sun-grad)"/>
    <circle cx="0" cy="0" r="34" fill="none" stroke="#fef08a" stroke-width="2" stroke-dasharray="4 3" opacity="0.8"/>
    <!-- Sunbeams -->
    <line x1="-38" y1="0" x2="-46" y2="0" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="38" y1="0" x2="46" y2="0" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="0" y1="-38" x2="0" y2="-46" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="0" y1="38" x2="0" y2="46" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="26" y1="26" x2="34" y2="34" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="-26" y1="-26" x2="-34" y2="-34" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
    <text x="0" y="4" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="11" font-weight="800" fill="#78350f">SUN</text>
  </g>
  <text x="60" y="145" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="9.5" font-weight="700" fill="#082f49">{sun_lbl}</text>

  <!-- Atmosphere Zone -->
  <rect x="155" y="60" width="220" height="155" rx="14" fill="#ffffff" fill-opacity="0.35" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4 2"/>
  <text x="265" y="78" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="10" font-weight="800" fill="#0369a1">EARTH'S ATMOSPHERE (Air: N₂ &amp; O₂)</text>

  <!-- Air Molecules (Particles) -->
  <g transform="translate(190, 110)">
    <circle cx="0" cy="0" r="9" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
    <text x="0" y="3" text-anchor="middle" font-size="7" font-weight="800" fill="#fff">N₂</text>
    <line x1="-4" y1="-7" x2="-22" y2="-22" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <line x1="6" y1="-6" x2="24" y2="-20" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <line x1="7" y1="5" x2="22" y2="22" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <line x1="-6" y1="5" x2="-20" y2="20" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
  </g>

  <g transform="translate(290, 125)">
    <circle cx="0" cy="0" r="9" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
    <text x="0" y="3" text-anchor="middle" font-size="7" font-weight="800" fill="#fff">O₂</text>
    <line x1="0" y1="-7" x2="0" y2="-26" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <line x1="7" y1="0" x2="26" y2="0" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <line x1="-7" y1="0" x2="-26" y2="0" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
    <line x1="0" y1="7" x2="0" y2="26" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
  </g>

  <g transform="translate(240, 165)">
    <circle cx="0" cy="0" r="8" fill="#0284c7" stroke="#ffffff" stroke-width="1.5"/>
    <text x="0" y="3" text-anchor="middle" font-size="6.5" font-weight="800" fill="#fff">N₂</text>
    <line x1="5" y1="-5" x2="18" y2="-18" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arrow-blue)"/>
    <line x1="-5" y1="5" x2="-18" y2="18" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arrow-blue)"/>
  </g>

  <!-- Incoming Sunlight Rays -->
  <line x1="95" y1="105" x2="180" y2="110" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
  <line x1="95" y1="112" x2="175" y2="112" stroke="#facc15" stroke-width="2.5"/>

  <!-- Long wavelengths (Red / Orange passing straight) -->
  <path d="M100 120 Q180 125 410 135" fill="none" stroke="#ef4444" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow-red)"/>
  <path d="M100 128 Q180 135 410 148" fill="none" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" marker-end="url(#arrow-red)"/>
  <text x="420" y="142" font-family="'Trebuchet MS', Arial, sans-serif" font-size="9" font-weight="700" fill="#b91c1c">Red light passes through</text>

  <!-- Earth Ground with Student Observer -->
  <path d="M0 220 Q240 205 480 220 L480 340 L0 340 Z" fill="#15803d"/>
  <g transform="translate(420, 212)">
    <circle cx="0" cy="-24" r="7" fill="#fde68a" stroke="#b45309" stroke-width="1"/>
    <line x1="0" y1="-17" x2="0" y2="-2" stroke="#1d4ed8" stroke-width="3"/>
    <line x1="0" y1="-2" x2="-5" y2="12" stroke="#0f172a" stroke-width="2.5"/>
    <line x1="0" y1="-2" x2="5" y2="12" stroke="#0f172a" stroke-width="2.5"/>
    <line x1="-3" y1="-26" x2="-18" y2="-42" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="2 2"/>
  </g>
  <text x="415" y="195" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="8.5" font-weight="700" fill="#ffffff">👦 Kid looking up</text>

  <!-- Informational Callout Box -->
  <g transform="translate(18, 235)">
    <rect width="444" height="92" rx="10" fill="#ffffff" stroke="#bae6fd" stroke-width="1.5"/>
    <text x="16" y="22" font-family="'Trebuchet MS', Arial, sans-serif" font-size="11.5" font-weight="800" fill="#0369a1">{blue_lbl}</text>
    <text x="16" y="40" font-family="Arial, sans-serif" font-size="10" fill="#334155">{red_lbl}</text>
    <text x="16" y="58" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#0284c7">{obs_lbl}</text>
    <rect x="16" y="66" width="412" height="20" rx="4" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1"/>
    <text x="222" y="80" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="9" font-weight="700" fill="#0369a1">{law_lbl}</text>
  </g>
</svg>"""


def gravity_svg(lang: str = "en") -> str:
    """Clear, attractive SVG demonstrating Earth's gravitational pull (w = m * g)."""
    is_hi = (lang == "hi")
    title = "GRAVITY • WHY THINGS FALL DOWN" if not is_hi else "GRAVITY • CHEEZEIN NEECHE KYUN GIRTI HAIN"
    formula = "Weight W = m × g  (g ≈ 9.8 m/s² on Earth)" if not is_hi else "Bhaar W = m × g  (g ≈ 9.8 m/s² Dharti Par)"
    desc = "Earth's mass creates an invisible pulling force toward its center." if not is_hi else "Dharti ka wazan har cheez ko apne center ki taraf kheenchta hai."

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 340" width="480" height="340">
  <defs>
    <linearGradient id="grav-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <linearGradient id="earth-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#38bdf8"/><stop offset="50%" stop-color="#10b981"/><stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
    <marker id="arrow-down" markerWidth="6" markerHeight="6" refX="3" refY="5" orient="auto">
      <path d="M0,0 L3,6 L6,0 Z" fill="#ef4444"/>
    </marker>
  </defs>

  <rect width="480" height="340" rx="16" fill="url(#grav-bg)" stroke="#334155" stroke-width="1.5"/>
  <text x="240" y="32" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="14" font-weight="800" fill="#38bdf8">{title}</text>
  <text x="240" y="50" text-anchor="middle" font-family="Arial, sans-serif" font-size="10.5" fill="#94a3b8">{desc}</text>

  <!-- Falling Ball -->
  <g transform="translate(240, 95)">
    <circle cx="0" cy="0" r="18" fill="#ef4444" stroke="#b91c1c" stroke-width="2"/>
    <text x="0" y="5" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="800" fill="#fff">m = 1 kg</text>
  </g>

  <!-- Gravity vector arrows -->
  <line x1="240" y1="120" x2="240" y2="180" stroke="#ef4444" stroke-width="5" marker-end="url(#arrow-down)"/>
  <rect x="255" y="135" width="130" height="26" rx="6" fill="#fee2e2" stroke="#ef4444" stroke-width="1"/>
  <text x="320" y="152" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="700" fill="#b91c1c">Pull: g = 9.8 m/s² ⬇</text>

  <!-- Curved Earth Horizon -->
  <path d="M-20 220 Q240 180 500 220 L500 340 L-20 340 Z" fill="url(#earth-grad)"/>
  <text x="240" y="245" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="16" font-weight="900" fill="#ffffff" letter-spacing="2">PLANET EARTH</text>

  <!-- Formula banner -->
  <g transform="translate(40, 275)">
    <rect width="400" height="45" rx="10" fill="#ffffff" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="200" y="28" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="13" font-weight="800" fill="#0369a1">{formula}</text>
  </g>
</svg>"""


def friction_svg(lang: str = "en") -> str:
    """Clear, educational SVG showing surface friction and interlocking asperities."""
    is_hi = (lang == "hi")
    title = "FRICTION • SURFACE GRIP &amp; HEAT" if not is_hi else "FRICTION • GHARSHAN AUR GARMI"
    desc = "Microscopic roughness between surfaces resists sliding motion" if not is_hi else "Do satah ke beech chhote khurdure kan gati ko rokte hain"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 340" width="480" height="340">
  <defs>
    <linearGradient id="fric-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f8fafc"/><stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <marker id="fric-push" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#2563eb"/>
    </marker>
    <marker id="fric-opp" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#ef4444"/>
    </marker>
  </defs>

  <rect width="480" height="340" rx="16" fill="url(#fric-bg)" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="240" y="28" text-anchor="middle" font-family="'Trebuchet MS', Arial, sans-serif" font-size="14" font-weight="800" fill="#0f172a">{title}</text>
  <text x="240" y="44" text-anchor="middle" font-family="Arial, sans-serif" font-size="10.5" fill="#64748b">{desc}</text>

  <!-- Top Block moving Right -->
  <rect x="160" y="75" width="160" height="60" rx="6" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
  <text x="240" y="110" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="13" font-weight="700" fill="#ffffff">Moving Block</text>

  <line x1="330" y1="105" x2="410" y2="105" stroke="#2563eb" stroke-width="5" marker-end="url(#fric-push)"/>
  <text x="370" y="95" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="700" fill="#2563eb">Motion ➔</text>

  <line x1="150" y1="145" x2="80" y2="145" stroke="#ef4444" stroke-width="5" marker-end="url(#fric-opp)"/>
  <text x="115" y="135" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="11" font-weight="700" fill="#ef4444">Friction ⬅</text>

  <!-- Microscopic Interlocking Teeth -->
  <path d="M120 135 L130 142 L140 135 L150 142 L160 135 L170 142 L180 135 L190 142 L200 135 L210 142 L220 135 L230 142 L240 135 L250 142 L260 135 L270 142 L280 135 L290 142 L300 135 L310 142 L320 135 L330 142 L340 135 L350 142 L360 135" stroke="#e11d48" stroke-width="2.5" fill="none"/>
  <text x="240" y="160" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#be123c">Microscopic roughness grips and opposes sliding</text>

  <!-- Bottom Floor Surface -->
  <rect x="80" y="170" width="320" height="50" rx="4" fill="#94a3b8" stroke="#64748b" stroke-width="2"/>
  <text x="240" y="200" text-anchor="middle" font-family="'Trebuchet MS', sans-serif" font-size="13" font-weight="700" fill="#ffffff">Floor Surface</text>

  <!-- Explanatory card -->
  <g transform="translate(30, 240)">
    <rect width="420" height="80" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="16" y="24" font-family="'Trebuchet MS', sans-serif" font-size="12" font-weight="800" fill="#0f172a">Formula: Friction f = μ × N</text>
    <text x="16" y="44" font-family="Arial, sans-serif" font-size="10.5" fill="#475569">💡 Walking: Friction prevents shoes from slipping.</text>
    <text x="16" y="62" font-family="Arial, sans-serif" font-size="10.5" fill="#475569">🔥 Heat: Rubbing hands creates warmth because friction turns motion into thermal energy!</text>
  </g>
</svg>"""


# ============================================================================= DISPATCH (used by the chat)
def render_spec(spec: str, lang: str = "en"):
    """Turn a visual spec string into ("svg", str) or ("plotly", Figure). Returns None if unknown."""
    parts = spec.split(":")
    try:
        if parts[0] == "body":
            if len(parts) > 2 and parts[1] == "kidneys" and parts[2] == "detail":
                return "svg", kidney_detail_svg(lang)
            return "svg", body_svg(parts[1], lang)
        if parts[0] == "physics":
            if parts[1] == "ohm":
                return "svg", circuit_svg(6, 3)
            if parts[1] == "force":
                return "svg", force_svg(lang)
            if parts[1] == "sky":
                return "svg", blue_sky_svg(lang)
            if parts[1] == "gravity":
                return "svg", gravity_svg(lang)
            if parts[1] == "friction":
                return "svg", friction_svg(lang)
            return "plotly", {"projectile": projectile_fig, "pendulum": pendulum_fig,
                              "refraction": refraction_fig}[parts[1]]()
        if parts[0] == "chem":
            if parts[1] == "atom":
                return "svg", atom_svg(int(parts[2]))
            if parts[1] == "mol":
                return "plotly", molecule_fig(parts[2])
            if parts[1] == "states":
                return "svg", states_svg(parts[2])
            if parts[1] == "ph":
                en, hi, ph = C.PH_SUBSTANCES[parts[2]]
                return "svg", ph_svg(ph, hi if lang == "hi" else en)
        if parts[0] == "reaction":
            return "svg", reaction_svg(parts[1], lang)
        if parts[0] == "vital":
            return "svg", vital_signs_svg(95, lang)
        if parts[0] == "math":
            if parts[1] == "circle":
                return "svg", math_geometry_svg("circle", {"r": 7}, lang)
            if parts[1] == "rectangle":
                return "svg", math_geometry_svg("rectangle", {"l": 8, "w": 5}, lang)
            if parts[1] == "cylinder":
                return "svg", math_geometry_svg("cylinder", {"r": 4, "h": 8}, lang)
            if parts[1] == "triangle":
                return "svg", math_geometry_svg("triangle", {"b": 8, "h": 6}, lang)
            if parts[1] == "pythagoras":
                return "svg", pythagoras_svg(3, 4, lang)
            if parts[1] == "fractions":
                return "svg", fraction_pizza_svg(3, 8, lang)
            if parts[1] == "algebra":
                return "svg", algebra_balance_svg(2, 5, 15, lang)
    except (KeyError, IndexError, ValueError):
        return None
    return None

