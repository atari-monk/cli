from cli_app.command_runner import parse_input

def test_single_command():
    assert parse_input("command") == ("command", [])

def test_command_with_arguments():
    assert parse_input("command arg1 arg2 arg3") == ("command", ["arg1", "arg2", "arg3"])

def test_command_with_quoted_argument():
    assert parse_input('command "arg2 is a string with spaces"') == ("command", ["arg2 is a string with spaces"])

def test_command_with_mixed_arguments():
    assert parse_input('command arg1 "arg2 is a string with spaces" arg3') == (
        "command",
        ["arg1", "arg2 is a string with spaces", "arg3"],
    )

def test_empty_input():
    assert parse_input("") == ("", [])

def test_whitespace_only_input():
    assert parse_input("    ") == ("", [])

def test_command_with_escaped_quotes():
    assert parse_input('command "arg with \\"embedded quotes\\""') == (
        "command",
        ['arg with "embedded quotes"'],
    )

def test_command_with_nested_quotes():
    assert parse_input('command "outer \\"inner quote\\" example"') == (
        "command",
        ['outer "inner quote" example'],
    )

def test_command_with_single_quote():
    assert parse_input("command 'single quoted arg'") == ("command", ["single quoted arg"])

def test_command_with_mixed_quotes():
    assert parse_input('command "double quoted" \'single quoted\'') == (
        "command",
        ["double quoted", "single quoted"],
    )

def test_command_with_special_characters():
    assert parse_input('command arg1 "@#$%^&*()"') == ("command", ["arg1", "@#$%^&*()"])

def test_no_arguments_but_whitespace_after_command():
    assert parse_input("command    ") == ("command", [])

def test_command_with_whitespace_before_and_after():
    assert parse_input("   command arg1   arg2   ") == ("command", ["arg1", "arg2"])
