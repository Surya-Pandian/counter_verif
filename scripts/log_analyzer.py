import os
import pandas as pd
import yaml


CONFIG_FILE = "../config/test_config.yaml"
LOG_DIR = "../logs"
REPORT_DIR = "../reports"


def main():
    # Load test configuration
    with open(CONFIG_FILE, "r") as file:
        config = yaml.safe_load(file)

    test_names = [test["name"] for test in config["tests"]]

    summary = []

    # Analyze each configured test
    for test_name in test_names:
        log_file = os.path.join(LOG_DIR, f"{test_name}.log")

        if not os.path.exists(log_file):
            summary.append({
                "test": test_name,
                "errors": 0,
                "warnings": 0,
                "fatals": 0,
                "result": "MISSING"
            })
            continue

        with open(log_file, "r") as file:
            content = file.read()

        info_count = content.count("UVM_INFO")
        warning_count = content.count("UVM_WARNING")
        error_count = content.count("UVM_ERROR")
        fatal_count = content.count("UVM_FATAL")

        result = "UNKNOWN"

        for line in content.splitlines():
            if "TEST_CASE" in line and "RESULT: PASSED" in line:
                result = "PASSED"
            elif "TEST_CASE" in line and "RESULT: FAILED" in line:
                result = "FAILED"

        summary.append({
            "test": test_name,
            "errors": error_count,
            "warnings": warning_count,
            "fatals": fatal_count,
            "result": result
        })

    # Create reports directory
    os.makedirs(REPORT_DIR, exist_ok=True)

    # Create DataFrame
    df = pd.DataFrame(summary)

    # Write CSV report
    df.to_csv(
        os.path.join(REPORT_DIR, "summary.csv"),
        index=False
    )

    # Write Excel report
    df.to_excel(
        os.path.join(REPORT_DIR, "summary.xlsx"),
        index=False
    )

    # Write YAML report
    with open(os.path.join(REPORT_DIR, "summary.yaml"), "w") as file:
        yaml.dump(
            summary,
            file,
            default_flow_style=False,
            sort_keys=False
        )

    print("Log analysis complete.")
    print(f"UVM_INFO count collected internally for {len(test_names)} tests.")
    print(f"Reports generated in: {REPORT_DIR}/")


if __name__ == "__main__":
    main()
