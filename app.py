# app.py - Sahaj Tax AI (Crash-Proof Edition)
import streamlit as st
import pandas as pd
import time

# --- IMPORTS ---
try:
    from auth import login_screen, logout_button
    from local_ai import ai_extract_data
    from tax_brain import get_custom_response
    from models import TaxPayer
    from calculator import calculate_new_regime, calculate_old_regime
    from database import save_tax_record, get_all_records
    from auditor import audit_tax_return
    from filing import generate_govt_json
except ImportError as e:
    st.error(f"❌ System Error: Missing File. {e}")
    st.stop()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sahaj Tax AI | Govt of India", 
    page_icon="🇮🇳", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FIXED CSS (Dark Text Enforcement) ---
st.markdown("""
    <style>
    /* 1. Global Text Color Force */
    .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #2c3e50 !important;
    }
    
    /* 2. White Text Exceptions */
    .header-title, .header-subtitle, .stButton button p, section[data-testid="stSidebar"] *, .badge-success, .badge-warning, .badge-danger {
        color: #ffffff !important;
    }

    /* 3. App Background */
    .stApp {
        background-color: #f4f7f6;
    }
    
    /* 4. Service Cards */
    .service-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-top: 5px solid #FF6F00;
        margin-bottom: 20px;
    }

    /* 5. Inputs */
    .stTextInput input, .stNumberInput input {
        background-color: #ffffff !important;
        border: 1px solid #9fa8da !important;
        color: #000000 !important;
    }
    
    /* 6. Fix for Blank Screen Issues */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

# --- 1. LOGIN / SIGN UP ---
if not st.session_state["logged_in"]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background-color:#1A237E; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
                <div class="header-title">🇮🇳 Sahaj Tax AI</div>
                <div class="header-subtitle">Unified Tax Filing Interface</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            login_screen()
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- 2. DASHBOARD ---
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=70)
        st.markdown(f"### {st.session_state.get('username', 'User').title()}")
        st.markdown(f"<span style='background:green; color:white; padding:2px 8px; border-radius:10px; font-size:12px;'>● {st.session_state['role'].upper()}</span>", unsafe_allow_html=True)
        st.divider()
        logout_button()

    # Main Header
    st.markdown("""
        <div style="background-color:#1A237E; padding:15px; border-radius:10px; display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <div>
                <div class="header-title" style="font-size:20px;">Sahaj Tax Dashboard</div>
                <div class="header-subtitle" style="font-size:12px;">Select a service to proceed</div>
            </div>
            <div style="background:white; color:#1A237E !important; padding:5px 15px; border-radius:20px; font-weight:bold; font-size:12px;">
                FY 2025-26
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Tabs
    if st.session_state["role"] == "admin":
        tab1, tab2, tab3 = st.tabs(["⚡ e-Filing Agent", "🗄️ Tax Records", "🤖 AI Sahayak"])
    else:
        tab1, tab3 = st.tabs(["⚡ e-Filing Agent", "🤖 AI Sahayak"])

    # --- TAB 1: FILING WIZARD ---
    with tab1:
        st.markdown('<div class="service-card">', unsafe_allow_html=True)
        st.markdown("#### 📄 New ITR Application")
        
        # Form
        c1, c2, c3 = st.columns(3)
        with c1:
            name_in = st.text_input("Full Name", value="Itishree Khadiratna")
            pan_in = st.text_input("PAN Number", value="ABCDE1234F")
        with c2:
            income_in = st.number_input("Gross Annual Salary (₹)", value=1200000.0)
            inv_in = st.number_input("80C Deductions (₹)", value=150000.0)
        with c3:
            age_in = st.number_input("Age", value=25)
            med_in = st.number_input("Health Insurance (₹)", value=0.0)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # ACTION BUTTON
        if st.button("🚀 Process Application", type="primary", use_container_width=True):
            with st.spinner("🔄 AI Agent is processing..."):
                time.sleep(1) # Visual delay
                try:
                    # 1. Calculation Logic
                    user = TaxPayer(name=name_in, pan_number=pan_in, age=age_in, salary_income=income_in, 
                                    section_80c_deductions=inv_in, section_80d_deductions=med_in)
                    
                    tax_new = calculate_new_regime(user)
                    tax_old = calculate_old_regime(user)
                    best_regime = "New" if tax_new < tax_old else "Old"
                    final_tax = min(tax_new, tax_old)
                    
                    summary = {
                        "selected_regime": best_regime, "better_regime": best_regime,
                        "taxable_income": max(0, income_in - inv_in) if best_regime == "Old" else income_in - 75000,
                        "total_deductions": inv_in if best_regime == "Old" else 0,
                        "final_tax": final_tax, "tax_payable": final_tax/1.04, "cess": final_tax - (final_tax/1.04), "audit_score": 0
                    }
                    
                    # 2. Show Results
                    st.success("✅ Calculation Complete!")
                    r1, r2, r3 = st.columns(3)
                    r1.metric("Tax (New)", f"₹ {tax_new:,.0f}")
                    r2.metric("Tax (Old)", f"₹ {tax_old:,.0f}")
                    r3.info(f"💡 Recommendation: **{best_regime} Regime**")

                    # 3. Audit
                    st.divider()
                    st.markdown("#### 📋 Compliance Audit")
                    audit_report = audit_tax_return(user, summary)
                    
                    if audit_report["risk_score"] == 0:
                        st.success(f"✅ {audit_report['message']}")
                    elif audit_report["risk_score"] < 50:
                        st.warning(f"⚠️ {audit_report['message']}")
                    else:
                        st.error(f"🛑 {audit_report['message']}")

                    # 4. Save to DB (Safe Mode)
                    # We wrap this in try/except so if DB fails, the App DOES NOT crash
                    try:
                        if audit_report["risk_score"] < 100:
                            save_tax_record({"name": name_in, "pan": pan_in, "status": "Generated", "income": income_in, "tax": final_tax})
                            st.toast("💾 Record Saved to Database")
                    except Exception as db_err:
                        # Just log it, don't stop the user
                        print(f"Database Warning: {db_err}")

                    # 5. Download
                    if audit_report["risk_score"] < 100:
                        json_packet = generate_govt_json(user, summary)
                        st.download_button("📥 Download ITR JSON", json_packet, f"ITR_{pan_in}.json")

                except Exception as e:
                    # IF IT CRASHES, SHOW THE REASON
                    st.error("⚠️ Processing Error Occurred")
                    st.exception(e)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: DB (Admin Only) ---
    if st.session_state["role"] == "admin":
        with tab2:
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            st.markdown("#### 🗄️ Tax Records")
            if st.button("🔄 Sync Records"): st.rerun()
            
            try:
                records = get_all_records()
                if records: st.dataframe(pd.DataFrame(records), use_container_width=True)
                else: st.info("No records found.")
            except Exception as e:
                st.warning("Could not connect to Database. Is MongoDB running?")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 3: CHAT ---
    if 'tab3' in locals():
        with tab3:
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            st.markdown("#### 🤖 Sahayak Chat")
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).markdown(msg["content"])
            
            if prompt := st.chat_input("Ask a question..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").markdown(prompt)
                
                # Safe Chat Call
                try:
                    reply = get_custom_response(prompt)
                    st.chat_message("assistant").markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error("Chat Engine is offline.")
            
            st.markdown('</div>', unsafe_allow_html=True)