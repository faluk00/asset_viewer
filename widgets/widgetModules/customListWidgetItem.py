try:
    from PySide2.QtWidgets import QListWidgetItem, QLabel, QVBoxLayout, QHBoxLayout, QWidget
    from PySide2.QtGui import QFont
    from PySide2.QtCore import Qt, QSize
except:
    from PySide6.QtWidgets import QListWidgetItem, QLabel, QVBoxLayout, QHBoxLayout, QWidget
    from PySide6.QtGui import QFont
    from PySide6.QtCore import Qt, QSize
import os
import time

# ==================================================================================================

class CustomListWidgetItem(QListWidgetItem):
    
    def __init__(self,
        text,
        path,
        image,
        imageSize=64,
        fontSize=12
    ):
        super(CustomListWidgetItem, self).__init__()

        self.labelText = text
        self.path = path
        self.image = image
        self.imageSize = imageSize
        self.fontSize = fontSize

        self.createWidgets()
        self.createLayout()

        self.update_image_size(self.imageSize)
        self.setSizeHint(QSize(self.widget.sizeHint().width(), self.widget.sizeHint().height() + 16))

    def createWidgets(self):
        self.widget = QWidget()
        
        font = QFont()
        font.setPointSize(self.fontSize)
        font.setBold(True)
        self.label = QLabel()
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setText(self.labelText)

        # file size label
        self.file_size_label = QLabel()
        self.file_size_label.setAlignment(Qt.AlignLeft)
        # date label
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignLeft)
        if os.path.isfile(self.path):

            # get modified date
            file_info = os.stat(self.path)
            year,month,day,hour,minute,second=time.localtime(file_info.st_mtime)[:-3]
            self.date_label.setText("%d/%02d/%02d   %02d:%02d"%(year,month,day,hour,minute))

            # get file size
            file_size = os.path.getsize(self.path)/1024
            if file_size < 1024:
                self.file_size_label.setText("%.2f KB"%(file_size))
            elif file_size < 1024*1024:
                file_size = file_size/1024
                self.file_size_label.setText("%.2f MB"%(file_size))
            else:
                file_size = file_size/(1024*1024)
                self.file_size_label.setText("%.2f GB"%(file_size))
        
        self.icon = QLabel()
    
    def createLayout(self):
        file_info_layout = QVBoxLayout()
        file_info_layout.addSpacing(4)
        file_info_layout.addWidget(self.label)
        file_info_layout.addWidget(self.file_size_label)
        file_info_layout.addWidget(self.date_label)
        file_info_layout.addStretch()

        layout = QHBoxLayout(self.widget)
        layout.setSpacing(1)
        layout.setContentsMargins(3, 3, 3, 3)
        
        layout.addWidget(self.icon)
        layout.addSpacing(16)
        layout.addLayout(file_info_layout)
        layout.addStretch()
    
    def update_image_size(self, size):
        """
        Update the size of the image
        """
        image = self.image.scaledToWidth(size)
        self.icon.setPixmap(image)
        self.setSizeHint(QSize(self.widget.sizeHint().width(), self.widget.sizeHint().height() + 16))

# ==================================================================================================