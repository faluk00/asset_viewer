try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore

# ==================================================================================================
# NewCatergoryItem
class NewCatergoryItem(QtWidgets.QWidget):

    WINDOW_TITLE = "New Catergory Item"
    startPath = "~"
    categoryTemplate = {
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

    def __init__(self, parent=None):
        super(NewCatergoryItem, self).__init__(parent)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

        self.resize(400, 300)

    def createWidgets(self):
        self.targetPathBox = QtWidgets.QLineEdit()
        self.targetPathBox.setPlaceholderText("Enter Target Path")
        self.searchPathButton = QtWidgets.QPushButton("...")
        self.searchPathButton.setFixedWidth(30)

        self.itemNameBox = QtWidgets.QLineEdit()
        self.itemNameBox.setPlaceholderText("Enter Item Name")

        self.categoryTypeCombo = QtWidgets.QComboBox()
        self.categoryTypeCombo.addItems(self.categoryTemplate.keys())
        self.categoryFolderList = QtWidgets.QListWidget()

        self.createButton = QtWidgets.QPushButton("Create")
        self.cancelButton = QtWidgets.QPushButton("Cancel")
    
    def createLayout(self):

        targetPathLayout = QtWidgets.QHBoxLayout()
        targetPathLayout.addWidget(self.targetPathBox)
        targetPathLayout.addWidget(self.searchPathButton)

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow("New Item Name:", self.itemNameBox)
        formLayout.addRow("Target Path:", targetPathLayout)
        formLayout.addRow("Category Type:", self.categoryTypeCombo)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.createButton)
        buttonLayout.addWidget(self.cancelButton)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setSpacing(5)
        mainLayout.setContentsMargins(5, 5, 5, 5)
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.categoryFolderList)
        mainLayout.addLayout(buttonLayout)

    def createConnections(self):
        self.categoryTypeCombo.currentIndexChanged.connect(self.update_category_folder)
        self.searchPathButton.clicked.connect(self.browse_folder)
        self.cancelButton.clicked.connect(self.close)
    
    def refresh(self):
        self.categoryTypeCombo.clear()

        for key in self.categoryTemplate.keys():
            self.categoryTypeCombo.addItem(key)
        
        self.categoryTypeCombo.setCurrentIndex(0)
        self.update_category_folder()
    
    def update_category_folder(self):
        key = self.categoryTypeCombo.currentText()
        if not key:
            return
        self.categoryFolderList.clear()
        for folder in self.categoryTemplate[key]:
            self.categoryFolderList.addItem(folder)
    
    def browse_folder(self):
        """
        Browse folder and set path into path box
        """
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.startPath)
        folder = dialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.targetPathBox.setText(folder)
    
    def update_category_template(self, categoryTemplate):
        if not categoryTemplate:
            return
        self.categoryTemplate = categoryTemplate
        self.refresh()

# ==================================================================================================