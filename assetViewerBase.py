import json
import os
import subprocess

from datetime import date
from pathlib import Path

# ============================================================

def get_project_template_path():
    path = str(Path(__file__).parent.absolute())
    path = os.path.join(path, "config")
    return path

# User Config
class UserConfig:
    userName = os.getlogin()
    documentsPath = f"C:/Users/{userName}/Documents"
    projectTemplatePath = get_project_template_path()
    configPath = f"C:/Users/{userName}/Documents/assetviewer_config.json"

class DefaultProjectTemplate:
    projectTemplate = {
        "folders": {
            "Assets": [
                "Buildings",
                "Characters",
                "Props",
                "Sets",
                "Vehicles",
                "Weapons"
            ],
            "Deliver": [],
            "Documents": [],
            "Images": [
                "SourceImages",
                "ReferenceImages",
                "Thumbnail"
            ],
            "Movies": [],
            "Originals_Materials": [],
            "Scenes": [],
            "Sounds": [],
            "Temp": []
        },
        "CategorySubFolders": {
            "Assets": [
                "Model",
                "Rig",
                "Texture",
                "Animation",
                "LookDev",
                "Export"
            ],
            "Scenes": []
        }
    }

class AssetViewerBase(object):

    def attributes(self):
        self.ConfigPath = UserConfig()
        self.Data = {}
        self.SelectedPath = ""
        self.CurrentPath = self.ConfigPath.documentsPath
        self.ProjectTemplate = {}
    
    def create_config(self):
        """
        Create the config file
        """
        with open(self.ConfigPath.configPath, "w") as file:
            data = {
                "bookmark": [],
                "defaultPath": self.ConfigPath.documentsPath,
                "doubleWarningDelete":False,
                "projectTemplate": DefaultProjectTemplate.projectTemplate,
                "quickSaveType":[
                    "modeling", 
                    "add_joints", 
                    "bind_skin", 
                    "skinning", 
                    "add_ctrl", 
                    "rig", 
                    "pose", 
                    "anim", 
                    "clear"
                ]
            }
            json.dump(data, file, indent=4)
    
    def load_config(self):
        """
        Load the config file
        """
        if not os.path.exists(self.ConfigPath.configPath):
            self.create_config()

        with open(self.ConfigPath.configPath, "r") as file:
            self.Data = json.load(file)
            self.CurrentPath = self.Data["defaultPath"]
    
    def save_config(self):
        """
        Save the config file
        """
        with open(self.ConfigPath.configPath, "w") as file:
            json.dump(self.Data, file, indent=4)
    
    # update functions
    def update_default_path(self, path):
        """
        Update the default path
        """
        self.Data["defaultPath"] = path
    
    def update_bookmark(self, bookmark):
        """
        Update the bookmark
        """
        self.Data["bookmark"] = bookmark
    
    def update_project_template(self, template_path):
        """
        Update the project template
        """
        if os.path.exists(template_path):
            self.Data["projectTemplatePath"] = template_path
    
    def update_current_path(self, path):
        """
        Update the current path
        """
        self.CurrentPath = path
    
    # get functions

    # bookmark functions
    def add_bookmark(self, name, path):
        """
        Add a bookmark
        """
        if [name, path] not in self.Data["bookmark"]:
            self.Data["bookmark"].append([name, path])
    
    def select_bookmark(self, index):
        """
        Select a bookmark
        """
        self.update_current_path(self.Data["bookmark"][index][1])
    
    def remove_bookmark(self, index):
        """
        Remove a bookmark
        """
        self.Data["bookmark"].pop(index)
    
    def update_bookmark_item(self, index, name, path):
        """
        Edit a bookmark
        """
        self.Data["bookmark"][index] = [name, path]

    # open functions
    def open_in_explorer(self, path):
        """
        Open the path in explorer
        """
        path = path.replace("/", "\\")
        subprocess.Popen(f'explorer {path}')
    
    def open_file(self, path):
        """
        Open the file
        """
        os.startfile(path)
    
    def search_item(self, search_term):
        """
        Search for the item from the current path
        """
        results = []
        for root, dirs, files in os.walk(self.CurrentPath):
            for name in files:
                if search_term.lower() in name.lower():
                    results.append(os.path.join(root, name))
            for name in dirs:
                if search_term.lower() in name.lower():
                    results.append(os.path.join(root, name))
        return results

# ============================================================