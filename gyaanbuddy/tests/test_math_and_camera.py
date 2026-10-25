import sys
from pathlib import Path
import pytest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app
import visuals as V
import tutor_engine as T
import content as C


def test_math_topics_in_content():
    assert hasattr(C, "MATH_TOPICS")
    expected_keys = ["circle", "rectangle", "triangle", "cylinder", "pythagoras", "fractions", "algebra"]
    for k in expected_keys:
        assert k in C.MATH_TOPICS
        item = C.MATH_TOPICS[k]
        assert "title_en" in item and "formula" in item and "keywords" in item


def test_math_visuals_xml_validity():
    specs = [
        "math:circle",
        "math:rectangle",
        "math:cylinder",
        "math:triangle",
        "math:pythagoras",
        "math:fractions",
        "math:algebra"
    ]
    for spec in specs:
        out = V.render_spec(spec, "en")
        assert out is not None and out[0] == "svg"
        ET.fromstring(out[1])

        out_hi = V.render_spec(spec, "hi")
        assert out_hi is not None and out_hi[0] == "svg"
        ET.fromstring(out_hi[1])


def test_pythagoras_triplet_detection():
    # 3, 4, 5 is a triplet
    svg_triplet = V.pythagoras_svg(3, 4)
    assert "PYTHAGOREAN TRIPLET" in svg_triplet
    ET.fromstring(svg_triplet)

    # 5, 12, 13 is a triplet
    svg_13 = V.pythagoras_svg(5, 12)
    assert "PYTHAGOREAN TRIPLET" in svg_13
    ET.fromstring(svg_13)

    # 3, 5, sqrt(34) is not a triplet
    svg_non = V.pythagoras_svg(3, 5)
    assert "PYTHAGOREAN TRIPLET" not in svg_non
    ET.fromstring(svg_non)


def test_fractions_pizza_and_conversions():
    svg_frac = V.fraction_pizza_svg(3, 8)
    assert "3 / 8" in svg_frac
    assert "37.5%" in svg_frac
    assert "0.375" in svg_frac
    ET.fromstring(svg_frac)


def test_algebra_balance_solver():
    svg_alg = V.algebra_balance_svg(2, 5, 15)
    # 2x + 5 = 15 -> x = 5
    assert "x = 5" in svg_alg
    ET.fromstring(svg_alg)


def test_math_offline_tutor_answers():
    r1 = T.answer("area of circle", "en")
    assert r1.visual == "math:circle"
    assert "C = 2πr" in r1.text or "circle" in r1.text.lower()

    r2 = T.answer("pythagoras theorem kya hai", "hi")
    assert r2.visual == "math:pythagoras"

    r3 = T.answer("solve linear equation", "en")
    assert r3.visual == "math:algebra"


def test_subject_search_matches():
    results = app.search_topics("pythagoras")
    assert len(results) > 0
    assert any("pythagoras" in r["spec"] for r in results)

    results_cyl = app.search_topics("cylinder")
    assert len(results_cyl) > 0
    assert any("cylinder" in r["spec"] for r in results_cyl)

    results_kd = app.search_topics("kidney")
    assert len(results_kd) > 0
    assert any("kidney" in r["spec"] for r in results_kd)


def test_apptest_maths_and_camera():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(Path(__file__).resolve().parent.parent / "app.py"), default_timeout=60).run()
    assert not at.exception

    tabs = app.TXT["en"]["tabs"]
    assert "📐 Mathematics" in tabs
    assert "💬 Ask Buddy" in tabs

    # Check file_uploader present in Ask Buddy snap & solve
    uploaders = [u for u in at.file_uploader]
    assert len(uploaders) >= 1
