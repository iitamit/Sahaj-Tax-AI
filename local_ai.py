# local_ai.py
import pytesseract
from PIL import Image
import re
import os

# --- CONFIGURATION ---
# IMPORTANT: This path must point to where you installed Tesseract.
# If you didn't change the default settings during installation, this is correct.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ai_extract_data(image_path):
    """
    The 'Brain' of the Offline Engine.
    1. Uses Tesseract (Vision) to read the text.
    2. Uses Regex (Logic) to find PAN numbers and Salary.
    """
    
    # Default response if things fail
    result = {
        "pan": "", 
        "salary": 0.0, 
        "text": "", 
        "error": None
    }
    
    try:
        # --- PHASE 1: VISION (OCR) ---
        if not os.path.exists(image_path):
            return {"error": "File not found"}

        img = Image.open(image_path)
        # extracting text from image
        raw_text = pytesseract.image_to_string(img)
        result["text"] = raw_text

        # --- PHASE 2: LOGIC (Pattern Recognition) ---
        
        # 1. Find PAN Number
        # Regex Rule: 5 Letters, 4 Digits, 1 Letter (e.g., ABCDE1234F)
        pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', raw_text)
        if pan_match:
            result["pan"] = pan_match.group(0)

        # 2. Find Salary
        # We look for lines containing "Salary", "Income", "Gross", or "Net"
        lines = raw_text.split('\n')
        for line in lines:
            clean_line = line.lower().replace(',', '') # Remove commas (12,000 -> 12000)
            
            # Check for money keywords
            if any(keyword in clean_line for keyword in ["salary", "income", "gross", "net pay", "total"]):
                # Find all numbers in that line
                numbers = re.findall(r'\d+', clean_line)
                
                # Check if any number looks like a salary (usually > 50,000)
                for num in numbers:
                    val = float(num)
                    # Simple filter: Ignore years (2024) or small IDs
                    if val > 50000:
                        result["salary"] = val
                        break # Stop after finding the first valid big number
                
                if result["salary"] > 0:
                    break

        return result

    except Exception as e:
        # If Tesseract is not installed or crashes, return the error safely
        return {"error": str(e)}