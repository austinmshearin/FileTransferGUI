"""
Package for handling basic file transfer processes
"""
# Standard Imports
import os
import shutil

# Local Imports


def drop_period_extension(file_extensions: list) -> list:
    """
    Drops the period from all file extensions in a list

    Parameters
    ----------
    file_extensions: list
        A list of file extensions that may or may not start with a period

    Returns
    -------
    list
        The list of file extensions with period removed
    """
    modified_extensions = []
    for extension in file_extensions:
        if extension[0] == ".":
            modified_extensions.append(extension[1:])
        else:
            modified_extensions.append(extension)
    return modified_extensions


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
    include_extensions = drop_period_extension(include_extensions)
    exclude_extensions = drop_period_extension(exclude_extensions)
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


def transfer_files(src: str, des: str, include_extensions: list = [], exclude_extensions: list = [], overwrite: bool = False):
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
    overwrite: bool = False
        Whether to overwrite files if they already exist in destination
    """
    # Assert that arguments are the correct format
    assert type(src) is str, "Source filepath must be a string"
    assert type(des) is str, "Destination filepath must be a string"
    assert type(include_extensions) is list, "Included extensions must be a list"
    assert type(exclude_extensions) is list, "Excluded extensions must be a list"
    assert all([type(extension) is str for extension in include_extensions]), "All included extensions must be strings"
    assert all([type(extension) is str for extension in exclude_extensions]), "All excluded extensions must be strings"
    # Modify all extensions to drop period if included
    include_extensions = drop_period_extension(include_extensions)
    exclude_extensions = drop_period_extension(exclude_extensions)
    # Modify source and destination so path delimiter is the same
    src = src.replace("\\", "/")
    des = des.replace("\\", "/")
    # Get all filepaths from source to transfer
    _, src_filepaths = get_files(src, include_extensions=include_extensions, exclude_extensions=exclude_extensions)
    # Modify all filepaths to be sure path delimiter is the same
    src_filepaths = [filepath.replace("\\", "/") for filepath in src_filepaths]
    # Create list of relative filepaths
    rel_filepaths = [filepath.replace(src, "")[1:] for filepath in src_filepaths]
    # Create list of destination filepaths
    des_filepaths = [os.path.join(des, filepath) for filepath in rel_filepaths]
    # Modify all filepaths to be sure path delimited is the same
    des_filepaths = [filepath.replace("\\", "/") for filepath in des_filepaths]
    if not overwrite:
        if any([os.path.exists(filepath) for filepath in des_filepaths]):
            raise Exception("File already exists in destination filepath, consider setting overwrite to True")
    # Transfer files
    for src_filepath, des_filepath in zip(src_filepaths, des_filepaths):
        os.makedirs(os.path.dirname(des_filepath), exist_ok=True)
        shutil.copyfile(src_filepath, des_filepath)
