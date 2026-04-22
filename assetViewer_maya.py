try:
    import PySide2.QtWidgets as QtWidgets
    import PySide2.QtCore as QtCore
    from shiboken2 import getCppPointer
except:
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore
    from shiboken6 import getCppPointer

import os, sys
import maya.cmds as cmds
import maya.OpenMayaUI as omui


from asset_viewer.assetViewer import AssetViewer
from asset_viewer.functions.maya.publish_item import publish_item
from asset_viewer.functions.maya.import_file import import_file

# ============================================================

class WorkspaceControl(object):
    
    def __init__(self, name):
        self.name = name
        self.widget = None
    
    def create(self, label, widget, ui_script=None):
        
        cmds.workspaceControl(self.name, label=label)
        
        if ui_script:
            cmds.workspaceControl(self.name, e=True, uiScript=ui_script)
        
        self.add_widget_to_layout(widget)
        self.set_visible(True)
    
    def restore(self, widget):
        self.add_widget_to_layout(widget)
    
    def add_widget_to_layout(self, widget):
        if widget:
            self.widget = widget
            self.widget.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)
        
            if sys.version_info.major >= 3:
                workspace_control_ptr = int(omui.MQtUtil.findControl(self.name))
                widget_ptr = int(getCppPointer(self.widget)[0])
            else:
                workspace_control_ptr = long(omui.MQtUtil.findControl(self.name))
                widget_ptr = long(getCppPointer(self.widget)[0])
            
            omui.MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr)
    
    def exists(self):
        return cmds.workspaceControl(self.name, q=True, exists=True)
    
    def is_visible(self):
        return cmds.workspaceControl(self.name, q=True, visible=True)
    
    def set_visible(self, visible):
        if visible:
            cmds.workspaceControl(self.name, e=True, restore=True)
        
        else:
            cmds.workspaceControl(self.name, e=True, visible=False)
    
    def set_label(self, label):
        cmds.workspaceControl(self.name, e=True, label=label)
    
    def is_floating(self):
        return cmds.workspaceControl(self.name, q=True, floating=True)
    
    def is_collapsed(self):
        return cmds.workspaceControl(self.name, q=True, collapse=True)

# ============================================================

class AssetViewerMaya(AssetViewer):
    
    WINDOW_TITLE = "Asset Viewer"
    UI_NAME = "assetViewerUI"
    ui_instance = None
    
    @classmethod
    def display(cls):
        if cls.ui_instance:
            cls.ui_instance.show_workspace_control()
        else:
            cls.ui_instance = AssetViewerMaya()
    
    @classmethod
    def get_workspace_control_name(cls):
        return "{0}WorkspaceControl".format(cls.UI_NAME)

    def __init__(self, parent=None):
        super(AssetViewerMaya, self).__init__(parent)
        self.create_workspace_control()

    def createConnections(self):
        super(AssetViewerMaya, self).createConnections()
        self.saveProgressWidget.save_btn.clicked.connect(self.save_progress)
        self.publishItemWidget.publishButton.clicked.connect(self.publish_item)
        self.treeView.doubleClicked.connect(self.double_click_file)
    
    def create_workspace_control(self):
        self.workspace_control_instance = WorkspaceControl(
            self.get_workspace_control_name()
        )
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            self.workspace_control_instance.create(
                self.WINDOW_TITLE,
                self,
                ui_script="from workspace_control import assetViewerUI\nassetViewerUI.display()"
            )
    
    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)
    
    def showEvent(self, e):
        if self.workspace_control_instance.is_floating():
            self.workspace_control_instance.set_label("Asset Viewer")
        else:
            self.workspace_control_instance.set_label("Asset Viewer")
    
    def save_progress(self):

        outputPath = self.saveProgressWidget.outputPath_le.text()
        
        if self.saveProgressWidget.progress_rb.isChecked():
            version = self.saveProgressWidget.progress_order_le.text()
            name = self.saveProgressWidget.progressType_cb.currentText()
            filename = f"{version}_{name}.ma"
        
        elif self.saveProgressWidget.custom_rb.isChecked():
            name = self.saveProgressWidget.custom_name.text()
            filename = f"{name}.ma"
            outputPath = self.saveProgressWidget.outputPath_le.text()
        
        sceneName = f"{outputPath}/{filename}"
        
        cmds.file(rename = sceneName)
        cmds.file(save = True, type = "mayaAscii")
        
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
            
            if fileType in [ "ma", "mb" ]:
                reply = QtWidgets.QMessageBox.question(self, 'Warning',
                    "Do you want to open {}?".format( fileName ), QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                
                if reply == QtWidgets.QMessageBox.Yes:
                    cmds.file( item, open = True, force = True )
    
    def double_click_file(self):
        
        item = self.treeView.CurrentItem
        check_isfile = os.path.isfile(item)
        if check_isfile == True:
            
            fileName = os.path.basename(item)
            fileType = fileName.split( "." )[-1]
            
            if fileType in [ "ma", "mb" ]:
                self.open_file()
            
            else:
                reply = QtWidgets.QMessageBox.question(self, 'Warning',
                    "Do you want to import {}?".format( fileName ), QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                
                if reply == QtWidgets.QMessageBox.Yes:
                    import_file(fileName, item)

# ============================================================

# if __name__ == "__main__":
    
#     workspace_control_name = AssetViewerMaya.get_workspace_control_name()
#     if cmds.window(workspace_control_name, exists=True):
#         cmds.deleteUI(workspace_control_name)
    
#     try:
#         assetViewer_ui.setParent(None)
#         assetViewer_ui.deleteLater()
#     except:
#         pass
#     assetViewer_ui = AssetViewerMaya()