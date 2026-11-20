import streamlit as st
from datetime import datetime
from pathlib import Path

from src.pipeline.pipeline import run_research_pipeline

st.set_page_config(
    page_title="Research Studio",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Apple-inspired visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap');

:root {
    --ink: #202124;
    --muted: #777b82;
    --line: #e8e9eb;
    --paper: #ffffff;
    --canvas: #f6f6f4;
    --accent: #2864dc;
    --soft-blue: #edf3ff;
}
html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--ink) !important;
}
.stApp { background: var(--canvas); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.1rem; padding-bottom: 4rem; max-width: 1380px; }
section[data-testid="stSidebar"] {
    background: #fbfbfa;
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] > div { padding-top: 1.8rem; }
.brand {
    font-size: 1.05rem; font-weight: 700; letter-spacing: -0.04em;
    display:flex; align-items:center; gap:.55rem; margin-bottom:2rem;
}
.brand-mark {
    width:28px;height:28px;border-radius:9px;background:#202124;color:#ffffff;
    display:inline-flex;align-items:center;justify-content:center;font-size:15px;
}
.eyebrow {
    color: var(--muted); font-size:.72rem; text-transform:uppercase;
    letter-spacing:.13em; font-weight:700;
}
.hero-title {
    font-family:'Newsreader', Georgia, serif; font-size:3.15rem;
    letter-spacing:-.045em; line-height:1.05; margin:.45rem 0 .65rem;
}
.hero-sub { color:var(--muted); font-size:1rem; max-width:650px; line-height:1.65; }
.panel {
    background:var(--paper); border:1px solid var(--line); border-radius:18px;
    padding:1.25rem 1.35rem; box-shadow:0 5px 24px rgba(20,25,35,.025);
    color:var(--ink);
}
.panel-title { font-size:1rem; font-weight:700; letter-spacing:-.02em; }
.panel-note { color:var(--muted); font-size:.83rem; margin-top:.2rem; }
.stage {
    display:flex; align-items:center; gap:.8rem; padding:.8rem 0;
    border-bottom:1px solid #f0f0f0;
}
.stage:last-child { border-bottom:0; }
.stage-num {
    width:30px;height:30px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;background:#f1f2f4;color:#666;font-size:.78rem;font-weight:700;
}
.stage-name { font-weight:600; font-size:.9rem; }
.stage-desc { color:var(--muted); font-size:.77rem; margin-top:2px; }
div.stButton > button[kind="primary"] {
    background:#202124; border:1px solid #202124; border-radius:999px;
    color:#ffffff !important; padding:.62rem 1.2rem; font-weight:600; min-height:2.8rem;
}
div.stButton > button[kind="primary"]:hover { background:#3a3b3e; border-color:#3a3b3e; }
div.stButton > button {
    border-radius:999px; border-color:#dedfe2; color:var(--ink) !important; font-weight:600;
}
.stTextArea textarea, .stTextInput input {
    border-radius:13px !important; border-color:#dedfe2 !important;
    background:var(--paper) !important; color:var(--ink) !important;
}
div[data-testid="stTabs"] button { font-weight:600; }
div[data-testid="stMetric"] {
    background:var(--paper); border:1px solid var(--line); border-radius:14px; padding:1rem;
    color:var(--ink);
}
.paper {
    background:var(--paper); border:1px solid var(--line); border-radius:18px;
    color:var(--ink); padding:2rem 2.2rem; line-height:1.8; white-space:pre-wrap;
}
div[data-testid="stAlert"] { border-radius:14px; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

def init_state():
    defaults = {
        "research_result": None,
        "research_topic": "",
        "history": [],
        "run_timestamp": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">✳</span> Research Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Workspace</div>', unsafe_allow_html=True)
    if st.button("＋  New research", use_container_width=True):
        st.session_state.research_result = None
        st.session_state.research_topic = ""
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Recent research</div>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.caption("Your completed research sessions will appear here.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history[-8:])):
            label = item["topic"]
            if len(label) > 34:
                label = label[:31] + "..."
            if st.button("▤  " + label, key=f"history_{idx}", use_container_width=True):
                st.session_state.research_result = item["result"]
                st.session_state.research_topic = item["topic"]
                st.session_state.run_timestamp = item["timestamp"]
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">About</div>', unsafe_allow_html=True)
    st.caption("A focused workspace for discovering sources, reading evidence, drafting papers and reviewing research quality.")

# ---------- Header ----------
st.markdown('<div class="eyebrow">Your research workspace</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Think deeper.<br>Research better.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Turn a research question into a sourced draft with a four-stage AI workflow. '
    'Follow each step, inspect the evidence, and review the final paper.</div>',
    unsafe_allow_html=True,
)

st.write("")

# ---------- Research input ----------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">What are you researching?</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-note">Be specific. A focused question usually produces stronger research.</div>', unsafe_allow_html=True)

topic = st.text_area(
    "Research topic",
    value=st.session_state.research_topic or "The impact of AI on human cognitive abilities",
    height=105,
    label_visibility="collapsed",
    placeholder="e.g. How does generative AI affect critical thinking and learning outcomes?",
)
col_a, col_b = st.columns([1, 5])
with col_a:
    run_clicked = st.button("Start research  →", type="primary", use_container_width=True)
with col_b:
    st.caption("The workflow runs search → source reading → paper writing → critical review.")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Pipeline execution ----------
if run_clicked:
    clean_topic = topic.strip()
    if not clean_topic:
        st.warning("Enter a research topic before starting.")
    else:
        st.session_state.research_topic = clean_topic
        st.session_state.research_result = None

        st.write("")
        st.markdown("### Research progress")
        progress = st.progress(0, text="Preparing your research workspace...")
        status_box = st.status("Research pipeline started", expanded=True)
        stage_order = {
            "search": (15, "Searching for reliable information"),
            "reader": (40, "Reading and extracting source material"),
            "writer": (68, "Drafting the research paper"),
            "critic": (88, "Reviewing the paper"),
            "complete": (100, "Research complete"),
        }

        def on_stage(stage, message):
            percent, label = stage_order.get(stage, (5, message))
            progress.progress(percent, text=label)
            status_box.write(message)
            if stage == "complete":
                status_box.update(label="Research complete", state="complete", expanded=False)

        try:
            with st.spinner("Your agents are working through the research..."):
                result = run_research_pipeline(clean_topic, progress_callback=on_stage)
            st.session_state.research_result = result
            st.session_state.run_timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
            st.session_state.history.append({
                "topic": clean_topic,
                "result": result,
                "timestamp": st.session_state.run_timestamp,
            })
            progress.progress(100, text="All four stages completed")
            status_box.update(label="Research complete", state="complete", expanded=False)
            st.success("Your research draft and critique are ready.")
        except Exception as exc:
            status_box.update(label="Research stopped", state="error", expanded=True)
            st.error(f"The research pipeline failed: {exc}")
            st.info("Check your terminal for the full traceback and verify your API key and tool configuration.")

# ---------- Results ----------
result = st.session_state.research_result
if result:
    st.write("")
    st.markdown("## Research report")
    st.caption(f"{st.session_state.research_topic}  ·  {st.session_state.run_timestamp or 'Completed'}")

    paper = result.get("paper", "No paper was returned.")
    critique = result.get("critique", "No critique was returned.")
    search_data = result.get("search_result", "No search results were returned.")
    scraped_data = result.get("scraped_result", "No scraped content was returned.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Workflow stages", "4 / 4")
    m2.metric("Search results", "Collected" if search_data else "Unavailable")
    m3.metric("Source reading", "Complete" if scraped_data else "Unavailable")
    m4.metric("Review", "Complete" if critique else "Unavailable")

    tab_paper, tab_sources, tab_critique = st.tabs(["✦  Research paper", "⌕  Sources & evidence", "◎  Critic review"])

    with tab_paper:
        left, right = st.columns([5, 1])
        with left:
            st.markdown("#### Generated draft")
            st.caption("Review and edit the draft before treating it as a finished academic paper.")
        with right:
            st.download_button(
                "Download .txt",
                data=f"# {st.session_state.research_topic}\n\n{paper}\n\n---\n\nCRITIQUE\n\n{critique}",
                file_name="research_report.txt",
                mime="text/plain",
                use_container_width=True,
            )
        edited_paper = st.text_area(
            "Research paper",
            value=paper,
            height=620,
            label_visibility="collapsed",
            key="paper_editor",
        )
        st.caption("Edits in this field are local to this session. They do not change the original pipeline output.")

    with tab_sources:
        st.markdown("#### Search findings")
        st.markdown('<div class="panel-note">The search agent output, as returned by your current tool.</div>', unsafe_allow_html=True)
        with st.expander("View search results", expanded=True):
            st.text(search_data)
        st.markdown("#### Extracted source material")
        with st.expander("View scraped content", expanded=True):
            st.text(scraped_data)

    with tab_critique:
        st.markdown("#### Critic's assessment")
        st.caption("Feedback generated by the critic chain. Use it to guide another revision.")
        st.markdown('<div class="paper">', unsafe_allow_html=True)
        st.write(critique)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.write("")
    st.markdown("### Your workflow")
    c1, c2, c3, c4 = st.columns(4)
    stages = [
        ("01", "Discover", "Search Agent", "Finds recent information and candidate sources."),
        ("02", "Understand", "Reader Agent", "Selects a relevant URL and extracts useful content."),
        ("03", "Compose", "Writer Chain", "Creates a structured research paper from the gathered information."),
        ("04", "Evaluate", "Critic Chain", "Reviews clarity, methodology, evidence and contribution."),
    ]
    for col, (num, title, agent, desc) in zip([c1, c2, c3, c4], stages):
        with col:
            st.markdown(f"""
            <div class="panel" style="min-height:190px">
                <div class="eyebrow">{num} / 04</div>
                <div style="font-size:1.15rem;font-weight:700;margin:.7rem 0 .25rem">{title}</div>
                <div style="font-size:.82rem;font-weight:600;color:#555">{agent}</div>
                <div style="font-size:.8rem;color:#777;line-height:1.55;margin-top:.65rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.info("Start a research run above. Your paper, source material and critic feedback will appear here.")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Research Studio · AI-generated research requires source verification and human academic review.")
