try:
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtGui import QIcon, QPixmap
    from PySide2.QtCore import QSize
except:
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtGui import QIcon, QPixmap
    from PySide6.QtCore import QSize

# ============================================================

class IconButton(QPushButton):

    externalFunction = None
    functionArgs = None

    def __init__(self, iconPath, size=24, parent=None):
        super(IconButton, self).__init__(parent)
        self.update_icon(iconPath, size)
    
    def update_icon(self, iconPath, size=24):
        self.setIcon(QIcon(QPixmap(iconPath)))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(QSize(size, size))
        self.setStyleSheet("border: none; padding: 0px; margin: 0px;")

    def mouseDoubleClickEvent(self, event):
        super(IconButton, self).mouseDoubleClickEvent(event)
        if self.externalFunction is not None:
            self.externalFunction(*self.functionArgs)

# ============================================================