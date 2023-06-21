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
dummy_src = os.path.join(os.getcwd(), "Temp_src")
dummy_des = os.path.join(os.getcwd(), "Temp_des")
dummy_dirs = ["A", "B", "C"]
dummy_files = ["A.txt", "B.png", "C.bin", "D.jpg"]


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
        """
        Test the filepath must be a string
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=1
            )

    def test_include_extension_not_list(self):
        """
        Test that included extensions must be a list
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=dummy_src,
                include_extensions="A"
            )

    def test_exclude_extension_not_list(self):
        """
        Test that excluded extensions must be a list
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=dummy_src,
                exclude_extensions="A"
            )

    def test_include_extension_contains_not_str(self):
        """
        Test that all included extensions must be strings
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=dummy_src,
                include_extensions=["A", 1]
            )

    def test_exclude_extensions_contains_not_str(self):
        """
        Test that all excluded extensions must be strings
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.get_files(
                filepath=dummy_src,
                exclude_extensions=["A", 1]
            )


@pytest.fixture()
def single_dummy_dir():
    """
    Filepath for first dummy directory
    """
    return os.path.join(dummy_src, dummy_dirs[0])


class TestGetFiles:
    """
    Tests that get files method returns appropriate output
    """
    @classmethod
    def setup_class(cls):
        """
        Populates the source directory with dummy data
        """
        for dummy_dir in dummy_dirs:
            dummy_filepath = os.path.join(dummy_src, dummy_dir)
            os.makedirs(dummy_filepath, exist_ok=True)
            for dummy_file in dummy_files:
                with open(os.path.join(dummy_filepath, dummy_file), "w"):
                    pass

    @classmethod
    def teardown_class(cls):
        """
        Clears the source directory of dummy data
        """
        for dummy_dir in dummy_dirs:
            dummy_filepath = os.path.join(dummy_src, dummy_dir)
            shutil.rmtree(dummy_filepath)

    @pytest.fixture(autouse=True)
    def _get_single_dummy_dir(self, single_dummy_dir):
        """
        Returns the single dummy directory fixture
        """
        self.single_directory = single_dummy_dir

    def test_get_single_directory(self):
        """
        Tests to make sure that all filenames are retrieved from a single directory and that filepaths are assembled correctly
        """
        filenames, filepaths = file_transfer.get_files(self.single_directory)
        if not all([filename in dummy_files for filename in filenames]):
            raise Exception("get_files did not return all files from single directory")
        elif not all([os.path.exists(filepath) for filepath in filepaths]):
            raise Exception("get_files did not return correct filepaths from single directory")
        
    def test_get_single_directory_inclusion_single(self):
        """
        Tests that specifying a single file extensions inclusion retrieves correct file
        """
        test_extension = "txt"
        filenames, _ = file_transfer.get_files(
            filepath=self.single_directory,
            include_extensions=[test_extension]
        )
        if not all([filename in [dummy_file for dummy_file in dummy_files if test_extension in dummy_file] for filename in filenames]):
            raise Exception("get_files did not only include specified extension from single directory")
        
    def test_get_single_directory_inclusion_multiple(self):
        """
        Tests that specifying multiple file extension inclusions retrieves correct files
        """
        test_extensions = ["txt", "png"]
        filenames, _ = file_transfer.get_files(
            filepath=self.single_directory,
            include_extensions=test_extensions
        )
        if not all([filename in [dummy_file for dummy_file in dummy_files if any([test_extension in dummy_file for test_extension in test_extensions])] for filename in filenames]):
            raise Exception("get_files did not retrieve all specified extensions from single directory")
        
    def test_get_single_directory_exclude_single(self):
        """
        Tests that specifying a single file extension excludes correct file
        """
        test_extension = "txt"
        filenames, _ = file_transfer.get_files(
            filepath=self.single_directory,
            exclude_extensions=[test_extension]
        )
        if not all([filename in [dummy_file for dummy_file in dummy_files if test_extension not in dummy_file] for filename in filenames]):
            raise Exception("get_files did not exclude specified extension from single directory")
        
    def test_get_single_directory_exclude_multiple(self):
        """
        Tests that specifying multiple file extensions excludes correct files
        """
        test_extensions = ["txt", "png"]
        filenames, _ = file_transfer.get_files(
            filepath=self.single_directory,
            exclude_extensions=test_extensions
        )
        if not all([filename in [dummy_file for dummy_file in dummy_files if all([test_extension not in dummy_file for test_extension in test_extensions])] for filename in filenames]):
            raise Exception("get_files did not exclude all specified extensions from single directory")

    def test_get_directory(self):
        """
        Tests to make sure that all filenames are retrieved from whole directory and that filepaths are assembled correctly
        """
        filenames, filepaths = file_transfer.get_files(dummy_src)
        if not len(filenames) == 12:
            raise Exception("get_files did not return correct number of files from directory")
        elif not all([os.path.exists(filepath) for filepath in filepaths]):
            raise Exception("get_files did no return correct number of files from directory")

    def test_get_directory_include(self):
        """
        Tests to make sure that all filenames are retrieved from whole directory with file extension inclusion
        """
        test_extensions = ["txt", "png"]
        filenames, _ = file_transfer.get_files(
            filepath=dummy_src,
            include_extensions=test_extensions
        )
        if not len(filenames) == 6:
            raise Exception("get_files did not return correct number of files from directory with included file extension")
        elif not all([filename.split('.')[-1] in test_extensions for filename in filenames]):
            raise Exception("get_files did not return correct files with specified file extension inclusion from whole directory")
        
    def test_get_directory_exclude(self):
        """
        Tests to make sure that all filenames are retrieved from whole directory with file extension exclusion
        """
        test_extensions = ["txt", "png"]
        filenames, _ = file_transfer.get_files(
            filepath=dummy_src,
            exclude_extensions=test_extensions
        )
        if not len(filenames) == 6:
            raise Exception("get_files did not return correct number of files from directory with excluded file extension")
        elif not all([filename.split('.')[-1] in [extension for extension in [dummy_file.split(".")[-1] for dummy_file in dummy_files] if extension not in test_extensions] for filename in filenames]):
            raise Exception("get_files did not return correct files with specified file extension inclusion from whole directory")


class TestTransferFilesAssertions:
    """
    Tests that transfer files method returns assertion errors for edge cases
    """
    def test_src_filepath_not_str(self):
        """
        Test the src filepath must be a string
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.transfer_files(
                src=1,
                des="A"
            )

    def test_des_filepath_not_str(self):
        """
        Test the des filepath must be a string
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.transfer_files(
                src="A",
                des=1
            )

    def test_include_extension_not_list(self):
        """
        Test that included extensions must be a list
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.transfer_files(
                src=dummy_src,
                des=dummy_des,
                include_extensions="A"
            )

    def test_exclude_extension_not_list(self):
        """
        Test that excluded extensions must be a list
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.transfer_files(
                src=dummy_src,
                des=dummy_des,
                exclude_extensions="A"
            )

    def test_include_extension_contains_not_str(self):
        """
        Test that all included extensions must be strings
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.transfer_files(
                src=dummy_src,
                des=dummy_des,
                include_extensions=["A", 1]
            )

    def test_exclude_extensions_contains_not_str(self):
        """
        Test that all excluded extensions must be strings
        """
        with pytest.raises(AssertionError):
            _ = file_transfer.transfer_files(
                src=dummy_src,
                des=dummy_des,
                exclude_extensions=["A", 1]
            )
