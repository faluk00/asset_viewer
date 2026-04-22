try:
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtCore import QRegularExpression
    from PySide2.QtGui import QRegularExpressionValidator
except:
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtCore import QRegularExpression
    from PySide6.QtGui import QRegularExpressionValidator

class IntLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(IntLineEdit, self).__init__(parent)

        self.setText("0")
        self.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*")))