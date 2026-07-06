"""
Agent registry that exposes each validation agent and its API key config.

The current implementation still uses deterministic validation tools, but the
registry makes it easy to swap each agent over to its own model/API key later.
"""
from typing import Dict, Any

from agent_config import get_agent_config
from tools import ValidationTools


class BaseValidationAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.config = get_agent_config(agent_name)
        self.tools = ValidationTools()

    def metadata(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "provider": self.config.provider,
            "model": self.config.model,
            "uses_api_key": bool(self.config.api_key),
        }


class EmailValidationAgent(BaseValidationAgent):
    def __init__(self):
        super().__init__("email")

    def validate(self, value: str):
        return self.tools.validate_email(value)


class PhoneValidationAgent(BaseValidationAgent):
    def __init__(self):
        super().__init__("phone")

    def validate(self, value: str):
        return self.tools.validate_phone(value)


class AgeValidationAgent(BaseValidationAgent):
    def __init__(self):
        super().__init__("age")

    def validate(self, value: str):
        return self.tools.validate_age(value)


class BloodGroupValidationAgent(BaseValidationAgent):
    def __init__(self):
        super().__init__("blood_group")

    def validate(self, value: str):
        return self.tools.validate_blood_group(value)


class DateValidationAgent(BaseValidationAgent):
    def __init__(self):
        super().__init__("date")

    def validate(self, value: str):
        return self.tools.validate_date(value)


class NameValidationAgent(BaseValidationAgent):
    def __init__(self):
        super().__init__("name")

    def validate(self, value: str):
        return self.tools.validate_name(value)


class ConsistencyValidationAgent(BaseValidationAgent):
    def __init__(self):
        super().__init__("consistency")

    def validate(self, data: Dict[str, Any]):
        return self.tools.consistency_check(data)
