from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import *
import os
import xml.etree.cElementTree as et

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.count = 0
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 100)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.retranslateUi(MainWindow)

        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 300, 100))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("打开文件夹")
        MainWindow.setCentralWidget(self.centralWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.sum_count)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "框框统计"))


    def openDirDialog(self):


        targetDirPath = QFileDialog.getExistingDirectory(self)

        return targetDirPath

    def get_xmlfiles(self, path):
        self.xmlfiles_path = []
        if path:
            for i in os.listdir(path):
                if 'xml' in i:
                    i = os.path.join(path,i)
                    self.xmlfiles_path.append(i)
        return self.xmlfiles_path
    def object_count(self, xmlfile):
        count = 0
        if xmlfile:
            tree = et.parse(xmlfile)
            root = tree.getroot()
            nodes = root.getchildren()
            for i in nodes:
                if i.tag == 'object':
                    count += 1
        return count
    def sum_count(self):
        xmlpath = self.openDirDialog()
        xmllist = self.get_xmlfiles(xmlpath)
        self.count = 0
        for i in xmllist:
            self.count += self.object_count(i)
        QMessageBox.information(self, '波哥版权', self.tr('该文件夹内有{0}个框框~~'.format(self.count)))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


