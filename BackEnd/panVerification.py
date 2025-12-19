import re
import os

def pan_auth_img(image_bytes):
    """
    Extracts and validates PAN card from image using OCR
    Returns: (is_valid_format, pan_number, confidence_score)
    """
    try:
        from google.cloud import vision
        
        # Use environment variable or fallback
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
        if creds_path and os.path.exists(creds_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
        
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        
        if not response.text_annotations:
            return False, "", 0
            
        full_text = response.text_annotations[0].description
        texts = full_text.split("\n")
        
        # Check for PAN keywords (more lenient - only need 1)
        pan_keywords = [
            'INCOME TAX',
            'GOVT',
            'GOVERNMENT',
            'PERMANENT ACCOUNT NUMBER',
            'PAN',
            'आयकर',
            'भारत',
            'INDIA',
            'FATHER',
            'NAME',
            'DOB',
            'SIGNATURE'
        ]
        
        keyword_matches = sum(1 for keyword in pan_keywords if keyword.upper() in full_text.upper())
        
        # Extract PAN number
        regex = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
        p = re.compile(regex)
        
        pan_number = None
        for text in texts:
            text_upper = text.strip().upper().replace(" ", "").replace("-", "")
            if len(text_upper) == 10 and re.match(regex, text_upper):
                pan_number = text_upper
                break
        
        if not pan_number:
            return False, "", 0
        
        # Validate PAN structure
        if not _validate_pan_structure(pan_number):
            return False, pan_number, 30
        
        # Calculate confidence
        confidence = 70  # Base confidence if number found
        confidence += min(keyword_matches * 5, 30)
        
        return True, pan_number, min(confidence, 100)
        
    except Exception as e:
        print(f"Error in pan_auth_img: {e}")
        import traceback
        traceback.print_exc()
        return False, "", 0

def pan_auth_number(number):
    """
    Validates PAN card number format and structure
    Returns: (is_valid_format, pan_number, confidence_score)
    """
    try:
        clean_number = number.strip().upper().replace(" ", "").replace("-", "")
        
        # Validate format
        regex = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        
        if len(clean_number) != 10 or not re.match(regex, clean_number):
            return False, "", 0
        
        # Validate PAN structure
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
            return False
        
        # Check 4th character is valid type
        valid_types = ['P', 'C', 'H', 'F', 'A', 'T', 'B', 'L', 'J', 'G']
        if pan[3] not in valid_types:
            return False
        
        # Check first 5 are letters
        if not pan[:5].isalpha():
            return False
        
        # Check middle 4 are digits
        if not pan[5:9].isdigit():
            return False
        
        # Check last is letter
        if not pan[9].isalpha():
            return False
        
        return True
    except:
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
