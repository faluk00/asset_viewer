try:
    import PySide2.QtWidgets as QtWidgets
except:
    import PySide6.QtWidgets as QtWidgets

import bpy
import os

from asset_viewer.assetViewer import AssetViewer
from asset_viewer.functions.blender.publish_item import publish_item
from asset_viewer.functions.blender.import_file import import_file

# ============================================================

class AssetViewerBlender(AssetViewer):

    def __init__(self, parent=None):
        super(AssetViewerBlender, self).__init__(parent)

    def createConnections(self):
        super(AssetViewerBlender, self).createConnections()
        self.saveProgressWidget.save_btn.clicked.connect(self.save_progress)
        self.publishItemWidget.publishButton.clicked.connect(self.publish_item)
        self.treeView.doubleClicked.connect(self.double_click_file)
    
    def save_progress(self):

        outputPath = self.saveProgressWidget.outputPath_le.text()
        
        if self.saveProgressWidget.progress_rb.isChecked():
            version = self.saveProgressWidget.progress_order_le.text()
            name = self.saveProgressWidget.progressType_cb.currentText()
            filename = f"{version}_{name}.blend"
        
        elif self.saveProgressWidget.custom_rb.isChecked():
            name = self.saveProgressWidget.custom_name.text()
            filename = f"{name}.blend"
            outputPath = self.saveProgressWidget.outputPath_le.text()
        
        sceneName = f"{outputPath}/{filename}"
        
        bpy.ops.wm.save_as_mainfile(filepath=sceneName)
        
        # update progress number
        self.saveProgressWidget.check_progress_files()

    def publish_item(self):
        output_path = self.publishItemWidget.currentPath_le.text()
        filename = self.publishItemWidget.resultName_le.text()
        filetype = self.publishItemWidget.fileType_cbb.currentIndex()

        current_version = self.publishItemWidget.version_sb.value()

        output_path = os.path.join(output_path, f"v{current_version:02}")
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        publish_item(output_path, filename, filetype)
    
    def import_selected_file(self):
        item = self.treeView.CurrentItem
        check_isfile = os.path.isfile(item)
        if check_isfile == True:
            fileName = os.path.basename(item)
            import_file(fileName, item)
    
    def open_file(self):
        
        item = self.treeView.CurrentItem
        check_isfile = os.path.isfile(item)
        if check_isfile == True:
            
            fileName = os.path.basename(item)
            fileType = fileName.split( "." )[-1]
            
            if fileType in ["blend"]:
                reply = QtWidgets.QMessageBox.question(self, 'Warning',
                    "Do you want to open {}?".format(fileName), QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                
                if reply == QtWidgets.QMessageBox.Yes:
                    bpy.ops.wm.open_mainfile(filepath=item)
    
    def double_click_file(self):
        
        item = self.treeView.CurrentItem
        check_isfile = os.path.isfile(item)
        if check_isfile == True:
            
            fileName = os.path.basename(item)
            fileType = fileName.split( "." )[-1]
            
            if fileType in ["blend"]:
                self.open_file()
            
            else:
                reply = QtWidgets.QMessageBox.question(self, 'Warning',
                    "Do you want to import {}?".format( fileName ), QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                
                if reply == QtWidgets.QMessageBox.Yes:
                    import_file(fileName, item)

# ============================================================