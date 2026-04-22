import os

def create_version_folder(path):
    """
    Create a folder with the current date
    args
    path    str     dir path
    """
    current_version = 1
    version_folder = os.path.join(path, f"v{current_version:02}")
    while os.path.exists(version_folder):
        current_version += 1
        version_folder = os.path.join(path, f"v{current_version:02}")
    os.makedirs(version_folder)
    return version_folder