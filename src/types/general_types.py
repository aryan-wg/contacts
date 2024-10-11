from typing import Annotated, Optional
from pydantic import BaseModel
from enum import Enum
from pydantic.functional_validators import AfterValidator
from ..utils.validations_utils import (
    check_password_format,
    check_email_format,
    check_phone_format,
    check_pin_code_format,
)


Password = Annotated[str, AfterValidator(check_password_format)]
Email = Annotated[str, AfterValidator(check_email_format)]
PostalCode = Annotated[int, AfterValidator(check_phone_format)]
Phone = Annotated[str, AfterValidator(check_pin_code_format)]


class ChangePassBody(BaseModel):
    old_pass: Password
    new_pass: Password


class UserTypeEnum(str, Enum):
    admin = "admin"
    hr = "hr"
    worker = "worker"


class Token(BaseModel):
    access_token: str
    token_type: str


class Address(BaseModel):
    street: str
    postal_code: PostalCode
    city: str
    state: str
    country: str


class EmployeeInfo(BaseModel):
    password: Password
    user_type: UserTypeEnum
    name: str
    phone: Phone
    email: Email
    address: Address
    # reports to should be optional or somone can say its 0
    reports_to: Optional[int]
