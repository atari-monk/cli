import pytest
from cli_app.cli_helpers import generate_string

def test_generate_string():
    # Test case 1: Basic string generation
    result = generate_string(5)
    assert result == "     "  # 5 spaces

    # Test case 2: Custom string generation
    result = generate_string(3, "*")
    assert result == "***"  # 3 stars

    # Test case 3: Exceeds max length
    with pytest.raises(ValueError):
        generate_string(1001)  # This will exceed the default max_length of 1000

    # Test case 4: Valid string with custom max length
    result = generate_string(1000, "*", 1000)
    assert result == "*" * 1000  # 1000 stars

    # Test case 5: String longer than max length
    with pytest.raises(ValueError):
        generate_string(1001, "*", 1000)  # Exceeds max_length
