from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from PyQt5 import QtWidgets , QtCore
from PyQt5.QtWidgets import QDialog, QApplication,QDateEdit, QTextEdit,QListWidgetItem,QMessageBox
from PyQt5.uic import loadUi
import pymongo
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import datetime

class MainWidget(QMainWindow): #main windows
    def __init__(self):
        super(MainWidget, self).__init__()
        loadUi("form4.ui", self)
        self.updateTask()
        i = 0
        my_date = datetime.datetime(2022, 1, 1)
        self.TaskButton.clicked.connect(self.AddSubTasks)   #  add subtask by bittoon
        self.savechangies.clicked.connect(self.task1SaveChangies)  # save changies main windows listwidgets
        while i < 365:                                     #  one years date set in listwidget
            my_date_days = my_date + datetime.timedelta(days=i)
            date = str(my_date_days)
            item = QListWidgetItem(date)
            self.listWidget.addItem(item)
            i = i + 1
        global count
        count = 0

        self.TaskListWidget.itemChanged.connect(self.task1SaveChangies)
        self.TaskListWidget_2.itemChanged.connect(self.task1SaveChangies)
        self.TaskListWidget_3.itemChanged.connect(self.task1SaveChangies)

        global datadic1
        datadic1 = {}
        global datadic2
        datadic2 = {}
        global datadic3
        datadic3 = {}

        self.TaskListWidget.itemDoubleClicked.connect(self.AddSubTasks)
        self.TaskListWidget_2.itemDoubleClicked.connect(self.AddSubTasks)
        self.TaskListWidget_3.itemDoubleClicked.connect(self.AddSubTasks)

        if count == 1:
            self.SaveChangies()
            count = count-1

    def updateTask(self):  #backend upate mongoDB
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb['people']
        x = mycol.find_one({'name': "dhruveshborad007@gmail.com"})
        print(x)
        try:
            for i in x['todo']:
                item1 = QListWidgetItem(i)
                self.TaskListWidget.addItem(item1)
        except Exception as ex:
            print("No have task.", ex)

        try:
            for i in x['inprogress']:
                item1 = QListWidgetItem(i)
                self.TaskListWidget_2.addItem(item1)
        except Exception as ex:
            print("worng....", ex)

        try:
            for i in x['done']:
                item1 = QListWidgetItem(i)
                self.TaskListWidget_3.addItem(item1)
        except Exception as ex:
            print("worng....", ex)

    def task1SaveChangies(self):
        datadic1 = {'todo': []}
        for i in range(self.TaskListWidget.count()):
            item = self.TaskListWidget.item(i)
            task = item.text()
            datadic1["todo"].append(task)
        print(datadic1)
        datadic2 = {"inprogress": []}
        for i in range(self.TaskListWidget_2.count()):
            item = self.TaskListWidget_2.item(i)
            task = item.text()
            datadic2["inprogress"].append(task)
        print(datadic2)
        datadic3 = {'done': []}
        for i in range(self.TaskListWidget_3.count()):
            item = self.TaskListWidget_3.item(i)
            task = item.text()
            datadic3['done'].append(task)
        print(datadic3)

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb['people']
        mycol.find_one_and_update({'name': "dhruveshborad007@gmail.com"}, {'$set': datadic1})
        mycol.find_one_and_update({'name': "dhruveshborad007@gmail.com"}, {'$set': datadic2})
        mycol.find_one_and_update({'name': "dhruveshborad007@gmail.com"}, {'$set': datadic3})
        count = 1


    def AddSubTasks(self):
        addtask = AddsubTask()
        widget.addWidget(addtask)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def selectdate(self):
        addtask = AddsubTaskEdit()
        widget.addWidget(addtask)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AddsubTask(QDialog):
    def __init__(self):
        super(AddsubTask, self).__init__()
        loadUi("form5.ui", self)
        self.CancleTask.clicked.connect(lambda: CancelTask())
        self.SaveTask.clicked.connect(self.saveTask)

        def CancelTask():
            calendar = MainWidget()
            widget.addWidget(calendar)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def saveTask(self):
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb['people']
        if mycol.find_one({'name': 'dhruveshborad007@gmail.com'}):
            mycol.find_one_and_update({'name': self.DevloperName.currentText()},
                                      {'$push': {'todo': self.TaskNo.text()}})
            mycol.insert_one({'userid': self.DevloperName.currentText(), 'task': self.TaskNo.text(),
                              'subtask': self.textEditTask.toPlainText(), 'commant': self.CommentEdit.toPlainText(),
                              'startdate': self.dateTimeEdit.text(), 'duedate': self.dateTimeEdit_2.text()
                              })

class AddsubTaskEdit(QDialog):  #add subtask widget
    def __init__(self):
        super(AddsubTaskEdit, self).__init__()
        loadUi("form5.ui", self)
        self.CancleTask.clicked.connect(lambda: CancelTask())  # cancle button on subtask widget
        self.SaveTask.clicked.connect(self.saveTask) #save task button in mongoDB

        def CancelTask():   # cancle subtask widget
            calendar = taskwidget()
            widget.addWidget(calendar)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def saveTask(self):  #save task in mongoDB
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb['people']
        if mycol.find_one({'name': 'dhruveshborad007@gmail.com'}):
            mycol.find_one_and_update({'name': self.DevloperName.currentText()},
                                      {'$push': {'todo': self.TaskNo.text()}})
            mycol.insert_one({'userid': self.DevloperName.currentText(), 'task': self.TaskNo.text(),
                              'subtask': self.textEditTask.toPlainText(), 'commant': self.CommentEdit.toPlainText(),
                              'startdate': self.dateTimeEdit.text(), 'duedate': self.dateTimeEdit_2.text()
                              })

    def updatesubtask(self):
        pass


app = QApplication(sys.argv)
mainwindow = MainWidget()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1500)
widget.setFixedHeight(720)
widget.show()
app.exec_()