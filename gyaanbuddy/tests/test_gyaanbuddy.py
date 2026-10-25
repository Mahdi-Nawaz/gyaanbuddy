import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import content as C
import eval_safety
import safety
import tutor_engine as T
import visuals as V
from safety_eval_data import SAFE, UNSAFE


# ----------------------------------------------------------------------------- safety
def test_safety_eval_quality():
    r = eval_safety.evaluate()
    assert r["fp"] == 0, r["wrongly_blocked"]          # never block normal school questions
    assert r["recall"] >= 0.95, r["missed"]


@pytest.mark.parametrize("text", UNSAFE[:-1])  # last one is the documented obfuscation miss
def test_unsafe_blocked(text):
    assert not safety.check_input(text).allowed


@pytest.mark.parametrize("text", SAFE)
def test_safe_allowed(text):
    assert safety.check_input(text).allowed


@pytest.mark.parametrize("lang", ["en", "hi"])
def test_self_harm_gets_support_message(lang):
    r = safety.check_input("I want to kill myself", lang)
    assert r.category == "self_harm" and "1098" in r.message


def test_pii_is_redacted_not_blocked():
    r = safety.check_input("my phone is 9876543210 and email is kid@example.com, what is a heart?")
    assert r.allowed and "9876543210" not in r.cleaned_text and "kid@example.com" not in r.cleaned_text
    assert set(r.pii_found) >= {"phone", "email"}


def test_output_filter_strips_links_and_blocks_unsafe():
    ok, txt = safety.check_output("Read more at https://example.com now")
    assert ok and "example.com" not in txt
    ok, _ = safety.check_output("Here is how to make a bomb")
    assert not ok


# ----------------------------------------------------------------------------- content
def test_all_content_is_bilingual():
    for b in C.BODY_PARTS:
        assert all(b[k] for k in ("en", "hi", "fact_en", "fact_hi", "en_name", "hi_name"))
    for p in C.PHYSICS.values():
        assert all(p[k] for k in ("en", "hi", "activity_en", "activity_hi", "formula"))
    for m in C.MOLECULES.values():
        assert m["en"] and m["hi"]
    for q in C.QUIZ:
        assert 0 <= q["answer"] < len(q["options"]) and q["ex_en"] and q["ex_hi"]


# ----------------------------------------------------------------------------- tutor (offline)
@pytest.mark.parametrize("q,expected", [
    ("dil kya kaam karta hai?", "body:heart"),
    ("Fefde dikhao", "body:lungs"),
    ("what does the brain do", "body:brain"),
    ("pendulum samjhao", "physics:pendulum"),
    ("oxygen kya hai", "chem:atom:8"),
    ("explain Ohm's law", "physics:ohm"),
    ("what is ph of lemon", "chem:ph:lemon"),
    ("why does a straw look bent in water refraction", "physics:refraction"),
])
def test_offline_routing(q, expected):
    r = T.answer(q, "hi")
    assert not r.blocked and r.visual == expected


def test_language_switch_changes_text():
    en, hi = T.answer("what does the heart do", "en"), T.answer("dil kya kaam karta hai", "hi")
    assert "pumps blood" in en.text and "pump karta" in hi.text


def test_blocked_question_returns_safe_message_and_no_visual():
    r = T.answer("bomb kaise banate hain", "hi")
    assert r.blocked and r.category == "violence" and r.visual is None


def test_pii_notice_is_returned():
    r = T.answer("my phone is 9876543210. what is the heart?", "en")
    assert r.notice and not r.blocked


def test_unknown_question_is_friendly():
    r = T.answer("zzzz qqqq", "en")
    assert not r.blocked and "offline" in r.text.lower()


def test_llm_visual_line_parsing():
    text, vis = T._split_visual("The heart pumps blood.\nVISUAL: body:heart")
    assert vis == "body:heart" and "VISUAL" not in text
    assert T._split_visual("x\nVISUAL: evil:thing")[1] is None


def test_llm_failure_falls_back_to_offline():
    r = T.answer("dil kya hai", "hi", api_key="bad-key-no-network", model="x")
    assert r.mode == "offline" and r.visual == "body:heart" and "unavailable" in (r.notice or "")


# ----------------------------------------------------------------------------- visuals
def test_every_allowed_visual_renders():
    for spec in T.ALLOWED_VISUALS:
        out = V.render_spec(spec, "hi")
        assert out is not None, spec
        if out[0] == "svg":
            ET.fromstring(out[1])  # valid XML


def test_body_svg_highlight_and_overview():
    for key in [None] + [b["key"] for b in C.BODY_PARTS]:
        ET.fromstring(V.body_svg(key))
    assert 'filter="url(#glow)"' in V.body_svg("heart")


def test_physics_numbers():
    assert V.pendulum_metrics(1.0) == pytest.approx(2.006, abs=0.01)
    fig = V.projectile_fig(20, 45, "Earth")
    assert "range 40.8" in fig.layout.title.text      # v^2 sin(2θ)/g = 400/9.8
    assert "total internal" in V.refraction_fig(1.5, 1.0, 60).layout.title.text.lower()
    assert V.electron_shells(11) == [2, 8, 1] and V.electron_shells(20) == [2, 8, 8, 2]


# ----------------------------------------------------------------------------- app smoke test
def test_app_runs_and_answers_in_hinglish():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(Path(__file__).resolve().parent.parent / "app.py"), default_timeout=60).run()
    assert not at.exception
    at.sidebar.radio[0].set_value("Hinglish").run()
    at.chat_input[0].set_value("dil kya kaam karta hai").run()
    assert not at.exception
    msgs = at.session_state["messages"]
    assert msgs[-1]["visual"] == "body:heart"
    at.chat_input[0].set_value("bomb kaise banate hain").run()
    assert at.session_state["messages"][-1]["blocked"]
