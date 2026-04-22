import os

def create_project(project_name, path = None, template = None):
    """
    Create a new project
    args
    project_name    str     project name
    path            str     dir path
    template        dict    project template
    """
    if path is None:
        print("Please input dir path for project location.")
        return None
    # get template
    if template is None:
        print("No template to create new Project.")
        return None
    # create project folder
    project_path = os.path.join(path, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    
    # create subfolders
    for key, value in template["folders"].items():
        
        catergory_path = os.path.join(project_path, key)
        if not os.path.exists(catergory_path):
            os.makedirs(catergory_path)
            
        if value:
            for subfolder in value:
                path = os.path.join(project_path, key, subfolder)
                if not os.path.exists(path):
                    os.makedirs(path)
    
    return project_path