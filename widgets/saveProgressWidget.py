try:
    import PySide2.QtWidgets as QtWidgets
except:
    import PySide6.QtWidgets as QtWidgets
import os

# ============================================================

class saveProgressWidget(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(saveProgressWidget, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    
    def create_widgets(self):
        
        # insert data widgets
        self.outputPath_le = QtWidgets.QLineEdit()
        self.outputPath_le.setPlaceholderText("output path")
        self.addPath_btn = QtWidgets.QPushButton("add path")
        
        # preset progress name
        self.progress_rb = QtWidgets.QRadioButton()
        self.progress_order_le     = QtWidgets.QLineEdit("01")
        self.progressType_cb = QtWidgets.QComboBox()
        self.progress_order_le.setEnabled( False )
        
        # custom name
        self.custom_rb = QtWidgets.QRadioButton()
        self.custom_name = QtWidgets.QLineEdit()
        self.custom_name.setPlaceholderText("Custom file name")
        
        # button group
        button_grp = QtWidgets.QButtonGroup()
        button_grp.addButton( self.progress_rb )
        button_grp.addButton( self.custom_rb )
        self.progress_rb.setChecked( True )
        
        # save button
        self.save_btn = QtWidgets.QPushButton("SAVE")
        self.save_btn.setFixedSize(70, 70)
        self.save_btn.setStyleSheet("background-color:rgb(245, 190, 40);color:black")
    
    def create_layouts(self):
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(3)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        content_layout = QtWidgets.QHBoxLayout()
        
        left_layout = QtWidgets.QVBoxLayout()
        insert_path_layout = QtWidgets.QHBoxLayout()
        insert_path_layout.addWidget(self.outputPath_le)
        insert_path_layout.addWidget(self.addPath_btn)
        
        progress_name_layout = QtWidgets.QHBoxLayout()
        progress_name_layout.addWidget(self.progress_rb)
        progress_name_layout.addWidget(self.progress_order_le)
        progress_name_layout.addWidget(self.progressType_cb)
        
        custom_name_layout = QtWidgets.QHBoxLayout()
        custom_name_layout.addWidget(self.custom_rb)
        custom_name_layout.addWidget(self.custom_name)
        
        left_layout.addLayout(insert_path_layout)
        left_layout.addLayout(progress_name_layout)
        left_layout.addLayout(custom_name_layout)
        
        content_layout.addLayout(left_layout)
        content_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(content_layout)
    
    def create_connections(self):
        self.outputPath_le.returnPressed.connect(self.check_progress_files)
    
    def check_progress_files(self):
        
        current_index = 1
        self.progress_order_le.setText("01")
        
        path = self.outputPath_le.text()
        items = os.listdir(path)
        for n in items:
            prefix = n.split( "_" )[0]
            
            try:
                current_index = int(prefix) 
                current_index += 1
                self.progress_order_le.setText(f"{current_index:02}")
            except:
                continue

# ============================================================