import os
import random
from random import randint
from time import sleep
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread,pyqtSignal
from PyQt6 import uic
count = -1
from processTwiter import ProcessTwiter

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("DATA/untitled123.ui", self)
        self.pushButton = self.findChild(QPushButton,'pushButton') # start
        self.pushButton.clicked.connect(self.startThread)
        self.pushButton_2 = self.findChild(QPushButton,'pushButton_2') # dialog Files
        self.pushButton_2.clicked.connect(self.dialogFiles)
        self.textEdit = self.findChild(QTextEdit,'textEdit')# input follow
        self.tableWidget = self.findChild(QTableWidget,'tableWidget') # table Widget
        self.lineEdit = self.findChild(QLineEdit,'lineEdit') # input url
        self.checkBox = self.findChild(QCheckBox,'checkBox') # follow
        self.checkBox_2 = self.findChild(QCheckBox,'checkBox_2') # reweet
        self.checkBox_3 = self.findChild(QCheckBox,'checkBox_3')# like
        self.checkBox_4 = self.findChild(QCheckBox,'checkBox_4') # comment
        self.spinBox = self.findChild(QSpinBox,'spinBox') # count tag
        self.spinBox_2 = self.findChild(QSpinBox,'spinBox_2') # number thread
        self.show()
        self.childThread = {}

    def dialogFiles(self):
        try:
            self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                           "Text Files (*.txt)")
            listGmails = open(self.fileName, 'r').readlines()
            self.tableWidget.setRowCount(len(listGmails))
            for i in range(len(listGmails)):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(f'Tài khoản {i + 1}'))
        except:
            pass

    def statusTable(self, index, text):
        # Row count
        self.tableWidget.setItem(index, 1, QTableWidgetItem(text))

    def startThread(self):
        for i in range(self.spinBox_2.value()):
            self.childThread[i] = StartQthread(index = i)
            self.childThread[i].fileName = self.fileName
            self.childThread[i].lineEdit = self.lineEdit
            self.childThread[i].checkBox = self.checkBox
            self.childThread[i].checkBox_2 = self.checkBox_2
            self.childThread[i].checkBox_3 = self.checkBox_3
            self.childThread[i].checkBox_4 = self.checkBox_4
            self.childThread[i].textEdit = self.textEdit
            self.childThread[i].spinBox = self.spinBox
            self.childThread[i].tableStatus.connect(self.statusTable)
            self.childThread[i].start()


class StartQthread(QThread):
    tableStatus = pyqtSignal(int,str)
    def __init__(self,index = 0):
        super(StartQthread, self).__init__()
        self.index = index
        #self.count = 0
    def processGetInfo(self):
        global count
        count += 1
        self.count = count
        self.listInfo = open(self.fileName,'r',encoding='utf8').readlines()
        self.cookies = self.listInfo[self.count]
        self.url = self.lineEdit.text()
        self.listUID = [item for item in self.textEdit.toPlainText().split('\n')]
        self.twiterID = self.url.split('/')[5]
        print(self.twiterID)
        self.numberTagFriend = self.spinBox.value()


    def run(self):
        while True:
            self.processGetInfo()
            self.processHandle()
            if self.count >= len(self.listInfo)-1:break



    def processHandle(self):
        self.processTwiter = ProcessTwiter()
        if self.checkBox.isChecked(): # follow
            for item in self.listUID:
                self.processTwiter.processFollowTwiter(cookies=self.cookies,screen_name=item)
                self.tableStatus.emit(self.count,'Follow Tài Khoản')
                sleep(1)
        if self.checkBox_2.isChecked():
            self.processTwiter.processReweetTwiter(cookies=self.cookies,twiterID=self.twiterID)
            self.tableStatus.emit(self.count, 'Reweet bài viết')
            sleep(randint(1,2))

        if self.checkBox_3.isChecked():
            self.processTwiter.processLikeTwiter(cookies=self.cookies,twiterID=self.twiterID)
            self.tableStatus.emit(self.count, 'Like bài viết')
            sleep(randint(1,2))
        if self.checkBox_4.isChecked():
            self.processTwiter.processCommentTwiter(cookies=self.cookies,twiterID=self.twiterID,countFriends=self.numberTagFriend)
            self.tableStatus.emit(self.count, 'Comment bài viết')
            sleep(randint(1,2))
        self.tableStatus.emit(self.count, 'Thành công')







if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    UiWindow = UI()
    app.exec()