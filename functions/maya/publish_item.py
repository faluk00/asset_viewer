import maya.cmds as cmds
import os

# ============================================================

def publish_item(output_path, filename, filetype=0):
    """
    args:
        output_path     str     output path
        filename        str     file name
        filetype        int     0 program default file type
                                1 FBX
                                2 OBJ
    """
    # save as .ma file
    if filetype == 0:
        sceneName = os.path.join(output_path, filename)
        cmds.file(rename = sceneName)
        cmds.file(f = True, save = True, type = "mayaAscii")
    
    elif filetype == 1:
        # load fbx plug-in
        plugin_path = cmds.pluginInfo("fbxmaya", query=True, path=True)
        cmds.loadPlugin(plugin_path)
        sceneName = os.path.join(output_path, filename + ".fbx")
        cmds.file(sceneName, exportAll = True, type = "FBX export")
    
    elif filetype == 2:
        # load obj plug-in
        plugin_path = cmds.pluginInfo("objExport", query=True, path=True)
        cmds.loadPlugin(plugin_path)
        sceneName = os.path.join(output_path, filename + ".obj")
        cmds.file(sceneName, exportAll = True, type = "OBJexport")

# ============================================================