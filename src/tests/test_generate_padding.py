from cli_app.cli_helpers import generate_padding

def test_generate_padding():
    # Test case 1: Basic padding generation
    result = generate_padding(10, "Hello")
    assert result == "     "  # 10 - 5 (length of "Hello") = 5 spaces

    # Test case 2: No padding needed
    result = generate_padding(5, "Hello")
    assert result == ""  # No padding needed, as length of "Hello" is 5

    # Test case 3: Padding for an empty string
    result = generate_padding(8, "")
    assert result == "        "  # 8 - 0 (length of "") = 8 spaces

    # Test case 4: Padding for a string longer than the specified length
    result = generate_padding(3, "LongString")
    assert result == ""  # Length of "LongString" is greater than 3, no padding

    # Test case 5: Padding for a string of length 1
    result = generate_padding(5, "X")
    assert result == "    "  # 5 - 1 (length of "X") = 4 spaces

    # Test case 6: Padding with large numbers
    result = generate_padding(1000, "Test")
    assert result == " " * 996  # 1000 - 4 (length of "Test") = 996 spaces

    # Test case 7: Padding for a string of length 0
    result = generate_padding(3, "A")
    assert result == " " * 2  # 3 - 1 (length of "A") = 2 spaces
