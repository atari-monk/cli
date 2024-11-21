import pytest
from shared.validator.validator import Validator

class TestValidator:
    # Test validate_length
    @pytest.mark.parametrize(
        "value, min_len, max_len, expected",
        [
            ("Hello", 3, 10, "Hello"),
            ("Valid input", 3, 50, "Valid input"),
            ("  Extra spaces  ", 3, 20, "Extra spaces"),
        ],
    )
    def test_validate_length_valid(self, value, min_len, max_len, expected):
        assert Validator.validate_length(value, min_len, max_len) == expected

    @pytest.mark.parametrize(
        "value, min_len, max_len",
        [
            ("Hi", 3, 50),
            ("", 3, 50),
            ("Too long value " * 10, 3, 20),
        ],
    )
    def test_validate_length_invalid(self, value, min_len, max_len):
        with pytest.raises(ValueError):
            Validator.validate_length(value, min_len, max_len)

    # Test validate_format
    @pytest.mark.parametrize(
        "value, expected",
        [
            ("Valid-input", "Valid-input"),
            ("Alphanumeric123", "Alphanumeric123"),
            ("_underscore", "_underscore"),
        ],
    )
    def test_validate_format_valid(self, value, expected):
        assert Validator.validate_format(value) == expected

    @pytest.mark.parametrize(
        "value",
        [
            "Invalid!Chars",
            "Symbols@$#",
            "New\nLine",
        ],
    )
    def test_validate_format_invalid(self, value):
        with pytest.raises(ValueError):
            Validator.validate_format(value)

    # Test validate_word_count
    @pytest.mark.parametrize(
        "value, min_words, expected",
        [
            ("One word", 1, "One word"),
            ("Two words here", 2, "Two words here"),
            ("Multiple valid words", 3, "Multiple valid words"),
        ],
    )
    def test_validate_word_count_valid(self, value, min_words, expected):
        assert Validator.validate_word_count(value, min_words) == expected

    @pytest.mark.parametrize(
        "value, min_words",
        [
            ("", 1),
            ("Single", 2),
            ("Few words", 5),
        ],
    )
    def test_validate_word_count_invalid(self, value, min_words):
        with pytest.raises(ValueError):
            Validator.validate_word_count(value, min_words)

    # Test validate_enum
    @pytest.mark.parametrize(
        "value, allowed_values, expected",
        [
            ("apple", ["apple", "banana", "cherry"], "apple"),
            ("cherry", ["apple", "banana", "cherry"], "cherry"),
        ],
    )
    def test_validate_enum_valid(self, value, allowed_values, expected):
        assert Validator.validate_enum(value, allowed_values) == expected

    @pytest.mark.parametrize(
        "value, allowed_values",
        [
            ("grape", ["apple", "banana", "cherry"]),
            ("", ["apple", "banana", "cherry"]),
        ],
    )
    def test_validate_enum_invalid(self, value, allowed_values):
        with pytest.raises(ValueError):
            Validator.validate_enum(value, allowed_values)

    # Test validate_name
    @pytest.mark.parametrize(
        "name, min_len, max_len, expected",
        [
            ("John Doe", 3, 50, "John Doe"),
            ("  Jane-Doe  ", 3, 50, "Jane-Doe"),
        ],
    )
    def test_validate_name_valid(self, name, min_len, max_len, expected):
        assert Validator.validate_name(name, min_len, max_len) == expected

    @pytest.mark.parametrize(
        "name, min_len, max_len",
        [
            ("Jo", 3, 50),
            ("Invalid@Name", 3, 50),
        ],
    )
    def test_validate_name_invalid(self, name, min_len, max_len):
        with pytest.raises(ValueError):
            Validator.validate_name(name, min_len, max_len)

    # Test validate_description
    @pytest.mark.parametrize(
        "description, min_len, min_words, expected",
        [
            ("A valid description", 10, 1, "A valid description"),
            ("  Properly formatted description  ", 10, 2, "Properly formatted description"),
        ],
    )
    def test_validate_description_valid(self, description, min_len, min_words, expected):
        assert Validator.validate_description(description, min_len, min_words) == expected

    @pytest.mark.parametrize(
        "description, min_len, min_words",
        [
            ("Short desc", 15, 2),
            ("Invalid characters @!", 10, 1),
        ],
    )
    def test_validate_description_invalid(self, description, min_len, min_words):
        with pytest.raises(ValueError):
            Validator.validate_description(description, min_len, min_words)
