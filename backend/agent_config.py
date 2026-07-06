"""
Per-agent API key configuration for validation agents.

This module centralizes the environment variable mapping so each agent can
use a different API key or provider configuration if you later swap the
rule-based logic for model-backed calls.
"""
from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


@dataclass(frozen=True)
class AgentConfig:
    name: str
    api_key: Optional[str]
    model: Optional[str]
    provider: str


AGENT_ENV_MAP = {
    "email": {"key": "EMAIL_AGENT_API_KEY", "model": "EMAIL_AGENT_MODEL", "provider": "EMAIL_AGENT_PROVIDER"},
    "phone": {"key": "PHONE_AGENT_API_KEY", "model": "PHONE_AGENT_MODEL", "provider": "PHONE_AGENT_PROVIDER"},
    "age": {"key": "AGE_AGENT_API_KEY", "model": "AGE_AGENT_MODEL", "provider": "AGE_AGENT_PROVIDER"},
    "blood_group": {"key": "BLOOD_GROUP_AGENT_API_KEY", "model": "BLOOD_GROUP_AGENT_MODEL", "provider": "BLOOD_GROUP_AGENT_PROVIDER"},
    "date": {"key": "DATE_AGENT_API_KEY", "model": "DATE_AGENT_MODEL", "provider": "DATE_AGENT_PROVIDER"},
    "name": {"key": "NAME_AGENT_API_KEY", "model": "NAME_AGENT_MODEL", "provider": "NAME_AGENT_PROVIDER"},
    "consistency": {"key": "CONSISTENCY_AGENT_API_KEY", "model": "CONSISTENCY_AGENT_MODEL", "provider": "CONSISTENCY_AGENT_PROVIDER"},
}


@lru_cache(maxsize=1)
def get_agent_configs() -> Dict[str, AgentConfig]:
    configs: Dict[str, AgentConfig] = {}
    for agent_name, env_names in AGENT_ENV_MAP.items():
        configs[agent_name] = AgentConfig(
            name=agent_name,
            api_key=os.getenv(env_names["key"]),
            model=os.getenv(env_names["model"]),
            provider=os.getenv(env_names["provider"], "openai"),
        )
    return configs


def get_agent_config(agent_name: str) -> AgentConfig:
    configs = get_agent_configs()
    if agent_name not in configs:
        raise KeyError(f"Unknown agent: {agent_name}")
    return configs[agent_name]
