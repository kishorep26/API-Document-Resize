import re
import os

def pan_auth_img(image_bytes):
    """
    Validates PAN card from image using Google Cloud Vision OCR
    Returns: (is_valid, pan_number, confidence_score)
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
        
        # Check for PAN keywords
        pan_keywords = [
            'INCOME', 'TAX', 'GOVT', 'GOVERNMENT', 'PERMANENT', 'ACCOUNT', 'NUMBER',
            'PAN', 'INDIA', 'FATHER', 'NAME', 'DOB', 'SIGNATURE', 'DATE', 'BIRTH'
        ]
        
        keyword_matches = sum(1 for keyword in pan_keywords if keyword.upper() in full_text.upper())
        print(f"Keyword matches found: {keyword_matches}")
        
        # Extract PAN number
        pan_number = None
        regex1 = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
        
        for text in texts:
            text_clean = text.strip().upper().replace(" ", "").replace("-", "").replace(".", "").replace("_", "")
            
            if len(text_clean) == 10:
                if re.match(regex1, text_clean):
                    pan_number = text_clean
                    print(f"Found PAN (exact match): {pan_number}")
                    break
            
            match = re.search(regex1, text_clean)
            if match:
                pan_number = match.group()
                print(f"Found PAN (regex search): {pan_number}")
                break
        
        if not pan_number:
            print("No PAN number pattern found in extracted text")
            print("Extracted lines:")
            for i, line in enumerate(texts[:20]):
                print(f"  Line {i}: '{line}'")
            return False, "NO_PAN_PATTERN", 0
        
        if not _validate_pan_structure(pan_number):
            print(f"PAN structure validation failed for: {pan_number}")
            return False, pan_number, 30
        
        confidence = 70
        confidence += min(keyword_matches * 3, 30)
        
        print(f"✓ Validation successful! PAN: {pan_number}, Confidence: {confidence}%")
        return True, pan_number, min(confidence, 100)
        
    except Exception as e:
        print(f"EXCEPTION in pan_auth_img: {e}")
        import traceback
        traceback.print_exc()
        return False, f"EXCEPTION: {str(e)}", 0

def pan_auth_number(number):
    """
    Validates PAN card number format and structure
    Returns: (is_valid, pan_number, confidence_score)
    """
    try:
        clean_number = number.strip().upper().replace(" ", "").replace("-", "")
        
        regex = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        
        if len(clean_number) != 10 or not re.match(regex, clean_number):
            return False, "", 0
        
        if not _validate_pan_structure(clean_number):
            return False, clean_number, 30
        
        return True, clean_number, 85
        
    except Exception as e:
        print(f"Error in pan_auth_number: {e}")
        return False, "", 0

def _validate_pan_structure(pan):
    """
    Validates PAN structure according to Indian Income Tax rules
    """
    try:
        if len(pan) != 10:
            print(f"  Invalid length: {len(pan)}")
            return False
        
        valid_types = ['P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G']
        if pan[3] not in valid_types:
            print(f"  Invalid 4th character: {pan[3]} (must be one of {valid_types})")
            return False
        
        if not pan[:5].isalpha():
            print(f"  First 5 chars not all letters: {pan[:5]}")
            return False
        
        if not pan[5:9].isdigit():
            print(f"  Middle 4 chars not all digits: {pan[5:9]}")
            return False
        
        if not pan[9].isalpha():
            print(f"  Last char not a letter: {pan[9]}")
            return False
        
        return True
    except Exception as e:
        print(f"  Exception in structure validation: {e}")
        return False

def get_pan_holder_type(pan):
    """
    Returns the type of PAN holder based on 4th character
    """
    types = {
        'P': 'Individual',
        'C': 'Company',
        'H': 'Hindu Undivided Family (HUF)',
        'F': 'Firm',
        'A': 'Association of Persons (AOP)',
        'T': 'Trust (AOP)',
        'B': 'Body of Individuals (BOI)',
        'L': 'Local Authority',
        'J': 'Artificial Juridical Person',
        'G': 'Government'
    }
    
    if len(pan) >= 4:
        return types.get(pan[3], 'Unknown')
    return 'Unknown'
