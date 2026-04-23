try:
    import PySide2.QtWidgets as QtWidgets
except:
    import PySide6.QtWidgets as QtWidgets
import os

from asset_viewer.assetViewerWidget import AssetViewerWidget
from asset_viewer.assetViewerBase import AssetViewerBase
from asset_viewer.functions.create_category_sub_folders import create_category_sub_folders
from asset_viewer.functions.create_current_date_folder import create_current_date_folder
from asset_viewer.functions.create_folder import create_folder
from asset_viewer.functions.create_project import create_project
from asset_viewer.functions.create_version_folder import create_version_folder

# ============================================================

class AssetViewer(AssetViewerWidget, AssetViewerBase):

    def __init__(self, parent=None):
        self.attributes()
        self.load_config()
        super(AssetViewer, self).__init__(parent)
        self.refresh(False)

    def createWidgets(self):
        super(AssetViewer, self).createWidgets()

        # load data from config file
        self.currentPath_le.setText(self.Data["defaultPath"])

    def createConnections(self):
        super(AssetViewer, self).createConnections()
        self.bookmarkList.itemClicked.connect(self.select_bookmark)
        self.bookmarkList.currentItemChanged.connect(self.select_bookmark)

        self.newProjectWidget.createButton.clicked.connect(self.create_new_project)
        self.settingWidget.saveButton.clicked.connect(self.save_config)

        self.saveProgressWidget.addPath_btn.clicked.connect(self.set_workin_path)

        # check bug
        self.settingWidget.folderListWidget.newSubFolderButton.clicked.connect(self.print_check)
    
    def save_config(self):
        super(AssetViewer, self).save_config()
        self.refresh(playSound=False)

    def refresh(self, playSound=True):
        """
        Refresh the asset viewer
        """
        self.settingWidget.Data = self.Data
        self.settingWidget.refresh()
        if self.CurrentPath != self.Data["defaultPath"]:
            self.CurrentPath = self.Data["defaultPath"]
        self.treeView.update_model_root(self.CurrentPath)
        self.currentPath_le.setText(self.CurrentPath.replace("\\", "/"))
        # self.addBookmarkWidget.startPath = self.Data["defaultPath"]
        # self.editBookmarkWidget.startPath = self.Data["defaultPath"]
        self.newFolderWidget.startPath = self.CurrentPath
        self.newFolderWidget.pathBox.setText(self.CurrentPath)

        # self.editBookmarkWidget.refresh_bookmarks(self.Data["bookmark"])
        self.update_bookmark_list(self.Data["bookmark"])

        self.newProjectWidget.startPath = self.Data["defaultPath"]
        self.newProjectWidget.pathBox.setText(self.Data["defaultPath"])
        self.newProjectWidget.update_project_template(self.Data["projectTemplate"])

        self.newCatergoryItemWidget.startPath = self.CurrentPath
        self.newCatergoryItemWidget.update_category_template(self.Data["projectTemplate"]["CategorySubFolders"])

        self.refresh_save_progress_wdg()

        super(AssetViewer, self).refresh(playSound)

    def create_category_item(self):
        """
        Create new category item
        """
        sceneName = self.newCatergoryItemWidget.itemNameBox.text()
        path = self.newCatergoryItemWidget.targetPathBox.text()
        category = self.newCatergoryItemWidget.categoryTypeCombo.currentText()

        create_category_sub_folders(
            sceneName,
            path,
            category,
            self.Data["projectTemplate"]
        )

        self.newCatergoryItemWidget.itemNameBox.clear()
        self.newCatergoryItemWidget.close()

    def create_new_current_date_folder(self):
        """
        Create new folder with current date
        """
        create_current_date_folder(self.SelectedPath)

    def create_new_folder(self):
        """
        Create new folder
        """
        name = self.newFolderWidget.newFolderNameBox.text()
        path = self.newFolderWidget.pathBox.text()

        if os.path.exists(path):
            create_folder(name, path)
            # clear input
            self.newFolderWidget.newFolderNameBox.clear()
            self.newFolderWidget.pathBox.clear()
            self.newFolderWidget.close()

    def create_new_project(self):
        """
        Create new project
        """
        project_name = self.newProjectWidget.projectNameBox.text()
        project_path = self.newProjectWidget.pathBox.text()
        project_template = self.newProjectWidget.projectTemplate

        if project_name:
            create_project(project_name, project_path, project_template)
            # add project to the list
            self.Data["bookmark"].append([project_name, project_path])
            self.save_config()
            # set current path
            self.CurrentPath = project_path
            # clear input
            self.newProjectWidget.projectNameBox.clear()
            self.newProjectWidget.pathBox.clear()
            message = QtWidgets.QMessageBox(self.newProjectWidget)
            message.warning(self, "Success", 'Project created!')
            self.newProjectWidget.close()
        else:
            message = QtWidgets.QMessageBox(self.newProjectWidget)
            message.warning(self, "Error", 'Please enter project name!')

    def create_new_version_folder(self):
        """
        Create new version folder
        """
        create_version_folder(self.SelectedPath)
        
    
    def add_bookmark_from_selected(self):
        """
        Add bookmark from selected path in tree view
        """
        path = self.treeView.CurrentItem
        name = os.path.basename(path)
        # confirm dialog
        message = QtWidgets.QMessageBox(self)
        message.setWindowTitle("Add Bookmark")
        message.setText(f"Add {name} to bookmark?")
        message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        message.setDefaultButton(QtWidgets.QMessageBox.Yes)
        reply = message.exec()
        if reply == QtWidgets.QMessageBox.Yes:
            self.add_bookmark(name, path)
            self.save_config()

    def open_selected_in_explorer(self):
        """
        Open selected item in explorer
        """
        self.open_in_explorer(self.treeView.CurrentItem)
    
    # path
    def update_current_path(self, path):
        """
        Update the current path
        """
        super(AssetViewer, self).update_current_path(path)
        self.currentPath_le.setText(self.CurrentPath.replace("\\", "/"))
    
    def update_selected_path(self):
        """
        Update selected path
        """
        super(AssetViewer, self).update_selected_path()
        self.SelectedPath = self.treeView.CurrentItem
        self.newCatergoryItemWidget.targetPathBox.setText(self.SelectedPath)
    
    # bookmark
    def select_bookmark(self):
        """
        Select bookmark from bookmark list in toolbar
        """
        index = self.bookmarkList.currentRow()
        super(AssetViewer, self).select_bookmark(index)
        self.treeView.update_model_root(self.CurrentPath)

        self.bookmarkMenu.close()
    
    # quick save progress
    def refresh_save_progress_wdg(self):
        self.saveProgressWidget.outputPath_le.clear()
        self.saveProgressWidget.progressType_cb.clear()
        progress_list = self.Data["quickSaveType"]
        for progress in progress_list:
            self.saveProgressWidget.progressType_cb.addItem(progress)
    
    def set_workin_path(self):
        self.saveProgressWidget.outputPath_le.setText(self.SelectedPath)
        self.saveProgressWidget.check_progress_files()

    # for bug check
    def print_check(self):
        print("Main", self.Data["projectTemplate"].get("folders").get("Deliver"))
        print("Setting", self.settingWidget.Data["projectTemplate"].get("folders").get("Deliver"))


# ============================================================

# import sys
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     win = AssetViewer()
#     win.show()
#     sys.exit( app.exec() )