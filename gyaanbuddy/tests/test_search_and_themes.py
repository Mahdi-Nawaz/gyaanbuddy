import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app
import visuals as V


def test_theme_definitions_and_css():
    expected_themes = [
        "🌈 Wonder Academy (Nursery - Class 8)",
        "🌌 Cosmic Explorer",
        "☀️ Sunny Playground",
        "🌿 Emerald Bio-Lab",
        "⚡ Cyber Scientist",
        "🦄 Sunset Wonder",
    ]
    for name in expected_themes:
        assert name in app.THEMES
        theme = app.THEMES[name]
        for key in ["app_bg", "text_color", "sidebar_bg", "hero_bg", "accent", "card_bg"]:
            assert key in theme and theme[key]


def test_search_index_comprehensive():
    index = app.build_search_index()
    assert len(index) >= 50
    specs = [item["spec"] for item in index if item["spec"] != "quiz"]
    # Verify that all specs render without crashing
    for spec in specs[:15]:
        out = V.render_spec(spec, "en")
        assert out is not None


@pytest.mark.parametrize("query,expected_keyword", [
    ("heart", "heart"),
    ("dil", "heart"),
    ("lungs", "lungs"),
    ("fefde", "lungs"),
    ("pendulum", "pendulum"),
    ("circuit", "circuit"),
    ("acid", "acid"),
    ("volcano", "volcano"),
    ("water", "water"),
    ("oxygen", "oxygen"),
])
def test_search_topic_queries(query, expected_keyword):
    results = app.search_topics(query)
    assert len(results) > 0
    blobs = [" ".join([r["title_en"], r["title_hi"], r["spec"]] + r["keywords"]).lower() for r in results]
    assert any(expected_keyword in b for b in blobs)


def test_empty_search_returns_empty():
    assert app.search_topics("") == []
    assert app.search_topics("   ") == []


def test_apptest_with_search_and_theme():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(Path(__file__).resolve().parent.parent / "app.py"), default_timeout=120).run()
    assert not at.exception
    
    # Check that language radio is still at index 0
    assert at.sidebar.radio[0].label == "Language / Bhasha"
    
    # Check class filter exists in sidebar
    class_filter = [sl for sl in at.sidebar.select_slider if "Class" in sl.label]
    assert len(class_filter) == 1
    
    # Change class
    class_filter[0].set_value("8").run()
    assert not at.exception
    assert at.session_state["class_level"] == "8"
