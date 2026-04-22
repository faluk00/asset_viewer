import bpy

def import_file(item, path):
    
    # check file type
    fileType = item.split(".")[-1]
    namespace = item.split("." + fileType)[0]
    
    if fileType in ["obj", "OBJ"]:
        bpy.ops.wm.obj_import(filepath=path)
    
    elif fileType in ["fbx", "FBX"]:
        bpy.ops.import_scene.fbx(filepath=path)
    
    # elif fileType in ["glb", "gltf"]:
    #     bpy.ops.import_scene.gltf(filepath=path)