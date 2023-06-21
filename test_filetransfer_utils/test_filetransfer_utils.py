"""
Unit testing of the file_transfer package
"""
# Standard Imports
import os
import shutil
import pytest

# Local Imports
import filetransfer_utils.file_transfer as file_transfer

# Environment variables
dummy_src = "Temp_src"
dummy_des = "Temp_des"


def setup_module():
    """
    Sets up a dummy source and destination folderpaths for unit testing
    """
    # Prepare source and destination filepaths
    os.makedirs(dummy_src, exist_ok=True)
    os.makedirs(dummy_des, exist_ok=True)


def teardown_module():
    """
    Tears down the dummy source and destination folderpaths for unit testing
    """
    # Delete all temporary files and folders from source and destination filepaths
    shutil.rmtree(dummy_src)
    shutil.rmtree(dummy_des)


class TestGetFilesAssertions:
    """
    Tests that get files method returns assertion errors for edge cases
    """
    def test_filepath_not_str(self):
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=1
            )

    def test_include_extension_not_list(self):
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=dummy_src,
                include_file_extensions="A"
            )

    def test_exclude_extension_not_list(self):
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=dummy_src,
                exclude_file_extensions="A"
            )

    def test_include_extension_contains_not_str(self):
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=dummy_src,
                include_file_extensions=["A", 1]
            )

    def test_exclude_extensions_contains_not_str(self):
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=dummy_src,
                exclude_file_extensions=["A", 1]
            )
