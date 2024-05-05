import hashlib

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

from connection import Connection

con = Connection()


def hash_password(password):
    password_bytes = password.encode('utf-8')
    sha256 = hashlib.sha256(password_bytes)
    sha256.update(password_bytes)
    hashed_password = sha256.hexdigest()
    return hashed_password


def cb_deparment():
    try:
        with con as cursor:
            cursor.execute('SELECT name FROM deparment')
            deparments = cursor.fetchall()
            return deparments
    except Exception as e:
        print('Error getting deparments:', e)
        return []


def load_departaments(cb):
    deparments = cb_deparment()
    deparments = [deparment[0] for deparment in deparments]
    cb.addItems(deparments)



# This function add data to table
def add_to_table(table, data):
    row_position = table.rowCount()
    table.insertRow(row_position)
    for i, field in enumerate(data):
        item = QtWidgets.QTableWidgetItem(str(field))
        table.setItem(row_position, i, item)


# Get data from table
def data_of_table(table):
    selected_indexes = table.selectionModel().selectedRows()
    if len(selected_indexes) == 1:
        row = selected_indexes[0].row()
        data = [table.item(row, col).text() for col in
                range(table.columnCount())]
    return data


def delete_from_table(table, controller=None):
    selected_rows = table.selectionModel().selectedRows()
    for row in selected_rows:
        data_id = table.item(row.row(), 0).text()
        if controller is not None:
            controller.delete(data_id)
        table.removeRow(row.row())


def message(message):
    mBox = QMessageBox()
    mBox.setText(message)
    mBox.exec()


def message_delete():
    message = QMessageBox()
    message.setWindowTitle('Eliminar Producto')
    message.setText('¿Desea eliminar este producto?')

    message.addButton(QMessageBox.StandardButton.Yes)
    message.addButton(QMessageBox.StandardButton.No)
    message.button(QMessageBox.StandardButton.Yes).setText('Sí')
    message.button(QMessageBox.StandardButton.No).setText('No')

    button = message.exec()
    return button


def limit_Double_spin(object):
    object.setMinimum(0)
    object.setMaximum(9999999.99)
