from pathlib import Path
import re

DEFAULT_RULES_PATH = Path(__file__).resolve().parents[2] / "knowledge" / "rules.txt"


def load_rules(rule_path=None):
    path = Path(rule_path or DEFAULT_RULES_PATH)
    if not path.exists():
        return {}

    rules = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        field, rule_text = [part.strip() for part in line.split(":", 1)]
        field_name = re.sub(r"\s+", "_", field.lower())
        rule_map = {}
        for part in rule_text.split(";"):
            part = part.strip()
            if not part:
                continue
            if part.startswith("allowed_values="):
                rule_map["allowed_values"] = [value.strip() for value in part.split("=", 1)[1].split(",") if value.strip()]
            elif part == "required":
                rule_map["required"] = True
            elif part == "title_case":
                rule_map["title_case"] = True
            elif part == "valid_email":
                rule_map["format"] = "email"
            elif part == "exactly_10_digits":
                rule_map["format"] = "phone"
            elif part == "integer":
                rule_map["format"] = "integer"
        rules[field_name] = rule_map

    return rules


def retrieve_rules_for_input(raw_input, rule_path=None):
    rules = load_rules(rule_path)
    mandatory_fields = [field for field, config in rules.items() if config.get("required")]
    pii_fields = ["phone"]
    return {
        "mandatory_fields": mandatory_fields,
        "pii_fields": pii_fields,
        "field_rules": rules,
        "source": str(rule_path or DEFAULT_RULES_PATH),
    }
