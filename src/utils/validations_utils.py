import re


def int_input(message):
    while True:
        input_num = input(message)
        if input_num.isdigit():
            return int(input_num)
        else:
            print("Invalid input try again")


def validate_email(email):
    match = re.fullmatch(
        r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b$", email
    )
    return bool(match)


def validate_phone(phone):
    phone_str = str(phone)
    match = re.fullmatch(r"^\d{10}$", phone_str)
    return bool(match)


def validate_pin_code(pin):
    pin_str = str(pin)
    match = re.fullmatch(r"^\d{6}$", pin_str)
    return bool(match)


def validate_password(password):
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    match = re.match(pattern, password)

    return bool(match)


def check_email_format(email):
    if validate_email(email):
        return email
    else:
        raise ValueError("Invalid email format")


def check_phone_format(phone):
    if validate_phone(phone):
        return phone
    else:
        raise ValueError("Invalid phone number format")


def check_pin_code_format(pin):
    if validate_pin_code(pin):
        return pin
    else:
        raise ValueError("Invalid pin code format")


def check_password_format(password):
    if validate_password(password):
        return password
    else:
        raise ValueError("Invalid password format")
