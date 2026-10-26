"""Tutor brain: safety check -> (LLM or offline lessons) -> output check.

Visual specs are short strings the UI knows how to draw, e.g. "body:heart", "physics:projectile",
"chem:atom:8", "chem:mol:H2O", "chem:states:gas", "chem:ph:lemon".
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass

import content as C
import safety

DEFAULT_MODEL = os.getenv("GYAAN_MODEL", "claude-sonnet-5-5")

MATH_VISUALS = [
    "math:circle", "math:rectangle", "math:cylinder", "math:triangle",
    "math:pythagoras", "math:fractions", "math:algebra",
    "math:count", "math:shapes", "math:addition"
]

NATURE_VISUALS = [
    "nature:tree", "nature:plant", "nature:photosynthesis", "nature:butterfly", "nature:foodchain",
    "nature:animals", "nature:seed", "nature:water_cycle"
]

ALLOWED_VISUALS = (
    [f"body:{b['key']}" for b in C.BODY_PARTS] + ["body:kidneys:detail"] + [f"physics:{k}" for k in C.PHYSICS]
    + [f"chem:mol:{k}" for k in C.MOLECULES] + [f"chem:states:{k}" for k in C.STATES]
    + [f"chem:ph:{k}" for k in C.PH_SUBSTANCES] + [f"chem:atom:{z}" for z in C.ELEMENT_BY_Z]
    + ["chem:metals"]
    + MATH_VISUALS
    + NATURE_VISUALS
)

AGE_GUIDE = {
    "Nursery - KG": "ultra simple words, playful analogies, lots of friendly emojis, 1-2 short sentences",
    "Class 1 - 2": "very simple words, 1-2 short sentences per idea, fun everyday comparisons",
    "Class 3 - 5": "simple words with a little scientific vocabulary, clear everyday examples",
    "Class 6 - 8": "clear explanations with proper science terms, concepts and formulas",
    "6-8": "very simple words, 1-2 short sentences per idea, fun comparisons",
    "9-12": "simple words with a little scientific vocabulary, clear examples",
    "13-15": "clear explanations with proper science terms and a formula when useful",
}

SYSTEM_PROMPT = """You are GyaanBuddy, a friendly, patient tutor for children aged {age} in India.
Topics: school science (human body, physics, chemistry), maths basics and general learning.
Language: {lang_rule}
Style: {style}. Maximum 120 words. Use one everyday analogy and one or two emojis. End with one tiny question that checks understanding.
Safety rules: never ask for or repeat personal information; never give instructions for anything dangerous
(weapons, drugs, harmful chemical mixing); for experiments only suggest safe ones that need an adult; do not include web links;
if asked something unsuitable for a child, kindly redirect to a learning topic.
Visuals: if one of these diagrams would help, add a final line exactly like `VISUAL: <key>` using only a key from this list:
{visuals}
"""

LANG_RULE = {
    "en": "Reply in simple English.",
    "hi": "Reply in Hinglish: Hindi written in English (Roman) letters, the way a friendly Indian teacher talks, "
          "mixing common English science words. Do not use Devanagari script.",
}


@dataclass
class TutorReply:
    text: str
    visual: str | None = None
    blocked: bool = False
    category: str | None = None
    mode: str = "offline"          # "llm" or "offline"
    subject: str = "General"
    topic: str = ""
    notice: str | None = None      # e.g. PII warning or "LLM unavailable"


# ----------------------------------------------------------------------------- offline lessons
def _tokens(text: str) -> set[str]:
    return set(safety.normalize(text).split())


def _build_lessons() -> list[dict]:
    lessons = []
    for b in C.BODY_PARTS:
        lessons.append(dict(key=b["key"], subject="Human body", topic=b["en_name"], visual=f"body:{b['key']}",
                            en=f"{b['en']}\n\n💡 Fun fact: {b['fact_en']}",
                            hi=f"{b['hi']}\n\n💡 Fun fact: {b['fact_hi']}", keywords=set(b["keywords"])))
    for k, p in C.PHYSICS.items():
        lessons.append(dict(key=k, subject="Physics", topic=p["title_en"], visual=f"physics:{k}",
                            en=f"{p['en']}\n\n📐 Formula: {p['formula']}", hi=f"{p['hi']}\n\n📐 Formula: {p['formula']}",
                            keywords=set(p["keywords"])))
    for k, c in C.CHEM_TEXT.items():
        vis = {"atom": "chem:atom:8", "molecule": "chem:mol:H2O", "states": "chem:states:liquid", "ph": "chem:ph:lemon", "metals": "chem:metals"}[k]
        lessons.append(dict(key=k, subject="Chemistry", topic=c["title_en"], visual=vis,
                            en=c["en"], hi=c["hi"], keywords=set(c["keywords"])))
    for k, m in C.MOLECULES.items():
        lessons.append(dict(key=f"mol_{k}", subject="Chemistry", topic=m["name_en"], visual=f"chem:mol:{k}",
                            en=f"{m['name_en']} ({m['formula']}): {m['en']}", hi=f"{m['name_hi']} ({m['formula']}): {m['hi']}",
                            keywords={m["name_en"].lower(), m["formula"].lower(), k.lower()} | set(m["name_en"].lower().split())))
    if hasattr(C, "MATH_TOPICS"):
        for k, m in C.MATH_TOPICS.items():
            lessons.append(dict(key=f"math_{k}", subject="Mathematics", topic=m["title_en"], visual=f"math:{k}",
                                en=f"{m['en']}\n\n📐 Formula: {m['formula']}", hi=f"{m['hi']}\n\n📐 Formula: {m['formula']}",
                                keywords=set(m["keywords"])))
    if hasattr(C, "NATURE_TOPICS"):
        vis_map = {
            "tree_parts": "nature:tree",
            "photosynthesis": "nature:photosynthesis",
            "butterfly_lifecycle": "nature:butterfly",
            "frog_lifecycle": "nature:butterfly",
            "animal_diets": "nature:foodchain",
            "food_chain": "nature:foodchain",
            "cute_animals": "nature:animals:dog",
            "seed_growth": "nature:seed:3",
            "water_cycle": "nature:water_cycle",
        }
        for k, n in C.NATURE_TOPICS.items():
            lessons.append(dict(key=f"nature_{k}", subject="General Science", topic=n["title_en"],
                                visual=vis_map.get(k, "nature:tree"),
                                en=f"{n['en']}\n\n🌿 {n['formula']}",
                                hi=f"{n['hi']}\n\n🌿 {n['formula']}",
                                keywords=set(n["keywords"])))
    return lessons


LESSONS = _build_lessons()
# Remove the very generic words that would match too many lessons on their own
_STOP = {"what", "is", "the", "a", "an", "of", "kya", "hai", "hota", "hoti", "ka", "ki", "ke", "me", "mein", "how", "why",
         "kaise", "kyun", "kyu", "does", "do", "samjhao", "batao", "dikhao", "show", "me", "explain", "tell", "about"}


def _element_lesson(query: str, lang: str) -> TutorReply | None:
    toks = _tokens(query)
    for z, sym, name, n in C.ELEMENTS:
        if name.lower() in toks or (len(sym) > 1 and sym.lower() in toks) or name.lower().rstrip("m") in toks:
            use = C.ELEMENT_USE.get(z)
            use_txt = ""
            if use:
                use_txt = f" It is {use[0]}." if lang == "en" else f" Yeh {use[1]}."
            if lang == "en":
                txt = (f"{name} ({sym}) has {z} proton{'s' if z > 1 else ''}, {n} neutron{'s' if n != 1 else ''} and "
                       f"{z} electron{'s' if z > 1 else ''}.{use_txt}")
            else:
                txt = (f"{name} ({sym}) mein {z} proton, {n} neutron aur {z} electron hote hain.{use_txt}")
            return TutorReply(txt, f"chem:atom:{z}", subject="Chemistry", topic=f"Element: {name}")
    return None


def find_lesson(query: str, lang: str) -> TutorReply | None:
    el = _element_lesson(query, lang)
    if el:
        return el

    norm_query = safety.normalize(query).lower()
    raw_toks = _tokens(query) - _STOP

    # Generate stemmed forms (e.g., "newtons" -> "newton", "laws" -> "law", "lungs" -> "lung")
    expanded_toks = set(raw_toks)
    for t in raw_toks:
        if t.endswith("s") and len(t) > 3:
            expanded_toks.add(t[:-1])
        if t.endswith("es") and len(t) > 4:
            expanded_toks.add(t[:-2])
        if t.endswith("ing") and len(t) > 5:
            expanded_toks.add(t[:-3])

    best, score = None, 0
    for les in LESSONS:
        s = 0
        topic_lower = les["topic"].lower()
        key_lower = les["key"].lower()

        # Direct topic match in query string
        if re.search(r'\b' + re.escape(topic_lower) + r'\b', norm_query) or re.search(r'\b' + re.escape(key_lower) + r'\b', norm_query):
            s += 8

        matched_tokens = set()
        for kw in les["keywords"]:
            kw_clean = safety.normalize(kw).lower()
            if not kw_clean:
                continue
            # Phrase match with word boundaries: "laws of motion", "newtons 2nd law", "ohms law", "ph", etc.
            if re.search(r'\b' + re.escape(kw_clean) + r'\b', norm_query):
                s += 8 + len(kw_clean.split()) * 3
            # Collect matching tokens without multiple counting
            kw_tokens = set(kw_clean.split())
            matched_tokens |= (kw_tokens & expanded_toks)

        # Award score based on unique matching tokens
        s += len(matched_tokens) * 4

        if s > score:
            best, score = les, s

    if best is None or score < 2:
        return None
    return TutorReply(best[lang], best["visual"], subject=best["subject"], topic=best["topic"])


def offline_answer(question: str, lang: str) -> TutorReply:
    toks = _tokens(question)
    if toks and toks <= C.GREETINGS | {"buddy", "gyaanbuddy", "hai", "hello", "hi"}:
        txt = ("Hello! 👋 I'm GyaanBuddy, your friendly science and math buddy. Ask me about the human body, physics, chemistry, or math!"
               if lang == "en" else
               "Namaste! 👋 Main GyaanBuddy hoon, aapka vigyan aur ganit saathi. Mujhse human body, physics, chemistry ya maths ke sawaal poochhein!")
        return TutorReply(txt, topic="Greeting")
    found = find_lesson(question, lang)
    if found:
        return found
    txt = ("I am currently in offline mode for school science and math topics for Nursery to Class 8! 🌟\n\n"
           "Here are great topics you can explore:\n"
           "• 🧍 **Human Body**: Brain & lobes, Heart & blood, Lungs, Kidneys, Bones\n"
           "• ⚡ **Physics**: Newton's Laws (F=m×a), Gravity, Light refraction, Electric circuits, Pendulums\n"
           "• 📐 **Maths**: Pythagoras theorem, Circles & area, Fractions, Algebra\n"
           "• 🧪 **Chemistry**: Oxygen atom structure, Water molecule (H₂O), Acid & pH, States of matter\n\n"
           "💡 Try asking one of the quick suggestions above or search any topic in the Search Bar!"
           if lang == "en" else
           "Main abhi offline mode mein hoon aur Nursery se Class 8 ke vigyan aur ganit ke vishayon par madad karta hoon! 🌟\n\n"
           "Yeh mazedaar topics try karein:\n"
           "• 🧍 **Insaani Sharir**: Dimaag, Dil, Fefde, Gurde, Haddiyan\n"
           "• ⚡ **Physics**: Newton ke Niyam (F=m×a), Gravity, Light, Bijli circuit, Pendulum\n"
           "• 📐 **Ganit**: Pythagoras Pramey, Circle ka area, Fractions, Algebra\n"
           "• 🧪 **Chemistry**: Oxygen Parmanu, Paani (H₂O), Acid aur pH, Padarth ki awasthayein\n\n"
           "💡 Upar diye gaye quick suggestions dabayein ya Search Bar mein koi bhi topic khojein!")
    return TutorReply(txt, topic="Unknown")


# ----------------------------------------------------------------------------- LLM path
def _split_visual(text: str) -> tuple[str, str | None]:
    m = re.search(r"^\s*VISUAL:\s*([\w:.\-]+)\s*$", text, re.M)
    visual = m.group(1) if m else None
    cleaned = re.sub(r"^\s*VISUAL:.*$", "", text, flags=re.M).strip()
    return cleaned, visual if visual in ALLOWED_VISUALS else None


def _llm_answer(question: str, lang: str, age: str, history: list[dict], api_key: str, model: str) -> TutorReply:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    system = SYSTEM_PROMPT.format(age=age, lang_rule=LANG_RULE[lang], style=AGE_GUIDE.get(age, AGE_GUIDE["9-12"]),
                                  visuals=", ".join(ALLOWED_VISUALS))
    try:
        import student_memory
        system = system + "\n\n" + student_memory.get_student_context_prompt()
    except Exception:
        pass

    msgs = []
    for h in history[-6:]:
        msgs += [{"role": "user", "content": h["q"]}, {"role": "assistant", "content": h["a"]}]
    msgs.append({"role": "user", "content": question})
    resp = client.messages.create(model=model, max_tokens=500, system=system, messages=msgs)
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    text, visual = _split_visual(text)
    lesson = find_lesson(question, lang)  # only used for labelling subject/topic in the parent dashboard
    return TutorReply(text, visual or (lesson.visual if lesson else None), mode="llm",
                      subject=lesson.subject if lesson else "General", topic=lesson.topic if lesson else "Other")


def answer(question: str, lang: str = "en", age: str = "9-12", history: list[dict] | None = None,
           api_key: str | None = None, model: str = DEFAULT_MODEL) -> TutorReply:
    lang = "hi" if lang == "hi" else "en"
    check = safety.check_input(question, lang)
    if not check.allowed:
        return TutorReply(check.message, blocked=True, category=check.category, topic=f"blocked:{check.category}")
    q = check.cleaned_text
    notice = check.message  # PII warning, if any
    reply = None
    if api_key:
        try:
            reply = _llm_answer(q, lang, age, history or [], api_key, model)
        except Exception as e:  # noqa: BLE001 - never leave the child with an error screen
            notice = (notice + " " if notice else "") + f"(AI helper unavailable: {type(e).__name__}. Using built-in lessons.)"
    if reply is None:
        reply = offline_answer(q, lang)
    ok, safe_text = safety.check_output(reply.text, lang)
    if not ok:
        return TutorReply(safe_text, blocked=True, category="output_filter", topic="blocked:output")
    reply.text, reply.notice = safe_text, notice
    return reply

