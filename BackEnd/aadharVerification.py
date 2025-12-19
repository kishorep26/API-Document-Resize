import re
import os

def aadhar_auth_img(image_bytes):
    """
    Validates Aadhar card from image using Google Cloud Vision OCR
    Returns: (is_valid, aadhar_number, confidence_score)
    """
    try:
        # Check for credentials first
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_path:
            creds_path = 'credentials.json'
        
        print(f"Looking for credentials at: {creds_path}")
        
        if not os.path.exists(creds_path):
            print(f"WARNING: Google Cloud credentials not found!")
            print("Returning error - please upload credentials.json or set GOOGLE_APPLICATION_CREDENTIALS")
            return False, "Please set up Google Cloud Vision API credentials to use image verification", 0
        
        from google.cloud import vision
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
        print("Credentials loaded successfully")
        
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        
        print("Calling Google Cloud Vision API...")
        response = client.text_detection(image=image)
        
        if response.error.message:
            print(f"Google Cloud Vision API error: {response.error.message}")
            return False, f"API_ERROR: {response.error.message}", 0
        
        if not response.text_annotations:
            print("No text found in image by OCR")
            return False, "NO_TEXT_FOUND", 0
            
        full_text = response.text_annotations[0].description
        texts = full_text.split("\n")
        
        print("="*50)
        print("EXTRACTED TEXT:")
        print(full_text)
        print("="*50)
        
        # Check for Aadhar keywords
        aadhar_keywords = [
            'GOVERNMENT', 'INDIA', 'AADHAAR', 'AADHAR', 'UNIQUE', 'IDENTIFICATION',
            'UIDAI', 'UID', 'DOB', 'MALE', 'FEMALE', 'YEAR', 'BIRTH', 'VID'
        ]
        
        keyword_matches = sum(1 for keyword in aadhar_keywords if keyword.upper() in full_text.upper())
        print(f"Keyword matches found: {keyword_matches}")
        
        # Extract Aadhar number
        aadhar_number = None
        
        for text in texts:
            clean_text = text.replace(" ", "").replace("-", "").replace(".", "").replace("_", "")
            
            if len(clean_text) == 12 and clean_text.isdigit():
                if clean_text[0] in '23456789':
                    aadhar_number = clean_text
                    print(f"Found Aadhar (12 digits): {aadhar_number}")
                    break
            
            regex = r"[2-9]{1}[0-9]{3}\s*[0-9]{4}\s*[0-9]{4}"
            match = re.search(regex, text)
            if match:
                aadhar_number = match.group().replace(" ", "")
                print(f"Found Aadhar (regex): {aadhar_number}")
                break
        
        if not aadhar_number:
            print("No Aadhar number pattern found in extracted text")
            print("Extracted lines:")
            for i, line in enumerate(texts[:20]):
                print(f"  Line {i}: '{line}'")
            return False, "NO_AADHAR_PATTERN", 0
        
        if len(aadhar_number) != 12:
            print(f"Invalid Aadhar length: {len(aadhar_number)}")
            return False, aadhar_number, 0
            
        formatted = f"{aadhar_number[0:4]} {aadhar_number[4:8]} {aadhar_number[8:12]}"
        
        if not _verhoeff_validate(aadhar_number):
            print(f"Verhoeff checksum failed for: {formatted}")
            return False, formatted, 30
        
        confidence = 70
        confidence += min(keyword_matches * 5, 30)
        
        print(f"✓ Validation successful! Aadhar: {formatted}, Confidence: {confidence}%")
        return True, formatted, min(confidence, 100)
        
    except Exception as e:
        print(f"EXCEPTION in aadhar_auth_img: {e}")
        import traceback
        traceback.print_exc()
        return False, f"EXCEPTION: {str(e)}", 0

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
