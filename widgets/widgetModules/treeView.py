try:
    from PySide2.QtWidgets import QTreeView, QFileSystemModel, QMenu, QApplication
    from PySide2.QtCore import Qt, QDir, QSortFilterProxyModel, Slot, QModelIndex
except:
    from PySide6.QtWidgets import QTreeView, QFileSystemModel, QMenu, QApplication
    from PySide6.QtCore import Qt, QDir, QSortFilterProxyModel, Slot, QModelIndex

# ============================================================

class TreeView(QTreeView):
    
    RootPath = ''
    CurrentItem = ""

    def __init__(self, path=''):
        super(TreeView, self).__init__()

        self.RootPath = path

        self.model = QFileSystemModel()
        self.model.setFilter(QDir.AllEntries | QDir.NoDot | QDir.Dirs | QDir.Files)
        self.model.setRootPath(self.RootPath)

        self.proxyModel = QSortFilterProxyModel(recursiveFilteringEnabled = True, filterRole = QFileSystemModel.FileNameRole)
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxyModel.setSourceModel(self.model)
        
        self.setModel(self.proxyModel)
        self.setRootIndex(self.proxyModel.mapFromSource(self.model.index(self.RootPath)))

        # Hide columns for file size and type
        self.setHeaderHidden(True)
        self.setColumnHidden(1, True)  # Hide Size column
        self.setColumnHidden(2, True)  # Hide Type column
        self.setColumnHidden(3, True)  # Hide Date Modified column

        self.create_menu()
        self.pressed.connect(self.update_current_item)
    
    def update_model_root(self, path):
        """
        Update the root path of the model.
        """
        self.RootPath = path
        self.model.setRootPath(self.RootPath)
        self.setRootIndex(self.proxyModel.mapFromSource(self.model.index(self.RootPath)))
    
    def filter_tree(self, text):
        """
        Filter the tree view based on the text.
        """
        self.proxyModel.setFilterWildcard(text)
        self.setRootIndex(self.proxyModel.mapFromSource(self.model.index(self.RootPath)))

    # get selected item
    @Slot(QModelIndex)
    def update_current_item(self, index):
        """
        Update the current item.
        """
        source_index = self.proxyModel.mapToSource(index)
        indexItem = self.model.index(source_index.row(), 0, source_index.parent())
        filePath = self.model.filePath(indexItem)
        self.CurrentItem = filePath.replace("/", "\\")

    # expand selected item
    def expand_selected_item(self):
        """
        Expand the selected item.
        """
        self.expandRecursively(self.selectionModel().selectedRows()[0])
    
    # collapse selected item
    def collapse_selected_item(self):
        """
        Collapse the selected item.
        """
        self.collapse(self.selectionModel().selectedRows()[0])
    
    def create_menu( self ):
        
        self.menu = QMenu(self)
        
        action_1 = self.menu.addAction("Expand")
        action_2 = self.menu.addAction("Expand All")
        action_3 = self.menu.addAction("Collapse")
        action_4 = self.menu.addAction("Collapse All")

        action_1.triggered.connect(self.expand_selected_item)
        action_2.triggered.connect(self.expandAll)
        action_3.triggered.connect(self.collapse_selected_item)
        action_4.triggered.connect(self.collapseAll)
    
    def mousePressEvent(self, event):
        super(TreeView, self).mousePressEvent(event)
        if event.button() == Qt.RightButton:
            self.menu.popup(event.globalPos())
        
        modifierPressed = QApplication.keyboardModifiers()
        if (modifierPressed & Qt.ShiftModifier) == Qt.ShiftModifier:
            self.expand_selected_item()

# ============================================================