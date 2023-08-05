from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from numpy import array
import sqlite3


class contact:
    def __init__(self, first_name, last_name, adress, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.adress = adress
        self.phone_number = phone_number
        self.email = email
    
    def addToDataBase(self, c):
        c.execute("INSERT INTO contacts VALUES(?, ?, ?, ?, ?)",(self.first_name, self.last_name, self.adress, self.phone_number, self.email))
        conn.commit()
    

conn = sqlite3.connect('contact.db')
c = conn.cursor()

c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            first_name TEXT,
            last_name TEXT,
            adress TEXT,
            phone_number TEXT,
            email TEXT
        )
    """)

conn.commit()


def check_existance(phone_number):
    c.execute("SELECT * FROM contacts WHERE phone_number = '{}'".format(phone_number))
    return len(c.fetchall())



def addContact():
    #input controle
    first_name = addWindow.firstNameInput.text()
    last_name = addWindow.lastNameInput.text()
    adress = addWindow.adressInput.text()
    phone_number = addWindow.phoneNumberInput.text()
    if check_existance(phone_number) != 0:
        Error = QMessageBox()
        Error.setIcon(QMessageBox.Critical)
        Error.setText("An error occurred")
        Error.setInformativeText("This phone number existe before.")
        Error.setWindowTitle("Error")
        Error.exec_()
        return False
    email = addWindow.emailInput.text()
    newContact = contact(first_name, last_name, adress, phone_number, email)
    newContact.addToDataBase(c)
    addWindow.close()
    displayContacts()


def displayContacts():
    mainWindow.contactTab.setRowCount(0)
    search = '%' + mainWindow.searchBar.text() + '%'
    if mainWindow.ASCRadio.isChecked():
        order = 'ASC'
    else:
        order = 'DESC'
    if search == "%%":
        c.execute("""
        SELECT * FROM contacts ORDER BY first_name {}
        """.format(order))
    else:
        c.execute("""
            SELECT * FROM contacts WHERE first_name LIKE ? OR last_name LIKE ? ORDER BY first_name {}
        """.format(order), (search, search))
    
    contactArray = c.fetchall()
    for i in range(len(contactArray)):
        mainWindow.contactTab.insertRow(i)
        for j in range(5):
            mainWindow.contactTab.setItem(i, j, QTableWidgetItem(str(contactArray[i][j])))



def deleteContact():
    row = mainWindow.contactTab.currentRow()
    if row == -1 :
        Error = QMessageBox()
        Error.setText("An error occurred")
        Error.setInformativeText("Please select a contact to delete.")
        Error.setIcon(QMessageBox.Critical)
        Error.setWindowTitle("Error")
        Error.exec_()
        return False
    phone_number = mainWindow.contactTab.item(row, 3).text()
    c.execute("DELETE FROM contacts WHERE phone_number = {}".format(phone_number))
    conn.commit()
    displayContacts()

def showEditWindow():
    row = mainWindow.contactTab.currentRow()
    if row == -1:
        Error = QMessageBox()
        Error.setIcon(QMessageBox.Critical)
        Error.setText("An error occurred")
        Error.setInformativeText("Please select a contact to edit.")
        Error.setWindowTitle("Error")
        Error.exec_()
        return False
    else:
        editWindow.show()
        editWindow.firstNameInput.setText(mainWindow.contactTab.item(row, 0).text())
        editWindow.lastNameInput.setText(mainWindow.contactTab.item(row, 1).text())
        editWindow.adressInput.setText(mainWindow.contactTab.item(row, 2).text())
        editWindow.phoneNumberInput.setText(mainWindow.contactTab.item(row, 3).text())
        editWindow.emailInput.setText(mainWindow.contactTab.item(row, 4).text())
        

def editContact():
    row = mainWindow.contactTab.currentRow()
    first_name = editWindow.firstNameInput.text()
    last_name = editWindow.lastNameInput.text()
    adress = editWindow.adressInput.text()
    phone_number = editWindow.phoneNumberInput.text()
    if check_existance(phone_number) != 1:
        Error = QMessageBox()
        Error.setIcon(QMessageBox.Critical)
        Error.setText("An error occurred")
        Error.setInformativeText("This phone number existe before.")
        Error.setWindowTitle("Error")
        Error.exec_()
        return False
    email = editWindow.emailInput.text()

    c.execute("UPDATE contacts SET first_name = ?, last_name = ?, adress = ?, phone_number = ?, email = ? WHERE phone_number = ?",(first_name, last_name, adress, phone_number, email, phone_number))
    conn.commit()
    displayContacts()
    editWindow.close()

app = QApplication([])
mainWindow = loadUi("main.ui")
addWindow = loadUi("add.ui")
editWindow = loadUi("edit.ui")
displayContacts()

mainWindow.addBtn.clicked.connect(addWindow.show)
mainWindow.displayBtn.clicked.connect(displayContacts)
mainWindow.editBtn.clicked.connect(showEditWindow)
mainWindow.deleteBtn.clicked.connect(deleteContact)
addWindow.addBtn.clicked.connect(addContact)
addWindow.cancelBtn.clicked.connect(addWindow.close)
editWindow.editBtn.clicked.connect(editContact)
editWindow.cancelBtn.clicked.connect(editWindow.close)

mainWindow.searchBar.textChanged.connect(displayContacts)
mainWindow.show()
app.exec_()