import pytest
from cli_app.command_loader import discover_folders_with_commands

@pytest.fixture
def setup_test_environment(tmp_path):
    """
    Creates a temporary folder structure for testing.
    """
    # Create folder structure
    (tmp_path / "folder1").mkdir()
    (tmp_path / "folder1" / "__init__.py").touch()
    (tmp_path / "folder2").mkdir()
    (tmp_path / "folder2" / "__init__.py").touch()
    (tmp_path / "cli_app").mkdir()
    (tmp_path / "cli_app" / "__init__.py").touch()
    (tmp_path / "shared").mkdir()
    (tmp_path / "shared" / "__init__.py").touch()
    (tmp_path / "nested" / "folder3").mkdir(parents=True)
    (tmp_path / "nested" / "folder3" / "__init__.py").touch()

    return tmp_path

def test_discover_folders_with_commands(setup_test_environment):
    """
    Tests the `discover_folders_with_commands` function with a mock directory structure.
    """
    root_path = setup_test_environment

    # Test with default ignored folders
    result = discover_folders_with_commands(src_folder_with_commands=str(root_path))
    expected = ["folder1", "folder2", "folder3"]  # Excludes ignored folders
    assert sorted(result) == sorted(expected)

    # Test with custom ignored folders
    result = discover_folders_with_commands(
        src_folder_with_commands=str(root_path),
        ignore_these_folders=["folder1", "folder2"]
    )
    expected = ["folder3","cli_app", "shared"]
    assert sorted(result) == sorted(expected)

    # Test with no ignored folders
    result = discover_folders_with_commands(
        src_folder_with_commands=str(root_path),
        ignore_these_folders=[]
    )
    expected = ["folder1", "folder2", "folder3", "cli_app", "shared"]  # All folders should be included
    assert sorted(result) == sorted(expected)

def test_empty_directory(tmp_path):
    """
    Tests the function with an empty directory.
    """
    result = discover_folders_with_commands(src_folder_with_commands=str(tmp_path))
    assert result == []

def test_no_init_files(tmp_path):
    """
    Tests the function when no `__init__.py` files are present.
    """
    (tmp_path / "folder1").mkdir()
    (tmp_path / "folder2").mkdir()
    result = discover_folders_with_commands(src_folder_with_commands=str(tmp_path))
    assert result == []

def test_nested_directories_with_init(tmp_path):
    """
    Tests nested directories containing `__init__.py`.
    """
    (tmp_path / "nested" / "folder1").mkdir(parents=True)
    (tmp_path / "nested" / "folder1" / "__init__.py").touch()
    result = discover_folders_with_commands(src_folder_with_commands=str(tmp_path))
    assert result == ["folder1"]
