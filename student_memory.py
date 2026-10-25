"""Persistent Student Learning Profile and Chat Memory for GyaanBuddy.

Saves conversation history to train future models and dynamically adapts
the tutor engine so it knows the exact level, strengths, and learning pace of each student.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent / "data"
PROFILE_FILE = DATA_DIR / "student_profile.json"
CHAT_LOG_FILE = DATA_DIR / "chat_history.jsonl"
TRAINING_FILE = DATA_DIR / "training_dataset.jsonl"


def _ensure_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_student_profile() -> dict[str, Any]:
    """Load persistent student profile or return defaults."""
    _ensure_dir()
    if PROFILE_FILE.exists():
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    default_profile: dict[str, Any] = {
        "student_grade": "Class 4",
        "assessed_level": "Class 4 • Curious Explorer",
        "total_chats": 0,
        "total_xp": 0,
        "topics_mastered": [],
        "topics_practicing": [],
        "subject_breakdown": {
            "Physics": 0,
            "Math": 0,
            "Biology": 0,
            "Chemistry": 0,
            "General": 0
        },
        "recent_chats": [],
        "last_active": datetime.now().isoformat()
    }
    save_student_profile(default_profile)
    return default_profile


def save_student_profile(profile: dict[str, Any]) -> None:
    """Save student profile to persistent JSON."""
    _ensure_dir()
    profile["last_active"] = datetime.now().isoformat()
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)


def assess_student_level(grade: str, total_chats: int, topics_mastered: list[str]) -> str:
    """Dynamically determine student level based on activity and grade."""
    count = total_chats
    if count >= 30 or len(topics_mastered) >= 5:
        tier = "Advanced Scholar 🏆"
    elif count >= 10 or len(topics_mastered) >= 2:
        tier = "Active Explorer 🌟"
    elif count >= 3:
        tier = "Rising Learner 🚀"
    else:
        tier = "Beginner Explorer 🌱"
    return f"{grade} • {tier}"


def record_student_chat(
    grade: str,
    lang: str,
    question: str,
    answer_text: str,
    subject: str = "General",
    topic: str = "General",
    xp: int = 10,
    visual: str | None = None
) -> dict[str, Any]:
    """Save interaction to chat log, dataset for model training, and update student profile."""
    _ensure_dir()
    ts = datetime.now().isoformat()

    entry = {
        "timestamp": ts,
        "grade": grade,
        "lang": lang,
        "question": question.strip(),
        "answer": answer_text.strip(),
        "subject": subject,
        "topic": topic,
        "visual": visual,
        "xp": xp
    }

    # 1. Append to chat history
    with open(CHAT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 2. Append to fine-tuning training dataset in ChatML / OpenAI conversational JSONL format
    system_prompt = (
        f"You are GyaanBuddy, an AI tutor for school students in India. "
        f"Target Level: {grade}. Language: {'English' if lang == 'en' else 'Hinglish'}. "
        f"Subject: {subject}. Topic: {topic}."
    )
    training_sample = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question.strip()},
            {"role": "assistant", "content": answer_text.strip()}
        ],
        "metadata": {
            "grade": grade,
            "subject": subject,
            "topic": topic,
            "timestamp": ts
        }
    }
    with open(TRAINING_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(training_sample, ensure_ascii=False) + "\n")

    # 3. Update student learning profile
    profile = load_student_profile()
    profile["student_grade"] = grade
    profile["total_chats"] = profile.get("total_chats", 0) + 1
    profile["total_xp"] = profile.get("total_xp", 0) + xp

    # Track subject counts
    sb = profile.setdefault("subject_breakdown", {})
    subj_key = subject if subject in sb else "General"
    sb[subj_key] = sb.get(subj_key, 0) + 1

    # Track topics
    mastered = profile.setdefault("topics_mastered", [])
    practicing = profile.setdefault("topics_practicing", [])

    topic_label = f"{subject}: {topic}" if topic != "General" else subject
    if topic_label not in practicing and topic_label not in mastered:
        practicing.append(topic_label)
    elif topic_label in practicing and topic_label not in mastered:
        # If studied again, elevate to mastered
        practicing.remove(topic_label)
        mastered.append(topic_label)

    profile["assessed_level"] = assess_student_level(grade, profile["total_chats"], mastered)

    # Keep last 10 chats in profile summary
    recent = profile.setdefault("recent_chats", [])
    recent.insert(0, {"q": question[:80], "topic": topic_label, "ts": ts})
    profile["recent_chats"] = recent[:10]

    save_student_profile(profile)
    return profile


def get_student_context_prompt() -> str:
    """Generate adaptive context to inject into LLM system prompt so it knows the student's level."""
    profile = load_student_profile()
    grade = profile.get("student_grade", "Class 4")
    level = profile.get("assessed_level", "Class 4")
    mastered = profile.get("topics_mastered", [])
    practicing = profile.get("topics_practicing", [])

    parts = [
        f"STUDENT PROFILE & ASSESSED LEVEL: {level}",
        f"Target Grade Curriculum: {grade}",
    ]
    if mastered:
        parts.append(f"Mastered Topics: {', '.join(mastered[-4:])}")
    if practicing:
        parts.append(f"Currently Learning / Needs Support: {', '.join(practicing[-4:])}")

    parts.append(
        "ADAPTIVE INSTRUCTION: Calibrate vocabulary and pacing to this student's exact grade and level. "
        "Reference concepts they mastered when introducing new topics, and give encouraging positive feedback!"
    )
    return "\n".join(parts)


def get_training_dataset_bytes() -> bytes:
    """Return raw bytes of training dataset for download."""
    _ensure_dir()
    if TRAINING_FILE.exists():
        with open(TRAINING_FILE, "rb") as f:
            return f.read()
    return b""


def reset_student_profile() -> None:
    """Reset learning profile and logs."""
    _ensure_dir()
    if PROFILE_FILE.exists():
        PROFILE_FILE.unlink()
    load_student_profile()
