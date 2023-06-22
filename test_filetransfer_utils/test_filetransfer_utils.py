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


def populate_src_dummy_dir():
    """
    Populates the source dummy directoy
    """
    for dummy_dir in dummy_dirs:
        dummy_filepath = os.path.join(dummy_src, dummy_dir)
        os.makedirs(dummy_filepath, exist_ok=True)
        for dummy_file in dummy_files:
            with open(os.path.join(dummy_filepath, dummy_file), "w"):
                pass


def clear_src_des_dummy_dirs():
    """
    Clears the source and destination dummy directories
    """
    for dummy_dir in dummy_dirs:
        dummy_src_filepath = os.path.join(dummy_src, dummy_dir)
        try:
            shutil.rmtree(dummy_src_filepath)
        except FileNotFoundError:
            pass
        dummy_des_filepath = os.path.join(dummy_des, dummy_dir)
        try:
            shutil.rmtree(dummy_des_filepath)
        except FileNotFoundError:
            pass


class TestDropPeriodExtensions:
    """
    Tests that drop period extensions method returns correct file extensions
    """

    def test_correct_extensions(self):
        """
        Tests that correct extensions are not modified
        """
        file_extensions = ["txt", "png"]
        modified_extensions = file_transfer.drop_period_extension(file_extensions)
        assert modified_extensions == file_extensions

    def test_incorrect_extensions(self):
        """
        Tests that incorrect extensions are modified
        """
        file_extensions = [".txt", ".png"]
        modified_extensions = file_transfer.drop_period_extension(file_extensions)
        assert modified_extensions == ["txt", "png"]


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
        populate_src_dummy_dir()

    @classmethod
    def teardown_class(cls):
        """
        Clears the source directory of dummy data
        """
        clear_src_des_dummy_dirs()

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


@pytest.fixture()
def src_des_single_dummy_dir():
    """
    Filepath for first source and destination dummy directories
    """
    return os.path.join(dummy_src, dummy_dirs[0]), os.path.join(dummy_des, dummy_dirs[0])


class TestTransferFiles:
    """
    Test the transfer files method
    """
    @pytest.fixture(autouse=True)
    def _get_single_dummy_dir(self, src_des_single_dummy_dir):
        """
        Returns the single dummy directory fixture
        """
        self.src_single_directory, self.des_single_directory = src_des_single_dummy_dir

    def setup_method(test_transfer_single_directory):
        """
        Populates the source directory with dummy data
        """
        populate_src_dummy_dir()

    def teardown_method(test_transfer_single_directory):
        """
        Clears the source directory of dummy data
        """
        clear_src_des_dummy_dirs()

    def test_transfer_single_directory(self):
        """
        Tests that all files are transferred from one directory to another
        """
        file_transfer.transfer_files(self.src_single_directory, self.des_single_directory)
        filenames, _ = file_transfer.get_files(self.des_single_directory)
        if not all([dummy_file in filenames for dummy_file in dummy_files]):
            raise Exception("transfer_files did not transfer all files from single directory")

    def setup_method(test_transfer_single_directory_inclusion):
        """
        Populates the source directory with dummy data
        """
        populate_src_dummy_dir()

    def teardown_method(test_transfer_single_directory_inclusion):
        """
        Clears the source directory of dummy data
        """
        clear_src_des_dummy_dirs()

    def test_transfer_single_directory_inclusion(self):
        """
        Tests that all files are transferred from one directory to another with inclusion specified
        """
        test_extensions = ["txt", "png"]
        file_transfer.transfer_files(
            src=self.src_single_directory,
            des=self.des_single_directory,
            include_extensions=test_extensions
        )
        filenames, _ = file_transfer.get_files(self.des_single_directory)
        if not all([dummy_file in filenames for dummy_file in [file for file in dummy_files if file.split(".")[-1] in test_extensions]]):
            raise Exception("transfer_files did not transfer all files from single directory with inclusion specified")

    def setup_method(test_transfer_single_directory_exclusion):
        """
        Populates the source directory with dummy data
        """
        populate_src_dummy_dir()

    def teardown_method(test_transfer_single_directory_exclusion):
        """
        Clears the source directory of dummy data
        """
        clear_src_des_dummy_dirs()

    def test_transfer_single_directory_exclusion(self):
        """
        Tests that all files are transferred from one directory to another with exclusion specified
        """
        test_extensions = ["txt", "png"]
        file_transfer.transfer_files(
            src=self.src_single_directory,
            des=self.des_single_directory,
            exclude_extensions=test_extensions
        )
        filenames, _ = file_transfer.get_files(self.des_single_directory)
        if not all([dummy_file in filenames for dummy_file in [file for file in dummy_files if file.split(".")[-1] not in test_extensions]]):
            raise Exception("transfer_files did not transfer all files from single directory with exclusion specified")

    def setup_method(test_transfer_directory):
        """
        Populates the source directory with dummy data
        """
        populate_src_dummy_dir()

    def teardown_method(test_transfer_directory):
        """
        Clears the source directory of dummy data
        """
        clear_src_des_dummy_dirs()

    def test_transfer_directory(self):
        """
        Tests that all files and folder structure are transferred from one directory to another
        """
        file_transfer.transfer_files(dummy_src, dummy_des)
        _, filepaths = file_transfer.get_files(dummy_des)
        if len(filepaths) != 12:
            raise Exception("transfer_files did not transfer all files")
        elif len([os.path.basename(os.path.dirname(filepath)) == "A" for filepath in filepaths]) == 4:
            raise Exception("transfer_files did not transfer folder structure")

    def setup_method(test_transfer_directory_inclusion):
        """
        Populates the source directory with dummy data
        """
        populate_src_dummy_dir()

    def teardown_method(test_transfer_directory_inclusion):
        """
        Clears the source directory of dummy data
        """
        clear_src_des_dummy_dirs()

    def test_transfer_directory_inclusion(self):
        """
        Tests that all files and folder structure are transferred from one directory to another with inclusion
        """
        test_extensions = ["txt", "png"]
        file_transfer.transfer_files(
            src=dummy_src,
            des=dummy_des,
            include_extensions=test_extensions
        )
        _, filepaths = file_transfer.get_files(dummy_des)
        if len(filepaths) != 6:
            raise Exception("transfer_files did not transfer all files with inclusion")
        elif len([os.path.basename(os.path.dirname(filepath)) == "A" for filepath in filepaths]) == 2:
            raise Exception("transfer_files did not transfer folder structure with inclusion")
        
    def setup_method(test_transfer_directory_exclusion):
        """
        Populates the source directory with dummy data
        """
        populate_src_dummy_dir()

    def teardown_method(test_transfer_directory_exclusion):
        """
        Clears the source directory of dummy data
        """
        clear_src_des_dummy_dirs()

    def test_transfer_directory_exclusion(self):
        """
        Tests that all files and folder structure are transferred from one directory to another with exclusion
        """
        test_extensions = ["txt", "png"]
        file_transfer.transfer_files(
            src=dummy_src,
            des=dummy_des,
            exclude_extensions=test_extensions
        )
        _, filepaths = file_transfer.get_files(dummy_des)
        if len(filepaths) != 6:
            raise Exception("transfer_files did not transfer all files with inclusion")
        elif len([os.path.basename(os.path.dirname(filepath)) == "A" for filepath in filepaths]) == 2:
            raise Exception("transfer_files did not transfer folder structure with inclusion")
