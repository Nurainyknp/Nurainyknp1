import streamlit as st
import streamlit.components.v1 as components

# ✅ Wide layout + Theme session
st.set_page_config(layout="wide")

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "selected_keywords" not in st.session_state:
    st.session_state.selected_keywords = []
if "cbc_selected" not in st.session_state:
    st.session_state.cbc_selected = False
if "cbc_subitems" not in st.session_state:
    st.session_state.cbc_subitems = []

# ✅ Theme toggle button (top right)
col_theme_left, col_theme_spacer, col_theme_right = st.columns([10, 1, 2])
with col_theme_right:
    selected = st.radio("โหมด", ["🌞 Light", "🌙 Night"], horizontal=True, label_visibility="collapsed")
    st.session_state.theme_mode = "dark" if "Night" in selected else "light"

# ✅ Custom CSS per theme
if st.session_state.theme_mode == "dark":
    custom_css = """
        <style>
            body, .block-container {
                background-color: #1e1e1e !important;
                color: white !important;
            }
            .stTextArea textarea, .stTextInput input {
                background-color: #2c2c2c !important;
                color: white !important;
            }
            .stButton > button {
                background-color: #444 !important;
                color: white !important;
            }
            .stRadio > div {
                color: white !important;
            }
        </style>
    """
else:
    custom_css = ""  # Light mode uses Streamlit default appearance

st.markdown(custom_css, unsafe_allow_html=True)

# ✅ Functions
def update_keywords():
    selected = []
    if st.session_state.get("chk_bp"):
        selected.append("Abnormal BP")
    if st.session_state.get("chk_pulse_fast") or st.session_state.get("chk_pulse_slow"):
        if "Abnormal Pulse" not in selected:
            selected.append("Abnormal Pulse")
    if st.session_state.get("chk_temp"):
        selected.append("Abnormal Temperature")
    if st.session_state.get("chk_resp"):
        selected.append("Abnormal Respiration")
    if st.session_state.get("chk_bmi_25"):
        selected.append("BMI ≥ 25")
    if st.session_state.get("chk_bmi_28"):
        selected.append("BMI ≥ 28")
    if st.session_state.get("cbc_main"):
        cbc_text = "Abnormal CBC"
        cbc_items = []
        if st.session_state.get("chk_hb"):
            cbc_items.append("Hb")
        if st.session_state.get("chk_hct"):
            cbc_items.append("Hct")
        if st.session_state.get("chk_rbc"):
            cbc_items.append("RBC")
        if st.session_state.get("chk_wbc"):
            cbc_items.append("WBC")
        if st.session_state.get("chk_plt"):
            cbc_items.append("PLT")
        if st.session_state.get("chk_neutro"):
            cbc_items.append("Neutrophils")
        if st.session_state.get("chk_lymph"):
            cbc_items.append("Lymphocytes")
        if st.session_state.get("chk_eos"):
            cbc_items.append("Eosinophils")
        if cbc_items:
            cbc_text += " (" + ", ".join(cbc_items) + ")"
        selected.append(cbc_text)
    if st.session_state.get("pe_input"):
        selected.append(f"Abnormal PE ({st.session_state.pe_input})")
    st.session_state.selected_keywords = selected

def clear_keywords():
    st.session_state.selected_keywords = []
    st.session_state.cbc_selected = False
    st.session_state.cbc_subitems = []
    for key in list(st.session_state.keys()):
        if key.startswith("chk_") or key == "cbc_main" or key == "pe_input":
            st.session_state[key] = False if key.startswith("chk_") or key == "cbc_main" else ""

# ✅ Consult keyword box + buttons
update_keywords()
combined_text = "; ".join(st.session_state.selected_keywords)

with st.container():
    bg_color = "#333" if st.session_state.theme_mode == "dark" else "#f0f2f6"
    st.markdown(f"""
        <div style="background-color:{bg_color}; padding:15px; border-radius:10px; margin-bottom:20px;">
            <h3 style="margin-top:0;">📝 ระบบช่วยเขียนข้อความ consult</h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 6, 2])

    with col1:
        components.html(
            f"""
            <button onclick=\"navigator.clipboard.writeText('{combined_text}'); alert('คัดลอกข้อความเรียบร้อยแล้ว!');\"
                    style=\"padding:0.5em 1.2em; font-size:16px; border-radius:5px; background-color:#4CAF50; color:white; border:none; cursor:pointer;\">
                📋 คัดลอกข้อความ
            </button>
            """,
            height=60,
        )

    with col2:
        st.text_area("รวมคำ consult", value=combined_text, height=80)

    with col3:
        if st.button("🗑 ล้างข้อความ"):
            clear_keywords()

    st.markdown("</div>", unsafe_allow_html=True)

# ✅ Section: Vital signs, BMI, PE
st.markdown(f"""
    <div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; 
                padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>
        1. ผล Vital signs และการตรวจร่างกาย
    </div>
""", unsafe_allow_html=True)

with st.expander("คลิกเพื่อเลือกข้อมูล", expanded=True):
    with st.container():
        col_vs, col_bmi, col_pe = st.columns(3)

        with col_vs:
            st.checkbox("BP สูง", key="chk_bp", on_change=update_keywords)
            st.checkbox("ชีพจรเร็ว", key="chk_pulse_fast", on_change=update_keywords)
            st.checkbox("ชีพจรช้า", key="chk_pulse_slow", on_change=update_keywords)
            st.checkbox("อุณหภูมิร่างกายผิดปกติ", key="chk_temp", on_change=update_keywords)
            st.checkbox("การหายใจผิดปกติ", key="chk_resp", on_change=update_keywords)

        with col_bmi:
            st.checkbox("BMI ≥ 25", key="chk_bmi_25", on_change=update_keywords)
            st.checkbox("BMI ≥ 27", key="chk_bmi_28", on_change=update_keywords)

        with col_pe:
            st.text_input("พิมพ์ผลตรวจร่างกาย", key="pe_input", on_change=update_keywords)

# ✅ Section 2: Lab results
st.markdown(f"""
    <div style='background-color:{'#444' if st.session_state.theme_mode == 'dark' else '#E0E0E0'}; 
                padding:10px; border-radius:8px; font-weight:bold; font-size:18px; margin-top:10px;'>
        2. ผลการตรวจทางห้องปฏิบัติการ
    </div>
""", unsafe_allow_html=True)

with st.expander("คลิกเพื่อเลือกข้อมูล (Lab results)", expanded=True):
    with st.container():
        col_cbc, col_met, col_liver = st.columns(3)
        with col_cbc:
            st.checkbox("ความสมบูรณ์ของเม็ดเลือด (CBC)", key="cbc_main", on_change=update_keywords)
            if st.session_state.get("cbc_main"):
                st.checkbox("Hemoglobin (Hb)", key="chk_hb", on_change=update_keywords)
                st.checkbox("Hematocrit (Hct)", key="chk_hct", on_change=update_keywords)
                st.checkbox("Red blood cell (RBC)", key="chk_rbc", on_change=update_keywords)
                st.checkbox("White blood cell (WBC)", key="chk_wbc", on_change=update_keywords)
                st.checkbox("Platelet count (PLT)", key="chk_plt", on_change=update_keywords)
                st.checkbox("Neutrophil", key="chk_neutro", on_change=update_keywords)
                st.checkbox("Lymphocytes", key="chk_lymph", on_change=update_keywords)
                st.checkbox("Eosinophils", key="chk_eos", on_change=update_keywords)

        with col_met:
            st.markdown("🔹 Metabolic")
        with col_liver:
            st.markdown("🔹 การทำงานของตับ (Liver function test)")

        col_kidney, col_thyroid, col_tumor = st.columns(3)
        with col_kidney:
            st.markdown("🔹 การทำงานของไตและเกลือแร่")
        with col_thyroid:
            st.markdown("🔹 การทำงานของต่อมไทรอยด์")
        with col_tumor:
            st.markdown("🔹 สารบ่งชี้มะเร็ง")
