
from PyQt6.QtWidgets import *
from maingui import *
from report import *
import csv

#import data.csv

class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        #self.ui = Ui_SecWindow()

        self.setFixedSize(315,387)
        self.ui = Ui_SecWindow()
        self.__cont = True
        #self.__choice = False
        self.listWidget.itemActivated.connect(self.edit)

        self.pushButton.clicked.connect(lambda: self.edit())

        self.pushButton_2.clicked.connect(lambda: self.openWindow())



        self.fill()

    def fill(self) -> None:
        """
        Method fills listWidget with names to click on
        from data.csv

        :return:
        """
        self.listWidget.clear()
        with open("data.csv", 'r', newline="") as f:
            for row in f:


                #else:

                    #list_name = row.split(',')[0]
                list_name = row.split(',')[0]
                self.listWidget.addItem(list_name)
        #self.listWidget.clear()

    def openWindow(self) -> None:
        """
        This method opens the second window and controls what
        the buttons for that window do.
        :return:
        """
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SecWindow()
        self.ui.setupUi(self.window)
        self.window.setFixedSize(287, 504)
        self.window.show()

        self.ui.done.clicked.connect(lambda: self.add())

        self.ui.butt_del.clicked.connect(lambda: self.close())


    def add(self) -> None:
        """
        When the user clicks the "ADD" button, they are brought
        here. This takes the values in the fields in window #2 and
        adds them to data.csv
        :return:
        """
        name = str(self.ui.nameedit.text())
        sports = str(self.ui.sportedit.text())
        pre_cal = str(self.ui.precaledit.text())
        computer = str(self.ui.computersciedit.text())
        history = str(self.ui.historyedit.text())
        text = self.ui.notepad.toPlainText()

        values = [name, sports, pre_cal, computer, history, text]

        for i in values:
            if i.isnumeric() or i == '':
                #print('no numbers or blanks pls')
                self.__cont = False
                self.ui.warning_error.setText('No numbers or blanks please')
                break


        for i in values[1:4]:
            if i not in ['A', 'B', 'C', 'D', 'F']:
                #print('no numbers or blanks pls')
                self.__cont = False
                self.ui.warning_error.setText('No numbers or blanks please')
                break

        else:
            self.__cont = True

        if self.__cont:
            with open('data.csv', 'a', newline="") as f:
                csvwriter = csv.writer(f)
                csvwriter.writerow(values)
                #print('done')


                self.listWidget.addItem(name)
            self.close()


    def edit(self) -> None:
        """
        This method edits the data.csv file. Detects if user clicked a name in
        listWidget. If so, extracts all data from csv file, edits selected line,
        and writes it back into a cleared csv file.
        :return:
        """
        lines = []
        d = self.listWidget.currentItem()
        if d is None:
            self.select_error.setText("Please select a name")
        else:
            with open("data.csv", 'r', newline="") as f:
                csv_file = csv.reader(f)
                for row in csv_file:
                    if row[0] == d.text():
                        remove = row[0]
                        self.openWindow()
                        self.ui.nameedit.setText(row[0])
                        self.ui.sportedit.setText(row[1])
                        self.ui.precaledit.setText(row[2])
                        self.ui.computersciedit.setText(row[3])
                        self.ui.historyedit.setText(row[4])
                        self.ui.notepad.setPlainText(row[5])

            with open("data.csv", 'r', newline="") as f:
                csv_file = csv.reader(f)
                for row in csv_file:
                    if row[0] == remove:
                        row.pop()
                    else:
                        lines.append(row)



            with open("data.csv", 'w', newline="") as f:
                csvwriter = csv.writer(f)
                csvwriter.writerows(lines)
            self.fill()


    def close(self) -> None:
        """
        method closes second window.
        :return:
        """
        self.window.close()