import streamlit as st

# Dictionary mapping
mapping = {
    "dlp": "ภาวะไขมันในเลือดผิดปกติ (DLP)",
    "ldl": "ภาวะไขมันในเลือดผิดปกติ (DLP)",
    "ไขมันสูง": "ภาวะไขมันในเลือดผิดปกติ (DLP)",
    "dm": "ภาวะเบาหวาน (DM)",
    "เบาหวาน": "ภาวะเบาหวาน (DM)",
    "ht": "ภาวะความดันโลหิตสูง (HT)",
    "ความดันสูง": "ภาวะความดันโลหิตสูง (HT)"
}

st.title("🔎 ระบบช่วยเขียนข้อความ consult")
user_input = st.text_input("พิมพ์คำ เช่น DLP, ไขมันสูง")

if user_input:
    keyword = user_input.strip().lower()
    result = mapping.get(keyword, "❌ ไม่พบคำนี้ในระบบ")
    st.text_area("📋 ข้อความที่ standardized", result, height=100)
    
    if result != "❌ ไม่พบคำนี้ในระบบ":
        st.success("กด Ctrl+C เพื่อคัดลอกไปวางในระบบโรงพยาบาล")
