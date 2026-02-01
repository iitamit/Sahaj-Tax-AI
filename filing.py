# filing.py
import json
import uuid
from datetime import datetime

def generate_govt_json(user_data, tax_summary):
    """
    Generates the Standard ITR JSON Payload for Government Integration.
    """
    
    # This structure mimics the official schema used by Income Tax Dept APIs
    itr_payload = {
        "filing_metadata": {
            "assessment_year": "2025-26",
            "schema_version": "ITR-1_v2.0",
            "submission_id": str(uuid.uuid4()), # Unique ID for this filing
            "timestamp": datetime.now().isoformat()
        },
        "taxpayer_profile": {
            "pan": user_data.pan_number,
            "name": user_data.name,
            "age": user_data.age,
            "status": "INDIVIDUAL"
        },
        "income_details": {
            "gross_salary": user_data.salary_income,
            "exempt_income": 0, # Can be expanded
            "net_taxable_income": tax_summary["taxable_income"]
        },
        "deductions": {
            "section_80c": min(user_data.section_80c_deductions, 150000),
            "section_80d": user_data.section_80d_deductions,
            "total_deductions": tax_summary["total_deductions"]
        },
        "tax_computation": {
            "regime_selected": tax_summary["selected_regime"],
            "tax_payable": tax_summary["tax_payable"],
            "cess": tax_summary["cess"],
            "total_liability": tax_summary["final_tax"]
        },
        "verification": {
            "declaration": "I hereby declare that the information given above is correct.",
            "verified_by_ai": True,
            "risk_score": tax_summary.get("audit_score", 0)
        }
    }
    
    # Convert to JSON string
    return json.dumps(itr_payload, indent=4)