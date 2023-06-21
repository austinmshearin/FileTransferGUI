"""
Package for handling basic file transfer processes
"""
# Standard Imports
import os

# Local Imports


def get_files(filepath: str, include_extensions: list = [], exclude_extensions: list = []) -> tuple:
    """
    Retrieves all files within the filepath with specified file extension excluding any specified file extensions

    Parameters
    ----------
    filepath: str
        Filepath to retrieve files
    include_extensions: list = [str]
        File extensions to include in retrieval  
        Will retrieve all if none specified  
    exclude_extensions: list = [str]
        File extensions to exclude in retrieval  
        Will exclude none if none specified

    Returns
    -------
    tuple
        List of all filenames, list of all full filepaths
    """
    # Assert that arguments are the correct format
    assert type(filepath) is str, "filepath must be a string"
    assert type(include_extensions) is list, "include_extensions must be a list"
    assert type(exclude_extensions) is list, "exclude_extensions must be a list"
    assert all([type(extension) is str for extension in include_extensions]), "File extentions must be strings"
    assert all([type(extension) is str for extension in exclude_extensions]), "File extentions must be strings"
    # Modify all extensions to drop period if included
    for extension_index, extension in enumerate(include_extensions):
        if extension[0] == ".":
            include_extensions[extension_index] = extension[1:]
    for extension_index, extension in enumerate(exclude_extensions):
        if extension[0] == ".":
            exclude_extensions[extension_index] = extension[1:]
    # List of all filenames retrieved
    retrieved_filenames = []
    # List of all full filepaths retrieved
    retrieved_filepaths = []
    # Walk the filepath to retrieve files
    for dirpath, _, filenames in os.walk(filepath):
        # Loop over all files in the directory
        for filename in filenames:
            # If included file extensions are specified
            if len(include_extensions) > 0:
                # If the file extension is in included file extensions and not in excluded file extensions
                if (any([extension == filename.split(".")[-1] for extension in include_extensions])) and not (filename.split(".")[-1] in exclude_extensions):
                    retrieved_filenames.append(filename)
                    retrieved_filepaths.append(os.path.join(dirpath, filename))
            # If all file extensions are included
            else:
                # If file extension is not excluded
                if not (filename.split(".")[-1] in exclude_extensions):
                    retrieved_filenames.append(filename)
                    retrieved_filepaths.append(os.path.join(dirpath, filename))
    # Return the tuple of filenames and filepaths
    return retrieved_filenames, retrieved_filepaths


def transfer_files(src: str, des: str, include_extensions: list = [], exclude_extensions: list = []):
    """
    Transfer all files and folder structure from source to destination

    Parameters
    ----------
    src: str
        The source filepath
    des: str
        The destination filepath
    include_extensions: list = []
        File extensions to include in the transfer
    exclude_extensions: list = []
        File extensions to exclude in the transfer
    """
    # Assert that arguments are the correct format
    assert type(src) is str, "Source filepath must be a string"
    assert type(des) is str, "Destination filepath must be a string"
    assert type(include_extensions) is list, "Included extensions must be a list"
    assert type(exclude_extensions) is list, "Excluded extensions must be a list"
    assert all([type(extension) is str for extension in include_extensions]), "All included extensions must be strings"
    assert all([type(extension) is str for extension in exclude_extensions]), "All excluded extensions must be strings"
