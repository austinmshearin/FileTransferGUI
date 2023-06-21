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
        List of all filenames, list of all full filepaths
    """
    # Assert that arguments are the correct format
    assert type(filepath) is str, "filepath must be a string"
    assert type(include_file_extensions) is list, "include_file_extensions must be a list"
    assert type(exclude_file_extensions) is list, "exclude_file_extensions must be a list"
    assert all([type(extension) is str for extension in include_file_extensions]), "File extentions must be strings"
    assert all([type(extension) is str for extension in exclude_file_extensions]), "File extentions must be strings"
    # Modify all extensions to drop period if included
    for extension_index, extension in enumerate(include_file_extensions):
        if extension[0] == ".":
            include_file_extensions[extension_index] = extension[1:]
    for extension_index, extension in enumerate(exclude_file_extensions):
        if extension[0] == ".":
            exclude_file_extensions[extension_index] = extension[1:]
    # List of all filenames retrieved
    retrieved_filenames = []
    # List of all full filepaths retrieved
    retrieved_filepaths = []
    # Walk the filepath to retrieve files
    for dirpath, _, filenames in os.walk(filepath):
        # Loop over all files in the directory
        for filename in filenames:
            # If included file extensions are specified
            if len(include_file_extensions) > 0:
                # If the file extension is in included file extensions and not in excluded file extensions
                if (any([extension == filename.split(".")[-1] for extension in include_file_extensions])) and not (filename.split(".")[-1] in exclude_file_extensions):
                    retrieved_filenames.append(filename)
                    retrieved_filepaths.append(os.path.join(dirpath, filename))
            # If all file extensions are included
            else:
                # If file extension is not excluded
                if not (filename.split(".")[-1] in exclude_file_extensions):
                    retrieved_filenames.append(filename)
                    retrieved_filepaths.append(os.path.join(dirpath, filename))
    # Return the tuple of filenames and filepaths
    return retrieved_filenames, retrieved_filepaths
