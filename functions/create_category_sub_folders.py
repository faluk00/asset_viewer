import os

def create_category_sub_folders(name, path, category, template):
    """
    Create subfolders for the category
    args
    name        str     item/scene name
    path        str     dir path
    category    str     category name
    template    dict    project template
    """
    # get template
    if template is None:
        print("No template to create new Project.")
        return None
    folders = template["CategorySubFolders"][category]
    for folder in folders:
        output_path = os.path.join(path, name, folder, "progress")
        if not os.path.exists(output_path):
            os.makedirs(output_path)