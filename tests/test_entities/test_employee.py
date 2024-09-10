import unittest
from unittest.mock import Mock, patch, call

from src.entities.worker.worker import Worker


# employee class is an abstract class derived class instance needed to test it using worker
class test_employee(unittest.TestCase):
    def setUp(self) -> None:
        empId = 1
        self.name = "test name"
        self.phone = 998822331
        self.email = "aryan@gmail.com"
        self.address = '{"street": "test street", "postal_code": "666666","city": "Test_city", "state": "test_state", "country": "test_country"}'
        self.user_type = "hr"
        employee_info = (empId, self.name, self.phone, self.email, self.address, self.user_type)
        self.employee_obj = Worker(employee_info)

        input_patcher = patch("builtins.input")
        self.mock_input = input_patcher.start()
        output_patcher = patch("builtins.print")
        self.mock_print = output_patcher.start()

    def test_get_profile_info(self):
        res = self.employee_obj.get_profile_info()
        assert res == {
            "name": "test name",
            "phone": 998822331,
            "email": "aryan@gmail.com",
            "address": {"street": "test street", "postal_code": "666666","city": "Test_city", "state": "test_state", "country": "test_country"},
            "empId":1 
        }

    @patch("src.entities.employee.employee.match_string_in_field")
    def test_search_other_employee(self,mock_match_in_db):
        mock_match_in_db.return_value = (1,"test_name",1234567890,"test@test.com")

        res = self.employee_obj.search_other_employee("test_name")
        
        assert res == (1,"test_name",1234567890,"test@test.com")
        mock_match_in_db.assert_called_with("employees", "empId, name, phone, email", "name", "test_name")


    @patch("src.entities.employee.employee.hash_pass")
    @patch("src.entities.employee.employee.check_pass")
    @patch("src.entities.employee.employee.read_fields_from_record")
    def test_update_password(self,mock_read_db,mock_check_pass,mock_hash_pass):

        mock_read_db.side_effect = [("password hash from db")]
        mock_check_pass.return_value = False
        mock_hash_pass.return_value = "Calculated hash for new password"
        res1 = self.employee_obj.update_password("old password","new password")

        assert res1 is False 

    @patch("src.entities.employee.employee.update_one_record")
    @patch("src.entities.employee.employee.hash_pass")
    @patch("src.entities.employee.employee.check_pass")
    @patch("src.entities.employee.employee.read_fields_from_record")
    def test_update_password_2(self,mock_read_db,mock_check_pass,mock_hash_pass,mock_update_db):

        mock_read_db.return_value = [("password hash from db")]
        mock_check_pass.return_value = True
        mock_hash_pass.return_value = "Calculated hash for new password"
        mock_update_db.return_value = True
        res2 = self.employee_obj.update_password("old password","new password")
        
        assert res2 is True 
        mock_update_db.assert_called_with("employees",{"password":"Calculated hash for new password"},"empId",self.employee_obj.empId)

    @patch("src.entities.employee.employee.write_to_table")
    @patch("src.entities.employee.employee.ceil")
    @patch("src.entities.employee.employee.random.choice")
    @patch("src.entities.employee.employee.read_fields_from_record")
    def test_request_self_info_change(self,mock_read_db,mock_random,mock_ceil,mock_write_to_db):
        mock_read_db.return_value = [(0,),(1,),(2,),(3,)]
        mock_random.side_effect = [2,0]
        mock_ceil.return_value = 1725873945

        mock_write_to_db.return_value = (13,2,"updated_info_json",0,None,1725873945,0,"hr_assigned")
        
        updated_info_dict = {"name":self.name,"phone":self.phone,"email":self.email,"address":self.address}
        res = self.employee_obj.request_self_info_change(updated_info_dict)
        assert res is True

    @patch("src.entities.employee.employee.write_to_table")
    @patch("src.entities.employee.employee.ceil")
    @patch("src.entities.employee.employee.random.choice")
    @patch("src.entities.employee.employee.read_fields_from_record")
    def test_request_self_info_change_2(self,mock_read_db,mock_random,mock_ceil,mock_write_to_db):
        mock_read_db.return_value = []
        mock_random.side_effect = []
        mock_ceil.return_value = 1725873945

        mock_write_to_db.return_value = (13,2,"updated_info_json",0,None,1725873945,0,"hr_assigned")
        
        updated_info_dict = {"name":self.name,"phone":self.phone,"email":self.email,"address":self.address}
        res = self.employee_obj.request_self_info_change(updated_info_dict)
        self.mock_print.assert_called_with("No HR employee to assign request to.") 

    @patch("src.entities.employee.employee.write_to_table")
    @patch("src.entities.employee.employee.ceil")
    @patch("src.entities.employee.employee.random.choice")
    @patch("src.entities.employee.employee.read_fields_from_record")
    def test_request_self_info_change_3(self,mock_read_db,mock_random,mock_ceil,mock_write_to_db):
        mock_read_db.return_value = [(1,)]
        mock_random.side_effect = [1]
        mock_ceil.return_value = 1725873945

        mock_write_to_db.return_value = (13,2,"updated_info_json",0,None,1725873945,1,"hr_assigned")
        
        updated_info_dict = {"name":self.name,"phone":self.phone,"email":self.email,"address":self.address}
        res = self.employee_obj.request_self_info_change(updated_info_dict)

        assert res is True
        calls = [call("\nWarning - you are the only HR hence you will be approving your own request\n"),call('updated user will be ', (13, 2, 'updated_info_json', 0, None, 1725873945, 1, 'hr_assigned')),]
        self.mock_print.assert_has_calls(calls) 

    @patch("src.entities.employee.employee.write_to_table")
    @patch("src.entities.employee.employee.ceil")
    @patch("src.entities.employee.employee.random.choice")
    @patch("src.entities.employee.employee.read_fields_from_record")
    def test_request_self_info_change_4(self,mock_read_db,mock_random,mock_ceil,mock_write_to_db):
        mock_read_db.return_value = [(1,),(2,)]
        mock_random.side_effect = [1,2]
        mock_ceil.return_value = 1725873945

        mock_write_to_db.return_value = (13,2,"updated_info_json",0,None,1725873945,1,"hr_assigned")
        
        updated_info_dict = {"name":self.name,"phone":self.phone,"email":self.email,"address":self.address}
        res = self.employee_obj.request_self_info_change(updated_info_dict)

        assert res is True
        calls = [call('updated user will be ', (13, 2, 'updated_info_json', 0, None, 1725873945, 1, 'hr_assigned')),]
        self.mock_print.assert_has_calls(calls) 

    def test_info(self):
        self.employee_obj.info()
if __name__ == "__main__":
    unittest.main()
