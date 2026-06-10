from parsing.file_validator import FileValidator
from parsing.line_validator import LineValidator
from parsing.key_value_validator import KeyValueValidator
from typing import Any


def test_file_validator_valid(tmp_path: Any) -> None:
    d = tmp_path / "sub"
    d.mkdir()
    f = d / "config.txt"
    f.write_text("WIDTH=20\nHEIGHT=15")

    validator = FileValidator(str(f), "r")
    assert validator.is_validate is True
    assert validator.data == ["WIDTH=20\n", "HEIGHT=15"]


def test_file_validator_not_found() -> None:
    validator = FileValidator("non_existent_file.txt", "r")
    assert validator.is_validate is False
    assert any("FileNotFoundError" in err for err in validator.error)


def test_file_validator_invalid_permission() -> None:
    validator = FileValidator("config.txt", "x")
    assert validator.is_validate is False
    assert any("InvalidPermission" in err for err in validator.error)


def test_line_validator() -> None:
    lines = [
        "WIDTH=20\n",
        "\n",
        "# This is a comment\n",
        "HEIGHT=15 # Inline comment\n",
        "INVALID_LINE\n"
    ]
    validator = LineValidator(lines)
    assert validator.valid_lines == ["WIDTH=20", "HEIGHT=15"]
    assert validator.invalid_lines == ["INVALID_LINE"]
    assert validator.report["empty_lines"] == 1
    assert validator.report["comments"] == 2
    assert "This is a comment" in validator.comments
    assert "Inline comment" in validator.comments


def test_key_value_validator_valid(tmp_path: Any) -> None:
    maze_file = tmp_path / "maze.txt"
    valid_lines = [
        "WIDTH=20",
        "HEIGHT=15",
        "ENTRY=0,0",
        "EXIT=14,19",  # Row 14, Col 19. Valid for HEIGHT=15, WIDTH=20
        f"OUTPUT_FILE={maze_file}",
        "PERFECT=True"
    ]

    validator = KeyValueValidator(valid_lines)
    assert validator.is_validated is True
    assert validator.valid_dict["WIDTH"] == 20
    assert validator.valid_dict["HEIGHT"] == 15
    assert validator.valid_dict["ENTRY"] == (0, 0)
    assert validator.valid_dict["EXIT"] == (14, 19)


def test_key_value_validator_missing_keys() -> None:
    valid_lines = ["WIDTH=20"]
    validator = KeyValueValidator(valid_lines)
    assert validator.is_validated is False
    assert "HEIGHT" in validator.missing_keys
    assert "ENTRY" in validator.missing_keys


def test_key_value_validator_invalid_values() -> None:
    valid_lines = [
        "WIDTH=abc",
        "HEIGHT=15",
        "ENTRY=0,0",
        "EXIT=14,19",
        "OUTPUT_FILE=maze.txt",
        "PERFECT=maybe"
    ]
    validator = KeyValueValidator(valid_lines)
    assert "WIDTH" not in validator.valid_dict
    assert "PERFECT" not in validator.valid_dict
    assert "WIDTH" in validator.errors
    assert "PERFECT" in validator.errors


def test_key_value_validator_wide_maze() -> None:
    valid_lines = [
        "WIDTH=30",
        "HEIGHT=10",
        "ENTRY=0,29",  # Row 0, Col 29. Should pass.
        "EXIT=9,0",    # Row 9, Col 0. Should pass.
        "OUTPUT_FILE=maze.txt",
        "PERFECT=True"
    ]
    validator = KeyValueValidator(valid_lines)
    assert validator.is_validated is True
    assert validator.valid_dict["ENTRY"] == (0, 29)
    assert validator.valid_dict["EXIT"] == (9, 0)


def test_log_file(tmp_path: Any) -> None:
    from parsing.log_file import LogFile
    log_path = tmp_path / "test.log"
    LogFile(
        file=str(log_path),
        comments=["test comment"],
        invalid_lines=["invalid"],
        report={"empty_lines": 0, "comments": 1, "nosign": 1},
        non_valid_key={"BAD": "VAL"},
        non_valid_value={"WIDTH": "abc"},
        missing_keys=["HEIGHT"],
        valid_data={"PERFECT": True},
        display=False,
        errors={"WIDTH": "must be int"}
    )
    assert log_path.exists()
    content = log_path.read_text()
    assert "test comment" in content
    assert "BAD = VAL" in content
