import os

def create_folder(folder_name, path):
    """
    Create a folder with the current date
    args
    folder_name     str     new dir name
    path            str     dir path
    """
    if not os.path.isdir(path):
        print("Invalid input path")
        return
    
    new_folder = os.path.join(path, folder_name)
    if not os.path.exists(new_folder):
        print(f"Making {new_folder}")
        os.makedirs(new_folder)