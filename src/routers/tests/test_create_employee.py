import pytest
from unittest.mock import AsyncMock, Mock
from ..employee_router import create_employee
from ...execptions.HttpExceptions import InvalidValueErr, InternalServerErr
from ...types.general_types import EmployeeInfo
from ...entities.admin.admin import Admin
from fastapi import Request
import json

@pytest.mark.asyncio
async def test_create_employee_success():
    # Arrange
    mock_request = Mock(spec=Request)
    mock_admin_obj = AsyncMock(spec=Admin)
    mock_request.state.admin_obj = mock_admin_obj

            # user_type = "hr",
            # name= "Test user",
            # phone= 1234567890,
            # email= "test@user.com",
            # address= {
            #     street= "string",
            #     postal_code= 243001,
            #     city= "string",
            #     state= "string",
            #     country= "string",
            # },
            # password= "Test@123",
            # reports_to= 0,
    new_employee_data = EmployeeInfo.parse_obj({
            "user_type": "hr",
            "name": "Test user",
            "phone": 1234567890,
            "email": "test@user.com",
            "address": {
                "street": "string",
                "postal_code": 243001,
                "city": "string",
                "state": "string",
                "country": "string",
            },
            "password": "Test@123",
            "reports_to": 0,
        })

    mock_admin_obj.create_new_employee.return_value = [42]  # Mocked employee ID

    # Act
    response = await create_employee(
        new_employee=new_employee_data, admin_obj=mock_admin_obj
    )

    # Assert
    assert response == {
        "success": True,
        "message": "Employee created successfully",
        "emp_id": 42,
    }
    mock_admin_obj.create_new_employee.assert_awaited_once_with(
        new_employee_data.dict()
    )
    mock_admin_obj.create_new_relation.assert_awaited_once_with(
        emp_id=42, reports_to_emp_id=1
    )


@pytest.mark.asyncio
async def test_create_employee_value_error():
    # Arrange
    mock_request = Mock(spec=Request)
    mock_admin_obj = AsyncMock(spec=Admin)
    mock_request.state.admin_obj = mock_admin_obj

    new_employee_data = EmployeeInfo(
        name="John Doe",
        age=30,
        address={"street": "123 Main St", "city": "Townsville", "zip": "12345"},
        reports_to=1,
    )

    mock_admin_obj.create_new_employee.side_effect = ValueError("Invalid employee data")

    # Act & Assert
    with pytest.raises(InvalidValueErr):
        await create_employee(new_employee=new_employee_data, admin_obj=mock_admin_obj)

    mock_admin_obj.create_new_employee.assert_awaited_once_with(
        new_employee_data.dict()
    )


@pytest.mark.asyncio
async def test_create_employee_internal_server_error():
    # Arrange
    mock_request = Mock(spec=Request)
    mock_admin_obj = AsyncMock(spec=Admin)
    mock_request.state.admin_obj = mock_admin_obj

    new_employee_data = EmployeeInfo(
        name="John Doe",
        age=30,
        address={"street": "123 Main St", "city": "Townsville", "zip": "12345"},
        reports_to=1,
    )

    mock_admin_obj.create_new_employee.side_effect = Exception("Unknown error")

    # Act & Assert
    with pytest.raises(InternalServerErr):
        await create_employee(new_employee=new_employee_data, admin_obj=mock_admin_obj)

    mock_admin_obj.create_new_employee.assert_awaited_once_with(
        new_employee_data.dict()
    )

