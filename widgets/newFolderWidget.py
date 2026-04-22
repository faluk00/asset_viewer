try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore

# ============================================================
# New Folder Widget
class NewFolderWidget(QtWidgets.QWidget):

    WINDOW_TITLE = "Create New Folder"
    startPath = "~"

    def __init__(self, parent=None):
        super(NewFolderWidget, self).__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(QtCore.Qt.Window)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

    def createWidgets(self):
        self.newFolderNameBox = QtWidgets.QLineEdit()
        self.newFolderNameBox.setPlaceholderText("Folder Name")
        self.pathBox = QtWidgets.QLineEdit()
        self.pathBox.setPlaceholderText("Path")
        
        self.browseButton = QtWidgets.QPushButton("...")
        self.browseButton.setFixedSize(30, 30)

        self.createButton = QtWidgets.QPushButton("Create")
        self.createButton.setFixedSize(100, 30)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setFixedSize(100, 30)

    def createLayout(self):
        pathLayout = QtWidgets.QHBoxLayout()
        pathLayout.addWidget(self.pathBox)
        pathLayout.addWidget(self.browseButton)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.createButton)
        buttonLayout.addWidget(self.cancelButton)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.newFolderNameBox)
        layout.addLayout(pathLayout)
        layout.addLayout(buttonLayout)

    def createConnections(self):
        self.browseButton.clicked.connect(self.browse_folder)

    def browse_folder(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.startPath)
        folder = dialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.pathBox.setText(folder)

# ============================================================
# import sys
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = NewFolderWidget()
#     window.show()
#     sys.exit(app.exec_())