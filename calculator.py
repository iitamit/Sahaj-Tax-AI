# calculator.py
from models import TaxPayer

def calculate_new_regime(user: TaxPayer) -> float:
    # New Regime (FY 2024-25 Slaps - simplified for demo)
    # 0-3L: Nil, 3-7L: 5%, 7-10L: 10%, 10-12L: 15%, 12-15L: 20%, >15L: 30%
    taxable_income = user.salary_income + user.interest_income - 75000 # Standard Deduction
    
    if taxable_income <= 300000:
        return 0.0
    
    tax = 0.0
    # Simple slab logic (You can expand this later)
    if taxable_income > 300000:
        # Tax for 3L to 7L (5%)
        tax += (min(taxable_income, 700000) - 300000) * 0.05
    if taxable_income > 700000:
        # Tax for 7L to 10L (10%)
        tax += (min(taxable_income, 1000000) - 700000) * 0.10
    if taxable_income > 1000000:
        # Tax for 10L to 12L (15%)
        tax += (min(taxable_income, 1200000) - 1000000) * 0.15
        
    # Rebate u/s 87A for income up to 7L
    if taxable_income <= 700000:
        return 0.0
        
    return tax

def calculate_old_regime(user: TaxPayer) -> float:
    # Old Regime allows deductions (80C, 80D)
    deductions = min(user.section_80c_deductions, 150000) + user.section_80d_deductions + 50000 # Std Ded
    taxable_income = (user.salary_income + user.interest_income) - deductions
    
    # Old Regime Slabs (Simplified)
    # 0-2.5L: Nil, 2.5-5L: 5%, 5-10L: 20%, >10L: 30%
    if taxable_income <= 250000:
        return 0.0
        
    tax = 0.0
    if taxable_income > 250000:
         tax += (min(taxable_income, 500000) - 250000) * 0.05
    if taxable_income > 500000:
         tax += (min(taxable_income, 1000000) - 500000) * 0.20
    if taxable_income > 1000000:
         tax += (taxable_income - 1000000) * 0.30
         
    # Rebate u/s 87A for income up to 5L
    if taxable_income <= 500000:
        return 0.0
        
    return tax