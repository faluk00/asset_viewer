try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore

from asset_viewer.widgets.projectFoldersWidget import ProjectFoldersWidget

# ============================================================
# New Project Widget
class NewProjectWidget(QtWidgets.QWidget):

    WINDOW_TITLE = "Create New Project"
    startPath = "~"
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

    def __init__(self, parent=None):
        super(NewProjectWidget, self).__init__(parent)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(QtCore.Qt.Window)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

        self.folderListWidget.update_folder_list(self.projectTemplate)

    def createWidgets(self):
        self.projectNameBox = QtWidgets.QLineEdit()
        self.projectNameBox.setPlaceholderText("Project Name")
        self.pathBox = QtWidgets.QLineEdit()
        self.pathBox.setPlaceholderText("Path")
        
        self.browseButton = QtWidgets.QPushButton("...")
        self.browseButton.setFixedSize(30, 30)

        # Folder and Sub folders list
        self.folderListWidget = ProjectFoldersWidget()

        self.createButton = QtWidgets.QPushButton("Create")
        self.createButton.setFixedSize(100, 30)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setFixedSize(100, 30)
    
    def createLayout(self):
        # project name and path layout
        projectPathLayout = QtWidgets.QHBoxLayout()
        projectPathLayout.addWidget(self.pathBox)
        projectPathLayout.addWidget(self.browseButton)

        projectLayout = QtWidgets.QFormLayout()
        projectLayout.addRow("Project Name", self.projectNameBox)
        projectLayout.addRow("Project Path", projectPathLayout)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.createButton)
        buttonLayout.addWidget(self.cancelButton)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(projectLayout)
        layout.addWidget(self.folderListWidget )
        layout.addLayout(buttonLayout)
    
    def createConnections(self):
        self.browseButton.clicked.connect(self.browse_folder)
        self.folderListWidget.newFolderButton.clicked.connect(self.add_folder)
        self.folderListWidget.removeFolderButton.clicked.connect(self.remove_folder)
        self.folderListWidget.newSubFolderButton.clicked.connect(self.add_sub_folder)
        self.folderListWidget.removeSubFolderButton.clicked.connect(self.remove_sub_folder)

        self.cancelButton.clicked.connect(self.close)
    
    def browse_folder(self):
        """
        Browse folder and set path into path box
        """
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.startPath)
        folder = dialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.pathBox.setText(folder)
    
    def add_folder(self):
        """
        Add new folder into folder list
        """
        folder = self.folderListWidget.add_folder()
        if folder:
            self.projectTemplate["folders"][folder] = []
    
    def add_sub_folder(self):
        """
        Add new sub folder into sub folder list
        """
        data = self.folderListWidget.add_sub_folder()
        if data:
            self.projectTemplate["folders"][data[0]] = data[1]

    def remove_folder(self):
        """
        Remove selected folder from folder list
        """
        folder = self.folderListWidget.remove_folder()
        if folder:
            self.projectTemplate["folders"].pop(folder)
    
    def remove_sub_folder(self):
        """
        Remove selected sub folder from sub folder list
        """
        data = self.folderListWidget.remove_sub_folder()
        if data:
            self.projectTemplate["folders"][data[0]] = data[1]
    
    def update_project_template(self, template):
        """
        Update project template
        """
        for key, value in template.items():
            if key in self.projectTemplate:
                self.projectTemplate[key].update(value)
        self.folderListWidget.update_folder_list(self.projectTemplate)

# ============================================================

# import sys
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     widget = NewProjectWidget()
#     widget.show()
#     sys.exit(app.exec_())