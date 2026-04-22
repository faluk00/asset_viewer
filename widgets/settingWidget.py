try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore
import os

from asset_viewer.widgets.widgetModules.tabWidget import TabWidget
from asset_viewer.widgets.projectFoldersWidget import ProjectFoldersWidget

# ============================================================
# Setting Widget
class SettingWidget(QtWidgets.QWidget):

    WINDOW_TITLE = "Setting"
    WINDOW_WIDTH = 400
    Data = {} # can pass by value

    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(self.WINDOW_WIDTH)
        self.setWindowFlags(QtCore.Qt.Window)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

    def createWidgets(self):
        # main data widgets
        self.defaultPathBox = QtWidgets.QLineEdit()
        self.defaultPathBox.setPlaceholderText("Default Path")
        self.defaultPathSearchButton = QtWidgets.QPushButton("...")
        self.defaultPathSearchButton.setFixedSize(30, 30)

        # project list
        self.projectList = QtWidgets.QListWidget()
        self.projectNameBox = QtWidgets.QLineEdit()
        self.projectNameBox.setPlaceholderText("Bookmark Name")
        self.projectPathBox = QtWidgets.QLineEdit()
        self.projectPathBox.setPlaceholderText("Bookmark Path")
        self.projectPathSearchButton = QtWidgets.QPushButton("...")
        self.projectPathSearchButton.setFixedSize(30, 30)
        self.addProjectButton = QtWidgets.QPushButton("Add")
        self.addProjectButton.setFixedSize(50, 30)
        self.editProjectInfoButton = QtWidgets.QPushButton("Edit")
        self.editProjectInfoButton.setFixedSize(50, 30)
        self.removeProjectButton = QtWidgets.QPushButton("Remove")
        self.removeProjectButton.setFixedSize(50, 30)

        # save progress
        self.progress_list = QtWidgets.QListWidget()
        self.progress_le = QtWidgets.QLineEdit()
        self.progress_le.setPlaceholderText("...")
        self.add_progress_btn = QtWidgets.QPushButton("Add")
        self.add_progress_btn.setFixedSize(50, 30)
        self.edit_progress_btn = QtWidgets.QPushButton("Edit")
        self.edit_progress_btn.setFixedSize(50, 30)
        self.remove_progress_btn = QtWidgets.QPushButton("Remove")
        self.remove_progress_btn.setFixedSize(50, 30)

        # project template
        self.folderListWidget = ProjectFoldersWidget()
        
        # sub folder catergory
        self.catergoryFolderWidget = ProjectFoldersWidget()
        self.catergoryFolderWidget.newFolderBox.setPlaceholderText("New Category")

        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setFixedSize(100, 30)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setFixedSize(100, 30)

    def createLayout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        tabWidget = TabWidget()

        # default path layout
        defaultPathLayout = QtWidgets.QHBoxLayout()
        defaultPathLayout.addWidget(self.defaultPathBox)
        defaultPathLayout.addWidget(self.defaultPathSearchButton)
        # main data layout
        mainDataWidget = QtWidgets.QWidget()
        mainDataLayout = QtWidgets.QFormLayout(mainDataWidget)
        mainDataLayout.addRow("Default Path", defaultPathLayout)

        # project list layout
        projectListWidget = QtWidgets.QWidget()
        projectListLayout = QtWidgets.QVBoxLayout(projectListWidget)
        projectListLayout.setSpacing(5)
        projectListLayout.setContentsMargins(5, 5, 5, 5)
        # project info layout
        projectPathLayout = QtWidgets.QHBoxLayout()
        projectPathLayout.addWidget(self.projectPathBox)
        projectPathLayout.addWidget(self.projectPathSearchButton)
        projectInfoLayout = QtWidgets.QFormLayout()
        projectInfoLayout.addRow("Bookmark Name", self.projectNameBox)
        projectInfoLayout.addRow("Bookmark Path", projectPathLayout)
        # project buttons layout
        projectButtonsLayout = QtWidgets.QHBoxLayout()
        projectButtonsLayout.addWidget(self.addProjectButton)
        projectButtonsLayout.addWidget(self.editProjectInfoButton)
        projectButtonsLayout.addWidget(self.removeProjectButton)
        # add into project list layout
        projectListLayout.addWidget(QtWidgets.QLabel("Bookmark List"))
        projectListLayout.addWidget(self.projectList)
        projectListLayout.addLayout(projectInfoLayout)
        projectListLayout.addLayout(projectButtonsLayout)

        # progress list layout
        progress_wdg = QtWidgets.QWidget()
        progress_layout = QtWidgets.QVBoxLayout(progress_wdg)
        progress_layout.setSpacing(5)
        progress_layout.setContentsMargins(5, 5, 5, 5)
        # progress buttons layout
        progress_btn_layout = QtWidgets.QHBoxLayout()
        progress_btn_layout.addWidget(self.add_progress_btn)
        progress_btn_layout.addWidget(self.edit_progress_btn)
        progress_btn_layout.addWidget(self.remove_progress_btn)
        # add into progress_layout
        progress_layout.addWidget(self.progress_list)
        progress_layout.addWidget(self.progress_le)
        progress_layout.addLayout(progress_btn_layout)

        # add into tab widget
        tabWidget.addTab("Bookmark List", projectListWidget)
        tabWidget.addTab("Save Progress", progress_wdg)
        tabWidget.addTab("Project Template", self.folderListWidget)
        tabWidget.addTab("Catergory Folder", self.catergoryFolderWidget)

        # buttons layout
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)

        layout.addWidget(mainDataWidget)
        layout.addWidget(tabWidget)
        layout.addLayout(buttonLayout)

    def createConnections(self):
        self.defaultPathBox.returnPressed.connect(self.set_default_path)
        self.defaultPathBox.textChanged.connect(self.set_default_path)
        self.defaultPathSearchButton.clicked.connect(self.searchDefaultPath)

        # project list
        self.projectPathSearchButton.clicked.connect(self.search_project_path)
        self.projectList.itemClicked.connect(self.select_project_list)
        self.projectList.currentItemChanged.connect(self.select_project_list)
        self.addProjectButton.clicked.connect(self.add_project)
        self.editProjectInfoButton.clicked.connect(self.edit_project)
        self.removeProjectButton.clicked.connect(self.remove_project)

        # progress list
        self.progress_list.itemClicked.connect(self.select_progress_list)
        self.progress_list.currentItemChanged.connect(self.select_progress_list)
        self.add_progress_btn.clicked.connect(self.add_progress_name)
        self.edit_progress_btn.clicked.connect(self.edit_progress_name)
        self.remove_progress_btn.clicked.connect(self.remove_progress_name)

        # project's folder
        self.folderListWidget.newFolderButton.clicked.connect(self.add_folder)
        self.folderListWidget.removeFolderButton.clicked.connect(self.remove_folder)
        self.folderListWidget.newSubFolderButton.clicked.connect(self.add_sub_folder)
        self.folderListWidget.removeSubFolderButton.clicked.connect(self.remove_sub_folder)

        # catergor folder
        self.catergoryFolderWidget.newFolderButton.clicked.connect(self.add_catergory_folder)
        self.catergoryFolderWidget.removeFolderButton.clicked.connect(self.remove_catergory_folder)
        self.catergoryFolderWidget.newSubFolderButton.clicked.connect(self.add_catergory_sub_folder)
        self.catergoryFolderWidget.removeSubFolderButton.clicked.connect(self.remove_catergory_sub_folder)

        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.cancel)

    def refresh(self):
        self.defaultPathBox.setText(self.Data["defaultPath"])
        self.folderListWidget.update_folder_list(self.Data["projectTemplate"])
        self.catergoryFolderWidget.update_folder_list(self.Data["projectTemplate"], key="CategorySubFolders")
        self.refresh_project_list()
        self.refresh_progress_list()

    # default path
    def set_default_path(self):
        """
        Set default path for project
        """
        self.Data["defaultPath"] = self.defaultPathBox.text()

    def searchDefaultPath(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.defaultPathBox.text())
        newPath = dialog.getExistingDirectory()
        if newPath:
            self.defaultPathBox.setText(newPath)
            self.Data["defaultPath"] = newPath
    
    # projectFoldersWidget
    def add_folder(self):
        """
        Add new folder into folder list
        """
        folder = self.folderListWidget.add_folder()
        if folder:
            self.Data["projectTemplate"]["folders"][folder] = []
    
    def add_sub_folder(self):
        """
        Add new sub folder into sub folder list
        """
        data = self.folderListWidget.add_sub_folder()
        if data:
            self.Data["projectTemplate"]["folders"][data[0]] = data[1]

    def remove_folder(self):
        """
        Remove selected folder from folder list
        """
        folder = self.folderListWidget.remove_folder()
        if folder:
            self.Data["projectTemplate"]["folders"].pop(folder)
    
    def remove_sub_folder(self):
        """
        Remove selected sub folder from sub folder list
        """
        data = self.folderListWidget.remove_sub_folder()
        if data:
            self.Data["projectTemplate"]["folders"][data[0]] = data[1]
    
    # project list
    def search_project_path(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.Data["defaultPath"])
        newPath = dialog.getExistingDirectory()
        if newPath:
            self.projectPathBox.setText(newPath)

    def add_project(self):
        name = self.projectNameBox.text()
        path = self.projectPathBox.text()
        if os.path.exists(path):
            self.Data["bookmark"].append([name, path])
            self.refresh_project_list()
            messageBox = QtWidgets.QMessageBox(self)
            messageBox.warning(self, "Add Project", f"\"{name}\" Added!")
    
    def edit_project(self):
        currentItem = self.projectList.currentItem()
        index = self.projectList.currentRow()
        if currentItem:
            name = self.projectNameBox.text()
            path = self.projectPathBox.text()
            self.Data["bookmark"][index] = [name, path]
            self.refresh_project_list()
            messageBox = QtWidgets.QMessageBox(self)
            messageBox.warning(self, "Edit Project", f"\"{name}\" hase been Edited!")
    
    def remove_project(self):
        currentItem = self.projectList.currentItem()
        if currentItem:
            messageBox = QtWidgets.QMessageBox(self)
            messageBox.setWindowTitle("Remove Project")
            messageBox.setText("Are you sure to remove this project?")
            messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            messageBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
            reply = messageBox.exec()
            if reply == QtWidgets.QMessageBox.Yes:
                index = self.projectList.currentRow()
                self.Data["bookmark"].pop(index)
                self.refresh_project_list()
    
    def select_project_list(self):
        currentItem = self.projectList.currentItem()
        if currentItem:
            name = currentItem.text()
            path = currentItem.data(QtCore.Qt.UserRole)
            self.projectNameBox.setText(name)
            self.projectPathBox.setText(path)
    
    def refresh_project_list(self):
        self.projectList.clear()
        for name, path in self.Data["bookmark"]:
            item = QtWidgets.QListWidgetItem(name)
            item.setData(QtCore.Qt.UserRole, path)
            self.projectList.addItem(item)

    # progress
    def add_progress_name(self):
        progress = self.progress_le.text()
        self.Data["quickSaveType"].append(progress)
        self.refresh_progress_list()
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.warning(self, "Add Progress", f"\"{progress}\" Added!")
    
    def edit_progress_name(self):
        currentItem = self.progress_list.currentItem()
        index = self.progress_list.currentRow()
        if currentItem:
            progress = self.progress_le.text()
            self.Data["quickSaveType"][index] = progress
            self.refresh_progress_list()
            messageBox = QtWidgets.QMessageBox(self)
            messageBox.warning(self, "Edit Progress", f"\"{progress}\" hase been Edited!")
            self.progress_le.clear()
    
    def remove_progress_name(self):
        currentItem = self.progress_list.currentItem()
        if currentItem:
            index = self.projectList.currentRow()
            self.Data["quickSaveType"].pop(index)
            self.refresh_progress_list()
    
    def select_progress_list(self):
        currentItem = self.progress_list.currentItem()
        if currentItem:
            progress = currentItem.text()
            self.progress_le.setText(progress)
    
    def refresh_progress_list(self):
        self.progress_list.clear()
        for progress in self.Data["quickSaveType"]:
            self.progress_list.addItem(progress)
    
    # catergory folder
    def add_catergory_folder(self):
        folder = self.catergoryFolderWidget.add_folder()
        if folder:
            self.Data["projectTemplate"]["CategorySubFolders"][folder] = []
    
    def add_catergory_sub_folder(self):
        data = self.catergoryFolderWidget.add_sub_folder()
        if data:
            self.Data["projectTemplate"]["CategorySubFolders"][data[0]] = data[1]
    
    def remove_catergory_folder(self):
        folder = self.catergoryFolderWidget.remove_folder()
        if folder:
            self.Data["projectTemplate"]["CategorySubFolders"].pop(folder)
    
    def remove_catergory_sub_folder(self):
        data = self.catergoryFolderWidget.remove_sub_folder()
        if data:
            self.Data["projectTemplate"]["CategorySubFolders"][data[0]] = data[1]

    def save(self):
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.warning(self, "Save Setting", "Saved!")
        self.close()

    def cancel(self):
        self.close()

# ============================================================