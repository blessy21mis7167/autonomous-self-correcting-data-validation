"""
Data Validation Tools for CrewAI Agents
"""
import re
from datetime import datetime
from typing import Dict, Any, List, Tuple


class ValidationTools:
    """Tools for data validation and correction"""

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate and correct email addresses"""
        email = email.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return True, email
        
        # Try to auto-correct common mistakes
        if '@' not in email and '.' in email:
            parts = email.rsplit('.', 1)
            corrected = f"{parts[0]}@{parts[1]}"
            if re.match(pattern, corrected):
                return True, corrected
        
        return False, email

    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Validate and correct phone numbers"""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        # Check if it's a valid length
        if len(digits) >= 10:
            # Format as standard phone
            if len(digits) == 10:
                corrected = f"+1{digits}"
            else:
                corrected = f"+{digits[-12:]}"
            return True, corrected
        
        return False, phone

    @staticmethod
    def validate_age(age_input: str) -> Tuple[bool, int]:
        """Validate and correct age"""
        age_input = age_input.strip().lower()
        
        # Try to extract number from text
        numbers = re.findall(r'\d+', age_input)
        if numbers:
            age = int(numbers[0])
            if 0 < age < 150:
                return True, age
        
        # Map word numbers to digits
        word_numbers = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
            'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
            'ten': 10, 'eleven': 11, 'twelve': 12, 'twenty': 20,
            'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60
        }
        
        for word, num in word_numbers.items():
            if word in age_input:
                if 0 < num < 150:
                    return True, num
        
        return False, None

    @staticmethod
    def validate_blood_group(bg: str) -> Tuple[bool, str]:
        """Validate and correct blood group"""
        bg = bg.strip().upper().replace(' ', '')
        valid_groups = ['A', 'B', 'AB', 'O', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        if bg in valid_groups:
            return True, bg
        
        # Try to auto-correct
        if bg.replace('+', '').replace('-', '') in ['A', 'B', 'AB', 'O']:
            return True, bg
        
        return False, bg

    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """Validate and correct date formats"""
        date_str = date_str.strip()
        
        # Try common formats
        formats = ['%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d.%m.%Y', '%B %d, %Y', '%d %B %Y']
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_str, fmt)
                corrected = parsed.strftime('%d-%m-%Y')
                if parsed.year > 1900:
                    return True, corrected
            except ValueError:
                continue
        
        return False, date_str

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate and correct names"""
        name = name.strip()
        
        # Check if name contains only letters and spaces
        if re.match(r'^[a-zA-Z\s]+$', name):
            corrected = ' '.join(word.capitalize() for word in name.split())
            return True, corrected
        
        # Try to clean special characters
        cleaned = re.sub(r'[^a-zA-Z\s]', '', name).strip()
        if cleaned and len(cleaned.split()) > 0:
            corrected = ' '.join(word.capitalize() for word in cleaned.split())
            return True, corrected
        
        return False, name

    @staticmethod
    def extract_fields(raw_text: str) -> Dict[str, Any]:
        """Extract all potential fields from messy input"""
        text_lower = raw_text.lower()
        fields = {}
        
        # Extract name
        name_match = re.search(r'name\s*:?\s*([^,\n]+)', text_lower)
        if name_match:
            fields['name'] = name_match.group(1).strip()
        
        # Extract email
        email_pattern = r'email\s*:?\s*([^\s,\n]+)'
        email_match = re.search(email_pattern, text_lower)
        if email_match:
            fields['email'] = email_match.group(1).strip()
        
        # Extract phone
        phone_pattern = r'(phone|contact|mobile)\s*:?\s*([^\s,\n]+)'
        phone_match = re.search(phone_pattern, text_lower)
        if phone_match:
            fields['phone'] = phone_match.group(2).strip()
        
        # Extract age
        age_pattern = r'age\s*:?\s*([^\s,\n]+)'
        age_match = re.search(age_pattern, text_lower)
        if age_match:
            fields['age'] = age_match.group(1).strip()
        
        # Extract blood group
        bg_pattern = r'(blood\s*group|blood\s*type|bg)\s*:?\s*([^\s,\n]+)'
        bg_match = re.search(bg_pattern, text_lower)
        if bg_match:
            fields['blood_group'] = bg_match.group(2).strip()
        
        # Extract date
        date_pattern = r'(date|dob|birth)\s*:?\s*([^\s,\n]+)'
        date_match = re.search(date_pattern, text_lower)
        if date_match:
            fields['date'] = date_match.group(2).strip()
        
        # Extract address
        address_pattern = r'(address|location|city)\s*:?\s*([^,\n]+)'
        address_match = re.search(address_pattern, text_lower)
        if address_match:
            fields['address'] = address_match.group(2).strip()
        
        return fields

    @staticmethod
    def consistency_check(data: Dict[str, Any]) -> Dict[str, Any]:
        """Check consistency of data"""
        issues = {}
        
        # Check age vs DOB consistency
        if 'age' in data and 'date' in data:
            try:
                if isinstance(data['age'], int):
                    issues['age_dob_consistency'] = "Age and DOB present - verify they match"
            except:
                pass
        
        return issues
