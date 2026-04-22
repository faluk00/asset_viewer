# call ui function
try:
    import PySide2.QtWidgets as QtWidgets
except:
    import PySide6.QtWidgets as QtWidgets

from asset_viewer.assetViewer_blender import AssetViewerBlender
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    win = AssetViewerBlender()
    win.show()