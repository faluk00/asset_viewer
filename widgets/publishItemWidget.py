try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore

import os
from ctypes import CDLL
import pathlib
path = str(pathlib.Path(__file__).parent.resolve())
path = path.replace("widgets", "functions")

lib = CDLL(os.path.join(path, "check_version.dll"))

# ============================================================
class publishItemWidget(QtWidgets.QWidget):

    WINDOW_TITLE = "Publish"

    def __init__(self, parent=None):
        super(publishItemWidget, self).__init__(parent)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(QtCore.Qt.Window)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

    def createWidgets(self):

        self.currentPath_le = QtWidgets.QLineEdit()
        self.updateCurrentPath_btn = QtWidgets.QPushButton("Update")
        self.updateCurrentPath_btn.setFixedSize(50, 25)
        self.searchPath_btn = QtWidgets.QPushButton("Search")
        self.searchPath_btn.setFixedSize(50, 25)
        # TODO Change to show project current path
        self.currentProject_lb = QtWidgets.QLabel("Current Project : ")
        self.projectName_lb = QtWidgets.QLabel("None")

        # naming
        self.itemName_rb = QtWidgets.QRadioButton("From Path")
        self.itemName_rb.setChecked(True)
        self.customName_rb = QtWidgets.QRadioButton("Custom name")
        nameButton_grp = QtWidgets.QButtonGroup()
        nameButton_grp.addButton(self.itemName_rb)
        nameButton_grp.addButton(self.customName_rb)

        self.baseName_le = QtWidgets.QLineEdit("")
        self.baseName_le.setDisabled(True)

        # suffix
        self.itemType_cbb = QtWidgets.QComboBox()
        self.itemType_cbb.addItem("None")
        self.itemType_cbb.addItem("Model")
        self.itemType_cbb.addItem("Rig")
        self.itemType_cbb.addItem("Anim")

        # version
        self.version_sb = QtWidgets.QSpinBox()
        self.version_sb.setMinimum(1)
        self.version_sb.setFixedWidth(80)
        self.version_sb.setDisabled(True)
        self.autoVersion_cb = QtWidgets.QCheckBox("Auto Version")
        self.autoVersion_cb.setChecked(True)

        # File type
        self.fileType_cbb = QtWidgets.QComboBox()
        self.fileType_cbb.addItem("Default")
        self.fileType_cbb.addItem("FBX")
        self.fileType_cbb.addItem("OBJ")

        # result
        self.resultName_le = QtWidgets.QLineEdit()
        self.resultName_le.setDisabled(True)

        # Buttons
        self.publishButton = QtWidgets.QPushButton("Publish")
        self.publishButton.setFixedSize(100, 30)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setFixedSize(100, 30)
    
    def createLayout(self):

        layout = QtWidgets.QVBoxLayout(self)

        project_layout = QtWidgets.QHBoxLayout()
        project_layout.addWidget(self.currentProject_lb)
        project_layout.addWidget(self.projectName_lb)

        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(QtWidgets.QLabel("Publish Path:"))
        path_layout.addWidget(self.currentPath_le)
        path_layout.addWidget(self.updateCurrentPath_btn)
        path_layout.addWidget(self.searchPath_btn)

        grid_layout = QtWidgets.QGridLayout()
        # row 0
        grid_layout.addWidget(QtWidgets.QLabel("Name"), 0, 0)
        grid_layout.addWidget(QtWidgets.QLabel("Type"), 0, 1)
        grid_layout.addWidget(QtWidgets.QLabel("Version"), 0, 2)
        grid_layout.addWidget(QtWidgets.QLabel("File Type"), 0, 3)
        # row 1
        grid_layout.addWidget(self.baseName_le, 1, 0)
        grid_layout.addWidget(self.itemType_cbb, 1, 1)
        grid_layout.addWidget(self.version_sb, 1, 2)
        grid_layout.addWidget(self.fileType_cbb, 1, 3)
        # row 2
        option_layout = QtWidgets.QHBoxLayout()
        option_layout.addWidget(self.itemName_rb)
        option_layout.addWidget(self.customName_rb)
        option_layout.addStretch()
        grid_layout.addLayout(option_layout, 2, 0)
        grid_layout.addWidget(self.autoVersion_cb, 2, 2)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.publishButton)
        button_layout.addWidget(self.cancelButton)
        
        layout.addLayout(project_layout)
        layout.addLayout(path_layout)
        layout.addLayout(grid_layout)
        layout.addWidget(QtWidgets.QLabel("Result"))
        layout.addWidget(self.resultName_le)
        layout.addStretch()
        layout.addLayout(button_layout)
    
    def createConnections(self):
        self.itemName_rb.toggled.connect(self.update_baseName_le)
        self.customName_rb.toggled.connect(self.update_baseName_le)
        self.autoVersion_cb.toggled.connect(self.update_version_sb)

        self.baseName_le.textChanged.connect(self.update_item_name)
        # combo box
        self.itemType_cbb.currentIndexChanged.connect(self.update_item_name)
        self.version_sb.valueChanged.connect(self.update_item_name)
        
        # buttons
        self.updateCurrentPath_btn.clicked.connect(self.update_base_name)
        self.searchPath_btn.clicked.connect(self.searchPath)
        self.cancelButton.clicked.connect(self.close)
    
    # ============================================================

    def update_baseName_le(self):
        if self.itemName_rb.isChecked() == True:
            self.baseName_le.setDisabled(True)
        else:
            self.baseName_le.setDisabled(False)

    def update_version_sb(self):
        if self.autoVersion_cb.isChecked() == True:
            self.version_sb.setDisabled(True)
            self.auto_check_version()
        else:
            self.version_sb.setDisabled(False)

    def searchPath(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(self.currentPath_le.text())
        newPath = dialog.getExistingDirectory()
        if newPath:
            self.currentPath_le.setText(newPath)
            self.update_base_name()
    
    def update_base_name(self):
        if self.itemName_rb.isChecked() == True:
            path = self.currentPath_le.text()
            path = path.replace("\\", "/")
            texts = path.split("/")
            item_name = "{}_{}".format(texts[-2], texts[-1])
            self.baseName_le.setText(item_name)
        if self.autoVersion_cb.isChecked() == True:
            self.auto_check_version()
        # update result
        self.update_item_name()
    
    def auto_check_version(self):
        current_version = 1
        path = self.currentPath_le.text()
        list_dir = os.listdir(path)
        for item in list_dir:
            result = lib.check_version(item)
            current_version+=result
        self.version_sb.setValue(current_version)
        # update result
        self.update_item_name()

    def update_item_name(self):
        base_name = self.baseName_le.text()
        item_type = self.itemType_cbb.currentText()
        version = f"v{self.version_sb.value():02}"

        if item_type == "None":
            file_name = f"{base_name}_{version}"
        else:
            file_name = f"{base_name}_{item_type}_{version}"
        
        self.resultName_le.setText(file_name)

# ============================================================

# import sys
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     win = publishItemWidget()
#     win.show()
#     sys.exit( app.exec() )