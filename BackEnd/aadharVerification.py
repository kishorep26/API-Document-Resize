import re
import os

def aadhar_auth_img(image_bytes):
    """
    Validates Aadhar card from image using Google Cloud Vision OCR
    Returns: (is_valid, aadhar_number, confidence_score)
    """
    try:
        from google.cloud import vision
        
        # Check for credentials
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
        if not creds_path or not os.path.exists(creds_path):
            print("ERROR: Google Cloud credentials not found!")
            print("Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
            return False, "", 0
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
        
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        
        if response.error.message:
            print(f"Google Cloud Vision error: {response.error.message}")
            return False, "", 0
        
        if not response.text_annotations:
            print("No text found in image")
            return False, "", 0
            
        full_text = response.text_annotations[0].description
        texts = full_text.split("\n")
        
        print(f"Extracted text: {full_text[:200]}...")  # Debug
        
        # Check for Aadhar keywords (lenient - only need 1)
        aadhar_keywords = [
            'GOVERNMENT OF INDIA',
            'आधार',
            'AADHAAR', 
            'AADHAR',
            'UNIQUE IDENTIFICATION',
            'UIDAI',
            'UID',
            'भारत सरकार',
            'DOB',
            'MALE',
            'FEMALE',
            'YEAR OF BIRTH',
            'VID',
            'INDIA'
        ]
        
        keyword_matches = sum(1 for keyword in aadhar_keywords if keyword.upper() in full_text.upper())
        print(f"Keyword matches: {keyword_matches}")
        
        # Extract Aadhar number (12 digits)
        regex = r"[2-9]{1}[0-9]{3}\s*[0-9]{4}\s*[0-9]{4}"
        p = re.compile(regex)
        
        aadhar_number = None
        for text in texts:
            clean_text = text.replace(" ", "").replace("-", "").replace(".", "")
            # Check for 12 digit pattern
            if re.search(p, text):
                aadhar_number = text.strip()
                break
            # Check if it's exactly 12 digits starting with 2-9
            elif len(clean_text) == 12 and clean_text.isdigit() and clean_text[0] in '23456789':
                aadhar_number = clean_text
                break
        
        if not aadhar_number:
            print("No Aadhar number found in text")
            return False, "", 0
        
        # Format the number
        clean_num = aadhar_number.replace(" ", "").replace("-", "").replace(".", "")
        if len(clean_num) != 12:
            print(f"Invalid Aadhar length: {len(clean_num)}")
            return False, "", 0
            
        formatted = f"{clean_num[0:4]} {clean_num[4:8]} {clean_num[8:12]}"
        print(f"Found Aadhar: {formatted}")
        
        # Validate checksum
        if not _verhoeff_validate(clean_num):
            print("Verhoeff checksum failed")
            return False, formatted, 30
        
        # Calculate confidence
        confidence = 70
        confidence += min(keyword_matches * 5, 30)
        
        print(f"Validation successful! Confidence: {confidence}%")
        return True, formatted, min(confidence, 100)
        
    except Exception as e:
        print(f"Error in aadhar_auth_img: {e}")
        import traceback
        traceback.print_exc()
        return False, "", 0

def aadhar_auth_number(number):
    """
    Validates Aadhar card number format and checksum
    Returns: (is_valid, aadhar_number, confidence_score)
    """
    try:
        clean_number = number.replace(" ", "").replace("-", "")
        
        if len(clean_number) != 12 or not clean_number.isdigit():
            return False, "", 0
            
        if clean_number[0] not in '23456789':
            return False, "", 0
        
        if not _verhoeff_validate(clean_number):
            return False, "", 0
        
        formatted = f"{clean_number[0:4]} {clean_number[4:8]} {clean_number[8:12]}"
        
        return True, formatted, 85
        
    except Exception as e:
        print(f"Error in aadhar_auth_number: {e}")
        return False, "", 0

def _verhoeff_validate(number):
    """
    Validates Aadhar number using Verhoeff algorithm
    """
    try:
        d = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ]
        
        p = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
        ]
        
        c = 0
        reversed_number = number[::-1]
        
        for i, digit in enumerate(reversed_number):
            c = d[c][p[(i % 8)][int(digit)]]
        
        return c == 0
    except:
        return False
