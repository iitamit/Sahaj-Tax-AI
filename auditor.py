# auditor.py
# This AI acts as a "Compliance Officer" to verify data before filing.

def audit_tax_return(user_data, tax_details):
    """
    Analyzes the tax return for risks, errors, and optimization opportunities.
    Returns a Compliance Report.
    """
    report = {
        "status": "PASS",
        "risk_score": 0, # 0 = Safe, 100 = High Audit Risk
        "flags": [],
        "recommendations": []
    }

    # --- RULE 1: PAN Card Validation ---
    pan = user_data.pan_number
    if len(pan) != 10:
        report["flags"].append("❌ Invalid PAN format (Must be 10 chars).")
        report["status"] = "FAIL"
        report["risk_score"] += 100

    # --- RULE 2: Investment Limit Checks ---
    if user_data.section_80c_deductions > 150000:
        report["flags"].append("⚠️ 80C Claim exceeds ₹1.5 Lakh limit. Excess will be ignored.")
        report["recommendations"].append("Restrict 80C claim to ₹1,50,000 to avoid query.")
    
    # --- RULE 3: Suspiciously Low Income vs Deductions ---
    total_deductions = user_data.section_80c_deductions + user_data.section_80d_deductions
    if user_data.salary_income > 0 and (total_deductions > user_data.salary_income * 0.5):
        report["flags"].append("⚠️ High Deductions detected (>50% of income). This triggers audit scrutiny.")
        report["risk_score"] += 30

    # --- RULE 4: Regime Analysis ---
    if tax_details["better_regime"] == "Old":
        report["recommendations"].append("✅ Old Regime selected. Ensure you have proofs for HRA and 80C.")
    else:
        report["recommendations"].append("✅ New Regime selected. No investment proofs needed.")

    # --- FINAL VERDICT ---
    if report["risk_score"] == 0:
        report["message"] = "✅ Perfect! Your return is clean and ready for filing."
    elif report["risk_score"] < 50:
        report["message"] = "⚠️ Good, but check the warnings above."
    else:
        report["status"] = "RISK"
        report["message"] = "🛑 HIGH RISK: Do not file until errors are fixed."

    return report