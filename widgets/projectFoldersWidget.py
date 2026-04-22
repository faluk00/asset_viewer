try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore

# ============================================================

class ProjectFoldersWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ProjectFoldersWidget, self).__init__(parent)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

    def createWidgets(self):
        # Folder List
        self.folderList = QtWidgets.QListWidget()
        self.newFolderBox = QtWidgets.QLineEdit()
        self.newFolderBox.setPlaceholderText("New Folder")
        self.newFolderButton = QtWidgets.QPushButton("Add")
        self.newFolderButton.setFixedSize(50, 30)
        self.removeFolderButton = QtWidgets.QPushButton("Remove")
        self.removeFolderButton.setFixedSize(50, 30)

        # Sub folders
        self.subFoldersList = QtWidgets.QListWidget()
        self.newSubFolderBox = QtWidgets.QLineEdit()
        self.newSubFolderBox.setPlaceholderText("New Sub Folder")
        self.newSubFolderButton = QtWidgets.QPushButton("Add")
        self.newSubFolderButton.setFixedSize(50, 30)
        self.removeSubFolderButton = QtWidgets.QPushButton("Remove")
        self.removeSubFolderButton.setFixedSize(50, 30)
    
    def createLayout(self):
        # folder list layout
        newFolderLayout = QtWidgets.QHBoxLayout()
        newFolderLayout.addWidget(self.newFolderBox)
        newFolderLayout.addWidget(self.newFolderButton)
        newFolderLayout.addWidget(self.removeFolderButton)

        folderLayout = QtWidgets.QVBoxLayout()
        folderLayout.addWidget(QtWidgets.QLabel("Folders"))
        folderLayout.addWidget(self.folderList)
        folderLayout.addLayout(newFolderLayout)

        # sub folder list layout
        newSubFolderLayout = QtWidgets.QHBoxLayout()
        newSubFolderLayout.addWidget(self.newSubFolderBox)
        newSubFolderLayout.addWidget(self.newSubFolderButton)
        newSubFolderLayout.addWidget(self.removeSubFolderButton)

        subFolderLayout = QtWidgets.QVBoxLayout()
        subFolderLayout.addWidget(QtWidgets.QLabel("Sub Folders"))
        subFolderLayout.addWidget(self.subFoldersList)
        subFolderLayout.addLayout(newSubFolderLayout)

        # main folder layout
        mainFolderLayout = QtWidgets.QHBoxLayout()
        mainFolderLayout.addLayout(folderLayout)
        mainFolderLayout.addLayout(subFolderLayout)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addLayout(mainFolderLayout)
    
    def createConnections(self):
        self.folderList.itemClicked.connect(self.update_sub_folder_list)
        self.folderList.currentItemChanged.connect(self.update_sub_folder_list)
    
    def update_folder_list(self, template, key="folders"):
        """
        Update folder list with selected template
        """
        self.folderList.clear()
        for key, value in template[key].items():
            item = QtWidgets.QListWidgetItem(key)
            item.setData(QtCore.Qt.UserRole, value)
            self.folderList.addItem(item)

        # set select latest added folder
        self.folderList.setCurrentRow(0)
        self.update_sub_folder_list()

    def update_sub_folder_list(self):
        """
        Update sub folder list with selected folder
        """
        currentItem = self.folderList.currentItem()
        if currentItem:
            self.subFoldersList.clear()
            for subFolder in currentItem.data(QtCore.Qt.UserRole):
                item = QtWidgets.QListWidgetItem(subFolder)
                self.subFoldersList.addItem(item)
    
    def add_folder(self):
        """
        Add new folder into folder list
        """
        folder = self.newFolderBox.text()
        if folder:
            item = QtWidgets.QListWidgetItem(folder)
            item.setData(QtCore.Qt.UserRole, [])
            self.folderList.addItem(item)
            self.newFolderBox.clear()
            
            # set select latest added folder
            self.folderList.setCurrentItem(item)
            return folder
        else:
            return None
    
    def add_sub_folder(self):
        """
        Add new sub folder into sub folder list
        """
        subFolder = self.newSubFolderBox.text()
        # get folder list current item
        currentItem = self.folderList.currentItem()
        if currentItem and subFolder:
            subFolders = currentItem.data(QtCore.Qt.UserRole)
            if subFolder in subFolders:
                return None
            self.subFoldersList.addItem(subFolder)
            subFolders.append(subFolder)
            currentItem.setData(QtCore.Qt.UserRole, subFolders)
            self.newSubFolderBox.clear()
            return currentItem.text(), subFolders
        else:
            return None

    def remove_folder(self):
        """
        Remove selected folder from folder list
        """
        currentItem = self.folderList.currentItem()
        if currentItem:
            folder = currentItem.text()
            self.folderList.takeItem(self.folderList.row(currentItem))
            return folder
        else:
            return None
    
    def remove_sub_folder(self):
        """
        Remove selected sub folder from sub folder list
        """
        currentItem = self.subFoldersList.currentItem()
        currentParentItem = self.folderList.currentItem()
        if currentItem and currentParentItem:
            folder = currentParentItem.text()
            subFolders = currentParentItem.data(QtCore.Qt.UserRole)
            subFolders.remove(currentItem.text())
            currentParentItem.setData(QtCore.Qt.UserRole, subFolders)
            self.subFoldersList.takeItem(self.subFoldersList.row(currentItem))
            return folder, subFolders
        else:
            return None

# ============================================================