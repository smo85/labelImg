try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    import sys
except ImportError:
    pass

from libs.lib import newIcon, labelValidator

BB = QDialogButtonBox
app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
height, width = size.height(), size.width()

class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None, multiselected=False):
        super(LabelDialog, self).__init__(parent)

        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)

        model = QStringListModel()
        model.setStringList(listItem)
        completer = QCompleter()
        completer.setModel(model)
        # self.edit.setCompleter(completer)
        # self.x15 = x_other
        # self.y15 = y_other
        layout = QVBoxLayout()
        #如果需要编辑将下行反注释
        #layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            if multiselected:
                self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            layout.addWidget(self.listWidget)

        self.resize(200,400)

        self.setLayout(layout)
        # self.move(self.x15, self.y15)

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()

    def postProcess(self):
        try:
            self.edit.setText(self.edit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text())

    def popUp(self, text='', move=True, x15=0, y15=0):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)

        if move:
            x15, y15=QCursor.pos().x(), QCursor.pos().y()
            x15, y15=self.avoid_outofscreen(x15, y15)
            self.move(x15,y15)
            #x15, y15=self.getQCursor_coordinate()
            return (self.edit.text() if self.exec_() else None), (x15, y15)
        else:
            self.move(x15, y15)
            return self.edit.text() if self.exec_() else None
    def getQCursor_coordinate(self):
        return self.x(), self.y()
    def avoid_outofscreen(self, x, y):
        y=height-480 if y>(height-480) else y
        return x,y
            
    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            # text = tQListWidgetItem.text().strip()
            # multi-selection
            text_list = self.listWidget.selectedItems()
            text = [i.text() for i in list(text_list)]
            text = '_'.join(text)
        self.edit.setText(text)
        
    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.validate()
