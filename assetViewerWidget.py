try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    from PySide2.QtWidgets import QAction
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore
    import PySide6.QtGui as QtGui
    from PySide6.QtGui import QAction
import os, sys
import winsound

from asset_viewer.widgets.widgetModules.treeView import TreeView

# from widgets.addBookmarkWidget import AddBookmarkWidget
# from widgets.editBookmarkWidget import EditBookmarkWidget
from asset_viewer.widgets.newFolderWidget import NewFolderWidget
from asset_viewer.widgets.newProjectWidget import NewProjectWidget
from asset_viewer.widgets.newCatergoryItem import NewCatergoryItem
from asset_viewer.widgets.settingWidget import SettingWidget
from asset_viewer.widgets.publishItemWidget import publishItemWidget
from asset_viewer.widgets.saveProgressWidget import saveProgressWidget

# ============================================================

class iconPath:
    iconPath = os.path.abspath(sys.argv[0])
    iconPath = os.path.dirname(iconPath)
    iconPath = os.path.join(iconPath, "icons")
    bookmark = os.path.join(iconPath, "bookmark.png")
    bookmark_add = os.path.join(iconPath, "bookmark_add.png")
    bookmark_remove = os.path.join(iconPath, "bookmark_remove.png")
    bookmark_edit = os.path.join(iconPath, "bookmark_edit.png")
    refresh = os.path.join(iconPath, "refresh.png")
    project = os.path.join(iconPath, "project.png")

# ============================================================

class AssetViewerWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AssetViewerWidget, self).__init__(parent)
        self.setWindowTitle("Asset Viewer")
        self.setGeometry(100, 100, 300, 600)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        # self.addBookmarkWidget = AddBookmarkWidget(self)
        # self.editBookmarkWidget = EditBookmarkWidget(self)
        self.newFolderWidget = NewFolderWidget(self)
        self.newProjectWidget = NewProjectWidget(self)
        self.newCatergoryItemWidget = NewCatergoryItem(self)
        self.settingWidget = SettingWidget(self)
        self.publishItemWidget = publishItemWidget(self)
        self.saveProgressWidget = saveProgressWidget(self)

        self.ChildrenWidgets = []
        # self.ChildrenWidgets.append(self.addBookmarkWidget)
        # self.ChildrenWidgets.append(self.editBookmarkWidget)
        self.ChildrenWidgets.append(self.newFolderWidget)
        self.ChildrenWidgets.append(self.newProjectWidget)
        self.ChildrenWidgets.append(self.newCatergoryItemWidget)
        self.ChildrenWidgets.append(self.settingWidget)
        self.ChildrenWidgets.append(self.publishItemWidget)

        self.createMenuBar()
        self.createWidgets()
        self.createLayouts()
        self.createConnections()

        # get center of the screen position
        self.move(QtGui.QGuiApplication.primaryScreen().geometry().center() - self.rect().center())

    def createMenuBar(self):
        self.menuBar = QtWidgets.QMenuBar(self)
        #self.setMenuBar(menuBar)

        # edit menu
        editMenu = self.menuBar.addMenu("&Edit")
        preferencesAction = editMenu.addAction("Preferences")
        preferencesAction.triggered.connect(self.settingWidget.show)

        refreshAction = editMenu.addAction("Refresh")
        refreshAction.triggered.connect(lambda: self.refresh(playSound=True))

        # create menu
        createMenu = self.menuBar.addMenu("&Create")
        createNewProjectAction = createMenu.addAction("New Project")
        createNewProjectAction.triggered.connect(self.newProjectWidget.show)
        createCatergoryAction = createMenu.addAction("New Category Item")
        createCatergoryAction.triggered.connect(self.newCatergoryItemWidget.show)
        createNewFolderAction = createMenu.addAction("New Folder")
        createNewFolderAction.triggered.connect(self.newFolderWidget.show)
        publishAction = createMenu.addAction("Publish Item")
        publishAction.triggered.connect(self.publishItemWidget.show)
        
        # bookmark menu
        self.bookmarkMenu = self.menuBar.addMenu("&Bookmark")
        # bookmark widgets
        self.bookmarkList = QtWidgets.QListWidget()
        self.bookmarkList.setFixedWidth(200)
        bookmark_action = QtWidgets.QWidgetAction(self.bookmarkMenu)
        bookmark_action.setDefaultWidget(self.bookmarkList)

        # addBookmarkAction = QAction(
        #     QtGui.QIcon(iconPath.bookmark_add),
        #     "Add Bookmark",
        #     bookmarkMenu
        # )
        # addBookmarkAction.triggered.connect(self.addBookmarkWidget.show)
        # editBookmarkAction = QAction(
        #     QtGui.QIcon(iconPath.bookmark_edit),
        #     "Edit Bookmark",
        #     bookmarkMenu
        # )
        # editBookmarkAction.triggered.connect(self.editBookmarkWidget.show)

        # add actions to menu
        self.bookmarkMenu.addAction(bookmark_action)
        # bookmarkMenu.addAction(addBookmarkAction)
        # bookmarkMenu.addAction(editBookmarkAction)

        # project menu
        #projectMenu = self.menuBar.addMenu("&Projects")
        # project widgets
        #self.projectList = QtWidgets.QListWidget()
        #self.projectList.setFixedWidth(200)
        #project_action = QtWidgets.QWidgetAction(projectMenu)
        #project_action.setDefaultWidget(self.projectList)
        # add actions to menu
        #projectMenu.addAction(project_action)

        #self.menuBar.addMenu(projectMenu)
        self.menuBar.addMenu(self.bookmarkMenu)
        self.menuBar.addMenu(createMenu)
        self.menuBar.addMenu(editMenu)

    def createWidgets(self):
        # root path widgets
        self.currentPath_le = QtWidgets.QLineEdit()
        self.currentPath_le.setPlaceholderText("path...")

        # selected path widgets
        self.selectedPathBox = QtWidgets.QLineEdit()

        # tree view widgets
        self.searchBox = QtWidgets.QLineEdit()
        self.searchBox.setPlaceholderText("Search...")
        self.treeView = TreeView()
        # add create dir in menu
        self.treeView.menu.addSeparator()
        addBookmarkAction = self.treeView.menu.addAction("Add Bookmark")
        self.treeView.menu.addSeparator()
        openFileAction = self.treeView.menu.addAction("Open File")
        importFileAction = self.treeView.menu.addAction("Import File")
        self.treeView.menu.addSeparator()
        newDirAction = self.treeView.menu.addAction("Create New Folder")
        newDateDirAction = self.treeView.menu.addAction("Create Current Date Folder")
        newVersionDirAction = self.treeView.menu.addAction("Create New Version Folder")
        self.treeView.menu.addSeparator()
        setWorkPathAction = self.treeView.menu.addAction("\"Set as Working path\"")
        # add connections
        addBookmarkAction.triggered.connect(self.add_bookmark_from_selected)
        openFileAction.triggered.connect(self.open_selected_in_explorer)
        importFileAction.triggered.connect(self.import_selected_file)
        newDirAction.triggered.connect(self.show_new_folder_widget)
        newDateDirAction.triggered.connect(self.create_new_current_date_folder)
        newVersionDirAction.triggered.connect(self.create_new_version_folder)
        setWorkPathAction.triggered.connect(self.set_current_as_working_path)

    def createLayouts(self):
        # create main layout
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setContentsMargins(5, 5, 5, 5)
        mainLayout.setSpacing(5)

        # path layout
        path_formLayout = QtWidgets.QFormLayout()
        path_formLayout.addRow("  Path:", self.currentPath_le)
        path_formLayout.addRow("Select:", self.selectedPathBox)

        # tree view layout
        treeLayoutWidget = QtWidgets.QWidget()
        treeLayout = QtWidgets.QVBoxLayout(treeLayoutWidget)
        treeLayout.setContentsMargins(0, 0, 0, 0)
        treeLayout.setSpacing(0)
        treeLayout.addWidget(self.searchBox)
        treeLayout.addWidget(self.treeView)

        # add widgets to layout
        mainLayout.addWidget(self.menuBar)
        mainLayout.addWidget(self.saveProgressWidget)
        mainLayout.addLayout(path_formLayout)
        mainLayout.addWidget(treeLayoutWidget)

    def createConnections(self):
        self.searchBox.textChanged.connect(self.filter_tree)
        self.currentPath_le.returnPressed.connect(self.update_root_path)
        self.treeView.pressed.connect(self.update_selected_path)

        self.newFolderWidget.createButton.clicked.connect(self.create_new_folder)
        self.newCatergoryItemWidget.createButton.clicked.connect(self.create_category_item)

    # Prototype functions
    def refresh(self, playSound=True):

        if playSound:
            # Play system sound
            winsound.MessageBeep(type=winsound.MB_OK)

    def create_new_folder(self):
        pass

    def create_new_current_date_folder(self):
        pass

    def create_new_version_folder(self):
        pass

    def create_new_project(self):
        pass

    def create_category_item(self):
        pass

    def add_bookmark_from_selected(self):
        pass

    def open_selected_in_explorer(self):
        pass

    def import_selected_file(self):
        pass

    # ============================================================
    def filter_tree(self, text):
        """
        Filter the tree view based on the text.
        """
        self.treeView.filter_tree(text)

    def update_root_path(self):
        """
        Update the root path of the tree view.
        """
        path = self.currentPath_le.text()
        self.treeView.update_model_root(path)
    
    def use_selected_path(self):
        """
        Use the selected path.
        """
        self.currentPath_le.setText(self.selectedPathBox.text())
        self.treeView.update_model_root(self.selectedPathBox.text())
        self.selectedPathBox.clear()
    
    def update_selected_path(self):
        """
        Update the selected path.
        """
        self.selectedPathBox.setText(self.treeView.CurrentItem)
    
    def update_bookmark_list(self, bookmarks):
        """
        Update the bookmark list.
        """
        self.bookmarkList.clear()
        for name, path in bookmarks:
            item = QtWidgets.QListWidgetItem(name)
            item.setData(QtCore.Qt.UserRole, path)
            self.bookmarkList.addItem(item)
    
    def show_new_folder_widget(self):
        """
        Show the new folder widget.
        """

        self.newFolderWidget.pathBox.setText(self.treeView.CurrentItem)
        self.newFolderWidget.show()
    
    def set_current_as_working_path(self):
        self.saveProgressWidget.outputPath_le.setText(self.treeView.CurrentItem)
        self.saveProgressWidget.check_progress_files()
    
    # @QtCore.Slot(str)
    # def print_signal(self):
    #     """
    #     Print signal to console.
    #     """
    #     assert isinstance(str), "text must be a string"
    #     print("Signal received:", str)

# ============================================================

# import sys
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     win = AssetViewerWidget()
#     win.show()
#     sys.exit( app.exec() )