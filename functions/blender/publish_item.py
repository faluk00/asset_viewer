import bpy
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
        sceneName = os.path.join(output_path, filename + ".blend")
        bpy.ops.wm.save_as_mainfile(filepath=sceneName)
    
    elif filetype == 1:
        sceneName = os.path.join(output_path, filename + ".fbx")
        bpy.ops.export_scene.fbx(filepath=sceneName)
    
    elif filetype == 2:
        sceneName = os.path.join(output_path, filename + ".obj")
        bpy.ops.wm.obj_export(filepath=sceneName)

# ============================================================