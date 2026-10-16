
from pathlib import Path
import html

import streamlit as st

from config import BANDS, SCORE_MAX, SCORE_MIN


COLORS = {
    "background": "#F6F4EF",
    "surface": "#FFFFFF",
    "primary": "#172C38",
    "text": "#253C42",
    "muted": "#718080",
    "sage": "#B7D8C8",
    "green": "#579A84",
    "lavender": "#A18AC4",
    "peach": "#BE9271",
    "border": "#E5E7E1",
}


def esc(value):
    return html.escape(str(value))


def render(content):
    st.markdown(content, unsafe_allow_html=True)


def inject_css():
    css_path = Path(__file__).parent / "styles.css"

    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )


def brand():
    render("""
        <div class="dusk-brand">
            <div class="dusk-brand-mark">☾</div>
            <div>
                <div class="dusk-brand-name">dusk</div>
                <div class="dusk-brand-caption">
                    YOUR WELLNESS SPACE
                </div>
            </div>
        </div>
    """)


def page_header(title, sub=""):
    render(f"""
        <div class="dusk-page-header">
            <h1>{esc(title)}</h1>
            <p>{esc(sub)}</p>
        </div>
    """)


def card_title(title, hint=""):
    render(f"""
        <div class="dusk-card-heading">
            <h3>{esc(title)}</h3>
            <span>{esc(hint)}</span>
        </div>
    """)


def notice(kind, title, body="", items=None):
    allowed = {"info", "success", "warning", "gentle"}
    kind = kind if kind in allowed else "info"

    list_html = ""

    if items:
        list_html = "<ul>" + "".join(
            f"<li>{esc(item)}</li>" for item in items
        ) + "</ul>"

    render(f"""
        <div class="dusk-notice dusk-notice-{kind}">
            <div class="dusk-notice-title">{esc(title)}</div>
            <div class="dusk-notice-body">{esc(body)}</div>
            {list_html}
        </div>
    """)


def stat_tile(label, value, sub=""):
    render(f"""
        <div class="dusk-stat-tile">
            <div class="dusk-stat-label">{esc(label)}</div>
            <div class="dusk-stat-value">{esc(value)}</div>
            <div class="dusk-stat-sub">{esc(sub)}</div>
        </div>
    """)


def chips(items):
    content = "".join(
        f'<span class="dusk-chip">{esc(item)}</span>'
        for item in items
    )
    render(f'<div class="dusk-chips">{content}</div>')


def band_for(score):
    selected = BANDS[0]

    for band in BANDS:
        if score >= band[0]:
            selected = band

    return {
        "key": selected[1],
        "label": selected[2],
        "text": selected[3],
    }



def score_dial(score, uid="score"):
    score = float(score)

    st.container(border=True)
    with st.container(border=True):

        st.subheader("Your Mental Wellbeing Score")

        st.metric(
            label="Predicted score",
            value=f"{score:.1f} / 10",
        )

        st.progress(max(0.0, min(score / 10, 1.0)))

        st.caption(
            "An ML-based estimate, not a clinical diagnosis."
        )


def day_ring(sleep, study, activity, screen):
    import streamlit as st

    routine = [
        ("Sleep", sleep, "#7185B8"),
        ("Study", study, "#BE9271"),
        ("Movement", activity, "#579A84"),
        ("Screen time", screen, "#A18AC4"),
    ]

    with st.container(border=True):
        st.subheader("Your Daily Rhythm")
        st.caption("A quick look at how you spend your day.")

        for label, value, color in routine:
            col1, col2, col3 = st.columns([0.4, 3, 1])

            with col1:
                st.markdown(
                    f"<span style='color:{color};font-size:24px'>●</span>",
                    unsafe_allow_html=True,
                )

            with col2:
                st.write(label)

            with col3:
                st.write(f"{value} h")
