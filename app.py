# app.py
import streamlit as st
from models import TaxPayer
from calculator import calculate_new_regime, calculate_old_regime
import time

# --- 1. UI Header ---
st.set_page_config(page_title="Sahaj Tax AI", page_icon="📝")
st.title("🤖 Sahaj Tax AI")
st.subheader("Automated ITR Filing Assistant")

# --- 2. Sidebar (Simulated AI Upload) ---
with st.sidebar:
    st.header("Upload Documents")
    uploaded_file = st.file_uploader("Upload Form 16 / Salary Slip (PDF/Img)", type=['png', 'jpg', 'pdf'])
    
    # MOCK AI PARSER
    # In a real app, this is where you call OpenAI/Tesseract
    if uploaded_file is not None:
        st.success("Document Uploaded!")
        st.info("AI is extracting data...")
        time.sleep(2) # Fake processing delay
        
        # Extracted Data (Simulated)
        extracted_data = {
            "name": "Itishree Khadiratna",
            "pan": "ABCDE1234F",
            "salary": 1250000.0,
            "deductions_80c": 150000.0
        }
        st.json(extracted_data)
    else:
        extracted_data = None

# --- 3. Main Form ---
st.write("### Verify Details")

# If AI extracted data, pre-fill the form. If not, use defaults.
default_name = extracted_data["name"] if extracted_data else ""
default_pan = extracted_data["pan"] if extracted_data else ""
default_salary = extracted_data["salary"] if extracted_data else 0.0
default_80c = extracted_data["deductions_80c"] if extracted_data else 0.0

with st.form("itr_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", value=default_name)
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        salary = st.number_input("Annual Salary", value=default_salary)
    with col2:
        pan = st.text_input("PAN Number", value=default_pan)
        deduction_80c = st.number_input("80C Investments (PF/LIC)", value=default_80c)
        deduction_80d = st.number_input("80D (Medical Insurance)", value=0.0)
    
    submitted = st.form_submit_button("Calculate Tax")

# --- 4. Result Processing ---
if submitted:
    try:
        # VALIDATION LAYER (Pydantic)
        # This checks if the data matches our Model rules
        user = TaxPayer(
            name=name,
            pan_number=pan,
            age=age,
            salary_income=salary,
            section_80c_deductions=deduction_80c,
            section_80d_deductions=deduction_80d
        )
        
        # CALCULATION LAYER
        tax_new = calculate_new_regime(user)
        tax_old = calculate_old_regime(user)
        
        # --- 5. Display Output ---
        st.divider()
        st.write(f"### 📊 Tax Analysis for {user.name}")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="New Regime Tax", value=f"₹ {tax_new:,.2f}")
        with res_col2:
            st.metric(label="Old Regime Tax", value=f"₹ {tax_old:,.2f}")
            
        st.success(f"✅ Recommendation: Choose **{'New' if tax_new < tax_old else 'Old'} Regime** to save ₹ {abs(tax_new - tax_old):,.2f}")
        
    except Exception as e:
        st.error(f"Validation Error: {e}")