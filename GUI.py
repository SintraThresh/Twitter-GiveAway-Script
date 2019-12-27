from PyQt5 import QtCore, QtGui, QtWidgets
import json
import GiveAway
import webbrowser

class winnerWindow():
    def winnerFunc(self, thirdWindow, winners):
        if len(winners) > 1:
            print(winners)
            thirdWindow.setObjectName('WinnerWindow')
            thirdWindow.resize(300, 500)
            thirdWindow.setMinimumSize(QtCore.QSize(300, 500))
            thirdWindow.setMaximumSize(QtCore.QSize(300, 500))
            self.thirdWindowCenter = QtWidgets.QWidget(thirdWindow)
            #self.list = QtWidgets.QTextBrowser(thirdWindow)
            #self.list.setGeometry(10, 10, 280, 480)
            self.groupbox = QtWidgets.QGroupBox(self.thirdWindowCenter)
            self.groupbox.setGeometry(0,0, 280, 500)
            self.formLayout = QtWidgets.QFormLayout(self.thirdWindowCenter)
            self.formLayout.setContentsMargins(0,0,0,0)
            thirdWindow.setCentralWidget(self.thirdWindowCenter)
            self.cycle = 0
            for sepWinners in winners:
                self.cycle +=1
                labeling = QtWidgets.QLabel()
                labeling.setText(f'{self.cycle}.<a href="https://www.twitter.com/{sepWinners}">{sepWinners}')
                labeling.setOpenExternalLinks(True)
                self.labelingFont = QtGui.QFont()
                self.labelingFont.setPointSize(15)
                labeling.setFont(self.labelingFont)

                self.formLayout.addRow(labeling)
            self.groupbox.setLayout(self.formLayout)
            self.scroll = QtWidgets.QScrollArea(self.thirdWindowCenter)
            self.scroll.setGeometry(0,0, 300, 500)
            self.scroll.setWidget(self.groupbox)
            self.scroll.setWidgetResizable(True)

            #for sepWinners in winners:
            #    sortedWinners = F'1. {sepWinners}'
            #    self.list.insertItem(1, sortedWinners)
        elif len(winners) == 1:
            winners = winners[0]
            thirdWindow.setObjectName('WinnerWindow')
            thirdWindow.resize(700, 250)
            thirdWindow.setMinimumSize(QtCore.QSize(700, 250))
            thirdWindow.setMaximumSize(QtCore.QSize(700, 250))
            self.thirdWindowCenter = QtWidgets.QWidget(thirdWindow)
            self.thirdWindowCenter.setObjectName('ThirdWindowCenter')
            self.labelWin = QtWidgets.QLabel(self.thirdWindowCenter)
            self.labelWin.setGeometry(QtCore.QRect(0, 0, 700, 180))
            self.labelWin.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
            self.hypeLink = QtWidgets.QLabel(self.thirdWindowCenter)
            self.hypeLink.setGeometry(QtCore.QRect(0, 155, 700, 70))


            thirdWindow.setCentralWidget(self.thirdWindowCenter)
            translate = QtCore.QCoreApplication.translate
            self.labelWin.setText(translate('thirdWindow', '{}'.format(winners)))
            self.winnerFont = QtGui.QFont()
            self.winnerFont.setBold(True)
            self.winnerFont.setPointSize(55)
            self.labelWin.setFont(self.winnerFont)
            self.hypeLink.setOpenExternalLinks(True)
            self.hypeLink.setText(f'<a href="https://www.twitter.com/{winners}">@{winners}')
            self.hypeLink.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
            self.hypeFont = QtGui.QFont()
            self.hypeFont.setPointSize(16)
            self.hypeLink.setFont(self.hypeFont)
        else:
            print(len(winners))

class Worker(QtCore.QThread):
    all_done = QtCore.pyqtSignal(object)
    def __init__(self, tweetLink, followers, winCount, tAgeDays):
        super(Worker, self).__init__()
        self.tweetLink = tweetLink
        self.followers = followers
        self.winCount = winCount
        self.tAgeDays = tAgeDays

    def next_step(self):
        winners = GiveAway.GStart(self.tweetLink, self.followers, self.winCount, self.tAgeDays)
        self.all_done.emit(winners)
    def run(self):
        self.next_step()

class keyWindow():
    def keyWinFunc(self, secondWindow):
        secondWindow.setObjectName("MainWindow")
        secondWindow.resize(500, 150)
        secondWindow.setMinimumSize(QtCore.QSize(500, 150))
        secondWindow.setMaximumSize(QtCore.QSize(500, 150))
        self.centralwidgetKey = QtWidgets.QWidget(secondWindow)
        self.centralwidgetKey.setObjectName('CentralWidgetKey')
        self.labelKey = QtWidgets.QLabel(self.centralwidgetKey)
        self.labelKey.setGeometry(QtCore.QRect(5, 5, 101, 16))
        self.labelKey.setObjectName("label_key")
        self.labelKeySecret = QtWidgets.QLabel(self.centralwidgetKey)
        self.labelKeySecret.setGeometry(QtCore.QRect(5, 31, 101, 16))
        self.labelKeySecret.setObjectName('Label_Key_Secret')
        self.labelToken = QtWidgets.QLabel(self.centralwidgetKey)
        self.labelToken.setGeometry(QtCore.QRect(5, 57, 101, 16))
        self.labelToken.setObjectName('Label_Token')
        self.labelTokenSecret = QtWidgets.QLabel(self.centralwidgetKey)
        self.labelTokenSecret.setGeometry(QtCore.QRect(5, 83, 101, 16))
        self.labelTokenSecret.setObjectName('Label_Token_Secret')
        self.saveButton = QtWidgets.QPushButton(self.centralwidgetKey)
        self.saveButton.setGeometry(QtCore.QRect(220, 130, 60, 20))
        self.saveButton.setObjectName('Button_Save')
        self.saveButton.clicked.connect(self.saveBtn)
        self.saveButton.clicked.connect(secondWindow.close)
        #Key
        self.key = QtWidgets.QLineEdit(self.centralwidgetKey)
        self.key.setGeometry(QtCore.QRect(75, 5, 415, 20))
        self.key.setObjectName('Key_Edit')
        #Key Secret
        self.keySecret = QtWidgets.QLineEdit(self.centralwidgetKey)
        self.keySecret.setGeometry(QtCore.QRect(75, 31, 415, 20))
        self.keySecret.setObjectName('KeySecret_Edit')
        #Token
        self.Token = QtWidgets.QLineEdit(self.centralwidgetKey)
        self.Token.setGeometry(QtCore.QRect(75, 57, 415, 20))
        self.Token.setObjectName('Token_Edit')
        #Token Secret
        self.tokenSecret = QtWidgets.QLineEdit(self.centralwidgetKey)
        self.tokenSecret.setGeometry(QtCore.QRect(75, 83, 415, 20))
        self.tokenSecret.setObjectName('TokenSecret_Edit')

        secondWindow.setCentralWidget(self.centralwidgetKey)
        translate = QtCore.QCoreApplication.translate
        self.labelKey.setText(translate("secondWindow", 'Key:'))
        self.labelKeySecret.setText(translate("secondWindow", 'Key Secret:'))
        self.labelToken.setText(translate("secondWindow", 'Token:'))
        self.labelTokenSecret.setText(translate("secondWindow", 'Token Secret:'))
        self.saveButton.setText(translate("secondWindow", 'Save'))
        QtCore.QMetaObject.connectSlotsByName(secondWindow)


        try:
            with open('twitter_credential.json', 'r') as reInput1:
                reInput = json.load(reInput1)
                self.key.setText(reInput['CONSUMER_KEY'])
                self.keySecret.setText(reInput['CONSUMER_SECRET'])
                self.Token.setText(reInput['ACCESS_TOKEN'])
                self.tokenSecret.setText(reInput['ACCESS_SECRET'])
        except FileNotFoundError:
            pass

    def saveBtn(self):
        newCred = {"CONSUMER_KEY": self.key.text().replace(' ',''),
                "CONSUMER_SECRET": self.keySecret.text().replace(' ',''),
                "ACCESS_TOKEN": self.Token.text().replace(' ',''),
                "ACCESS_SECRET": self.tokenSecret.text().replace(' ','')}
        with open('twitter_credential.json','w') as creds:
            json.dump(newCred, creds)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(498, 300)
        MainWindow.setMinimumSize(QtCore.QSize(498, 300))
        MainWindow.setMaximumSize(QtCore.QSize(498, 300))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(350, 0, 141, 280))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.clicked)

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 179, 351, 181))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 5, 101, 16))
        self.label.setObjectName("label")
        self.tAge = QtWidgets.QLabel(self.centralwidget)
        self.tAge.setGeometry(QtCore.QRect(80, 95, 110, 16))
        self.tAge_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.tAge_edit.setGeometry(QtCore.QRect(80, 115, 100, 20))
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(2, 25, 341, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.tweetInput = QtWidgets.QLabel(self.centralwidget)
        self.tweetInput.setGeometry(QtCore.QRect(0, 50, 101, 16))
        self.tweetInput.setObjectName("tweetInput")
        self.followerEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.followerEdit.setGeometry(QtCore.QRect(2, 70, 341, 20))
        self.followerEdit.setObjectName("followerEdit")
        self.followerEdit.returnPressed.connect(self.pressed)
        self.winnerCountLabel = QtWidgets.QLabel(self.centralwidget)
        self.winnerCountLabel.setGeometry(QtCore.QRect(0, 95, 101, 16))
        self.winnerCountLabel.setObjectName("WinnerCountLabel")
        self.winnerCountEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.winnerCountEdit.setGeometry(QtCore.QRect(2, 115, 50, 20))
        self.winnerCountEdit.setObjectName('WinnerCountEdit')

        self.kError = QtWidgets.QLabel(self.centralwidget)
        self.kError.setGeometry(QtCore.QRect(2, 90, 341, 16))
        self.kError.setObjectName("kError")
        self.tError = QtWidgets.QLabel(self.centralwidget)
        self.tError.setGeometry(QtCore.QRect(2, 90, 341, 16))
        self.tError.setObjectName("tError")
        self.rError = QtWidgets.QLabel(self.centralwidget)
        self.rError.setGeometry(QtCore.QRect(2, 90, 341, 16))
        self.rError.setObjectName("rError")
        self.error = QtWidgets.QLabel(self.centralwidget)
        self.error.setGeometry(QtCore.QRect(2, 90, 341, 16))
        self.error.setObjectName("error")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 498, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def pressed(self):
        copiedText = self.followerEdit.text()
        self.listWidget.insertItem(1, str(copiedText))
        self.followerEdit.clear()
    def clicked(self):
        self.listWidget.takeItem(self.listWidget.currentRow())


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.setText(_translate("MainWindow", "Change Keys"))
        self.pushButton_2.clicked.connect(self.keyChecker)
        self.label.setText(_translate("MainWindow", "Target Tweet Link:"))
        self.tweetInput.setText(_translate("MainWindow", "Required To Follow:"))
        self.winnerCountLabel.setText(_translate("MainWindow", "# Winners"))
        self.winnerCountEdit.setText(_translate("MainWindow", '1'))
        self.tAge.setText(_translate("MainWindow", 'Account Age (in days)'))

        self.kError.setStyleSheet('color: red')
        self.kError.hide()
        self.kError.setText(_translate("MainWindow", "Key Error! Please re-check your keys."))
        self.rError.setStyleSheet('color: red')
        self.rError.setText(_translate("MainWindow", "Rate limit exceeded! Please try again in 15 minutes."))
        self.rError.hide()
        self.tError.setStyleSheet('color: red')
        self.tError.setText(_translate("MainWindow", "Invalid Tweet link, please re-check your link."))
        self.tError.hide()
        self.error.setStyleSheet('color: red')
        self.error.setText(_translate("MainWindow", "An error has occured, please try again."))
        self.error.hide()

    def winFunc(self, winners):
        _translate = QtCore.QCoreApplication.translate
        if winners in ['|keys|', '|tweet|', '|rate|', '|Error|']:
            self.pushButton.setDisabled(False)
            self.pushButton_2.setDisabled(False)
            if winners == '|keys|':
                self.kError.show()
            elif winners == '|tweet|':
                self.tError.show()
            elif winners == '|rate|':
                self.rError.show()
            elif winners == '|Error|':
                self.error.show()
        else:
            self.pushButton.setDisabled(False)
            self.pushButton_2.setDisabled(False)
            self.thirdWindow = QtWidgets.QMainWindow()
            self.win = winnerWindow()
            self.win.winnerFunc(self.thirdWindow, winners)
            self.thirdWindow.show()
            self.pushButton.setDisabled(False)
            self.pushButton_2.setDisabled(False)

    def start(self):
        self.kError.hide()
        self.rError.hide()
        self.tError.hide()
        self.error.hide()
        self.lineEdit.setFocus(False)
        self.tweetInput.setFocus(False)
        self.pushButton.setDisabled(True)
        self.pushButton_2.setDisabled(True)
        tweetLink = self.lineEdit.text()
        winCount = self.winnerCountEdit.text()
        tAgeDays = self.tAge_edit.text()
        followers = []
        for followerItem in range(0, self.listWidget.count()):
            followers.append(self.listWidget.item(followerItem).text())
        self.worker = Worker(tweetLink, followers, winCount, tAgeDays)
        self.worker.start()
        self.worker.all_done.connect(self.winFunc)

        

    def keyChecker(self):
        alertButton = QtWidgets.QMessageBox()
        alertButton.setWindowTitle('Alert!')
        alertButton.setText("Do you want to edit keys?")
        alertButton.setIcon(QtWidgets.QMessageBox.Question)
        alertButton.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        alertButton.setDefaultButton(QtWidgets.QMessageBox.No)
        alertButton.buttonClicked.connect(self.alertwind)
        a = alertButton.exec_()

    def alertwind(self, i):
        if i.text() == "&Yes":
            self.secondWindow = QtWidgets.QMainWindow()
            self.keyWin = keyWindow()
            self.keyWin.keyWinFunc(self.secondWindow)
            self.secondWindow.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
