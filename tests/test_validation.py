from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from autonomous_self_correcting_data_validation_system.validation import run_validation_pipeline


def test_sample_input_is_corrected_and_logged(tmp_path):
    sample = "Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad"
    result = run_validation_pipeline(sample, database_path=tmp_path / "validation.db")

    assert result["corrected_data"]["name"] == "John Doe"
    assert result["corrected_data"]["email"] == "john@gmail.com"
    assert result["corrected_data"]["phone"] is None
    assert result["corrected_data"]["age"] == 25
    assert result["corrected_data"]["blood_group"] == "Unknown"
    assert result["final_report"]["overall_confidence"] >= 0.9
    assert (tmp_path / "validation.db").exists()
