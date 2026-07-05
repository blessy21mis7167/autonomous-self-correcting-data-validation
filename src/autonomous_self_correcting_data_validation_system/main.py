#!/usr/bin/env python
import sys
from autonomous_self_correcting_data_validation_system.validation import run_validation_pipeline


def run():

    sample_input = """
    Name : john doe
    Email : john@gmail
    Phone : 9876543
    Age : twenty five
    Blood Group : ABC
    Address : Hyderabad
    """

    crew = AutonomousSelfCorrectingDataValidationSystemCrew()

    result = crew.crew().kickoff(
        inputs={
            "raw_input": sample_input
        }
    )

    print(result)


def train():
    raise NotImplementedError("Training is not required for the deterministic local workflow")


def replay():
    raise NotImplementedError("Replay is not required for the deterministic local workflow")


def test():
    raise NotImplementedError("Use pytest for regression tests")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

from autonomous_self_correcting_data_validation_system.crew import AutonomousSelfCorrectingDataValidationSystemCrew
