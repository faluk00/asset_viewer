# call ui function
import maya.cmds as cmds

from asset_viewer.assetViewer_maya import AssetViewerMaya

if __name__ == "__main__":
    
    workspace_control_name = AssetViewerMaya.get_workspace_control_name()
    if cmds.window(workspace_control_name, exists=True):
        cmds.deleteUI(workspace_control_name)
    
    try:
        assetViewer_ui.setParent(None)
        assetViewer_ui.deleteLater()
    except:
        pass
    assetViewer_ui = AssetViewerMaya()