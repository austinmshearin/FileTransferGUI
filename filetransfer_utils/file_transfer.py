"""
Package for handling basic file transfer processes
"""
# Standard Imports
import os

# Local Imports


def get_files(filepath: str, include_file_extensions: list = [], exclude_file_extensions: list = []) -> tuple:
    """
    Retrieves all files within the filepath with specified file extension excluding any specified file extensions

    Parameters
    ----------
    filepath: str
        Filepath to retrieve files
    include_file_extensions: list = [str]
        File extensions to include in retrieval  
        Will retrieve all if none specified  
    exclude_file_extensions: list = [str]
        File extensions to exclude in retrieval  
        Will exclude none if none specified

    Returns
    -------
    tuple
        List of all filenames, list of all relative filepaths, list of all full filepaths
    """
    # Assert that arguments are the correct format
    assert type(filepath) is str, "filepath must be a string"
    assert type(include_file_extensions) is list, "include_file_extensions must be a list"
    assert type(exclude_file_extensions) is list, "exclude_file_extensions must be a list"
    assert all([type(extension) is str for extension in include_file_extensions]), "File extentions must be strings"
    assert all([type(extension) is str for extension in exclude_file_extensions]), "File extentions must be strings"
