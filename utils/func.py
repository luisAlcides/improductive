import hashlib

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox, QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox

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


def cb_fill_category_habit(cb, controller):
    cb.clear()
    category_habit = controller.get_category_habits()
    for category in category_habit:
        cb.addItem(category[0])


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


def data_of_table_all(table):
    data = []
    for row in range(table.rowCount()):
        row_data = [table.item(row, col).text()
                    for col in range(table.columnCount())]
        data.append(row_data)

    return data


def delete_from_table(table, controller=None, data=None):
    selected_rows = table.selectionModel().selectedRows()
    for row in selected_rows:
        item_name = table.item(row.row(), 0).text()
        if controller is not None:
            item_id = controller.get_id(item_name)
            controller.delete(item_id)
        table.removeRow(row.row())


def edit_from_table(table, controller, data):
    selected_rows = table.selectionModel().selectedRows()
    for row in selected_rows:
        item_name = table.item(row.row(), 0).text()
        if controller is not None:
            item_id = controller.get_id(item_name)
            return controller.get_data_for_update(item_id)

def edit_from_table_today(table, controller, data):
    selected_rows = table.selectionModel().selectedRows()
    for row in selected_rows:
        item_name = table.item(row.row(), 0).text()
        if controller is not None:
            item_id = controller.get_id_study_today(item_name)
            return item_id


def message(message):
    mBox = QMessageBox()
    mBox.setText(message)
    mBox.exec()


def message_delete():
    message = QMessageBox()
    message.setWindowTitle('Delete')
    message.setText('Do you want to delete')

    message.addButton(QMessageBox.StandardButton.Yes)
    message.addButton(QMessageBox.StandardButton.No)
    message.button(QMessageBox.StandardButton.Yes).setText('Yes')
    message.button(QMessageBox.StandardButton.No).setText('No')

    button = message.exec()
    return button


def message_edit():
    message = QMessageBox()
    message.setWindowTitle('Update')
    message.setText('Do you want to update?')

    message.addButton(QMessageBox.StandardButton.Yes)
    message.addButton(QMessageBox.StandardButton.No)
    message.button(QMessageBox.StandardButton.Yes).setText('Yes')
    message.button(QMessageBox.StandardButton.No).setText('No')

    button = message.exec()
    return button


def limit_Double_spin(object):
    object.setMinimum(0)
    object.setMaximum(9999999.99)


def clean_fields(fields):
    for field in fields:
        if type(field[0]) == QLineEdit:
            field[0].setText('')
        if type(field[0]) == QTextEdit:
            field[0].setPlainText('')
        if type(field[0]) == QComboBox:
            field[0].setCurrentIndex(-1)
        if type(field[0]) == QSpinBox:
            field[0].setValue(0)
        if type(field[0]) == QDoubleSpinBox:
            field[0].setValue(0.0)
