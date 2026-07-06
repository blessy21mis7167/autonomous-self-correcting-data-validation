"""
Validation engine using CrewAI agents
"""
from typing import Dict, Any
from datetime import datetime
from tools import ValidationTools
from database import save_validation_result, save_escalation
from agent_registry import (
    EmailValidationAgent,
    PhoneValidationAgent,
    AgeValidationAgent,
    BloodGroupValidationAgent,
    DateValidationAgent,
    NameValidationAgent,
    ConsistencyValidationAgent,
)


class DataValidationEngine:
    """Main validation engine orchestrating multiple agents"""
    
    def __init__(self):
        self.tools = ValidationTools()
        self.confidence_threshold = 0.8  # Escalate if confidence below this
        self.email_agent = EmailValidationAgent()
        self.phone_agent = PhoneValidationAgent()
        self.age_agent = AgeValidationAgent()
        self.blood_group_agent = BloodGroupValidationAgent()
        self.date_agent = DateValidationAgent()
        self.name_agent = NameValidationAgent()
        self.consistency_agent = ConsistencyValidationAgent()
        
    def validate_and_correct(self, raw_input: str) -> Dict[str, Any]:
        """
        Main validation pipeline
        1. Extract fields
        2. Validate each field type
        3. Correct errors
        4. Check consistency
        5. Escalate uncertain fields
        """
        
        # Step 1: Extract fields from messy input
        extracted_fields = self.tools.extract_fields(raw_input)
        
        corrected_data = {}
        validation_errors = {}
        correction_log = []
        confidence_scores = {}
        escalations = []
        
        # Step 2: Agent 1 - Email Validator
        if 'email' in extracted_fields:
            is_valid, corrected = self.email_agent.validate(extracted_fields['email'])
            confidence = 0.95 if is_valid else 0.3
            confidence_scores['email'] = confidence
            corrected_data['email'] = corrected
            
            if not is_valid:
                validation_errors['email'] = f"Invalid email: {extracted_fields['email']}"
                correction_log.append({
                    'field': 'email',
                    'original': extracted_fields['email'],
                    'corrected': corrected,
                    'reason': 'Invalid email format'
                })
                if confidence < self.confidence_threshold:
                    escalations.append({
                        'field': 'email',
                        'original': extracted_fields['email'],
                        'corrected': corrected,
                        'confidence': confidence,
                        'reason': 'Low confidence in correction'
                    })
            else:
                if extracted_fields['email'] != corrected:
                    correction_log.append({
                        'field': 'email',
                        'original': extracted_fields['email'],
                        'corrected': corrected,
                        'reason': 'Format correction'
                    })
        
        # Step 3: Agent 2 - Phone Validator
        if 'phone' in extracted_fields:
            is_valid, corrected = self.phone_agent.validate(extracted_fields['phone'])
            confidence = 0.9 if is_valid else 0.2
            confidence_scores['phone'] = confidence
            corrected_data['phone'] = corrected
            
            if not is_valid:
                validation_errors['phone'] = f"Invalid phone: {extracted_fields['phone']}"
                if confidence < self.confidence_threshold:
                    escalations.append({
                        'field': 'phone',
                        'original': extracted_fields['phone'],
                        'corrected': corrected,
                        'confidence': confidence,
                        'reason': 'Invalid phone format'
                    })
        
        # Step 4: Agent 3 - Age Validator
        if 'age' in extracted_fields:
            is_valid, corrected = self.age_agent.validate(extracted_fields['age'])
            confidence = 0.85 if is_valid else 0.4
            confidence_scores['age'] = confidence
            
            if is_valid:
                corrected_data['age'] = corrected
                if extracted_fields['age'] != str(corrected):
                    correction_log.append({
                        'field': 'age',
                        'original': extracted_fields['age'],
                        'corrected': corrected,
                        'reason': 'Text to number conversion'
                    })
            else:
                validation_errors['age'] = f"Could not parse age: {extracted_fields['age']}"
                if confidence < self.confidence_threshold:
                    escalations.append({
                        'field': 'age',
                        'original': extracted_fields['age'],
                        'corrected': None,
                        'confidence': confidence,
                        'reason': 'Unable to parse age value'
                    })
        
        # Step 5: Agent 4 - Blood Group Validator
        if 'blood_group' in extracted_fields:
            is_valid, corrected = self.blood_group_agent.validate(extracted_fields['blood_group'])
            confidence = 0.95 if is_valid else 0.2
            confidence_scores['blood_group'] = confidence
            corrected_data['blood_group'] = corrected
            
            if not is_valid:
                validation_errors['blood_group'] = f"Invalid blood group: {extracted_fields['blood_group']}"
                if confidence < self.confidence_threshold:
                    escalations.append({
                        'field': 'blood_group',
                        'original': extracted_fields['blood_group'],
                        'corrected': corrected,
                        'confidence': confidence,
                        'reason': 'Invalid blood group'
                    })
        
        # Step 6: Agent 5 - Date Validator
        if 'date' in extracted_fields:
            is_valid, corrected = self.date_agent.validate(extracted_fields['date'])
            confidence = 0.9 if is_valid else 0.1
            confidence_scores['date'] = confidence
            corrected_data['date'] = corrected
            
            if not is_valid:
                validation_errors['date'] = f"Could not parse date: {extracted_fields['date']}"
                if confidence < self.confidence_threshold:
                    escalations.append({
                        'field': 'date',
                        'original': extracted_fields['date'],
                        'corrected': corrected,
                        'confidence': confidence,
                        'reason': 'Unrecognized date format'
                    })
        
        # Step 7: Agent 6 - Name Validator
        if 'name' in extracted_fields:
            is_valid, corrected = self.name_agent.validate(extracted_fields['name'])
            confidence = 0.85 if is_valid else 0.3
            confidence_scores['name'] = confidence
            corrected_data['name'] = corrected
            
            if extracted_fields['name'] != corrected and is_valid:
                correction_log.append({
                    'field': 'name',
                    'original': extracted_fields['name'],
                    'corrected': corrected,
                    'reason': 'Capitalization correction'
                })
        
        # Step 8: Copy other fields
        for field in extracted_fields:
            if field not in corrected_data:
                corrected_data[field] = extracted_fields[field]
        
        # Step 9: Agent 7 - Consistency Checker
        consistency_issues = self.consistency_agent.validate(corrected_data)
        if consistency_issues:
            validation_errors.update(consistency_issues)
        
        # Step 10: Generate final report
        final_report = {
            'total_fields': len(extracted_fields),
            'corrected_fields': len(correction_log),
            'validation_errors': len(validation_errors),
            'escalations': len(escalations),
            'average_confidence': sum(confidence_scores.values()) / len(confidence_scores) if confidence_scores else 0,
            'timestamp': datetime.now().isoformat(),
            'status': 'requires_review' if escalations else 'completed'
        }
        
        return {
            'corrected_data': corrected_data,
            'validation_errors': validation_errors,
            'correction_log': correction_log,
            'confidence_scores': confidence_scores,
            'escalations': escalations,
            'final_report': final_report,
            'agent_metadata': {
                'email': self.email_agent.metadata(),
                'phone': self.phone_agent.metadata(),
                'age': self.age_agent.metadata(),
                'blood_group': self.blood_group_agent.metadata(),
                'date': self.date_agent.metadata(),
                'name': self.name_agent.metadata(),
                'consistency': self.consistency_agent.metadata(),
            }
        }


# Global instance
validation_engine = DataValidationEngine()


def run_validation_pipeline(raw_input: str) -> Dict[str, Any]:
    """Execute the validation pipeline"""
    result = validation_engine.validate_and_correct(raw_input)
    
    # Save to database
    validation_id = save_validation_result(
        raw_input,
        result['corrected_data'],
        result['validation_errors'],
        result['confidence_scores'],
        result['final_report']
    )
    
    # Save escalations
    for escalation in result['escalations']:
        save_escalation(
            validation_id,
            escalation['field'],
            escalation['original'],
            escalation['corrected'],
            escalation['confidence'],
            escalation['reason']
        )
    
    result['validation_id'] = validation_id
    return result
