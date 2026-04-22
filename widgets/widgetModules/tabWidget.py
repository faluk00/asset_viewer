try:
    from PySide2.QtWidgets import QWidget, QTabBar, QStackedWidget, QVBoxLayout
except:
    from PySide6.QtWidgets import QWidget, QTabBar, QStackedWidget, QVBoxLayout

# ============================================================

class TabWidget(QWidget):
	
    def __init__(self, parent = None):
        super(TabWidget, self).__init__(parent)
		
        self.create_widgets()
        self.create_layout()
        self.create_connections()
	
    def create_widgets(self):
        self.tab_bar = QTabBar()
        self.tab_bar.setObjectName("customTabBar")
        self.tab_bar.setStyleSheet("#customTabBar {background-color: #383838}")
		
        self.stacked_wdg = QStackedWidget()
        self.stacked_wdg.setObjectName("tabBarStackedWidget" )
        self.stacked_wdg.setStyleSheet("#tabBarStackedWidget {border: 1px solid #2e2e2e}")
	
    def create_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.tab_bar)
        main_layout.addWidget(self.stacked_wdg)
	
    def create_connections(self):
        self.tab_bar.currentChanged.connect(self.stacked_wdg.setCurrentIndex)
	
    def addTab(self, label, widget):
        """
        Add a tab to the tab bar and the corresponding widget to the stacked widget
		"""
        self.tab_bar.addTab(label)
        self.stacked_wdg.addWidget(widget)

# ============================================================