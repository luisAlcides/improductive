import re
from PySide6.QtWidgets import QMessageBox, QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox

from utils.func import hash_password, message

CB_CURRENT_0 = ['Seleccionar', 'Departamento', 'Municipio', '']


def validate_names(text, lbl):
    if lbl in ['Primer nombre', 'Primer apellido'] and not text.text().strip():
        message(f'El campo {lbl} no puede estar vacio')
        text.setFocus()
        return False

    if text.text().strip() and not re.match(r'^[a-zA-Z]+$', text.text().strip()):
        message(f'El campo {lbl} solo puede contener letras')
        text.setFocus()
        return False
    return True


def validate_text(text, lbl):
    if not text.text().strip():
        message(f'El campo {lbl} no puede estar vacio')
        text.setFocus()
        return False
    if not re.match(r'^[a-zA-Z ]+$', text.text().strip()):
        message(f'El campo {lbl} solo puede contener letras')
        text.setFocus()
        return False
    return True


def validate_username(username):
    if not username.text().strip():
        message('El usuario no puede estar vacio')
        username.setFocus()
        return False
    if len(username.text().strip()) < 4:
        message('El usuario debe contener al menos 4 caracteres')
        username.setFocus()
        return False
    return True


def validate_password(password):
    if not password.text().strip():
        message('Debe ingrese la contraseña')
        password.setFocus()
        return False
    if len(password.text().strip()) < 8:
        message('La contraseña debe contener al menos 8 caracteres')
        password.setFocus()
        return False
    if not re.search(r'\d', password.text().strip()):
        message('La contraseña debe contener al menos un numero')
        password.setFocus()
        return False
    if not re.search(r'[A-Z]]', password.text().strip()):
        message('La contraseña debe contener al menos una letra mayuscula')
        password.setFocus()
        return False
    if not re.search(r'[a-z]', password.text().strip()):
        message('La contraseña debe contener al menos una letra minuscula')
        password.setFocus()
        return False
    return True


def validate_phone(phone):
    if not phone.text().strip():
        message('Debe ingresar el numero de telefono')
        phone.setFocus()
        return False
    if not re.match(r'^\d{8}$', phone.text().strip()):
        message('El numero de telefono debe contener 8 digitos')
        phone.setFocus()
        return False
    return True


def validate_role(role):
    if role not in ['admin', 'user']:
        message('Debe seleccionar un rol')
        return False
    return True


def validate_number(number, lbl):
    if not float(number.text().strip()):
        message(f'El campo {lbl} no puede estar vacio')
        number.setFocus()
        return False
    if not isinstance(float(number.text().strip()), (int, float)):
        message(f'El campo {lbl} debe ser un número')
        number.setFocus()
        return False
    return True


def validate_id_number(id_number):
    pattern = r'^\d{3}-\d{6}-\d{4}[a-zA-Z]?$'
    if not re.match(pattern, id_number.text().strip()):
        message('El numero de identidad no es valido')
        return False
    return True


def validate_foreign_key(fk, lbl):
    if not int(fk.text().strip()):
        message(f'El campo {lbl} no puede estar vacio')
        return False
    return True


def validate_toPlainText(description, lbl):
    description = description.toPlainText()
    if description and (not description.strip()
                        or all(char.isdigit()
                               or not char.isalnum()
                               for char in description)):
        message(f'Este formato para el campo {lbl} no es permitido utiliza una mejor descripción')
        return False
    return True


def validate_cb(cb, lbl):
    if cb.currentText() in CB_CURRENT_0:
        message(f'Debe seleccionar una opción para {lbl}')
        return False
    return True


def validate_address(address, lbl):
    if not address.text().strip():
        message(f'El campo {lbl} no puede estar vacio')
        return False
    if not re.match(r'^[a-zA-Z0-9 /]+$', address.text().strip()):
        message(f'El campo {lbl} contiene caracteres inválidos. Solo se permiten letras, números, espacios y "/".')
        return False
    return True


def validate_password_hash(input_password, stored_hash):
    hashed_input_password = hash_password(input_password)

    if hashed_input_password == stored_hash:
        return True
    else:
        return False


def validate_fields(fields):
    try:
        for field in fields:
            if field[1] == 'text':
                if not validate_text(field[0], field[2].text()):
                    return False
            elif field[1] == 'number':
                if not validate_number(field[0], field[2].text()):
                    return False
            elif field[1] == 'names':
                if not validate_names(field[0], field[2].text()):
                    return False
            elif field[1] == 'username':
                if not validate_username(field[0]):
                    return False
            elif field[1] == 'password':
                if not validate_password(field[0]):
                    return False
            elif field[1] == 'phone':
                if not validate_phone(field[0]):
                    return False
            elif field[1] == 'id_number':
                if not validate_id_number(field[0]):
                    return False
            elif field[1] == 'largeText':
                if not validate_toPlainText(field[0], field[2].text()):
                    return False
            elif field[1] == 'cb':
                if not validate_cb(field[0], field[2].text()):
                    return False
            elif field[1] == 'address':
                if not validate_address(field[0], field[2].text()):
                    return False

    except TypeError as e:
        print(f'Ha ocurrido un error de tipo: {e}')
    except ValueError as e:
        print(f'Error de valor: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}, {field[2]}')

    return True

