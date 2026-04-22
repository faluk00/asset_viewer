import maya.cmds as cmds

def import_file(item, path):
    
    # check file type
    fileType = item.split(".")[-1]
    namespace = item.split("." + fileType)[0]
    
    if fileType in ["obj", "OBJ"]:
        importType = "OBJ"
    
    elif fileType in ["fbx", "FBX"]:
        importType = "FBX"
    
    elif fileType == "ma":
        importType = "mayaAscii"
    
    elif fileType == "mb":
        importType = "mayaBinary"
    
    cmds.file( 
        path,
        i = True,
        type = importType,
        mergeNamespaceWithRoot = True,
        mergeNamespacesOnClash = True,
        namespace = namespace,
        importTimeRange = "keep"
    )