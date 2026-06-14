import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os

# Try to find Groq key from environment or local .env file
def get_default_api_key():
    key = os.environ.get("GROQ_API_KEY", "")
    if not key and os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GROQ_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except:
            pass
    return key

default_key = get_default_api_key()

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="DebateBot",
    page_icon="⚖️",
    layout="wide"
)

# ── Custom Styling ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.title-container {
    text-align: center;
    padding: 20px 0px;
}

.title-gradient {
    background: linear-gradient(135deg, #FF3B30 0%, #34C759 50%, #007AFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.2rem !important;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    color: #8E8E93;
    font-size: 1.1rem;
    margin-bottom: 25px;
}

/* ── Section Cards ────────────────────────────── */
.section-card {
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(128, 128, 128, 0.15);
}

.for-section {
    background: linear-gradient(135deg, rgba(52, 199, 89, 0.08) 0%, rgba(52, 199, 89, 0.02) 100%);
    border-left: 5px solid #34C759;
}

.against-section {
    background: linear-gradient(135deg, rgba(255, 59, 48, 0.08) 0%, rgba(255, 59, 48, 0.02) 100%);
    border-left: 5px solid #FF3B30;
}

.judge-section {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.08) 0%, rgba(255, 215, 0, 0.02) 100%);
    border: 1px solid rgba(255, 215, 0, 0.2);
    border-left: 5px solid #FFD700;
    padding: 32px;
    border-radius: 16px;
    margin-top: 10px;
}

/* ── Argument Cards inside sections ───────────── */
.arg-card {
    background: rgba(128, 128, 128, 0.06);
    border: 1px solid rgba(128, 128, 128, 0.15);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.arg-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.arg-number {
    display: inline-block;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    text-align: center;
    line-height: 28px;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 10px;
    flex-shrink: 0;
}

.for-num { background: #34C759; color: #fff; }
.against-num { background: #FF3B30; color: #fff; }

.arg-claim {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 8px;
    line-height: 1.4;
}

.arg-detail {
    font-size: 0.92rem;
    opacity: 0.85;
    line-height: 1.6;
}

.arg-label {
    font-weight: 600;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    opacity: 0.6;
    margin-top: 8px;
    margin-bottom: 3px;
}

/* ── Score Badge ──────────────────────────────── */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #000;
    font-weight: 800;
    font-size: 1.4rem;
    padding: 8px 20px;
    border-radius: 30px;
    margin: 10px 0;
}

/* ── Comparison Header ────────────────────────── */
.vs-badge {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    padding: 10px;
    opacity: 0.4;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown('<div class="title-container"><h1 class="title-gradient">⚖️ DebateBot</h1><p class="subtitle">Multi-Agent AI Reasoning System · Powered by Llama 3.1 & 3.3 (Groq)</p></div>', unsafe_allow_html=True)
st.divider()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "Groq API Key",
        value=default_key,
        type="password",
        help="Get a free key at console.groq.com — no credit card required!"
    )
    
    model_name = st.selectbox(
        "Select Model",
        options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0,
        help="Llama 3.3 70B is recommended for high reasoning accuracy."
    )
    
    st.divider()
    st.markdown("### 🤖 Multi-Agent Flow")
    st.markdown("""
1. **Agent FOR** (Temp 0.85)  
   *Creates persuasive arguments*
2. **Agent AGAINST** (Temp 0.85)  
   *Creates robust counters*
3. **Agent JUDGE** (Temp 0.15)  
   *Delivers objective verdict*
""")
    st.divider()
    st.markdown("**Cost:** $0 (100% Free API)")

# ── Helper: Run One Agent ────────────────────────────────────
def run_agent(llm, template, **kwargs):
    prompt = PromptTemplate(
        input_variables=list(kwargs.keys()),
        template=template
    )
    chain = prompt | llm
    response = chain.invoke(kwargs)
    if hasattr(response, 'content'):
        return response.content
    return str(response)

def clean_markdown_bold(s):
    import re
    s = s.strip()
    while (s.startswith("**") and s.endswith("**")) or (s.startswith("*") and s.endswith("*")):
        if s.startswith("**") and s.endswith("**"):
            s = s[2:-2].strip()
        elif s.startswith("*") and s.endswith("*"):
            s = s[1:-1].strip()
    s = re.sub(r'^[:\*\s]+|[:\*\s]+$', '', s)
    return s.strip()

def render_arguments(text, side_class):
    import re
    # Split text into blocks of arguments.
    parts = re.split(r'(?i)\*?\*?\s*Argument\s+\d+\s*\*?\*?\s*:?', text)
    
    # If we don't have matched parts, return fallback
    if len(parts) <= 1:
        return f'<div style="white-space: pre-wrap;">{text}</div>'
        
    intro = parts[0].strip()
    arg_blocks = parts[1:]
    
    html_output = []
    if intro:
        html_output.append(f'<div class="arg-intro" style="margin-bottom: 15px; font-style: italic;">{intro}</div>')
        
    # Strict markers
    claim_marker = r'(?:🔹\s*\*?\*?Claim\*?\*?|\*?\*?Claim\*?\*?\s*:)'
    evidence_marker = r'(?:📊\s*\*?\*?Evidence\*?\*?|\*?\*?Evidence\*?\*?\s*:)'
    impact_marker = r'(?:💡\s*\*?\*?Impact\*?\*?|\*?\*?Impact\*?\*?\s*:)'

    for i, block in enumerate(arg_blocks, 1):
        block = block.strip()
        if not block:
            continue
            
        claim_match = re.search(r'(?:🔹\s*)?(?:\*?\*?Claim\*?\*?:?)\s*(.*?)(?=' + claim_marker + '|' + evidence_marker + '|' + impact_marker + '|$)', block, re.DOTALL | re.IGNORECASE)
        evidence_match = re.search(evidence_marker + r'\s*(.*?)(?=' + impact_marker + '|$)', block, re.DOTALL | re.IGNORECASE)
        impact_match = re.search(impact_marker + r'\s*(.*?)$', block, re.DOTALL | re.IGNORECASE)
        
        claim = claim_match.group(1).strip() if claim_match else ""
        evidence = evidence_match.group(1).strip() if evidence_match else ""
        impact = impact_match.group(1).strip() if impact_match else ""
        
        claim = clean_markdown_bold(claim)
        evidence = clean_markdown_bold(evidence)
        impact = clean_markdown_bold(impact)
        
        if not claim and not evidence and not impact:
            html_output.append(f"""<div class="arg-card">
<div style="display: flex; align-items: flex-start;">
<div class="arg-number {side_class}-num">{i}</div>
<div class="arg-detail" style="white-space: pre-wrap;">{block}</div>
</div>
</div>""")
        else:
            evidence_html = f'<div class="arg-label">📊 Evidence</div><div class="arg-detail">{evidence}</div>' if evidence else ''
            impact_html = f'<div class="arg-label">💡 Impact</div><div class="arg-detail">{impact}</div>' if impact else ''
            html_output.append(f"""<div class="arg-card">
<div style="display: flex; align-items: flex-start; margin-bottom: 8px;">
<div class="arg-number {side_class}-num">{i}</div>
<div class="arg-claim">🔹 {claim}</div>
</div>
{evidence_html}
{impact_html}
</div>""")
            
    return "\n".join(html_output)

def render_strongest_argument(text):
    import re
    text = text.strip()
    
    quote = ""
    explanation = ""
    
    # Match quote blocks like "[quote]" [explanation]
    quote_match = re.match(r'^["\'“]\s*(.*?)\s*["\'”]\s*(?:-|—|:\s*)?\s*(.*)$', text, re.DOTALL)
    if quote_match:
        quote = quote_match.group(1).strip()
        explanation = quote_match.group(2).strip()
    else:
        explanation_split = re.split(r'(?i)(?=\b(?:this argument|it stands out|the judge|reasoning|explanation|why:)\b)', text, maxsplit=1)
        if len(explanation_split) > 1:
            quote = explanation_split[0].strip()
            explanation = explanation_split[1].strip()
        else:
            quote = text
            explanation = ""
            
    # Strict markers
    claim_marker = r'(?:🔹\s*\*?\*?Claim\*?\*?|\*?\*?Claim\*?\*?\s*:)'
    evidence_marker = r'(?:📊\s*\*?\*?Evidence\*?\*?|\*?\*?Evidence\*?\*?\s*:)'
    impact_marker = r'(?:💡\s*\*?\*?Impact\*?\*?|\*?\*?Impact\*?\*?\s*:)'
    
    claim_match = re.search(r'(?:🔹\s*)?(?:\*?\*?Claim\*?\*?:?)\s*(.*?)(?=' + claim_marker + '|' + evidence_marker + '|' + impact_marker + '|$)', quote, re.DOTALL | re.IGNORECASE)
    evidence_match = re.search(evidence_marker + r'\s*(.*?)(?=' + impact_marker + '|$)', quote, re.DOTALL | re.IGNORECASE)
    impact_match = re.search(impact_marker + r'\s*(.*?)$', quote, re.DOTALL | re.IGNORECASE)
    
    claim = claim_match.group(1).strip() if claim_match else ""
    evidence = evidence_match.group(1).strip() if evidence_match else ""
    impact = impact_match.group(1).strip() if impact_match else ""
    
    claim = clean_markdown_bold(claim)
    evidence = clean_markdown_bold(evidence)
    impact = clean_markdown_bold(impact)
    
    quote_html = ""
    if claim or evidence or impact:
        evidence_html = f'<div class="arg-label" style="font-size: 0.75rem; margin-top: 6px; margin-bottom: 2px;">📊 Evidence</div><div class="arg-detail" style="font-size: 0.88rem;">{evidence}</div>' if evidence else ''
        impact_html = f'<div class="arg-label" style="font-size: 0.75rem; margin-top: 6px; margin-bottom: 2px;">💡 Impact</div><div class="arg-detail" style="font-size: 0.88rem;">{impact}</div>' if impact else ''
        quote_html = f"""<div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(128, 128, 128, 0.15); border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;">
<div style="font-weight: 700; font-size: 0.95rem; color: #007AFF;">🔹 {claim}</div>
{evidence_html}
{impact_html}
</div>"""
    else:
        quote_html = f'<blockquote style="border-left: 3px solid #007AFF; padding-left: 10px; margin: 0 0 10px 0; font-style: italic; opacity: 0.85;">"{quote}"</blockquote>'
        
    explanation_html = f'<p style="margin: 0; line-height: 1.5; font-size: 0.92rem; opacity: 0.9;">{explanation}</p>' if explanation else ''
    
    return f"""<div style="margin-bottom: 20px; padding: 15px; background: rgba(128, 128, 128, 0.05); border-radius: 8px; border-left: 3px solid #007AFF;">
<h4 style="margin: 0 0 8px 0; color: #007AFF; font-size: 1.15rem;">⚡ Strongest Argument</h4>
{quote_html}
{explanation_html}
</div>"""

def render_verdict(text):
    import re
    # Pattern to match the sections
    pattern = r'(?i)(\*?\*?\s*(?:🏆|📊|⚡|🔍|📌)\s*\*?\*?\s*(?:VERDICT|CONFIDENCE SCORE|STRONGEST ARGUMENT|BLIND SPOT|FINAL RECOMMENDATION)\s*\*?\*?\s*:\s*\*?\*?)'
    parts = re.split(pattern, text)
    
    # If we don't have matched parts, return fallback
    if len(parts) <= 1:
        return f'<div style="white-space: pre-wrap;">{text}</div>'
        
    sections = {}
    intro = parts[0].strip()
    
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            key_text = parts[i].lower()
            val_text = parts[i+1].strip()
            
            if "verdict" in key_text:
                sections["verdict"] = val_text
            elif "confidence score" in key_text:
                sections["confidence"] = val_text
            elif "strongest argument" in key_text:
                sections["strongest"] = val_text
            elif "blind spot" in key_text:
                sections["blind_spot"] = val_text
            elif "final recommendation" in key_text:
                sections["recommendation"] = val_text
                
    html_output = []
    if intro:
        html_output.append(f'<div style="margin-bottom: 15px; font-style: italic;">{intro}</div>')
        
    if "verdict" in sections:
        verdict_val = clean_markdown_bold(sections["verdict"])
        html_output.append(f"""<div style="margin-bottom: 20px;">
<h4 style="margin: 0 0 8px 0; color: #FFD700; font-size: 1.25rem;">🏆 Verdict</h4>
<p style="font-size: 1.05rem; line-height: 1.6; margin: 0;">{verdict_val}</p>
</div>""")
        
    if "confidence" in sections:
        val = clean_markdown_bold(sections["confidence"])
        score_num_match = re.search(r'(\d+)\s*/\s*100', val)
        if not score_num_match:
            score_num_match = re.search(r'(\d+)\s*%', val)
        if not score_num_match:
            score_num_match = re.search(r'(\d+)', val)
            
        score_num = score_num_match.group(1) if score_num_match else ""
        badge_html = f'<div class="score-badge">📊 {score_num}/100</div>' if score_num else ''
        
        # Strip duplicate confidence score prefix from explanation text
        explain_val = re.sub(r'^\s*\d+(?:\s*/\s*100|\s*%)?\s*(?:-|—|:\s*)?\s*', '', val).strip()
        
        html_output.append(f"""<div style="margin-bottom: 20px;">
<h4 style="margin: 0 0 8px 0; color: #FFA500; font-size: 1.15rem;">📊 Confidence Score</h4>
{badge_html}
<p style="font-size: 0.95rem; line-height: 1.6; margin: 5px 0 0 0;">{explain_val}</p>
</div>""")
        
    if "strongest" in sections:
        html_output.append(render_strongest_argument(sections["strongest"]))
        
    if "blind_spot" in sections:
        blind_spot_val = clean_markdown_bold(sections["blind_spot"])
        html_output.append(f"""<div style="margin-bottom: 20px;">
<h4 style="margin: 0 0 8px 0; color: #FF3B30; font-size: 1.15rem;">🔍 Blind Spot</h4>
<p style="font-size: 0.95rem; line-height: 1.6; margin: 0;">{blind_spot_val}</p>
</div>""")
        
    if "recommendation" in sections:
        rec_val = clean_markdown_bold(sections["recommendation"])
        html_output.append(f"""<div style="margin-bottom: 10px; padding: 15px; background: rgba(128, 128, 128, 0.05); border-radius: 8px; border-left: 3px solid #34C759;">
<h4 style="margin: 0 0 8px 0; color: #34C759; font-size: 1.15rem;">📌 Final Recommendation</h4>
<p style="font-size: 0.95rem; line-height: 1.6; margin: 0;">{rec_val}</p>
</div>""")
        
    if not html_output:
        return f'<div style="white-space: pre-wrap;">{text}</div>'
        
    return "\n".join(html_output)


# ── Main UI ──────────────────────────────────────────────────
if "topic" not in st.session_state:
    st.session_state.topic = ""

def set_topic(new_topic):
    st.session_state.topic = new_topic

# Example buttons
st.caption("💡 Try an example:")
col1, col2, col3, col4 = st.columns(4)
examples = [
    "Should AI replace human teachers?",
    "Is social media harmful for students?",
    "Should India invest more in space research?",
    "Is remote work better than office work?"
]
if col1.button(examples[0], use_container_width=True): set_topic(examples[0])
if col2.button(examples[1], use_container_width=True): set_topic(examples[1])
if col3.button(examples[2], use_container_width=True): set_topic(examples[2])
if col4.button(examples[3], use_container_width=True): set_topic(examples[3])

topic = st.text_input(
    "🎯 Enter any topic or decision to debate",
    value=st.session_state.topic,
    placeholder="e.g. Should AI replace teachers? / Is remote work better?"
)
st.session_state.topic = topic

st.divider()

# ── Prompt Templates ─────────────────────────────────────────
ADVOCATE_PROMPT = """You are a sharp debate champion arguing {side}: "{topic}"

Generate exactly 5 arguments. For each argument, you MUST use this EXACT format with line breaks. Do not merge them into a single line. Every label (Claim, Evidence, Impact) MUST start on a new line.

**Argument 1:**
🔹 **Claim:** [one bold sentence stating your position]
📊 **Evidence:** [a specific real-world example, statistic, or case study]
💡 **Impact:** [why this matters — the real-world consequence]

**Argument 2:**
🔹 **Claim:** [one bold sentence]
📊 **Evidence:** [specific example or data]
💡 **Impact:** [why it matters]

...continue for all 5 arguments.

Be specific, confident, and highly persuasive. Do not write any intro or conclusion."""

JUDGE_PROMPT = """You are a strict, impartial judge evaluating a structured debate.

Topic: "{topic}"

ARGUMENTS FOR:
{for_args}

ARGUMENTS AGAINST:
{against_args}

Deliver your judgment in this exact format:

**🏆 VERDICT:** Which side won and why (2-3 sentences, be direct)

**📊 CONFIDENCE SCORE:** X/100 — explain why you're this confident (choose a score above 90/100 to indicate a clear, decisive winner based on argument strength)

**⚡ STRONGEST ARGUMENT:** The single most powerful argument from either side — quote it and explain why

**🔍 BLIND SPOT:** What critical point did BOTH sides completely miss?

**📌 FINAL RECOMMENDATION:** What should someone think or do based on this debate?

No hedging. No "both sides have merit." Pick a winner."""

# ── Run Debate ───────────────────────────────────────────────
if topic and api_key:
    if st.button("⚔️ Start Debate", type="primary", use_container_width=True):

        llm_creative = ChatGroq(
            api_key=api_key,
            model_name=model_name,
            temperature=0.85
        )
        llm_analytical = ChatGroq(
            api_key=api_key,
            model_name=model_name,
            temperature=0.15
        )

        # Agent 1: FOR
        with st.spinner("🟢 Agent 1 is building arguments FOR..."):
            for_result = run_agent(
                llm_creative,
                ADVOCATE_PROMPT,
                side="FOR",
                topic=topic
            )

        # Agent 2: AGAINST
        with st.spinner("🔴 Agent 2 is building arguments AGAINST..."):
            against_result = run_agent(
                llm_creative,
                ADVOCATE_PROMPT,
                side="AGAINST",
                topic=topic
            )

        # Agent 3: JUDGE
        with st.spinner("🏛️ Agent 3 (Judge) is evaluating both sides..."):
            verdict = run_agent(
                llm_analytical,
                JUDGE_PROMPT,
                topic=topic,
                for_args=for_result,
                against_args=against_result
            )

        # ── Display Results ───────────────────────────────────
        st.markdown(f"## 🎯 Debate: *{topic}*")
        st.divider()

        # ── FOR Section (full width) ──────────────────────────
        st.markdown("### ✅ Arguments FOR")
        rendered_for = render_arguments(for_result, "for")
        st.markdown(f"""<div class="section-card for-section">

{rendered_for}

</div>""", unsafe_allow_html=True)

        # ── VS Divider ────────────────────────────────────────
        st.markdown('<div class="vs-badge">⚔️ VS</div>', unsafe_allow_html=True)

        # ── AGAINST Section (full width) ──────────────────────
        st.markdown("### ❌ Arguments AGAINST")
        rendered_against = render_arguments(against_result, "against")
        st.markdown(f"""<div class="section-card against-section">

{rendered_against}

</div>""", unsafe_allow_html=True)

        st.divider()

        # ── Judge's Verdict ───────────────────────────────────
        st.markdown("### 🏛️ Judge's Verdict")
        rendered_verdict_html = render_verdict(verdict)
        st.markdown(f"""<div class="judge-section">

{rendered_verdict_html}

</div>""", unsafe_allow_html=True)
        st.divider()

        # Download button
        full_debate = f"""# DebateBot Results
## Topic: {topic}

## ✅ Arguments FOR
{for_result}

## ❌ Arguments AGAINST
{against_result}

## 🏛️ Judge's Verdict
{verdict}
"""
        st.download_button(
            label="⬇️ Download Full Debate as Markdown",
            data=full_debate,
            file_name="debate_result.md",
            mime="text/markdown",
            use_container_width=True
        )

elif not api_key:
    st.info("👈 Enter your free Groq API key in the sidebar to get started.")
elif not topic:
    st.info("👆 Type a topic above or click an example button.")