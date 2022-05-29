import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import pymongo
import random
import math
import smtplib

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("form1.ui",self)
        self.pushButtonlogin.clicked.connect(self.loginfunction)
        self.lineEditpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButtonsignup.clicked.connect(self.gotocreate)
        self.pushButtonforegatepassword.clicked.connect(self.gotoforegotpass)

    def loginfunction(self):
        email = self.lineEditusername.text()
        password = self.lineEditpassword.text()
        client = pymongo.MongoClient()
        mydb = client['mydb']
        mycol = mydb["people"]
        data = {'name': email, 'password': password}

        if mycol.find_one(data):
            print("Successfully logged in with email: ", email, "and password:", password)
        else:
            print("username not found")

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoforegotpass(self):
        forgotpass = ForgotPass()
        widget.addWidget(forgotpass)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("form.ui",self)
        self.pushButtonsignup1.clicked.connect(self.create_db)
        self.lineEditpassword1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditconfrimpassword1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.beackbutton.clicked.connect(self.beackfunc)


    def create_db(self):
        password = self.lineEditpassword1.text()
        email = self.lineEditusername1.text()
        if self.lineEditpassword1.text() == self.lineEditconfrimpassword1.text():

            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)

            try:
                client = pymongo.MongoClient()
                mydb = client['mydb']
                mycol = mydb["people"]
                data = {'name':email,'password':password}
                if mycol.insert_one(data):
                    print("Successfully created acc with email: ", email, "and password: ", password)

            except Exception as e:
                print("Something went wrong....", e)
    def beackfunc(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ForgotPass(QDialog):

    def __init__(self):
        super(ForgotPass,self).__init__()
        loadUi("form3.ui",self)
        self.lineEditpassword2zg.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditconfrimpassword1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButtonSubmmite.clicked.connect(self.submmitepass)
        self.pushButtonsendotp.clicked.connect(self.sendemail)

    def sendemail(self):
            email = self.lineEditusername2.text()
            client = pymongo.MongoClient()
            mydb = client['mydb']
            mycol = mydb["people"]
            data = {'name': email}
            if(mycol.find_one(data)):
                digits = [i for i in range(0, 10)]
                global random_str
                random_str = ""
                for i in range(6):
                    index = math.floor(random.random() * 10)
                    random_str += str(digits[index])
                print(random_str)
                domainemail = "dhruveshborad007@gmail.com"
                domainpass = "Dh@#$008"
                useremail = self.lineEditusername2.text()
                try:
                    # Create your SMTP session
                    smtp = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp.starttls()
                    smtp.login(domainemail,domainpass )
                    message = random_str
                    smtp.sendmail(domainemail, useremail, message)
                    smtp.quit()
                    print("Email sent successfully!")

                except Exception as ex:
                    print("Something went wrong....", ex)
            else:
                print("username is invelide....")
    def submmitepass(self):
        if (self.lineEditpassword2.text() == self.lineEditconfrimpassword1.text() and random_str == self.lineEditotp.text()):
            email = self.lineEditusername2.text()
            client = pymongo.MongoClient()
            mydb = client['mydb']
            mycol = mydb["people"]
            if(mycol.find_one_and_update({'name': email},{'$set':{'password':self.lineEditpassword2.text()}})):
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                print("true")

app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(701)
widget.setFixedHeight(467)
widget.show()
app.exec_()