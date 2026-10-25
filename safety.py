"""Child-safety layer for GyaanBuddy: works on English, Hinglish (Roman Hindi) and a little Devanagari.

Pipeline:  input check (unsafe topics, jailbreaks, personal info)  ->  LLM / lessons  ->  output check.

This is a rule-based filter, deliberately transparent and testable. It is a first line of defence,
not a guarantee; see README for limitations and how it is evaluated (safety_eval_data.py).
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})


def normalize(text: str) -> str:
    """Lowercase, squash repeated letters ('killlll' -> 'kill'), drop punctuation."""
    t = unicodedata.normalize("NFKC", text).lower()
    t = re.sub(r"(.)\1{2,}", r"\1\1", t)
    t = re.sub(r"[^a-z0-9ऀ-ॿ\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ----------------------------------------------------------------------------- patterns
_MAKE = r"(?:make|making|build|create|prepare|banate|banata|banane|banana|banao|bnate|bnana|banaye|bana)"
_WEAPON = r"(?:bomb|bam|explosives?|grenade|gun|pistol|bandook|hathiyar|weapons?|poison|zeher)"
_DRUGS = (r"(?:weed|ganja|cocaine|heroin|meth|drugs?|charas|afeem|opium|cigarettes?|cigars?|beer|whisky|"
          r"whiskey|vodka|sharab|daru|nasha|vape|vaping)")
_ACT = r"(?:make|buy|get|try|sell|smoke|drink|banate|banana|banao|kharide|kharidna|piye|pite|pina|peena|piyu)"
_GROUPS = (r"(?:muslims?|hindus?|christians?|sikhs?|jews?|dalits?|blacks?|whites?|girls|boys|women|"
           r"indians|pakistanis)")

PATTERNS: dict[str, list[str]] = {
    "self_harm": [
        r"\b(?:kill myself|end my life|want to die|wanna die|suicide|suicidal|hurt myself|cut myself|"
        r"khudkushi|khudkhushi)\b",
        r"\bkhud ko (?:maar|khatam|hurt|nuksan)",
        r"\b(?:marna|mar jana|mar jaun|mar jau)\b.{0,12}\b(?:chahta|chahti|hai|hoon|hun)\b",
        r"\bjeena nahi (?:chahta|chahti)\b",
        r"(?:खुदकुशी|आत्महत्या|मरना चाहता|मरना चाहती)",
    ],
    "violence": [
        rf"\b{_MAKE}\b.{{0,25}}\b{_WEAPON}\b",
        rf"\b{_WEAPON}\b.{{0,25}}\b(?:kaise|how)\b.{{0,15}}\b{_MAKE}\b",
        r"\b(?:kill|murder|stab|shoot|strangle|hurt|beat up|poison)\s+(?:someone|somebody|a person|people|him|her|"
        r"them|my (?:teacher|friend|brother|sister|mom|mother|dad|father|classmate|parents))\b",
        r"\b(?:maar|maro)\s*(?:dalo|dalna|daalo|do|dena)\b",
        r"\b(?:katl|qatl|khoon)\b.{0,15}\b(?:kaise|karna|kare|karo)\b",
        r"\bkisi ko (?:maar|marna|jaan se)\b",
        r"(?:बम (?:कैसे )?बना|मार डालो)",
    ],
    "sexual": [
        r"\b(?:porn|porno|pornography|nudes?|xxx|sexy video|sex video|sex chat|chudai|randi|nanga|nangi)\b",
        r"\bnaked (?:photo|photos|pic|pics|girl|boy|woman|man|video|videos)\b",
    ],
    "drugs": [
        rf"\b{_ACT}\b.{{0,25}}\b{_DRUGS}\b",
        rf"\b{_DRUGS}\b.{{0,25}}\b(?:kaise|how to)\b.{{0,15}}\b{_ACT}\b",
    ],
    "hate": [
        rf"\b{_GROUPS}\b.{{0,15}}\b(?:are|hain|hai)\b.{{0,12}}\b(?:dirty|stupid|bad|inferior|evil|gande|ganda|"
        r"bure|buri|bewakoof|worthless)\b",
        rf"\bi hate (?:all )?(?:the )?{_GROUPS}\b",
        rf"\bkill all {_GROUPS}\b",
    ],
    "jailbreak": [
        r"\bignore (?:all |your |the )?(?:previous|above|prior|earlier) (?:instructions|rules|prompts?)\b",
        r"\bpretend (?:you are|to be|you re) (?:not|an? unrestricted|evil|dan)\b",
        r"\byou are (?:now )?dan\b",
        r"\b(?:jailbreak|developer mode|do anything now)\b",
        r"\bbypass (?:the |your )?(?:filter|filters|safety|rules)\b",
        r"\bpichle (?:rules|instructions|niyam) bhool\b",
        r"\bfilter (?:band|off|hata)\b",
    ],
}

# order matters: most serious first
CATEGORY_ORDER = ["self_harm", "violence", "sexual", "drugs", "hate", "jailbreak"]
_COMPILED = {c: [re.compile(p) for p in PATTERNS[c]] for c in CATEGORY_ORDER}

PII_PATTERNS = {
    "phone": re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "aadhaar_like": re.compile(r"(?<!\d)\d{4}\s\d{4}\s\d{4}(?!\d)"),
    "address": re.compile(r"\b(?:my|mera|meri)\s+(?:home\s+|ghar\s+ka\s+)?(?:address|pata)\b[^.?!\n]*", re.I),
}
_URL = re.compile(r"https?://\S+|www\.\S+", re.I)

MESSAGES = {
    "violence": {
        "en": "I can't help with things that could hurt people. 🙅 Let's explore something amazing instead, "
              "like how the heart pumps blood or how a rocket flies!",
        "hi": "Main aise topics mein help nahi kar sakta jisse kisi ko nuksaan ho. 🙅 Chalo kuch mazedaar "
              "seekhte hain, jaise dil khoon kaise pump karta hai ya rocket kaise udta hai!",
    },
    "sexual": {
        "en": "That's not something I can talk about. 🙈 If you have questions, please ask a parent or teacher. "
              "Want to learn about the human body parts instead?",
        "hi": "Is baare mein main baat nahi kar sakta. 🙈 Agar koi sawaal hai toh mummy-papa ya teacher se poochho. "
              "Chalo insaani sharir ke parts seekhte hain?",
    },
    "drugs": {
        "en": "I can't help with that. Things like this can be very harmful for kids. 🚫 Please talk to a parent or "
              "teacher. Let's learn how a healthy body works instead!",
        "hi": "Isme main help nahi kar sakta. Aisi cheezein bachon ke liye bahut nuksaandeh hoti hain. 🚫 "
              "Mummy-papa ya teacher se baat karo. Chalo seekhte hain ki healthy sharir kaise kaam karta hai!",
    },
    "hate": {
        "en": "Everyone deserves respect, no matter who they are. 💛 I can't say unkind things about people. "
              "Want to learn something new instead?",
        "hi": "Har insaan ki izzat honi chahiye, chahe woh kaun bhi ho. 💛 Main kisi ke baare mein bura nahi bol "
              "sakta. Chalo kuch naya seekhte hain?",
    },
    "jailbreak": {
        "en": "I'm GyaanBuddy and I always follow my safety rules. 😊 Let's learn something cool together!",
        "hi": "Main GyaanBuddy hoon aur hamesha apne safety rules follow karta hoon. 😊 Chalo saath mein kuch cool "
              "seekhte hain!",
    },
    "self_harm": {
        "en": "I'm really sorry you're feeling this way. 💙 You matter a lot. Please tell a trusted grown-up right "
              "now, like a parent, teacher or relative. In India you can call Childline on 1098 (free, 24x7) "
              "to talk to someone who cares.",
        "hi": "Mujhe bahut afsos hai ki tum aisa mehsoos kar rahe ho. 💙 Tum bahut important ho. Abhi kisi bharose "
              "ke bade ko batao, jaise mummy-papa, teacher ya rishtedar. India mein tum Childline 1098 par call "
              "kar sakte ho (free, 24x7), wahan koi tumhari baat sunega.",
    },
}
PII_NOTE = {
    "en": "🔒 Please don't share private details like phone numbers, emails or home address. I've hidden them.",
    "hi": "🔒 Phone number, email ya ghar ka pata jaisi private baatein share mat karo. Maine unhe hide kar diya hai.",
}
OUTPUT_FALLBACK = {
    "en": "Oops, I can't share that answer. Let's try a different question! 😊",
    "hi": "Oops, main yeh answer share nahi kar sakta. Chalo koi doosra sawaal poochho! 😊",
}


@dataclass
class SafetyResult:
    allowed: bool
    category: str | None = None
    message: str | None = None
    cleaned_text: str = ""
    pii_found: list[str] = field(default_factory=list)


def _match_category(text: str) -> str | None:
    norm = normalize(text)
    variants = {norm, norm.translate(_LEET)}
    for cat in CATEGORY_ORDER:
        for rx in _COMPILED[cat]:
            if any(rx.search(v) for v in variants):
                return cat
    return None


def redact_pii(text: str) -> tuple[str, list[str]]:
    found = []
    for name, rx in PII_PATTERNS.items():
        if rx.search(text):
            found.append(name)
            text = rx.sub("[private info removed]", text)
    return text, found


def check_input(text: str, lang: str = "en") -> SafetyResult:
    """Return whether a child's message may be answered, plus a cleaned version of it."""
    lang = "hi" if lang == "hi" else "en"
    cat = _match_category(text)
    if cat:
        return SafetyResult(False, cat, MESSAGES[cat][lang], "")
    cleaned, pii = redact_pii(text)
    return SafetyResult(True, None, PII_NOTE[lang] if pii else None, cleaned.strip(), pii)


def check_output(text: str, lang: str = "en") -> tuple[bool, str]:
    """Scan a model reply before showing it. Strips links; replaces unsafe replies with a fallback."""
    lang = "hi" if lang == "hi" else "en"
    cat = _match_category(text)
    if cat in {"violence", "sexual", "drugs", "hate"}:
        return False, OUTPUT_FALLBACK[lang]
    cleaned, _ = redact_pii(text)
    cleaned = _URL.sub("[link removed]", cleaned)
    return True, cleaned
