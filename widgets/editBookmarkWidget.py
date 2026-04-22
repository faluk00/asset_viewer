try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore
import os

# ============================================================
# Edit Bookmark Widget
class EditBookmarkWidget(QtWidgets.QWidget):

    WINDOW_TITLE = "Edit Bookmark"
    startPath = "~"

    def __init__(self, parent=None):
        super(EditBookmarkWidget, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(QtCore.Qt.Window)

        self.createWidgets()
        self.createLayout()
        self.createConnections()
    
    def createWidgets(self):
        self.bookmarkList = QtWidgets.QListWidget()

        self.bookmarkNameBox = QtWidgets.QLineEdit()
        self.bookmarkNameBox.setPlaceholderText("Bookmark Name")
        self.bookmarkPathBox = QtWidgets.QLineEdit()
        self.bookmarkPathBox.setPlaceholderText("Bookmark Path")
        self.bookmarkPathSearchButton = QtWidgets.QPushButton("...")
        self.bookmarkPathSearchButton.setFixedSize(30, 30)

        self.updateBookmarkButton = QtWidgets.QPushButton("Update")
        self.updateBookmarkButton.setFixedSize(100, 30)
        self.deleteBookmarkButton = QtWidgets.QPushButton("Delete")
        self.deleteBookmarkButton.setFixedSize(100, 30)

    def createLayout(self):
        bookmarkPathLayout = QtWidgets.QHBoxLayout()
        bookmarkPathLayout.addWidget(self.bookmarkPathBox)
        bookmarkPathLayout.addWidget(self.bookmarkPathSearchButton)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.updateBookmarkButton)
        buttonLayout.addWidget(self.deleteBookmarkButton)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.bookmarkList)
        layout.addWidget(self.bookmarkNameBox)
        layout.addLayout(bookmarkPathLayout)
        layout.addLayout(buttonLayout)
    
    def createConnections(self):
        self.bookmarkList.itemClicked.connect(self.update_selected_bookmark)
        self.bookmarkPathSearchButton.clicked.connect(self.browse_folder)
        self.updateBookmarkButton.clicked.connect(self.update_bookmark)
        self.deleteBookmarkButton.clicked.connect(self.delete_bookmark)
    
    def browse_folder(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(os.path.expanduser(self.startPath))
        folder = dialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.bookmarkPathBox.setText(folder)
    
    def refresh_bookmarks(self, bookmarkList):
        self.bookmarkList.clear()
        for name, path in bookmarkList:
            item = QtWidgets.QListWidgetItem(name)
            item.setData(QtCore.Qt.UserRole, path)
            self.bookmarkList.addItem(item)

    def update_selected_bookmark(self):
        getItem = self.bookmarkList.currentItem()
        if getItem:
            self.bookmarkNameBox.setText(getItem.text())
            self.bookmarkPathBox.setText(getItem.data(QtCore.Qt.UserRole))

    def update_bookmark(self):
        bookmarkName = self.bookmarkNameBox.text()
        bookmarkPath = self.bookmarkPathBox.text()
        
        self.bookmarkList.currentItem().setText(bookmarkName)
        self.bookmarkList.currentItem().setData(QtCore.Qt.UserRole, bookmarkPath)
        itemIndex = self.bookmarkList.currentRow()

        return itemIndex, bookmarkName, bookmarkPath
    
    def delete_bookmark(self):
        getItem = self.bookmarkList.currentItem()
        if getItem:
            itemIndex = self.bookmarkList.currentRow()
            itemData = getItem.data(QtCore.Qt.UserRole)

            return itemIndex, [getItem.text(), itemData]

# ============================================================