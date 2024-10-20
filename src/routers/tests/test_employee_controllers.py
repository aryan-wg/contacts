import pytest
from unittest.mock import AsyncMock, Mock
from ..employee_router import get_reports_to
from ...execptions.HttpExceptions import NotFoundErr, InternalServerErr

from fastapi import Request


@pytest.mark.asyncio
async def test_get_reports_to_success():
    # Arrange
    mock_request = Mock(spec=Request)
    mock_user_obj = AsyncMock()
    mock_request.state.user_obj = mock_user_obj
    mock_user_obj.get_reports_to.return_value = "some_data"

    # Act
    response = await get_reports_to(emp_id=1, request=mock_request)

    # Assert
    mock_user_obj.get_reports_to.assert_awaited_once_with(1)
    assert response == {"success": True, "data": "some_data"}


@pytest.mark.asyncio
async def test_get_reports_to_not_found_error():
    # Arrange
    mock_request = Mock(spec=Request)
    mock_user_obj = AsyncMock()
    mock_request.state.user_obj = mock_user_obj
    mock_user_obj.get_reports_to.side_effect = ValueError("User not found")

    # Act & Assert
    with pytest.raises(NotFoundErr):
        await get_reports_to(emp_id=1, request=mock_request)

    mock_user_obj.get_reports_to.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_reports_to_internal_server_error():
    # Arrange
    mock_request = Mock(spec=Request)
    mock_user_obj = AsyncMock()
    mock_request.state.user_obj = mock_user_obj
    mock_user_obj.get_reports_to.side_effect = Exception("Unknown error")

    # Act & Assert
    with pytest.raises(InternalServerErr):
        await get_reports_to(emp_id=1, request=mock_request)

    mock_user_obj.get_reports_to.assert_awaited_once_with(1)

