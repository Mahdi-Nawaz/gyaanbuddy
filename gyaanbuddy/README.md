# 🧠 GyaanBuddy: Kid-Safe AI Science & Maths Tutor (Class 1 to 8)

> **"Built with pride by Mahdi Nawaz"**  
> An interactive, bilingual AI learning companion that transforms science and mathematics into an enjoyable, magical adventure for school students aged 6–14 (Classes 1 to 8).

[![Tests](https://img.shields.io/badge/tests-123%20passed-brightgreen.svg)](https://pytest.org)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.50%2B-FF4B4B.svg)](https://streamlit.io)
[![Author](https://img.shields.io/badge/author-Mahdi%20Nawaz-orange.svg)](#-author--creator)

---

## 🌟 What Makes GyaanBuddy Magical?

GyaanBuddy bridges the gap between textbook theory and real-world understanding using **rich interactive SVGs, hands-on physics simulations, virtual chemistry reactions, visual algebra scales, fraction pizzas, and multimodal camera question-solving** in both **English and Hinglish**.

---

## 🚀 Key Feature Labs (7 Interactive Hubs)

| Lab | What Students Can Do | Curriculum Focus |
|---|---|---|
| **💬 Ask Buddy & 📸 Snap & Solve** | • Ask anything in English or Hinglish with instant audio readout (`gTTS`).<br>• **📸 Snap & Solve Camera:** Photograph any textbook or notebook question using phone/laptop webcam or upload an image.<br>• **Multimodal AI Vision:** Reads handwritten or printed questions with step-by-step guidance.<br>• 6 instant offline problem presets. | Class 1–8 Problem Solving |
| **🧍 Human Body Anatomy** | • 8 anatomically detailed organs (Brain, Lungs, Heart, Stomach, Liver, Kidneys, Intestines, Skeleton).<br>• Realistic kidney cross-section with cortex, medulla pyramids, and renal pelvis.<br>• **Interactive Vital Signs Monitor:** Live ECG, heart rate, and respiration rate with activity slider (Resting to Sprinting). | Class 3–8 Biology |
| **⚡ Physics Lab** | • **Interactive Circuit:** Real-time switch controlling a glowing Edison lightbulb, battery, and ammeter.<br>• **Light & Optics Prism:** Dynamic white light dispersion into 7 rainbow colors (VIBGYOR).<br>• **Projectile Motion:** Interactive target practice game on Earth, Moon, and Mars.<br>• **Pendulum Simulation:** Live periodic oscillation calculations. | Class 6–8 Physics |
| **🧪 Chemistry Lab** | • **Interactive Atom Builder:** Elements 1 to 20 with electron shells & periodic table card.<br>• **Virtual Reaction Chamber:** Safe simulations of Vinegar + Baking Soda volcano, Red Cabbage pH shift, and Salt dissolution.<br>• **Interactive pH Rainbow Scale:** Real-time acid/base indicator dipping test.<br>• Safe kitchen science experiments. | Class 6–8 Chemistry |
| **📐 Mathematics Lab** | • **2D Geometry:** Interactive Circle, Rectangle, and Triangle with real-time area, perimeter, and diagonal calculations.<br>• **🥫 3D Mensuration:** Isometric Cylinder with live Curved Surface Area ($2\pi rh$), Total Surface Area, and Volume.<br>• **📐 Pythagoras Theorem:** Dynamic right-angled triangle with square area visualizers ($a^2, b^2, c^2$) and automatic **Pythagorean Triplet detector**.<br>• **🍕 Fraction Pizza:** Interactive pizza slices (cheese & pepperoni) with live 3-way conversion (**Fraction $\leftrightarrow$ Percentage $\leftrightarrow$ Decimal**).<br>• **⚖️ Algebra Balance Scale:** Visual two-pan mechanical scale for linear equations ($ax + b = c$).<br>• **⚡ Speed Math Arena:** 3-tier gamified math quiz with confetti celebrations. | Class 1–8 Mathematics |
| **🎯 Quiz Arena** | • 15+ bilingual questions with instant explanations, audio readout, streak multiplier, and confetti balloons celebration (+25 XP per win). | All Subjects |
| **👨‍👩‍👧 Parent & Awards** | • Real-time parent analytics (topics explored, accuracy, safety logs, CSV export).<br>• **Official Printable & Downloadable "Certificate of Excellence"** customized with the student's name, rank, XP, and signed by **Mahdi Nawaz**. | Parent Dashboard |

---

## 🔍 Dedicated Search in Every Subject

Every subject tab features its own dedicated search bar and quick-access topic chips:
- **🧍 Human Body Search:** `Heart`, `Lungs`, `Brain`, `Kidney`, `Stomach`, `Skeleton`.
- **⚡ Physics Search:** `Circuit`, `Prism`, `Pendulum`, `Gravity`, `Reflection`.
- **🧪 Chemistry Search:** `pH Scale`, `Reaction`, `Vinegar & Baking Soda`, `Atom`.
- **📐 Mathematics Search:** `Pythagoras`, `Circle`, `Fractions`, `Algebra`, `Cylinder`.
- **💬 Universal Search:** Search across 70+ topics at once with instant preview cards and diagram popups.

---

## 🎨 4 Curated Visual Themes

Personalize the entire learning experience with curated color palettes from the sidebar:
1. 🌌 **Cosmic Explorer** (Default Deep Indigo & Nebula Violet)
2. ☀️ **Sunny Playground** (Bright Emerald & Friendly Sky Blue)
3. ⚡ **Neon Cyberpunk** (High-Contrast Electric Cyan, Fuchsia & Black)
4. 🦄 **Sunset Wonder** (Warm Tangerine, Rose Gold & Purple Sunset)

---

## 🛡️ Child-Safety Architecture

1. **Strict Input Filter:** Blocks inappropriate themes, violence, weapons, substances, hate speech, and jailbreak attempts in English and Hinglish (handles leetspeak like `b0mb`).
2. **Supportive Care for Self-Harm:** Supportive, empathetic guidance providing Childline India helpline **1098**.
3. **PII Masking:** Automatic redaction of phone numbers, emails, Aadhaar-like IDs, and physical addresses before processing.
4. **Output Verification:** Responses are scanned to strip external links or unsafe instructions.
5. **Offline Fallback Guarantee:** Full functionality without any API key required through the built-in offline lesson engine.

---

## 📲 Mobile & Phone Compatibility

GyaanBuddy is fully responsive and works on smartphones and tablets:
1. Connect your phone to the **same Wi-Fi** as your computer.
2. In your phone's browser (Safari / Chrome), open:
   ```
   http://<YOUR-COMPUTER-IP>:8501
   ```
3. Use the phone's **rear camera** in **Snap & Solve** to photograph textbook questions directly.

---

## 💻 Local Installation & Setup

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/gyaanbuddy.git
cd gyaanbuddy

# 2. Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS / Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

### Run Automated Tests
```bash
pytest tests/
# 123 tests passing with 100% success rate!
```

---

## 📁 Repository Structure

```
gyaanbuddy/
├── .gitignore                   # Clean ignore rules for Python/Streamlit
├── README.md                    # Comprehensive documentation & guide
├── requirements.txt             # Project dependencies
├── app.py                       # Main Streamlit application & 7 interactive labs
├── content.py                   # Bilingual curriculum database (Science & Maths)
├── visuals.py                   # Responsive SVG visualizers & Plotly physics engines
├── tutor_engine.py              # Offline intelligent tutor & LLM bridge
├── safety.py                    # Child safety guardrails & PII redaction
├── safety_eval_data.py          # Benchmark test suite for safety filters
├── eval_safety.py               # Safety evaluation runner
└── tests/
    ├── test_gyaanbuddy.py       # Core unit tests (101 tests)
    ├── test_search_and_themes.py# Search indexing & UI themes tests (14 tests)
    └── test_math_and_camera.py  # Mathematics lab & Snap & Solve tests (8 tests)
```

---

## 👨‍💻 Author & Creator

Created and developed with ❤️ for young scientists and curious minds by **Mahdi Nawaz**.
