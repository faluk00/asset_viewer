try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore

# ============================================================
# Add Bookmark Widget
class AddBookmarkWidget(QtWidgets.QWidget):

    WINDOW_TITLE = "Add Bookmark"
    startPath = "~"

    def __init__(self, parent=None):
        super(AddBookmarkWidget, self).__init__(parent)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(QtCore.Qt.Window)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

    def createWidgets(self):
        self.bookmarkNameBox = QtWidgets.QLineEdit()
        self.bookmarkNameBox.setPlaceholderText("Bookmark Name")
        self.bookmarkPathBox = QtWidgets.QLineEdit()
        self.bookmarkPathBox.setPlaceholderText("Bookmark Path")
        self.bookmarkPathSearchButton = QtWidgets.QPushButton("...")
        self.bookmarkPathSearchButton.setFixedSize(30, 30)

        self.addBookmarkButton = QtWidgets.QPushButton("Add Bookmark")
        self.addBookmarkButton.setFixedSize(100, 30)

    def createLayout(self):
        bookmarkPathLayout = QtWidgets.QHBoxLayout()
        bookmarkPathLayout.addWidget(self.bookmarkPathBox)
        bookmarkPathLayout.addWidget(self.bookmarkPathSearchButton)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.addBookmarkButton)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.bookmarkNameBox)
        layout.addLayout(bookmarkPathLayout)
        layout.addLayout(buttonLayout)

    def createConnections(self):
        self.bookmarkPathSearchButton.clicked.connect(self.browse_folder)

    def browse_folder(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.startPath)
        folder = dialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.bookmarkPathBox.setText(folder)

# ============================================================